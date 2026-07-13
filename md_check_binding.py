"""PBC-correct check of whether the ligand stays in the pocket.

Computes the minimum-image distance between the ligand center of mass and the
pocket center (CA of the known ToxT fatty-acid-pocket residues) each frame.
This avoids periodic-boundary wrapping artifacts that inflate raw ligand RMSD.

Run (.venv):  .venv\\Scripts\\python.exe md_check_binding.py <name>
"""
import sys, numpy as np, mdtraj as md

NAME = sys.argv[1] if len(sys.argv) > 1 else "methyl_epa_50ns"
D = "md/" + NAME
t = md.load(D + "/traj.dcd", top=D + "/system.pdb")
ps_per_frame = 250.0
time_ns = np.arange(t.n_frames) * ps_per_frame / 1000.0

pocket_res = [9, 10, 11, 17, 19, 22, 28, 30, 68, 78, 213, 246, 248, 253]
sel = " or ".join("(residue %d and name CA)" % r for r in pocket_res)
pocket = t.topology.select(sel)
lig = t.topology.select("resname UNK")

# masses for ligand COM (approx by element)
masses = np.array([a.element.mass for a in t.topology.atoms])
lig_m = masses[lig]

box = t.unitcell_lengths  # (nframes, 3) nm
dists = np.zeros(t.n_frames)
for i in range(t.n_frames):
    xyz = t.xyz[i]
    pc = xyz[pocket].mean(axis=0)                       # pocket center
    lc = (xyz[lig] * lig_m[:, None]).sum(0) / lig_m.sum()  # ligand COM
    d = lc - pc
    b = box[i]
    d -= b * np.round(d / b)                            # minimum image
    dists[i] = np.linalg.norm(d) * 10.0                 # A

bound = dists < 10.0   # within 10 A of pocket center = bound
print("%s: %d frames (%.1f ns)" % (NAME, t.n_frames, time_ns[-1]))
print("Ligand COM-to-pocket distance: mean %.1f A, min %.1f, max %.1f"
      % (dists.mean(), dists.min(), dists.max()))
print("Fraction of trajectory bound (<10 A): %.0f%%" % (100 * bound.mean()))
# first frame where it leaves and stays out
print("Distance every 5 ns:")
for i in range(0, t.n_frames, max(1, t.n_frames // 10)):
    print("  %5.1f ns : %5.1f A  %s" % (time_ns[i], dists[i], "bound" if dists[i] < 10 else "OUT"))
