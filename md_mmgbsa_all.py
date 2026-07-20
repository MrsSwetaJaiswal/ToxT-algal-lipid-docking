"""Batch MM-GBSA over all 13 MD systems (calls the validated md_mmgbsa.py).
Writes results_mmgbsa/mmgbsa.csv. Run (md env):
   ...python.exe md_mmgbsa_all.py [n_frames]
"""
import os, re, csv, subprocess, sys

PY = r"C:\Users\ASUS\miniforge3\envs\md\python.exe"
NFR = sys.argv[1] if len(sys.argv) > 1 else "25"
os.makedirs("results_mmgbsa", exist_ok=True)

# (run_name, pose_sdf, display, form)
RUNS = [
    ("epa_50ns","md/epa_pose.sdf","EPA","free acid"),
    ("methyl_epa_50ns","md/methyl_epa_pose.sdf","EPA","methyl ester"),
    ("epa_deprot_50ns","md/epa_deprot_pose.sdf","EPA","carboxylate"),
    ("gla_50ns","md/gla_pose.sdf","gamma-linolenic","free acid"),
    ("gla_ester_50ns","md/gla_ester_pose.sdf","gamma-linolenic","methyl ester"),
    ("gla_deprot_50ns","md/gla_deprot_pose.sdf","gamma-linolenic","carboxylate"),
    ("palmitic_50ns","md/palmitic_pose.sdf","palmitic","free acid"),
    ("methyl_palmitate_50ns","md/methyl_palmitate_pose.sdf","palmitic","methyl ester"),
    ("palmitic_deprot_50ns","md/palmitic_deprot_pose.sdf","palmitic","carboxylate"),
    ("pam_50ns","md/pam_pose.sdf","palmitoleate (native)","+control"),
    ("glucose_decoy_50ns","md/glucose_pose.sdf","glucose","decoy"),
    ("pentadecanal_50ns","md/pentadecanal_pose.sdf","pentadecanal","weak"),
    ("tridecanoic_50ns","md/tridecanoic_pose.sdf","tridecanoic","weak"),
]

rows = []
for name, sdf, disp, form in RUNS:
    print("=== %s ===" % name, flush=True)
    out = subprocess.run([PY, "md_mmgbsa.py", sdf, name, NFR],
                         capture_output=True, text=True)
    m = re.search(r"dG_bind = ([-\d.]+) \+/- ([-\d.]+)", out.stdout)
    if m:
        mean, sd = float(m.group(1)), float(m.group(2))
        rows.append((disp, form, mean, sd))
        print("  %-22s %-13s %.1f +/- %.1f kcal/mol" % (disp, form, mean, sd), flush=True)
    else:
        print("  FAILED:", out.stdout[-200:], out.stderr[-200:], flush=True)

rows.sort(key=lambda r: r[2])
with open("results_mmgbsa/mmgbsa.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ligand","form","mmgbsa_kcal_mol","sd_kcal_mol"])
    w.writerows(rows)
print("\nWrote results_mmgbsa/mmgbsa.csv (%d systems)" % len(rows))
