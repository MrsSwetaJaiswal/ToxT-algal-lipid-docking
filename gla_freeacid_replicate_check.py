"""Diagnostic: does the GLA free-acid n=3 MM-GBSA trend (r1 -34.2 -> r2 -39.1 ->
r3 -42.6, sd +/-4.2) reflect progressive pose drift, or is the pose equally
stable/bound in all three independent replicates (ordinary replicate noise)?

For gla_50ns / gla_50ns_r2 / gla_50ns_r3, computes:
  (a) ligand-COM -> pocket-COM distance per frame (retention)
  (b) ligand heavy-atom RMSD to its own frame 0 after protein superposition
PBC-correct minimum image on original coords before superpose.
Writes figures/gla_freeacid_replicate_check.png and prints a comparison table.

Run (conda analysis env -- OpenBLAS-based, avoids the "md" env's MKL crash
on concurrent numpy/mdtraj processes):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe gla_freeacid_replicate_check.py
"""
import os, numpy as np, mdtraj as md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPS = [("gla_50ns", 1), ("gla_50ns_r2", 2), ("gla_50ns_r3", 3)]
POCKET = [12, 13, 14, 20, 22, 25, 31, 33, 71, 81, 226, 259, 261, 266]  # crystal numbering
ppf = 250.0  # ps per frame

def stats(x): return (x.mean(), x.std(), x.min(), x.max())

results = {}
for name, rep in REPS:
    D = "md/" + name
    top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
    t = md.load(D + "/traj.dcd", top=top)
    tn = np.arange(t.n_frames) * ppf / 1000.0  # ns

    lig = t.topology.select("resname UNK")
    sel = " or ".join("(residue %d and name CA)" % r for r in POCKET)
    pocket = t.topology.select(sel)

    def com_dist(atoms):
        out = np.zeros(t.n_frames)
        for i in range(t.n_frames):
            xyz = t.xyz[i]; box = t.unitcell_lengths[i]
            d = xyz[atoms].mean(0) - xyz[pocket].mean(0)
            d -= box * np.round(d / box)  # minimum image
            out[i] = np.linalg.norm(d) * 10.0  # nm -> A
        return out

    d_lig = com_dist(lig)

    prot = t.topology.select("protein and not resname UNK")
    t.superpose(t, 0, atom_indices=prot)
    lig_rmsd = md.rmsd(t, t, 0, atom_indices=lig) * 10.0  # A

    results[rep] = dict(tn=tn, d_lig=d_lig, lig_rmsd=lig_rmsd, n_frames=t.n_frames)
    print("=== %s (rep %d, %d frames, %.1f ns) ===" % (name, rep, t.n_frames, tn[-1]))
    print("ligand-COM -> pocket  mean %.2f  sd %.2f  range %.2f-%.2f A" % stats(d_lig))
    print("ligand RMSD(t0)       mean %.2f  sd %.2f  range %.2f-%.2f A" % stats(lig_rmsd))

print("\n=== summary across replicates ===")
print("%-5s %10s %10s %10s %10s" % ("rep", "COM mean", "COM sd", "RMSD mean", "RMSD sd"))
for rep in (1, 2, 3):
    r = results[rep]
    print("%-5d %10.2f %10.2f %10.2f %10.2f"
          % (rep, r["d_lig"].mean(), r["d_lig"].std(), r["lig_rmsd"].mean(), r["lig_rmsd"].std()))

fig, ax = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True)
colors = {1: "#2c7fb8", 2: "#d7191c", 3: "#238b45"}
for rep in (1, 2, 3):
    r = results[rep]
    ax[0].plot(r["tn"], r["d_lig"], color=colors[rep], lw=1.3, label="r%d" % rep)
    ax[1].plot(r["tn"], r["lig_rmsd"], color=colors[rep], lw=1.3, label="r%d" % rep)
ax[0].axhspan(0, 6, color="#cfe8cf", alpha=0.5)
ax[0].set_ylabel("ligand COM -> pocket (A)")
ax[0].legend(fontsize=9, loc="upper left"); ax[0].grid(alpha=0.25)
ax[0].set_title("GLA free acid (gla_50ns): pose retention across r1/r2/r3\n"
                "checking for progressive drift behind the n=3 MM-GBSA trend",
                fontsize=10.5, fontweight="bold")
ax[1].set_ylabel("ligand RMSD to t0 (A)"); ax[1].set_xlabel("Time (ns)")
ax[1].legend(fontsize=9, loc="upper left"); ax[1].grid(alpha=0.25)
fig.tight_layout()
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/gla_freeacid_replicate_check.png", dpi=200)
print("\nwrote figures/gla_freeacid_replicate_check.png")
