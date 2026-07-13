"""PBC-correct ligand-contact persistence.

For each frame, the whole ligand is shifted into the periodic image nearest the
protein (by minimizing ligand-COM to protein-COM under the minimum-image
convention), then per-residue minimum ligand distances are computed. This fixes
the undercount that raw distances give when the ligand crosses the box edge.

Run (.venv):  .venv\\Scripts\\python.exe md_contacts_pbc.py <name> [equil_ns]
"""
import sys, numpy as np, mdtraj as md

NAME = sys.argv[1] if len(sys.argv) > 1 else "methyl_epa_50ns"
EQUIL_NS = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
CUTOFF = 0.40  # nm
D = "md/" + NAME
t = md.load(D + "/traj.dcd", top=D + "/system.pdb")
ps_per_frame = 250.0
start = min(int(EQUIL_NS * 1000 / ps_per_frame), max(0, t.n_frames - 2))

prot = t.topology.select("protein")
lig = t.topology.select("resname UNK")
prot_com_ref = None

prot_res = {}
for ai in prot:
    prot_res.setdefault(t.topology.atom(ai).residue.index, []).append(ai)
res_list = sorted(prot_res)
counts = np.zeros(len(res_list))
nframes = 0
for fi in range(start, t.n_frames):
    xyz = t.xyz[fi].copy()
    box = t.unitcell_lengths[fi]
    pcom = xyz[prot].mean(0)
    lcom = xyz[lig].mean(0)
    shift = box * np.round((lcom - pcom) / box)   # image offset
    lig_xyz = xyz[lig] - shift                     # bring ligand next to protein
    nframes += 1
    for ri, residx in enumerate(res_list):
        a = xyz[prot_res[residx]]
        d = a[:, None, :] - lig_xyz[None, :, :]
        if np.sqrt((d**2).sum(-1)).min() < CUTOFF:
            counts[ri] += 1
frac = counts / max(1, nframes)
rows = []
for ri, residx in enumerate(res_list):
    if frac[ri] > 0.05:
        r = t.topology.residue(residx)
        if r.name == "UNK":
            continue
        rows.append((r.name, r.resSeq, frac[ri]))
rows.sort(key=lambda x: -x[2])
print("%s: contact persistence over %d production frames (min-image, <4 A)" % (NAME, nframes))
for name, num, f in rows[:20]:
    print("  %-4s%-5d %5.0f%%" % (name, num, f*100))
