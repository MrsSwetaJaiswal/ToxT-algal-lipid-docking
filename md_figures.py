"""Generate manuscript MD figures (PBC-correct) for the EPA acid & methyl-ester runs."""
import os, numpy as np, mdtraj as md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = "figures"; os.makedirs(FIG, exist_ok=True)
RUNS = [("epa_50ns", "EPA free acid", "#2c7fb8"),
        ("methyl_epa_50ns", "methyl-EPA ester", "#d95f0e"),
        ("epa_deprot_50ns", "EPA carboxylate (pH 7.4)", "#31a354")]
# pocket residues in published crystal (3GBG) numbering
POCKET = [12,13,14,20,22,25,31,33,71,81,226,259,261,266]
ps_per_frame = 250.0

def analyze(name):
    D = "md/" + name
    top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
    t = md.load(D + "/traj.dcd", top=top)
    tn = np.arange(t.n_frames) * ps_per_frame / 1000.0
    bb = t.topology.select("protein and backbone")
    lig = t.topology.select("resname UNK")
    prot = t.topology.select("protein")
    sel = " or ".join("(residue %d and name CA)" % r for r in POCKET)
    pocket = t.topology.select(sel)
    # --- PBC-dependent metrics on ORIGINAL coordinates (before any superposition) ---
    com = np.zeros(t.n_frames)
    for i in range(t.n_frames):
        xyz = t.xyz[i]; box = t.unitcell_lengths[i]
        d = xyz[lig].mean(0) - xyz[pocket].mean(0)
        d -= box * np.round(d / box)
        com[i] = np.linalg.norm(d) * 10.0
    # contacts (min image), production only (>5 ns)
    start = int(5000 / ps_per_frame)
    prot_res = {}
    for ai in prot:
        prot_res.setdefault(t.topology.atom(ai).residue.index, []).append(ai)
    res_list = sorted(prot_res); counts = np.zeros(len(res_list)); nf = 0
    for fi in range(start, t.n_frames):
        xyz = t.xyz[fi]; box = t.unitcell_lengths[fi]
        shift = box * np.round((xyz[lig].mean(0) - xyz[prot].mean(0)) / box)
        lig_xyz = xyz[lig] - shift; nf += 1
        for ri, rid in enumerate(res_list):
            a = xyz[prot_res[rid]]
            if np.sqrt(((a[:,None,:]-lig_xyz[None,:,:])**2).sum(-1)).min() < 0.40:
                counts[ri] += 1
    contacts = []
    for ri, rid in enumerate(res_list):
        r = t.topology.residue(rid)
        if r.name != "UNK" and counts[ri]/nf > 0.05:
            contacts.append((r.name, r.resSeq, counts[ri]/nf))
    contacts.sort(key=lambda x: -x[2])
    # --- RMSD last (superposition modifies coordinates in place) ---
    t.superpose(t, 0, atom_indices=bb)
    rmsd = md.rmsd(t, t, 0, atom_indices=bb) * 10.0
    return tn, rmsd, com, contacts

data = {name: analyze(name) for name, _, _ in RUNS}

# Figure 5: stability (backbone RMSD + ligand COM distance)
fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
for name, lab, col in RUNS:
    tn, rmsd, com, _ = data[name]
    ax[0].plot(tn, rmsd, color=col, label=lab, lw=1)
    ax[1].plot(tn, com, color=col, label=lab, lw=1)
ax[0].set_title("Protein backbone RMSD"); ax[0].set_xlabel("Time (ns)"); ax[0].set_ylabel("RMSD (A)")
ax[1].set_title("Ligand distance from pocket (min-image)"); ax[1].set_xlabel("Time (ns)")
ax[1].set_ylabel("COM-pocket distance (A)"); ax[1].axhline(10, ls="--", c="grey", alpha=0.6)
for a in ax: a.legend(fontsize=8); a.grid(alpha=0.3)
fig.suptitle("MD stability of ToxT-EPA complexes (50 ns each)", fontweight="bold")
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(FIG+"/fig5_md_stability.png", dpi=200); plt.close(fig)

# Figure 6: contact persistence (EPA acid)
_, _, _, contacts = data["epa_50ns"]
top = contacts[:15][::-1]
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(["%s%d" % (c[0], c[1]) for c in top], [c[2]*100 for c in top],
        color="#756bb1", edgecolor="black", linewidth=0.4)
ax.set_xlabel("Contact persistence (% of production frames, < 4 A)")
ax.set_title("ToxT residues contacting EPA (50 ns)")
ax.grid(axis="x", alpha=0.3); ax.set_xlim(0, 100)
fig.tight_layout(); fig.savefig(FIG+"/fig6_md_contacts.png", dpi=200); plt.close(fig)

print("Wrote fig5_md_stability.png, fig6_md_contacts.png")
for name, lab, _ in RUNS:
    tn, rmsd, com, contacts = data[name]
    prod = slice(int(5000/ps_per_frame), None)
    print("%s: bbRMSD %.2f A, COM %.1f A, bound %.0f%%, top contacts %s"
          % (lab, rmsd[prod].mean(), com[prod].mean(),
             100*(com[prod] < 10).mean(),
             ", ".join("%s%d" % (c[0], c[1]) for c in contacts[:6])))
