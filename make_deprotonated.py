"""Create a deprotonated (carboxylate, charge -1) version of a docked fatty-acid
pose, keeping the docked coordinates. For the pH-state MD comparison.

Run (meeko venv):  .venv\\Scripts\\python.exe make_deprotonated.py <in.sdf> <out.sdf>
"""
import sys
from rdkit import Chem

inp = sys.argv[1] if len(sys.argv) > 1 else "md/epa_pose.sdf"
out = sys.argv[2] if len(sys.argv) > 2 else "md/epa_deprot_pose.sdf"

m = Chem.MolFromMolFile(inp, removeHs=False)
patt = Chem.MolFromSmarts("[CX3](=O)[OX2H1]")
match = m.GetSubstructMatch(patt)
if not match:
    raise SystemExit("No protonated carboxylic acid found in " + inp)
o_h = match[2]  # the -OH oxygen
rw = Chem.RWMol(m)
# remove the hydrogen bonded to that oxygen
h_idx = [n.GetIdx() for n in rw.GetAtomWithIdx(o_h).GetNeighbors() if n.GetSymbol() == "H"]
for hi in sorted(h_idx, reverse=True):
    rw.RemoveAtom(hi)
rw.GetAtomWithIdx(o_h).SetFormalCharge(-1)
mol = rw.GetMol()
Chem.SanitizeMol(mol)
mol.SetProp("_Name", "EPA_carboxylate")
w = Chem.SDWriter(out); w.write(mol); w.close()
print("Wrote %s : net charge %d, %d atoms"
      % (out, Chem.GetFormalCharge(mol), mol.GetNumAtoms()))
