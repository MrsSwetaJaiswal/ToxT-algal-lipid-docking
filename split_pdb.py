"""Split a PDB into (1) protein-only and (2) the bound ligand, for docking prep.
Replaces the grep commands so it works on Windows. Run with the venv python:
    .venv\\Scripts\\python.exe split_pdb.py
"""
import os

SRC = "structures/3GBG.pdb"
PROTEIN_OUT = "prepared_structures/3GBG_protein_only.pdb"
LIGAND_OUT = "prepared_structures/pam_ref.pdb"
LIGAND_RESNAME = "PAM"   # the co-crystallized fatty acid in 3GBG

os.makedirs("prepared_structures", exist_ok=True)

protein, ligand = [], []
with open(SRC) as f:
    for line in f:
        if line.startswith(("ATOM", "TER")):
            protein.append(line)
        elif line.startswith("HETATM") and line[17:20].strip() == LIGAND_RESNAME:
            ligand.append(line)

with open(PROTEIN_OUT, "w") as f:
    f.writelines(protein)
    f.write("END\n")

with open(LIGAND_OUT, "w") as f:
    f.writelines(ligand)

print("Wrote %s  (%d protein lines)" % (PROTEIN_OUT, len(protein)))
print("Wrote %s  (%d ligand atoms)" % (LIGAND_OUT, len(ligand)))
