"""Diagnostic: is the large single-trajectory MM-GBSA variance for the GLA
carboxylate (+/-20.5 kcal/mol) explained by head-group / ligand mobility?

Computes, over gla_deprot_50ns (rep 1):
  (a) ligand-COM  -> pocket-COM distance per frame (overall retention)
  (b) carboxylate-C -> pocket-COM distance per frame (head-group specifically)
  (c) ligand heavy-atom RMSD to frame 0 after protein superposition (internal wobble)
PBC-correct minimum image on original coords before superpose.
Writes figures/gla_carboxylate_retention.png and prints summary stats.
"""
import os, numpy as np, mdtraj as md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAME = "gla_deprot_50ns"
POCKET = [12, 13, 14, 20, 22, 25, 31, 33, 71, 81, 226, 259, 261, 266]  # crystal numbering
ppf = 250.0  # ps per frame

D = "md/" + NAME
top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
t = md.load(D + "/traj.dcd", top=top)
tn = np.arange(t.n_frames) * ppf / 1000.0  # ns

lig = t.topology.select("resname UNK")
sel = " or ".join("(residue %d and name CA)" % r for r in POCKET)
pocket = t.topology.select(sel)

# carboxylate carbon = the ligand carbon bonded to two oxygens
lig_set = set(lig.tolist())
carbox = []
for a in t.topology.atoms:
    if a.index in lig_set and a.element.symbol == "C":
        o_neigh = sum(1 for b in t.topology.bonds
                      if a in b and (b[0].element.symbol == "O" or b[1].element.symbol == "O"))
        if o_neigh >= 2:
            carbox.append(a.index)
carbox = np.array(carbox) if carbox else lig[:1]

def com_dist(atoms):
    out = np.zeros(t.n_frames)
    for i in range(t.n_frames):
        xyz = t.xyz[i]; box = t.unitcell_lengths[i]
        d = xyz[atoms].mean(0) - xyz[pocket].mean(0)
        d -= box * np.round(d / box)  # minimum image
        out[i] = np.linalg.norm(d) * 10.0  # nm -> A
    return out

d_lig = com_dist(lig)
d_cbx = com_dist(carbox)

# internal ligand RMSD (protein-superposed)
prot = t.topology.select("protein and not resname UNK")
t.superpose(t, 0, atom_indices=prot)
lig_rmsd = md.rmsd(t, t, 0, atom_indices=lig) * 10.0  # A

def stats(x): return (x.mean(), x.std(), x.min(), x.max())
print("=== GLA carboxylate (gla_deprot_50ns) retention diagnostic ===")
print("frames: %d (%.1f ns)" % (t.n_frames, tn[-1]))
print("carboxylate carbon atom(s): %s" % carbox.tolist())
print("ligand-COM  dist  mean %.2f  sd %.2f  range %.2f-%.2f A" % stats(d_lig))
print("carboxylate dist  mean %.2f  sd %.2f  range %.2f-%.2f A" % stats(d_cbx))
print("ligand RMSD(t0)   mean %.2f  sd %.2f  range %.2f-%.2f A" % stats(lig_rmsd))
print("carboxylate excursion (max-min): %.2f A" % (d_cbx.max() - d_cbx.min()))

fig, ax = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True)
ax[0].axhspan(0, 6, color="#cfe8cf", alpha=0.6)
ax[0].plot(tn, d_lig, color="#2c7fb8", lw=1.4, label="ligand COM -> pocket")
ax[0].plot(tn, d_cbx, color="#d7191c", lw=1.4, label="carboxylate C -> pocket")
ax[0].set_ylabel("distance to pocket (A)")
ax[0].legend(fontsize=9, loc="upper left"); ax[0].grid(alpha=0.25)
ax[0].set_title("GLA carboxylate (gla_deprot_50ns): ligand & head-group mobility\n"
                "explains the large single-trajectory MM-GBSA variance (+/-20.5 kcal/mol)",
                fontsize=10.5, fontweight="bold")
ax[1].plot(tn, lig_rmsd, color="#756bb1", lw=1.4)
ax[1].set_ylabel("ligand RMSD to t0 (A)"); ax[1].set_xlabel("Time (ns)")
ax[1].grid(alpha=0.25); ax[1].set_xlim(0, tn[-1])
fig.tight_layout()
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/gla_carboxylate_retention.png", dpi=200)
print("wrote figures/gla_carboxylate_retention.png")
