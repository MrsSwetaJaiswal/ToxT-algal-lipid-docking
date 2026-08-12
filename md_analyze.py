"""Analyze an MD trajectory of a ToxT-ligand complex.

Produces the publication deliverables:
  - protein backbone RMSD vs time (complex stability)
  - ligand RMSD vs time (does the ligand stay put?)
  - per-residue RMSF (flexibility)
  - ligand-protein contact persistence (which residues hold the ligand, and for
    what fraction of the trajectory)
  - radius of gyration (compactness)
Outputs CSVs + PNG figures in md/<name>/analysis/.

Run (conda analysis env -- OpenBLAS-based, avoids the "md" env's MKL crash
on concurrent numpy/mdtraj processes):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe md_analyze.py <name> [equil_ns]
  e.g.  ...python.exe md_analyze.py epa_50ns 5
(equil_ns = how many ns at the start to treat as equilibration and exclude from
 averaged metrics like RMSF and contact fractions; default 5.)
"""
import os, sys, csv
import numpy as np
import mdtraj as md
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAME = sys.argv[1] if len(sys.argv) > 1 else "epa_50ns"
LIG_LABEL = NAME.replace("_50ns_r2", "").replace("_50ns_r3", "").replace("_50ns", "").replace("_", " ")
EQUIL_NS = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
D = os.path.join("md", NAME)
TOP = os.path.join(D, "system.pdb")
TRAJ = os.path.join(D, "traj.dcd")
OUT = os.path.join(D, "analysis"); os.makedirs(OUT, exist_ok=True)
CONTACT_CUTOFF = 0.40  # nm (4.0 A)

print("Loading trajectory ...")
t = md.load(TRAJ, top=TOP)
print("  frames: %d  atoms: %d" % (t.n_frames, t.n_atoms))
# time per frame: DCD written every 250 ps (save_every in md_production.py)
ps_per_frame = 250.0
time_ns = np.arange(t.n_frames) * ps_per_frame / 1000.0

# selections
prot = t.topology.select("protein")
prot_bb = t.topology.select("protein and backbone")
# ligand = the small-molecule residue (named UNK by OpenFF/Modeller)
lig = t.topology.select("resname UNK")
if len(lig) == 0:  # fallback
    lig = t.topology.select("not protein and not water and resname != NA and resname != CL")
lig = lig.astype(int)
HAS_LIG = len(lig) > 0  # apo (ligand-free) systems have no ligand atoms at all
# mdtraj's "protein" selector treats residue name UNK as a protein placeholder,
# so the ligand's own atoms leak into `prot` -- drop them to avoid a spurious
# self-contact entry and a phantom "protein" residue in later analysis.
lig_set = set(lig.tolist())
prot = np.array([a for a in prot if a not in lig_set])
print("  protein atoms: %d  ligand atoms: %d" % (len(prot), len(lig)))

# unwrap the ligand into the same periodic image as the protein, per frame,
# before superposing -- otherwise a ligand that crosses the box edge produces
# a spurious multi-nm "jump" in its RMSD that looks like unbinding but isn't.
if HAS_LIG:
    for fi in range(t.n_frames):
        box = t.unitcell_lengths[fi]
        pcom = t.xyz[fi, prot, :].mean(0)
        lcom = t.xyz[fi, lig, :].mean(0)
        shift = box * np.round((lcom - pcom) / box)
        t.xyz[fi, lig, :] -= shift

# align whole trajectory on protein backbone of frame 0
t.superpose(t, 0, atom_indices=prot_bb)

# --- RMSD ---
rmsd_prot = md.rmsd(t, t, 0, atom_indices=prot_bb) * 10.0  # A
# ligand RMSD after protein alignment (already superposed on protein)
ref = t[0]
def lig_rmsd():
    d = t.xyz[:, lig, :] - ref.xyz[0, lig, :]
    return np.sqrt((d**2).sum(axis=(1, 2)) / len(lig)) * 10.0
rmsd_lig = lig_rmsd() if HAS_LIG else np.full(t.n_frames, np.nan)

with open(os.path.join(OUT, "rmsd.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["time_ns", "protein_bb_rmsd_A", "ligand_rmsd_A"])
    for i in range(t.n_frames):
        w.writerow([round(time_ns[i], 3), round(float(rmsd_prot[i]), 3),
                    (round(float(rmsd_lig[i]), 3) if HAS_LIG else "")])

# --- RMSF (production part only) ---
start = int(EQUIL_NS * 1000 / ps_per_frame)
start = min(start, max(0, t.n_frames - 2))
tp = t[start:]
tp.superpose(tp, 0, atom_indices=prot_bb)
ca = tp.topology.select("protein and name CA")
rmsf = md.rmsf(tp, tp, 0, atom_indices=ca) * 10.0  # A
resids = [tp.topology.atom(i).residue.resSeq for i in ca]
with open(os.path.join(OUT, "rmsf.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["residue", "rmsf_A"])
    for r, v in zip(resids, rmsf): w.writerow([r, round(float(v), 3)])

# --- Radius of gyration ---
rg = md.compute_rg(t.atom_slice(prot)) * 10.0

# --- Ligand-protein contact persistence ---
# protein atoms within cutoff of any ligand atom, per frame -> residue contact fraction
contacts = []
if HAS_LIG:
    prot_res = {}
    for ai in prot:
        prot_res.setdefault(t.topology.atom(ai).residue.index, []).append(ai)
    res_list = sorted(prot_res)
    neighbor_counts = np.zeros(len(res_list))
    frames_used = range(start, t.n_frames)
    for fi in frames_used:
        xyz = t.xyz[fi]
        lig_xyz = xyz[lig]            # (Nl, 3)
        for ri, residue_idx in enumerate(res_list):
            a = xyz[prot_res[residue_idx]]          # (Na, 3)
            d = a[:, None, :] - lig_xyz[None, :, :]  # (Na, Nl, 3)
            mind = np.sqrt((d**2).sum(-1)).min()
            if mind < CONTACT_CUTOFF:
                neighbor_counts[ri] += 1
    contact_frac = neighbor_counts / max(1, len(list(frames_used)))
    for ri, residue_idx in enumerate(res_list):
        if contact_frac[ri] > 0.05:
            res = t.topology.residue(residue_idx)
            contacts.append((res.name, res.resSeq, round(float(contact_frac[ri]), 3)))
    contacts.sort(key=lambda x: -x[2])
with open(os.path.join(OUT, "contacts.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["residue_name", "residue_number", "contact_fraction"])
    for c in contacts: w.writerow(c)

# --- Figures ---
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(time_ns, rmsd_prot, label="protein backbone", color="#2c7fb8")
if HAS_LIG:
    ax.plot(time_ns, rmsd_lig, label="ligand (%s)" % LIG_LABEL, color="#d95f0e", alpha=0.8)
ax.set_xlabel("Time (ns)"); ax.set_ylabel("RMSD (A)")
ax.set_title("%s: complex stability" % NAME); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rmsd.png"), dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(resids, rmsf, color="#31a354")
ax.set_xlabel("Residue number"); ax.set_ylabel("RMSF (A)")
ax.set_title("%s: per-residue flexibility (production)" % NAME); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rmsf.png"), dpi=200); plt.close(fig)

if contacts:
    top = contacts[:15][::-1]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(["%s%d" % (c[0], c[1]) for c in top], [c[2]*100 for c in top],
            color="#756bb1", edgecolor="black", linewidth=0.4)
    ax.set_xlabel("Contact persistence (% of production frames, < 4 A)")
    ax.set_title("%s: ToxT residues contacting the ligand" % NAME)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "contacts.png"), dpi=200); plt.close(fig)

print("\n=== SUMMARY (%s) ===" % NAME)
print("Trajectory length: %.1f ns (%d frames)" % (time_ns[-1] if t.n_frames else 0, t.n_frames))
prod = slice(start, t.n_frames)
print("Protein backbone RMSD (production): mean %.2f +/- %.2f A"
      % (rmsd_prot[prod].mean(), rmsd_prot[prod].std()))
print("Radius of gyration (production):    mean %.2f A" % rg[prod].mean())
if HAS_LIG:
    print("Ligand RMSD (production):           mean %.2f +/- %.2f A"
          % (rmsd_lig[prod].mean(), rmsd_lig[prod].std()))
    print("Ligand remained bound:", "YES" if rmsd_lig[prod].mean() < 5.0 else "CHECK (drifted)")
    print("\nTop persistent ligand-contact residues:")
    for c in contacts[:10]:
        print("  %s%-4d  %5.0f%% of frames" % (c[0], c[1], c[2]*100))
else:
    print("(apo / ligand-free system -- no ligand RMSD or contacts to report)")
print("\nOutputs in", OUT)
