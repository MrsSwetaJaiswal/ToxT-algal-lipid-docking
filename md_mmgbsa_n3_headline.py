"""n=3 MM-GBSA recompute for the headline free-acid ligands (EPA, GLA, palmitic),
the only systems with a completed r1+r2+r3 triplicate so far.

Runs md_mmgbsa.py once per (ligand, replicate), then reports
mean +/- SD ACROSS THE 3 REPLICATE MEANS (between-run error), per
MANUSCRIPT_TODO_reps.md item 1 -- NOT per-frame SD.

Run (md env):  ...python.exe md_mmgbsa_n3_headline.py [n_frames]
"""
import os, re, csv, subprocess, sys
import numpy as np

PY = r"C:\Users\ASUS\miniforge3\envs\md\python.exe"
NFR = sys.argv[1] if len(sys.argv) > 1 else "100"
os.makedirs("results_mmgbsa", exist_ok=True)

# (base_name, pose_sdf, display, form) -- free-acid headline systems only
LIGANDS = [
    ("epa_50ns",      "md/epa_pose.sdf",      "EPA",             "free acid"),
    ("gla_50ns",      "md/gla_pose.sdf",      "gamma-linolenic", "free acid"),
    ("palmitic_50ns", "md/palmitic_pose.sdf", "palmitic",        "free acid"),
]

rows = []
for base, sdf, disp, form in LIGANDS:
    reps = {}
    for rep, suffix in ((1, ""), (2, "_r2"), (3, "_r3")):
        name = base + suffix
        print("=== %s (rep %d) ===" % (name, rep), flush=True)
        out = subprocess.run([PY, "md_mmgbsa.py", sdf, name, NFR],
                             capture_output=True, text=True)
        m = re.search(r"dG_bind = ([-\d.]+) \+/- ([-\d.]+)", out.stdout)
        if m:
            mean = float(m.group(1))
            reps[rep] = mean
            print("  rep%d mean = %.1f kcal/mol" % (rep, mean), flush=True)
        else:
            print("  FAILED %s: %s %s" % (name, out.stdout[-300:], out.stderr[-300:]), flush=True)

    if len(reps) == 3:
        means = np.array([reps[1], reps[2], reps[3]])
        grand_mean = means.mean()
        sd_across = means.std(ddof=1)  # sample SD across the 3 replicate means
        rows.append((disp, form, reps[1], reps[2], reps[3], grand_mean, sd_across))
        print("  %-18s %-10s n=3 mean=%.1f +/- %.1f  (reps: %.1f, %.1f, %.1f)"
              % (disp, form, grand_mean, sd_across, reps[1], reps[2], reps[3]), flush=True)
    else:
        print("  INCOMPLETE for %s -- only %d/3 replicates succeeded" % (base, len(reps)), flush=True)

with open("results_mmgbsa/mmgbsa_n3_headline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ligand", "form", "r1_mean", "r2_mean", "r3_mean", "mean_of_means", "sd_across_means"])
    w.writerows(rows)
print("\nWrote results_mmgbsa/mmgbsa_n3_headline.csv (%d systems)" % len(rows))
