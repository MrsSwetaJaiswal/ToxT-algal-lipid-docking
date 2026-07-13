"""Benchmark: dock known ToxT ligands under the SAME protocol as the algal lipids,
so binding scores are directly comparable (same program, box, seed). Prior papers
used different programs/units (GOLD fitness, kJ/mol, etc.) that cannot be compared.

Run (.venv):  .venv\\Scripts\\python.exe benchmark_inhibitors.py
"""
import os, csv, subprocess, urllib.request, urllib.parse
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = os.path.dirname(os.path.abspath(__file__))
MK   = os.path.join(ROOT, ".venv", "Scripts", "mk_prepare_ligand.exe")
VINA = os.path.join(ROOT, "tools", "vina.exe")
CFG  = os.path.join(ROOT, "docking_configs", "vina_config.txt")
SDF_DIR = os.path.join(ROOT, "ligands", "benchmark"); os.makedirs(SDF_DIR, exist_ok=True)
PDBQT_DIR = os.path.join(ROOT, "ligands_pdbqt")
OUT_DIR = os.path.join(ROOT, "results_benchmark"); os.makedirs(OUT_DIR, exist_ok=True)

# label : (pubchem name, role)
TARGETS = {
    "virstatin":      ("virstatin", "known ToxT inhibitor (synthetic)"),
    "butyric_acid":   ("butyric acid", "SCFA, recent ToxT-targeting (natural)"),
    "oleic_acid":     ("oleic acid", "unsaturated FA comparator (native-type)"),
}

def smiles(name):
    url = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/CanonicalSMILES/TXT"
           % urllib.parse.quote(name))
    return urllib.request.urlopen(url, timeout=30).read().decode().strip().splitlines()[0]

def top_aff(pdbqt):
    for line in open(pdbqt):
        if line.startswith("REMARK VINA RESULT"):
            return float(line.split()[3])

rows = []
for label, (name, role) in TARGETS.items():
    sdf = os.path.join(SDF_DIR, label + ".sdf")
    pdbqt = os.path.join(PDBQT_DIR, label + ".pdbqt")
    out = os.path.join(OUT_DIR, label + "_docked.pdbqt")
    if not os.path.exists(sdf):
        smi = smiles(name)
        m = Chem.AddHs(Chem.MolFromSmiles(smi))
        p = AllChem.ETKDGv3(); p.randomSeed = 42
        AllChem.EmbedMolecule(m, p); AllChem.MMFFOptimizeMolecule(m, maxIters=2000)
        m.SetProp("_Name", label)
        w = Chem.SDWriter(sdf); w.write(m); w.close()
        print("built %-14s %s" % (label, smi))
    if not os.path.exists(pdbqt):
        subprocess.run([MK, "-i", sdf, "-o", pdbqt], check=True, capture_output=True)
    if not os.path.exists(out):
        subprocess.run([VINA, "--config", CFG, "--ligand", pdbqt, "--out", out],
                       check=True, capture_output=True)
    aff = top_aff(out)
    rows.append((label, role, aff))
    print("  %-14s %6.2f kcal/mol   (%s)" % (label, aff, role))

with open(os.path.join(OUT_DIR, "benchmark.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["compound", "role", "affinity_kcal_mol"]); w.writerows(rows)
print("\nWrote results_benchmark/benchmark.csv")
print("Compare against algal lipids: CV/CCM range -6.8 to -8.8 kcal/mol")
