"""Specificity figure: ligand-pocket distance over time for cognate fatty acids
and the native ligand vs. the glucose decoy. PBC-correct, published numbering.

Uses all available replicates (r1/r2/r3) per system and plots the mean as a
line with a +/-SD shaded band (across replicate means, not per-frame). Systems
with no replicates (glucose_core_50ns, seeded-in-core variant) fall back to a
single trajectory, no band.

Run (conda analysis env -- OpenBLAS-based, avoids the "md" env's MKL crash
on concurrent numpy/mdtraj processes):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe make_specificity_fig.py
"""
import os, numpy as np, mdtraj as md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

POCKET = [12, 13, 14, 20, 22, 25, 31, 33, 71, 81, 226, 259, 261, 266]  # crystal numbering
ppf = 250.0

RUNS = [
    ("epa_50ns",           "EPA (C20:5)",          "#2c7fb8", 1.4, "-"),
    ("gla_50ns",           "γ-linolenic (C18:3)", "#41ab5d", 1.4, "-"),
    ("palmitic_50ns",      "palmitic (C16:0)",     "#7fbf7b", 1.4, "-"),
    ("pentadecanal_50ns",  "pentadecanal (weak)",  "#66c2a4", 1.4, "-"),
    ("tridecanoic_50ns",   "tridecanoic (weak)",   "#3690c0", 1.4, "-"),
    ("pam_50ns",           "palmitoleate (native, +ctrl)", "#e6ab02", 2.2, "-"),
    ("glucose_decoy_50ns", "glucose decoy (docked start)", "#d7191c", 2.6, "-"),
    ("glucose_core_50ns",  "glucose decoy (seeded in core)", "#d7191c", 2.6, "--"),
]

def com_series(name):
    D = "md/" + name
    top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
    t = md.load(D + "/traj.dcd", top=top)
    lig = t.topology.select("resname UNK")
    sel = " or ".join("(residue %d and name CA)" % r for r in POCKET)
    pocket = t.topology.select(sel)
    tn = np.arange(t.n_frames) * ppf / 1000.0
    com = np.zeros(t.n_frames)
    for i in range(t.n_frames):
        xyz = t.xyz[i]; box = t.unitcell_lengths[i]
        d = xyz[lig].mean(0) - xyz[pocket].mean(0)
        d -= box * np.round(d / box)
        com[i] = np.linalg.norm(d) * 10.0
    return tn, com

def replicate_series(base):
    """Returns (tn, mean, sd or None) across available r1/r2/r3 for base."""
    reps = []
    tn = None
    for suffix in ("", "_r2", "_r3"):
        name = base + suffix
        if os.path.exists("md/%s/traj.dcd" % name):
            tn, com = com_series(name)
            reps.append(com)
    if not reps:
        return None
    stack = np.array(reps)
    mean = stack.mean(0)
    sd = stack.std(0, ddof=1) if len(reps) > 1 else None
    return tn, mean, sd

fig, ax = plt.subplots(figsize=(9, 5.2))
ax.axhspan(0, 4, color="#cfe8cf", alpha=0.6, zorder=0)
ax.text(0.6, 1.4, "pocket core (bound)", fontsize=9, color="#2d6a2d")
for name, label, col, lw, ls in RUNS:
    result = replicate_series(name)
    if result is None:
        continue
    tn, mean, sd = result
    ax.plot(tn, mean, color=col, lw=lw, ls=ls, label=label)
    if sd is not None:
        ax.fill_between(tn, mean - sd, mean + sd, color=col, alpha=0.15, lw=0)
ax.set_xlabel("Time (ns)", fontsize=11)
ax.set_ylabel("Ligand–pocket distance (Å)", fontsize=11)
ax.set_title("MD ligand retention reflects a buried pocket (traps even the decoy if seeded);\nspecificity is set by binding preference — see blind docking",
             fontsize=10.5, fontweight="bold")
ax.set_ylim(0, 12)
ax.set_xlim(0, 50)
ax.legend(fontsize=9, loc="center right", framealpha=0.9)
ax.grid(alpha=0.25)
fig.text(0.99, 0.01, "lines: mean of n=3 replicates (n=1 for core-seeded decoy); bands: ±SD",
          fontsize=7.5, color="#666666", ha="right")
fig.tight_layout()
fig.savefig("figures/fig10_specificity.png", dpi=200)
print("wrote figures/fig10_specificity.png")
