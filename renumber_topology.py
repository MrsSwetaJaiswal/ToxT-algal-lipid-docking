"""Renumber MD topology files from the OpenMM/PDBFixer internal numbering to the
published crystal (PDB 3GBG) residue numbering, so shipped files match the paper.

Deterministic: the map is built by order-aligning the protein sequence of the MD
system to the crystal sequence (verified 0/260 identity mismatches). Only protein
residue NUMBERS are changed; coordinates, atom order, waters, ions and the ligand
are untouched. Writes system_pub.pdb next to each system.pdb. The trajectories
(DCD) store no residue numbers, so nothing there needs changing.

Run (.venv):  .venv\\Scripts\\python.exe renumber_topology.py
"""
import os, glob

AA = set("ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split())

def resseq(path):
    seen = []; last = None
    for line in open(path):
        if line[:4] == "ATOM":
            resi = int(line[22:26])
            if resi != last:
                seen.append((resi, line[17:20].strip())); last = resi
    return seen

# build MD -> crystal map (order alignment)
crystal = [(i, n) for i, n in resseq("structures/3GBG.pdb") if n in AA]
ref_md = [(i, n) for i, n in resseq("md/epa_50ns/system.pdb") if n in AA]
assert len(crystal) == len(ref_md), "residue count mismatch: %d vs %d" % (len(crystal), len(ref_md))
mismatch = sum(1 for (mi, mn), (ci, cn) in zip(ref_md, crystal) if mn != cn)
assert mismatch == 0, "identity mismatches in alignment: %d" % mismatch
MAP = {mi: ci for (mi, mn), (ci, cn) in zip(ref_md, crystal)}
print("Map built: %d residues, 0 identity mismatches." % len(MAP))

def renumber(inp, outp):
    out = []
    for line in open(inp):
        if line[:6] in ("ATOM  ", "HETATM") and line[17:20].strip() in AA:
            mi = int(line[22:26]); ci = MAP.get(mi)
            if ci is not None:
                line = line[:22] + ("%4d" % ci) + line[26:]
        out.append(line)
    with open(outp, "w") as f:
        f.writelines(out)

n = 0
for sysfile in sorted(glob.glob("md/*/system.pdb")):
    out = os.path.join(os.path.dirname(sysfile), "system_pub.pdb")
    renumber(sysfile, out)
    n += 1
    print("  renumbered ->", out)
print("Done: %d topologies renumbered to published 3GBG numbering." % n)
