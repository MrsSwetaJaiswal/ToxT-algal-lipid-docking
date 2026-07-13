"""Native-ligand redocking control.

Redock palmitoleic acid (the co-crystallized fatty acid 'PAM' in 3GBG) into the
same pocket/box, then measure heavy-atom RMSD between the top docked pose and the
crystallographic PAM coordinates. RMSD < ~2.0 A validates the docking protocol.

Run:  .venv\\Scripts\\python.exe pam_control.py
"""
import os, subprocess, urllib.request, urllib.parse
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign
from meeko import PDBQTMolecule, RDKitMolCreate

ROOT = os.path.dirname(os.path.abspath(__file__))
MK   = os.path.join(ROOT, ".venv", "Scripts", "mk_prepare_ligand.exe")
VINA = os.path.join(ROOT, "tools", "vina.exe")
CFG  = os.path.join(ROOT, "docking_configs", "vina_config.txt")
CRYSTAL = os.path.join(ROOT, "prepared_structures", "pam_ref.pdb")
SDF   = os.path.join(ROOT, "ligands", "generated", "palmitoleic_acid.sdf")
PDBQT = os.path.join(ROOT, "ligands_pdbqt", "palmitoleic_acid.pdbqt")
OUT   = os.path.join(ROOT, "results_batch", "palmitoleic_acid_docked.pdbqt")

# 1. build 3D palmitoleic acid (cis-9-hexadecenoic acid, PubChem CID 445638)
if not os.path.exists(SDF):
    url = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/CanonicalSMILES/TXT"
           % urllib.parse.quote("palmitoleic acid"))
    smi = urllib.request.urlopen(url, timeout=30).read().decode().strip().splitlines()[0]
    m = Chem.AddHs(Chem.MolFromSmiles(smi))
    p = AllChem.ETKDGv3(); p.randomSeed = 42
    AllChem.EmbedMolecule(m, p); AllChem.MMFFOptimizeMolecule(m, maxIters=2000)
    m.SetProp("_Name", "palmitoleic_acid")
    w = Chem.SDWriter(SDF); w.write(m); w.close()
    print("Built", SDF, smi)

# 2. prep + 3. dock
if not os.path.exists(PDBQT):
    subprocess.run([MK, "-i", SDF, "-o", PDBQT], check=True, capture_output=True)
if not os.path.exists(OUT):
    subprocess.run([VINA, "--config", CFG, "--ligand", PDBQT, "--out", OUT],
                   check=True, capture_output=True)

def top_affinity(pdbqt):
    for line in open(pdbqt):
        if line.startswith("REMARK VINA RESULT"):
            return float(line.split()[3])

# 4. RMSD of docked pose vs crystal PAM (heavy atoms, symmetry-corrected, IN-PLACE)
# Build a clean topology template from the generated ligand:
template = Chem.RemoveHs(next(Chem.SDMolSupplier(SDF, removeHs=False)))

# Probe = top docked pose, reconstructed by Meeko with correct bonds + pose coords:
pmol  = PDBQTMolecule.from_file(OUT, skip_typing=True)
probe = Chem.RemoveHs(RDKitMolCreate.from_pdbqt_mol(pmol)[0])

# Reference = crystal PAM coordinates, given proper bond orders from the template:
ref_raw = Chem.MolFromPDBFile(CRYSTAL, removeHs=True, sanitize=False)
ref = AllChem.AssignBondOrdersFromTemplate(template, ref_raw)

print("\nDocked affinity: %.2f kcal/mol" % top_affinity(OUT))
print("Crystal PAM heavy atoms: %d | docked pose heavy atoms: %d"
      % (ref.GetNumAtoms(), probe.GetNumAtoms()))
# CalcRMS = symmetry-corrected RMSD using existing coordinates (no superposition),
# which is correct here because both are in the receptor (crystal) frame.
rmsd = rdMolAlign.CalcRMS(probe, ref)
print("Redocking RMSD (in-place, symmetry-corrected): %.2f A" % rmsd)
print("VALID (<2.0 A): protocol reproduces the crystal pose" if rmsd < 2.0
      else "CHECK (>=2.0 A): inspect pose/box in PyMOL")
