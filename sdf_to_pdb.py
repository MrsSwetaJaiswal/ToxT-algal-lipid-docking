"""Minimal SDF (V2000) -> PDB converter. No external dependencies.
Reads 3D coordinates + elements from the first molecule in an SDF and
writes HETATM records plus CONECT bonds for use with MGLTools prepare_ligand4.
"""
import sys

def convert(sdf_path, pdb_path, resname="LIG"):
    with open(sdf_path) as f:
        lines = f.read().splitlines()
    counts = lines[3]
    natoms = int(counts[0:3])
    nbonds = int(counts[3:6])
    atoms = []  # (x,y,z,element)
    for i in range(natoms):
        ln = lines[4 + i]
        x = float(ln[0:10]); y = float(ln[10:20]); z = float(ln[20:30])
        elem = ln[31:34].strip()
        atoms.append((x, y, z, elem))
    bonds = []
    for j in range(nbonds):
        ln = lines[4 + natoms + j]
        a = int(ln[0:3]); b = int(ln[3:6])
        bonds.append((a, b))

    # per-element counter for unique atom names
    elem_count = {}
    names = []
    for (_, _, _, elem) in atoms:
        elem_count[elem] = elem_count.get(elem, 0) + 1
        names.append("%s%d" % (elem, elem_count[elem]))

    out = open(pdb_path, "w")
    idx = 0
    for (x, y, z, elem) in atoms:
        idx += 1
        name = names[idx - 1]
        atom_name = (name if len(name) >= 4 else " " + name).ljust(4)[:4]
        out.write(
            "HETATM%5d %s%3s A   1    %8.3f%8.3f%8.3f  1.00  0.00          %2s\n"
            % (idx, atom_name, resname, x, y, z, elem)
        )
    for (a, b) in bonds:
        out.write("CONECT%5d%5d\n" % (a, b))
    out.write("END\n")
    out.close()
    print("Wrote %s: %d atoms, %d bonds" % (pdb_path, natoms, nbonds))

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
