"""Batch docking pipeline for the CV / CCM lipid panel against ToxT (3GBG).

For every ligand SDF (from ligands/CV, ligands/CCM, ligands/generated):
  1. prepare PDBQT with Meeko (mk_prepare_ligand)
  2. dock with AutoDock Vina 1.2.7 using docking_configs/vina_config.txt
  3. record the top-pose affinity
Shared compounds (same PubChem CID) are docked only once and tagged with
both organisms. Deterministic (seed=42 in the config).

Run:  .venv\\Scripts\\python.exe dock_all.py
"""
import os, re, csv, subprocess, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MK   = os.path.join(ROOT, ".venv", "Scripts", "mk_prepare_ligand.exe")
VINA = os.path.join(ROOT, "tools", "vina.exe")
CFG  = os.path.join(ROOT, "docking_configs", "vina_config.txt")
PDBQT_DIR  = os.path.join(ROOT, "ligands_pdbqt")
RESULT_DIR = os.path.join(ROOT, "results_batch")
os.makedirs(PDBQT_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# organism membership overrides for generated structures (user-provided lists)
GENERATED_ORG = {
    "methyl_stearate":          "CV;CCM",
    "stearic_acid":             "CV",
    "methyl_heptadecanoate":    "CV",
    "methyl_heneicosanoate":    "CCM",
    "methyl_18_fluorostearate": "CCM",
}

def label_of(path):
    """Human-friendly, filesystem-safe ligand label from an SDF filename."""
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(r"Conformer3D_COMPOUND_", "", base)
    base = re.sub(r"CID_\d+", "", base)
    base = base.strip(" -_")
    base = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_").lower()
    return base or "ligand"

def cid_of(path):
    m = re.search(r"CID_(\d+)", os.path.basename(path))
    return m.group(1) if m else None

# --- collect unique ligands, keyed by CID (or label for generated) ---
ligands = {}  # key -> dict(label, sdf, organisms set, source)
def add(folder, organism, source):
    for sdf in sorted(glob.glob(os.path.join(ROOT, folder, "*.sdf"))):
        cid = cid_of(sdf)
        key = "CID_" + cid if cid else label_of(sdf)
        if key not in ligands:
            ligands[key] = {"label": label_of(sdf), "sdf": sdf,
                            "organisms": set(), "source": source}
        if organism:
            ligands[key]["organisms"].add(organism)

add("ligands/CV", "CV", "PubChem 3D")
add("ligands/CCM", "CCM", "PubChem 3D")
# generated: assign organisms from the override map
for sdf in sorted(glob.glob(os.path.join(ROOT, "ligands", "generated", "*.sdf"))):
    lbl = label_of(sdf)
    key = lbl
    ligands.setdefault(key, {"label": lbl, "sdf": sdf,
                             "organisms": set(), "source": "RDKit 3D (ETKDG/MMFF)"})
    for org in GENERATED_ORG.get(lbl, "").split(";"):
        if org:
            ligands[key]["organisms"].add(org)

print("Unique ligands to dock: %d" % len(ligands))

def top_affinity(pdbqt):
    with open(pdbqt) as f:
        for line in f:
            if line.startswith("REMARK VINA RESULT"):
                return float(line.split()[3])
    return None

rows = []
for key, info in sorted(ligands.items()):
    lbl = info["label"]
    pdbqt = os.path.join(PDBQT_DIR, lbl + ".pdbqt")
    out   = os.path.join(RESULT_DIR, lbl + "_docked.pdbqt")
    # 1. prepare
    if not os.path.exists(pdbqt):
        subprocess.run([MK, "-i", info["sdf"], "-o", pdbqt],
                       check=True, capture_output=True)
    # 2. dock
    if not os.path.exists(out):
        subprocess.run([VINA, "--config", CFG, "--ligand", pdbqt, "--out", out],
                       check=True, capture_output=True)
    aff = top_affinity(out)
    org = ";".join(sorted(info["organisms"])) or "?"
    rows.append((lbl, org, info["source"], aff))
    print("  %-40s %-7s %6.2f kcal/mol" % (lbl, org, aff))

rows.sort(key=lambda r: (r[3] if r[3] is not None else 0))
with open(os.path.join(RESULT_DIR, "affinities.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ligand", "organism", "structure_source", "affinity_kcal_mol"])
    w.writerows(rows)
print("\nWrote results_batch/affinities.csv (%d ligands)" % len(rows))
