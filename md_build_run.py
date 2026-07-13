"""Build a solvated ToxT-ligand complex and run a short MD test on the GPU.

Pipeline (all open-source, Windows-compatible):
  protein  : PDBFixer  (add missing atoms + H at pH 7.4)
  ligand   : OpenFF Sage (openff-2.2.0) + NAGL AM1BCC-quality charges
  system   : Amber14 (protein) + OpenFF (ligand) + TIP3P water + 0.15 M NaCl
  engine   : OpenMM on the RTX 3050 (OpenCL), Langevin 300 K, NPT 1 atm

Run with the conda md env python:
  C:\\Users\\ASUS\\miniforge3\\envs\\md\\python.exe md_build_run.py <ligand.sdf> <name> <ns>

Outputs in md/<name>/ : solvated PDB, trajectory (DCD), state log, final speed.
"""
import os, sys, time
from openmm import app, unit, Platform, MonteCarloBarostat, LangevinMiddleIntegrator
from openff.toolkit import Molecule
from openff.toolkit.utils.nagl_wrapper import NAGLToolkitWrapper
from openff.nagl_models import list_available_nagl_models
from openmmforcefields.generators import SystemGenerator
from pdbfixer import PDBFixer

LIG_SDF = sys.argv[1] if len(sys.argv) > 1 else "md/epa_pose.sdf"
NAME    = sys.argv[2] if len(sys.argv) > 2 else "epa_test"
NS      = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
PROTEIN = "prepared_structures/3GBG_protein_only.pdb"
OUTDIR  = os.path.join("md", NAME)
os.makedirs(OUTDIR, exist_ok=True)

print("[1/6] Preparing protein with PDBFixer (pH 7.4) ...")
fixer = PDBFixer(filename=PROTEIN)
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(7.4)

print("[2/6] Loading ligand + assigning NAGL (AM1BCC) charges ...")
lig = Molecule.from_file(LIG_SDF)
model = [m for m in list_available_nagl_models() if "am1bcc" in str(m).lower()][-1]
lig.assign_partial_charges(str(model), toolkit_registry=NAGLToolkitWrapper())
print("      net ligand charge:", round(sum(c.m for c in lig.partial_charges), 3))

print("[3/6] Building force field (Amber14 + OpenFF Sage) ...")
sysgen = SystemGenerator(
    forcefields=["amber14-all.xml", "amber14/tip3p.xml"],
    small_molecule_forcefield="openff-2.2.0",
    molecules=[lig],
    forcefield_kwargs={"constraints": app.HBonds, "rigidWater": True,
                       "removeCMMotion": True, "hydrogenMass": 1.5*unit.amu},
    periodic_forcefield_kwargs={"nonbondedMethod": app.PME})

print("[4/6] Combining protein + ligand, solvating (TIP3P, 0.15 M NaCl) ...")
modeller = app.Modeller(fixer.topology, fixer.positions)
modeller.add(lig.to_topology().to_openmm(), lig.conformers[0].to_openmm())
modeller.addSolvent(sysgen.forcefield, model="tip3p",
                    padding=1.0*unit.nanometer,
                    ionicStrength=0.15*unit.molar, neutralize=True)
n_atoms = modeller.topology.getNumAtoms()
print("      solvated system: %d atoms" % n_atoms)
app.PDBFile.writeFile(modeller.topology, modeller.positions,
                      open(os.path.join(OUTDIR, "system.pdb"), "w"))

print("[5/6] Creating system + minimizing ...")
system = sysgen.create_system(modeller.topology)
system.addForce(MonteCarloBarostat(1*unit.bar, 300*unit.kelvin, 25))
integrator = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond,
                                      0.004*unit.picoseconds)  # 4 fs (HMR)
platform = Platform.getPlatformByName("OpenCL")
props = {"OpenCLPlatformIndex": "0", "OpenCLDeviceIndex": "0", "Precision": "mixed"}
sim = app.Simulation(modeller.topology, system, integrator, platform, props)
sim.context.setPositions(modeller.positions)
sim.minimizeEnergy()
print("      device:", platform.getPropertyValue(sim.context, "DeviceName"))

print("[6/6] Equilibrating (100 ps) then running %.1f ns ..." % NS)
sim.context.setVelocitiesToTemperature(300*unit.kelvin)
sim.step(25000)  # 100 ps equilibration at 4 fs

steps = int(NS * 1000 / 0.004)
sim.reporters.append(app.DCDReporter(os.path.join(OUTDIR, "traj.dcd"), 25000))  # every 100 ps
sim.reporters.append(app.StateDataReporter(
    os.path.join(OUTDIR, "md_log.csv"), 5000, step=True, time=True,
    potentialEnergy=True, temperature=True, density=True, speed=True))
t0 = time.time()
sim.step(steps)
dt = time.time() - t0
nsday = NS / (dt/86400.0)
sim.saveState(os.path.join(OUTDIR, "final_state.xml"))
print("\nDONE: %.1f ns in %.1f min  =>  %.1f ns/day on this system (%d atoms)"
      % (NS, dt/60, nsday, n_atoms))
print("Outputs in", OUTDIR)
