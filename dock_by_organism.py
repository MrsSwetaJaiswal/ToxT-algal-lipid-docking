"""Two separate docking runs: CV and CCM, against ToxT (3GBG).

Each organism has its own ligand set, output folder, and results CSV.
Ligand PDBQT prep (Meeko) is shared/cached; docking (Vina 1.2.7, seed=42) is
run per organism into results_<ORG>/. Usage:

    .venv\\Scripts\\python.exe dock_by_organism.py CV
    .venv\\Scripts\\python.exe dock_by_organism.py CCM
"""
import os, re, csv, sys, glob, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
MK   = os.path.join(ROOT, ".venv", "Scripts", "mk_prepare_ligand.exe")
VINA = os.path.join(ROOT, "tools", "vina.exe")
CFG  = os.path.join(ROOT, "docking_configs", "vina_config.txt")
PDBQT_DIR = os.path.join(ROOT, "ligands_pdbqt")
os.makedirs(PDBQT_DIR, exist_ok=True)

def label_of(path):
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(r"Conformer3D_COMPOUND_", "", base)
    base = re.sub(r"CID_\d+", "", base).strip(" -_")
    return re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_").lower() or "ligand"

def g(*parts):
    return sorted(glob.glob(os.path.join(ROOT, *parts)))

GEN = lambda name: os.path.join(ROOT, "ligands", "generated", name + ".sdf")
CCM_FILE = lambda cid: g("ligands", "CCM", "*CID_%s*.sdf" % cid)[0]

# ---- explicit per-organism ligand sets (SDF paths) ----
SETS = {
    "CV": g("ligands", "CV", "*.sdf") + [
        GEN("methyl_stearate"),
        GEN("stearic_acid"),
        GEN("methyl_heptadecanoate"),
        CCM_FILE("5312435"),          # cis-10-heptadecenoic acid (in CV's missing list)
    ],
    "CCM": g("ligands", "CCM", "*.sdf") + [
        GEN("methyl_stearate"),
        GEN("methyl_heneicosanoate"),
        GEN("methyl_18_fluorostearate"),
    ],
}

def top_affinity(pdbqt):
    for line in open(pdbqt):
        if line.startswith("REMARK VINA RESULT"):
            return float(line.split()[3])

def run(org):
    sdfs = SETS[org]
    out_dir = os.path.join(ROOT, "results_%s" % org)
    os.makedirs(out_dir, exist_ok=True)
    # dedup by label within the organism
    seen, items = set(), []
    for s in sdfs:
        lbl = label_of(s)
        if lbl not in seen:
            seen.add(lbl); items.append((lbl, s))
    print("=== %s : %d ligands ===" % (org, len(items)))
    rows = []
    for lbl, sdf in items:
        pdbqt = os.path.join(PDBQT_DIR, lbl + ".pdbqt")
        out   = os.path.join(out_dir, lbl + "_docked.pdbqt")
        if not os.path.exists(pdbqt):
            subprocess.run([MK, "-i", sdf, "-o", pdbqt], check=True, capture_output=True)
        if not os.path.exists(out):
            subprocess.run([VINA, "--config", CFG, "--ligand", pdbqt, "--out", out],
                           check=True, capture_output=True)
        aff = top_affinity(out)
        rows.append((lbl, aff))
        print("  %-42s %6.2f kcal/mol" % (lbl, aff), flush=True)
    rows.sort(key=lambda r: r[1])
    csv_path = os.path.join(ROOT, "results_%s" % org, "affinities_%s.csv" % org)
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["ligand", "affinity_kcal_mol"]); w.writerows(rows)
    print("Wrote", csv_path, "\n")

if __name__ == "__main__":
    targets = [sys.argv[1]] if len(sys.argv) > 1 else ["CV", "CCM"]
    for org in targets:
        run(org)
