"""Export the top docked pose of a ligand to SDF (with bonds + explicit H + pose
coordinates) for use as the MD starting structure. Run with the MEEKO venv:
    .venv\\Scripts\\python.exe export_docked_pose.py <docked.pdbqt> <out.sdf>
"""
import sys
from meeko import PDBQTMolecule, RDKitMolCreate
from rdkit import Chem

infile, out = sys.argv[1], sys.argv[2]
pmol = PDBQTMolecule.from_file(infile, skip_typing=True)
mol = RDKitMolCreate.from_pdbqt_mol(pmol)[0]   # best pose = conformer 0
w = Chem.SDWriter(out)
w.write(mol, confId=0)
w.close()
print("Wrote %s : %d atoms (Hs included), top pose" % (out, mol.GetNumAtoms()))
