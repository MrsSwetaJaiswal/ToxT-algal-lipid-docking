"""Generate 3D SDF conformers for ligands lacking a PubChem 3D record.
Method: fetch canonical SMILES from PubChem (by name) OR use a supplied SMILES,
then embed 3D with RDKit ETKDGv3 and minimize with MMFF94 (same approach as
PubChem's Conformer3D). Fully reproducible (fixed random seed).

Run:  .venv\\Scripts\\python.exe generate_missing_3d.py
"""
import os, sys, time
import urllib.request, urllib.parse
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

OUTDIR = "ligands/generated"
os.makedirs(OUTDIR, exist_ok=True)

# label : ("name", pubchem_name)  OR  ("smiles", SMILES)
TARGETS = {
    "methyl_stearate":            ("name", "methyl stearate"),
    "stearic_acid":               ("name", "octadecanoic acid"),
    "methyl_heptadecanoate":      ("name", "methyl heptadecanoate"),
    "methyl_heneicosanoate":      ("name", "methyl heneicosanoate"),
    # custom synthetic compound; built directly from SMILES (F on omega carbon)
    "methyl_18_fluorostearate":   ("smiles", "COC(=O)CCCCCCCCCCCCCCCCCF"),
}

def smiles_from_pubchem(name):
    url = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/CanonicalSMILES/TXT"
           % urllib.parse.quote(name))
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode().strip().splitlines()[0]

def build(label, kind, value):
    smi = value if kind == "smiles" else smiles_from_pubchem(value)
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        raise ValueError("Bad SMILES for %s: %s" % (label, smi))
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    if AllChem.EmbedMolecule(mol, params) != 0:
        raise RuntimeError("Embedding failed for %s" % label)
    AllChem.MMFFOptimizeMolecule(mol, maxIters=2000)
    mol.SetProp("_Name", label)
    out = os.path.join(OUTDIR, label + ".sdf")
    w = Chem.SDWriter(out)
    w.write(mol); w.close()
    formula = rdMolDescriptors.CalcMolFormula(mol)
    print("OK  %-26s %-32s %s  -> %s" % (label, smi, formula, out))

if __name__ == "__main__":
    for label, (kind, value) in TARGETS.items():
        try:
            build(label, kind, value)
            time.sleep(0.3)
        except Exception as e:
            print("FAIL %-26s %s" % (label, e))
