"""Structural property analysis: relate computed descriptors to docking affinity.

Reads results_batch/affinities.csv and the source SDFs, computes physicochemical
descriptors for each lipid, merges them, and reports correlations with binding
affinity. Answers: why do the lipids differ, and what makes a good ToxT binder?

Run:  .venv\\Scripts\\python.exe structural_analysis.py
"""
import os, csv, glob, re
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Crippen

ROOT = os.path.dirname(os.path.abspath(__file__))
AFF_FILES = {"CV":  os.path.join(ROOT, "results_CV", "affinities_CV.csv"),
             "CCM": os.path.join(ROOT, "results_CCM", "affinities_CCM.csv")}
OUT  = os.path.join(ROOT, "results_batch", "structure_property.csv")
os.makedirs(os.path.join(ROOT, "results_batch"), exist_ok=True)

def label_of(path):
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(r"Conformer3D_COMPOUND_", "", base)
    base = re.sub(r"CID_\d+", "", base).strip(" -_")
    return re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_").lower() or "ligand"

# map label -> first SDF found
sdf_by_label = {}
for folder in ("ligands/CV", "ligands/CCM", "ligands/generated"):
    for sdf in glob.glob(os.path.join(ROOT, folder, "*.sdf")):
        sdf_by_label.setdefault(label_of(sdf), sdf)

def descriptors(sdf):
    m = next(Chem.SDMolSupplier(sdf, removeHs=False))
    if m is None:
        return None
    n_C = sum(1 for a in m.GetAtoms() if a.GetSymbol() == "C")
    n_dbond = sum(1 for b in m.GetBonds()
                  if b.GetBondType() == Chem.BondType.DOUBLE
                  and b.GetBeginAtom().GetSymbol() == "C"
                  and b.GetEndAtom().GetSymbol() == "C")
    smi = Chem.MolToSmiles(Chem.RemoveHs(m))
    headgroup = "ester" if ("OC" in smi and "C(=O)O" not in smi.replace("C(=O)OC", "")) else "acid"
    if "C(=O)OC" in smi or smi.count("OC") and "(=O)O" in smi and not smi.rstrip().endswith("O"):
        pass
    is_ester = m.HasSubstructMatch(Chem.MolFromSmarts("[CX3](=O)[OX2][CX4]"))
    is_acid  = m.HasSubstructMatch(Chem.MolFromSmarts("[CX3](=O)[OX2H1]"))
    return {
        "n_carbons": n_C,
        "C_C_double_bonds": n_dbond,
        "headgroup": "ester" if is_ester else ("acid" if is_acid else "other"),
        "MW": round(Descriptors.MolWt(m), 1),
        "logP": round(Crippen.MolLogP(m), 2),
        "TPSA": round(rdMolDescriptors.CalcTPSA(m), 1),
        "rot_bonds": rdMolDescriptors.CalcNumRotatableBonds(m),
    }

# merge both organism CSVs; dedup shared ligands and record organism membership
merged = {}  # label -> dict
for org, path in AFF_FILES.items():
    with open(path) as f:
        for r in csv.DictReader(f):
            lbl = r["ligand"]
            rec = merged.setdefault(lbl, {"affinity": float(r["affinity_kcal_mol"]),
                                          "orgs": set()})
            rec["orgs"].add(org)

rows = []
for lbl, rec in merged.items():
    sdf = sdf_by_label.get(lbl)
    d = descriptors(sdf) if sdf else None
    if d:
        d.update({"ligand": lbl, "organism": ";".join(sorted(rec["orgs"])),
                  "affinity": rec["affinity"]})
        rows.append(d)

cols = ["ligand", "organism", "affinity", "n_carbons", "C_C_double_bonds",
        "headgroup", "MW", "logP", "TPSA", "rot_bonds"]
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in sorted(rows, key=lambda x: x["affinity"]):
        w.writerow({c: r[c] for c in cols})

# Pearson correlations of numeric descriptors vs affinity (more negative = stronger)
def pearson(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    cov = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    sx = (sum((x-mx)**2 for x in xs))**0.5
    sy = (sum((y-my)**2 for y in ys))**0.5
    return cov/(sx*sy) if sx and sy else float("nan")

aff = [r["affinity"] for r in rows]
print("n ligands: %d\n" % len(rows))
print("Correlation with affinity (negative r => property increases binding strength):")
for p in ["n_carbons", "C_C_double_bonds", "MW", "logP", "TPSA", "rot_bonds"]:
    print("  %-18s r = %+.2f" % (p, pearson([r[p] for r in rows], aff)))

# acid vs ester comparison
for grp in ("acid", "ester"):
    g = [r["affinity"] for r in rows if r["headgroup"] == grp]
    if g:
        print("\n%-6s n=%2d  mean affinity = %.2f kcal/mol" % (grp, len(g), sum(g)/len(g)))
print("\nWrote results_batch/structure_property.csv")
