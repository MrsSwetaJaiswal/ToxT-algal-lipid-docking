"""Consensus scoring: re-dock every ligand with the Vinardo scoring function
(the scoring function introduced by SMINA) and compare rankings to the default
Vina scoring. Agreement => credible binding ranking; disagreement => possible
false positive. Uses Vina 1.2.7 --scoring vinardo (independent search, seed=42).

Run:  .venv\\Scripts\\python.exe consensus_scoring.py
"""
import os, csv, glob, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VINA = os.path.join(ROOT, "tools", "vina.exe")
CFG  = os.path.join(ROOT, "docking_configs", "vina_config.txt")
PDBQT_DIR = os.path.join(ROOT, "ligands_pdbqt")
OUT_DIR   = os.path.join(ROOT, "results_vinardo")
os.makedirs(OUT_DIR, exist_ok=True)

def top_affinity(pdbqt):
    for line in open(pdbqt):
        if line.startswith("REMARK VINA RESULT"):
            return float(line.split()[3])

# Vina (default) affinities already computed, gather from per-organism CSVs
vina_aff = {}
for path in (os.path.join(ROOT, "results_CV", "affinities_CV.csv"),
             os.path.join(ROOT, "results_CCM", "affinities_CCM.csv")):
    with open(path) as f:
        for r in csv.DictReader(f):
            vina_aff[r["ligand"]] = float(r["affinity_kcal_mol"])

# Vinardo redock for every prepared ligand
vinardo_aff = {}
for pdbqt in sorted(glob.glob(os.path.join(PDBQT_DIR, "*.pdbqt"))):
    lbl = os.path.splitext(os.path.basename(pdbqt))[0]
    out = os.path.join(OUT_DIR, lbl + "_vinardo.pdbqt")
    if not os.path.exists(out):
        subprocess.run([VINA, "--config", CFG, "--scoring", "vinardo",
                        "--ligand", pdbqt, "--out", out],
                       check=True, capture_output=True)
    vinardo_aff[lbl] = top_affinity(out)
    print("  %-42s vinardo %6.2f" % (lbl, vinardo_aff[lbl]), flush=True)

# merge + Spearman rank correlation
common = sorted(set(vina_aff) & set(vinardo_aff))
def ranks(d, keys):
    order = sorted(keys, key=lambda k: d[k])
    return {k: i for i, k in enumerate(order)}
rv, rd = ranks(vina_aff, common), ranks(vinardo_aff, common)
n = len(common)
dsq = sum((rv[k]-rd[k])**2 for k in common)
spearman = 1 - 6*dsq/(n*(n*n-1)) if n > 1 else float("nan")

with open(os.path.join(OUT_DIR, "consensus.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ligand", "vina_kcal_mol", "vinardo_kcal_mol", "mean_kcal_mol"])
    for k in sorted(common, key=lambda k: (vina_aff[k]+vinardo_aff[k])/2):
        w.writerow([k, vina_aff[k], vinardo_aff[k],
                    round((vina_aff[k]+vinardo_aff[k])/2, 2)])

print("\nLigands compared: %d" % n)
print("Spearman rank correlation (Vina vs Vinardo): %.3f" % spearman)
print("Strong agreement (>0.7): consensus supports the ranking" if spearman > 0.7
      else "Weak agreement: inspect disagreeing ligands")
print("Wrote results_vinardo/consensus.csv")
