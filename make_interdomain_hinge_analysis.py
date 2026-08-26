"""Inter-domain geometry (hinge angle / COM-COM distance) between the
N-terminal pocket domain and the C-terminal HTH DNA-binding domain, apo vs.
holo, to test the allosteric-restraint hypothesis (Discussion /
Supplementary Section S.13) directly -- rather than via the whole-protein
RMSF proxy already reported (Section 3.8, Figure 14), which found no
domain-specific effect (HTH -0.16 A vs. rest of protein -0.12 A) and can't
distinguish local jitter from restrained relative domain motion in the
first place.

apo:  apo_toxt_50ns (+ r2, r3)                      -- n = 3 replicates
holo: epa_50ns, gla_50ns, palmitic_50ns (free acid)  -- n = 3 replicates each

Method:
  1. Per trajectory, superpose every frame onto that trajectory's own
     frame 0 using ONLY the N-terminal domain CA atoms (residues < 188) as
     the alignment reference. This isolates true C-domain motion relative
     to the N-domain from whole-molecule translation/rotation/diffusion --
     a raw, unaligned COM-COM distance would be contaminated by that.
  2. Per frame (production window, >5 ns): compute the N-domain CA
     centroid, the C-terminal HTH domain (188-273) CA centroid, and the
     hinge angle at the domain-boundary residue (CA of residue 188) between
     vectors to each centroid -- the standard "elbow angle" construction
     used for other hinged multi-domain proteins.
  3. Per replicate: report the frame-level mean (average relative
     geometry) and SD (how much the geometry fluctuates/spreads -- this
     is the direct "restraint" readout: a narrower per-replicate SD in
     holo than apo means occupancy is restraining inter-domain motion,
     not just damping local jitter).
  4. Compare apo (n=3 replicate values) vs. each holo system (n=3 replicate
     values) on both the mean and the SD, matching the paper's existing
     replicate-level (not frame-pseudoreplicated) statistical convention.
     A Welch's t-test is reported for completeness but, with n=3 per group,
     should be read as indicative, not confirmatory.

Run (conda analysis env -- OpenBLAS-based, avoids the "md" env's MKL crash
on concurrent numpy/mdtraj processes):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe make_interdomain_hinge_analysis.py
"""
import os, csv
import numpy as np
import mdtraj as md
from scipy import stats
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ppf = 250.0
PROD_START = int(5000 / ppf)  # 5 ns, matches make_apo_holo_rmsf_fig.py

N_DOMAIN_MAX = 187      # N-terminal / pocket domain: resSeq <= 187
HTH_MIN, HTH_MAX = 188, 273   # C-terminal HTH domain, per Section 3.8 / Fig 14
HINGE_RESI = 188        # domain-boundary residue used as the angle vertex

APO_SYSTEM = "apo_toxt_50ns"
HOLO_SYSTEMS = {"EPA": "epa_50ns", "GLA": "gla_50ns", "palmitic": "palmitic_50ns"}
REPLICATE_SUFFIXES = ("", "_r2", "_r3")


def load_traj(name):
    D = "md/" + name
    top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
    t = md.load(D + "/traj.dcd", top=top)
    return t[PROD_START:]


def per_frame_geometry(t):
    ca = t.topology.select("protein and name CA")
    resseq = np.array([t.topology.atom(i).residue.resSeq for i in ca])

    n_idx = ca[resseq <= N_DOMAIN_MAX]
    hth_idx = ca[(resseq >= HTH_MIN) & (resseq <= HTH_MAX)]
    hinge_idx = ca[resseq == HINGE_RESI]
    if len(hinge_idx) != 1:
        raise ValueError("expected exactly one CA at residue %d, found %d" % (HINGE_RESI, len(hinge_idx)))
    hinge_idx = hinge_idx[0]

    # superpose every frame onto this trajectory's own frame 0, using ONLY
    # the N-domain as the alignment reference, so downstream C-domain
    # coordinates reflect real inter-domain motion, not whole-molecule drift
    t.superpose(t, 0, atom_indices=n_idx)

    xyz = t.xyz  # (frames, atoms, 3), nm
    n_com = xyz[:, n_idx, :].mean(axis=1)      # (frames, 3)
    hth_com = xyz[:, hth_idx, :].mean(axis=1)  # (frames, 3)
    hinge = xyz[:, hinge_idx, :]               # (frames, 3)

    com_dist = np.linalg.norm(hth_com - n_com, axis=1) * 10.0  # nm -> A

    v1 = n_com - hinge
    v2 = hth_com - hinge
    cosang = (v1 * v2).sum(axis=1) / (np.linalg.norm(v1, axis=1) * np.linalg.norm(v2, axis=1))
    cosang = np.clip(cosang, -1.0, 1.0)
    hinge_angle = np.degrees(np.arccos(cosang))  # (frames,)

    return com_dist, hinge_angle


def replicate_stats(base):
    """Returns per-replicate (mean_dist, sd_dist, mean_angle, sd_angle) and
    the pooled per-frame angle array (for the distribution plot only)."""
    out = []
    pooled_angles = []
    for suffix in REPLICATE_SUFFIXES:
        name = base + suffix
        if not os.path.exists("md/%s/traj.dcd" % name):
            continue
        t = load_traj(name)
        com_dist, hinge_angle = per_frame_geometry(t)
        out.append((com_dist.mean(), com_dist.std(ddof=1),
                     hinge_angle.mean(), hinge_angle.std(ddof=1)))
        pooled_angles.append(hinge_angle)
        print("  %-20s frames=%4d  COM dist %.2f A  hinge angle %.1f +/- %.1f deg"
              % (name, len(hinge_angle), com_dist.mean(), hinge_angle.mean(), hinge_angle.std(ddof=1)))
    return np.array(out), pooled_angles


def summarize(label, arr):
    # arr: (n_replicates, 4) columns = mean_dist, sd_dist, mean_angle, sd_angle
    mean_dist, sd_dist, mean_angle, sd_angle = arr.T
    print("%-10s  COM dist: %.2f +/- %.2f A (across-replicate)   "
          "hinge mean: %.1f +/- %.1f deg (across-replicate)   "
          "hinge within-rep SD: %.1f +/- %.1f deg"
          % (label, mean_dist.mean(), mean_dist.std(ddof=1),
             mean_angle.mean(), mean_angle.std(ddof=1),
             sd_angle.mean(), sd_angle.std(ddof=1)))
    return mean_dist, mean_angle, sd_angle


print("=== apo ===")
apo_arr, apo_pooled = replicate_stats(APO_SYSTEM)
apo_dist, apo_mean_angle, apo_sd_angle = summarize("apo", apo_arr)

holo_results = {}
for label, base in HOLO_SYSTEMS.items():
    print("\n=== %s (free acid) ===" % label)
    arr, pooled = replicate_stats(base)
    dist, mean_angle, sd_angle = summarize(label, arr)
    holo_results[label] = (arr, pooled, dist, mean_angle, sd_angle)

print()
print("=== apo vs. holo comparison (n=3 replicates per group; Welch's t-test, indicative only) ===")
rows = [("system", "mean_hinge_angle_deg", "sd_across_reps", "within_rep_sd_deg", "sd_across_reps",
          "mean_COM_dist_A", "sd_across_reps",
          "t_meanangle_vs_apo", "p_meanangle_vs_apo", "t_withinSD_vs_apo", "p_withinSD_vs_apo")]
rows.append(("apo", "%.2f" % apo_mean_angle.mean(), "%.2f" % apo_mean_angle.std(ddof=1),
             "%.2f" % apo_sd_angle.mean(), "%.2f" % apo_sd_angle.std(ddof=1),
             "%.2f" % apo_dist.mean(), "%.2f" % apo_dist.std(ddof=1), "-", "-", "-", "-"))

for label, (arr, pooled, dist, mean_angle, sd_angle) in holo_results.items():
    t_mean, p_mean = stats.ttest_ind(apo_mean_angle, mean_angle, equal_var=False)
    t_sd, p_sd = stats.ttest_ind(apo_sd_angle, sd_angle, equal_var=False)
    print("%-10s mean hinge angle %.1f +/- %.1f deg (apo %.1f +/- %.1f)   t=%.2f p=%.3f"
          % (label, mean_angle.mean(), mean_angle.std(ddof=1),
             apo_mean_angle.mean(), apo_mean_angle.std(ddof=1), t_mean, p_mean))
    print("%-10s within-replicate angular SD %.2f +/- %.2f deg (apo %.2f +/- %.2f)   t=%.2f p=%.3f  <-- restraint test"
          % (label, sd_angle.mean(), sd_angle.std(ddof=1),
             apo_sd_angle.mean(), apo_sd_angle.std(ddof=1), t_sd, p_sd))
    rows.append((label, "%.2f" % mean_angle.mean(), "%.2f" % mean_angle.std(ddof=1),
                 "%.2f" % sd_angle.mean(), "%.2f" % sd_angle.std(ddof=1),
                 "%.2f" % dist.mean(), "%.2f" % dist.std(ddof=1),
                 "%.2f" % t_mean, "%.3f" % p_mean, "%.2f" % t_sd, "%.3f" % p_sd))

os.makedirs("figures", exist_ok=True)
with open("interdomain_hinge_summary.csv", "w", newline="") as f:
    csv.writer(f).writerows(rows)
print("\nwrote interdomain_hinge_summary.csv")

# distribution plot: pooled per-frame hinge angle, apo vs each holo system
fig, ax = plt.subplots(figsize=(7, 5))
all_pooled = [np.concatenate(apo_pooled)] + [np.concatenate(holo_results[l][1]) for l in HOLO_SYSTEMS]
labels = ["apo"] + list(HOLO_SYSTEMS.keys())
colors = ["#756bb1", "#2c7fb8", "#31a354", "#de2d26"]
parts = ax.violinplot(all_pooled, showmeans=True, showextrema=False)
for pc, c in zip(parts["bodies"], colors):
    pc.set_facecolor(c); pc.set_alpha(0.55)
parts["cmeans"].set_color("black")
ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(labels)
ax.set_ylabel("Inter-domain hinge angle (deg)\n(N-domain COM -- residue 188 CA -- HTH-domain COM)", fontsize=10)
ax.set_title("Inter-domain hinge angle, apo vs. holo ToxT\n(pooled production frames, n=3 replicates each; see interdomain_hinge_summary.csv for replicate-level stats)",
             fontsize=10, fontweight="bold")
ax.grid(alpha=0.25, axis="y")
fig.tight_layout()
fig.savefig("figures/fig_interdomain_hinge.png", dpi=200)
print("wrote figures/fig_interdomain_hinge.png")
