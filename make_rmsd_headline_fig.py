"""Headline backbone-RMSD stability figure: EPA, gamma-linolenic and palmitic
(free-acid form) vs. the ligand-free apo baseline, each as mean +/-SD across
n=3 independent-seed replicates (50 ns, 250 ps/frame).

Tests whether ligand binding perturbs global backbone stability relative to
apo -- supports the "dynamically stable, ligand-bound or not" framing and
sets up the (optional, separate) per-residue apo-vs-holo RMSF comparison.

Run (conda analysis env -- OpenBLAS-based, avoids the "md" env's MKL crash
on concurrent numpy/mdtraj processes):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe make_rmsd_headline_fig.py
"""
import os, numpy as np, mdtraj as md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ppf = 250.0
SYSTEMS = [
    ("epa_50ns",      "EPA (C20:5, free acid)",         "#2c7fb8"),
    ("gla_50ns",       "\u03b3-linolenic (C18:3, free acid)", "#41ab5d"),
    ("palmitic_50ns", "palmitic (C16:0, free acid)",    "#7fbf7b"),
    ("apo_toxt_50ns", "apo ToxT (ligand-free)",         "#756bb1"),
]

def rmsd_series(name):
    D = "md/" + name
    top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
    t = md.load(D + "/traj.dcd", top=top)
    tn = np.arange(t.n_frames) * ppf / 1000.0
    bb = t.topology.select("protein and backbone")
    t.superpose(t, 0, atom_indices=bb)
    rmsd = md.rmsd(t, t, 0, atom_indices=bb) * 10.0  # nm -> A
    return tn, rmsd

def replicate_series(base):
    reps = []; tn = None
    for suffix in ("", "_r2", "_r3"):
        name = base + suffix
        if os.path.exists("md/%s/traj.dcd" % name):
            tn, rmsd = rmsd_series(name)
            reps.append(rmsd)
    if not reps:
        return None
    stack = np.array(reps)
    mean = stack.mean(0)
    sd = stack.std(0, ddof=1) if len(reps) > 1 else None
    return tn, mean, sd, len(reps)

fig, ax = plt.subplots(figsize=(8, 5))
for name, label, col in SYSTEMS:
    result = replicate_series(name)
    if result is None:
        print("SKIP %s -- no trajectories found" % name); continue
    tn, mean, sd, n = result
    ax.plot(tn, mean, color=col, lw=1.6, label="%s (n=%d)" % (label, n))
    if sd is not None:
        ax.fill_between(tn, mean - sd, mean + sd, color=col, alpha=0.15, lw=0)
    print("%-40s production (>5ns) mean RMSD %.2f +/- %.2f A"
          % (label.encode("ascii", "replace").decode(), mean[20:].mean(),
             (sd[20:].mean() if sd is not None else float("nan"))))

ax.set_xlabel("Time (ns)", fontsize=11)
ax.set_ylabel("Protein backbone RMSD (\u00c5)", fontsize=11)
ax.set_title("Backbone stability is comparable ligand-bound or apo (n=3 replicates each)",
             fontsize=10.5, fontweight="bold")
ax.set_xlim(0, 50)
ax.legend(fontsize=9, loc="upper left", framealpha=0.9)
ax.grid(alpha=0.25)
fig.text(0.99, 0.01, "lines: mean of n=3 replicates; bands: \u00b1SD", fontsize=7.5,
          color="#666666", ha="right")
fig.tight_layout()
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/fig_rmsd_headline_apo.png", dpi=200)
print("wrote figures/fig_rmsd_headline_apo.png")
