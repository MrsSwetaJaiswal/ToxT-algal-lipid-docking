"""Dock every fatty acid in BOTH forms (free acid AND methyl ester), per organism.

GC-MS identifies the species but not the bioactive form. For each fatty-acid
backbone in CV and CCM we generate both the free-acid and methyl-ester form
(RDKit reaction transform), dock both (Vina 1.2.7, seed=42), and report them
side by side so the form preference can be read off directly.

Non fatty-acids (e.g. neophytadiene, pentadecanal) are skipped automatically.

Run:  .venv\\Scripts\\python.exe pairs_pipeline.py
"""
import os, re, csv, glob, hashlib, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

ROOT = os.path.dirname(os.path.abspath(__file__))
MK   = os.path.join(ROOT, ".venv", "Scripts", "mk_prepare_ligand.exe")
VINA = os.path.join(ROOT, "tools", "vina.exe")
CFG  = os.path.join(ROOT, "docking_configs", "vina_config.txt")
SDF_DIR   = os.path.join(ROOT, "ligands", "pairs_sdf")
PDBQT_DIR = os.path.join(ROOT, "ligands", "pairs_pdbqt")
DOCK_DIR  = os.path.join(ROOT, "results_pairs")
for d in (SDF_DIR, PDBQT_DIR, DOCK_DIR):
    os.makedirs(d, exist_ok=True)

ESTER = Chem.MolFromSmarts("[CX3](=O)[OX2][CH3]")
ACID  = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")
RX_ESTER_TO_ACID = AllChem.ReactionFromSmarts("[CX3:1](=[O:2])[OX2:3][CH3]>>[CX3:1](=[O:2])[OX2:3][H]")
RX_ACID_TO_ESTER = AllChem.ReactionFromSmarts("[CX3:1](=[O:2])[OX2H:3]>>[CX3:1](=[O:2])[O:3]C")

def label_of(path):
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(r"Conformer3D_COMPOUND_", "", base)
    base = re.sub(r"CID_\d+", "", base).strip(" -_")
    return re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_").lower() or "ligand"

def g(*p): return sorted(glob.glob(os.path.join(ROOT, *p)))
GEN = lambda n: os.path.join(ROOT, "ligands", "generated", n + ".sdf")
def ccm(cid): return g("ligands", "CCM", "*CID_%s*.sdf" % cid)[0]

SETS = {
    "CV":  g("ligands", "CV", "*.sdf") + [GEN("methyl_stearate"), GEN("stearic_acid"),
            GEN("methyl_heptadecanoate"), ccm("5312435")],
    "CCM": g("ligands", "CCM", "*.sdf") + [GEN("methyl_stearate"),
            GEN("methyl_heneicosanoate"), GEN("methyl_18_fluorostearate")],
}

def both_forms(sdf):
    """Return (acid_smiles, ester_smiles) or None if not a fatty acid/ester."""
    m = next(Chem.SDMolSupplier(sdf, removeHs=False))
    if m is None: return None
    m = Chem.MolFromSmiles(Chem.MolToSmiles(Chem.RemoveHs(m)))
    if m is None: return None
    if m.HasSubstructMatch(ACID):
        acid = m
        prod = RX_ACID_TO_ESTER.RunReactants((m,))
        ester = prod[0][0] if prod else None
    elif m.HasSubstructMatch(ESTER):
        ester = m
        prod = RX_ESTER_TO_ACID.RunReactants((m,))
        acid = prod[0][0] if prod else None
    else:
        return None
    if acid is None or ester is None: return None
    for x in (acid, ester):
        Chem.SanitizeMol(x)
    return Chem.MolToSmiles(Chem.RemoveHs(acid)), Chem.MolToSmiles(Chem.RemoveHs(ester))

def embed_prep_dock(smi):
    """Cached: SMILES -> top docked affinity. Returns (affinity, sdf, formula)."""
    h = hashlib.md5(smi.encode()).hexdigest()[:10]
    sdf   = os.path.join(SDF_DIR, h + ".sdf")
    pdbqt = os.path.join(PDBQT_DIR, h + ".pdbqt")
    out   = os.path.join(DOCK_DIR, h + "_docked.pdbqt")
    m = Chem.AddHs(Chem.MolFromSmiles(smi))
    if not os.path.exists(sdf):
        p = AllChem.ETKDGv3(); p.randomSeed = 42
        AllChem.EmbedMolecule(m, p); AllChem.MMFFOptimizeMolecule(m, maxIters=2000)
        m.SetProp("_Name", smi)
        w = Chem.SDWriter(sdf); w.write(m); w.close()
    if not os.path.exists(pdbqt):
        subprocess.run([MK, "-i", sdf, "-o", pdbqt], check=True, capture_output=True)
    if not os.path.exists(out):
        subprocess.run([VINA, "--config", CFG, "--ligand", pdbqt, "--out", out],
                       check=True, capture_output=True)
    aff = None
    for line in open(out):
        if line.startswith("REMARK VINA RESULT"):
            aff = float(line.split()[3]); break
    return aff, rdMolDescriptors.CalcMolFormula(Chem.RemoveHs(m))

def descriptors(smi):
    m = Chem.MolFromSmiles(smi)
    nC = sum(1 for a in m.GetAtoms() if a.GetSymbol() == "C")
    ndb = sum(1 for b in m.GetBonds() if b.GetBondType() == Chem.BondType.DOUBLE
              and b.GetBeginAtom().GetSymbol() == "C" and b.GetEndAtom().GetSymbol() == "C")
    return nC, ndb

def main():
  for org, sdfs in SETS.items():
    backbones = {}  # acid_smiles -> dict(name, acid, ester)
    for sdf in sdfs:
        forms = both_forms(sdf)
        if forms is None:
            print("skip (not fatty acid/ester):", label_of(sdf)); continue
        acid_smi, ester_smi = forms
        backbones.setdefault(acid_smi, {"name": label_of(sdf),
                                        "acid": acid_smi, "ester": ester_smi})
    print("\n=== %s : %d fatty-acid backbones x 2 forms ===" % (org, len(backbones)))
    rows = []
    for acid_smi, info in backbones.items():
        a_aff, _ = embed_prep_dock(info["acid"])
        e_aff, _ = embed_prep_dock(info["ester"])
        nC, ndb = descriptors(acid_smi)
        rows.append({"backbone": info["name"], "C": nC, "C_C_double": ndb,
                     "acid_kcal": a_aff, "ester_kcal": e_aff,
                     "ester_minus_acid": round(e_aff - a_aff, 2)})
        print("  %-34s C%d:%d  acid %6.2f  ester %6.2f  (d=%+.2f)" %
              (info["name"], nC, ndb, a_aff, e_aff, e_aff - a_aff), flush=True)
    rows.sort(key=lambda r: min(r["acid_kcal"], r["ester_kcal"]))
    out_csv = os.path.join(ROOT, "results_pairs", "pairs_%s.csv" % org)
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["backbone","C","C_C_double",
                            "acid_kcal","ester_kcal","ester_minus_acid"])
        w.writeheader(); w.writerows(rows)
    print("Wrote", out_csv)

if __name__ == "__main__":
    main()
