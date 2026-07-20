"""Single-trajectory MM-GBSA (OBC) from an existing MD trajectory, Windows-native.

AmberTools MMPBSA.py is unavailable on Windows, so this rebuilds vacuum
complex/receptor/ligand systems with the original force fields (Amber14 + OpenFF
via SystemGenerator) and attaches an OBC GBSA model whose per-atom parameters
(charge from the NonbondedForce, mbondi2 radius + OBC screening by element) are
assigned directly -- force-field agnostic, so the OpenFF ligand needs no GB DB.

  dG_bind = <E(complex) - E(receptor) - E(ligand)>   (single trajectory; -TdS omitted)

Run (md env):  ...python.exe md_mmgbsa.py <lig_pose.sdf> <run_name> [n_frames]
"""
import sys, numpy as np, mdtraj as md
import openmm as mm
from openmm import app, unit, Platform
from openff.toolkit import Molecule
from openff.toolkit.utils.nagl_wrapper import NAGLToolkitWrapper
from openff.nagl_models import list_available_nagl_models
from openmmforcefields.generators import SystemGenerator
from pdbfixer import PDBFixer

LIG_SDF = sys.argv[1]
NAME    = sys.argv[2]
NFR     = int(sys.argv[3]) if len(sys.argv) > 3 else 25
PROTEIN = "prepared_structures/3GBG_protein_only.pdb"
D = "md/" + NAME
KJ2KCAL = 1.0 / 4.184

# mbondi2 radii (nm) and OBC screening by element
RAD = {"H":0.12,"C":0.17,"N":0.155,"O":0.15,"S":0.18,"P":0.185,"F":0.15,
       "Cl":0.17,"Br":0.185,"I":0.198,"Na":0.133,"Cl-":0.17}
SCR = {"H":0.85,"C":0.72,"N":0.79,"O":0.85,"S":0.96,"P":0.86,"F":0.88,
       "Cl":0.80,"Br":0.80,"I":0.80}

def add_obc(system, topology):
    nbf = [f for f in system.getForces() if isinstance(f, mm.NonbondedForce)][0]
    gb = mm.GBSAOBCForce()
    gb.setNonbondedMethod(mm.GBSAOBCForce.NoCutoff)
    gb.setSoluteDielectric(1.0); gb.setSolventDielectric(78.5)
    for i, atom in enumerate(topology.atoms()):
        q = nbf.getParticleParameters(i)[0]
        el = atom.element.symbol if atom.element else "C"
        gb.addParticle(q, RAD.get(el, 0.15), SCR.get(el, 0.8))
    system.addForce(gb)
    return system

# --- build ligand molecule with NAGL charges (once) ---
lig = Molecule.from_file(LIG_SDF)
model = [m for m in list_available_nagl_models() if "am1bcc" in str(m).lower()][-1]
lig.assign_partial_charges(str(model), toolkit_registry=NAGLToolkitWrapper())
sysgen = SystemGenerator(
    forcefields=["amber14-all.xml"], small_molecule_forcefield="openff-2.2.0",
    molecules=[lig], forcefield_kwargs={"constraints": None, "rigidWater": False,
    "removeCMMotion": False}, periodic_forcefield_kwargs=None,
    nonperiodic_forcefield_kwargs={"nonbondedMethod": app.NoCutoff})

# build complex/receptor/ligand topologies by stripping the trajectory's own
# topology (guarantees atom-count / order match with the DCD)
full = app.PDBFile(D + "/system_pub.pdb")
def stripped(keep_ligand, only_ligand=False):
    m = app.Modeller(full.topology, full.positions)
    if only_ligand:
        drop = [r for r in m.topology.residues() if r.name != "UNK"]
    else:
        names = ("HOH", "NA", "CL", "WAT") + (() if keep_ligand else ("UNK",))
        drop = [r for r in m.topology.residues() if r.name in names]
    m.delete(drop)
    m.topology.setPeriodicBoxVectors(None)  # force non-periodic
    return m

def sysof(m):
    s = sysgen.create_system(m.topology)
    return add_obc(s, m.topology)

sys_c = sysof(stripped(keep_ligand=True))
sys_r = sysof(stripped(keep_ligand=False))
sys_l = sysof(stripped(keep_ligand=True, only_ligand=True))

def ctx(system):
    return mm.Context(system, mm.VerletIntegrator(0.001*unit.picoseconds),
                      Platform.getPlatformByName("CPU"))
cc, cr, cl = ctx(sys_c), ctx(sys_r), ctx(sys_l)

def E(c, pos):
    c.setPositions(pos)
    return c.getState(getEnergy=True).getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)

# --- trajectory: protein+ligand atoms (order matches rebuilt systems) ---
t = md.load(D + "/traj.dcd", top=D + "/system_pub.pdb")
prot_idx = t.topology.select("protein and not resname UNK"); lig_idx = t.topology.select("resname UNK")
comp_idx = np.concatenate([prot_idx, lig_idx])
n_prot = len(prot_idx)
start = int(5000/250.0)
frames = np.linspace(start, t.n_frames-1, min(NFR, t.n_frames-start)).astype(int)

print("PARTICLES  sys_c=%d sys_r=%d sys_l=%d | comp_idx=%d prot_idx=%d lig_idx=%d"
      % (sys_c.getNumParticles(), sys_r.getNumParticles(), sys_l.getNumParticles(),
         len(comp_idx), len(prot_idx), len(lig_idx)))
dG = []
for fi in frames:
    xyz = t.xyz[fi]
    ec = E(cc, xyz[comp_idx]); er = E(cr, xyz[prot_idx]); el = E(cl, xyz[lig_idx])
    dG.append((ec - er - el) * KJ2KCAL)
dG = np.array(dG)
print("%s : MM-GBSA(OBC) dG_bind = %.1f +/- %.1f kcal/mol  (n=%d)"
      % (NAME, dG.mean(), dG.std(), len(dG)))
