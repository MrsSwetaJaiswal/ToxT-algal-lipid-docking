"""n=3 MM-GBSA recompute for the remaining ligand forms -- everything except the
3 headline free-acid systems already done in md_mmgbsa_n3_headline.py (EPA,
GLA, palmitic free acid). Covers all carboxylate/ester forms plus the
palmitoleate control, glucose decoy, and the two weak binders, now that the
full n=3 replicate campaign (md_supervisor_reps.py) has finished for all of
them.

Reports mean +/- SD ACROSS THE 3 REPLICATE MEANS (between-run error), per
MANUSCRIPT_TODO_reps.md item 1 -- NOT per-frame SD.

Run (md env -- needs OpenMM/OpenFF/PDBFixer; ONLY safe when no other md-env
process is running concurrently, see CAMPAIGN_LOG.md 2026-08-01):
  C:\\Users\\ASUS\\miniforge3\\envs\\md\\python.exe md_mmgbsa_n3_remaining.py [n_frames]
"""
import os, re, csv, subprocess, sys
import numpy as np

PY = r"C:\Users\ASUS\miniforge3\envs\md\python.exe"
NFR = sys.argv[1] if len(sys.argv) > 1 else "100"
os.makedirs("results_mmgbsa", exist_ok=True)

# (base_name, pose_sdf, display, form)
LIGANDS = [
    ("methyl_epa_50ns",      "md/methyl_epa_pose.sdf",      "EPA",                 "methyl ester"),
    ("epa_deprot_50ns",      "md/epa_deprot_pose.sdf",      "EPA",                 "carboxylate"),
    ("gla_ester_50ns",       "md/gla_ester_pose.sdf",       "gamma-linolenic",     "methyl ester"),
    ("gla_deprot_50ns",      "md/gla_deprot_pose.sdf",      "gamma-linolenic",     "carboxylate"),
    ("methyl_palmitate_50ns","md/methyl_palmitate_pose.sdf","palmitic",            "methyl ester"),
    ("palmitic_deprot_50ns", "md/palmitic_deprot_pose.sdf", "palmitic",            "carboxylate"),
    ("pam_50ns",             "md/pam_pose.sdf",             "palmitoleate (native)","+control"),
    ("glucose_decoy_50ns",   "md/glucose_pose.sdf",         "glucose",             "decoy"),
    ("pentadecanal_50ns",    "md/pentadecanal_pose.sdf",    "pentadecanal",        "weak"),
    ("tridecanoic_50ns",     "md/tridecanoic_pose.sdf",     "tridecanoic",         "weak"),
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
        sd_across = means.std(ddof=1)
        rows.append((disp, form, reps[1], reps[2], reps[3], grand_mean, sd_across))
        print("  %-22s %-14s n=3 mean=%.1f +/- %.1f  (reps: %.1f, %.1f, %.1f)"
              % (disp, form, grand_mean, sd_across, reps[1], reps[2], reps[3]), flush=True)
    else:
        print("  INCOMPLETE for %s -- only %d/3 replicates succeeded" % (base, len(reps)), flush=True)

with open("results_mmgbsa/mmgbsa_n3_remaining.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ligand", "form", "r1_mean", "r2_mean", "r3_mean", "mean_of_means", "sd_across_means"])
    w.writerows(rows)
print("\nWrote results_mmgbsa/mmgbsa_n3_remaining.csv (%d systems)" % len(rows))
