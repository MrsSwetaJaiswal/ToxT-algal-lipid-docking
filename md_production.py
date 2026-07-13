"""Production MD with checkpoint/restart (safe for multi-day runs on a laptop).

First run: builds the solvated complex, minimizes, equilibrates, saves an
equilibrated state, then runs production while writing a checkpoint every 250 ps.
If interrupted (sleep / reboot / crash), just run the SAME command again -- it
resumes from the last checkpoint automatically.

Usage (conda md env):
  C:\\Users\\ASUS\\miniforge3\\envs\\md\\python.exe md_production.py <ligand.sdf> <name> <total_ns>

Example:
  ...python.exe md_production.py md\\epa_pose.sdf epa_100ns 100
"""
import os, sys
from openmm import app, unit, Platform, MonteCarloBarostat, LangevinMiddleIntegrator, XmlSerializer
from openff.toolkit import Molecule
from openff.toolkit.utils.nagl_wrapper import NAGLToolkitWrapper
from openff.nagl_models import list_available_nagl_models
from openmmforcefields.generators import SystemGenerator
from pdbfixer import PDBFixer

LIG_SDF = sys.argv[1]
NAME    = sys.argv[2]
TOTAL_NS = float(sys.argv[3])
PROTEIN = "prepared_structures/3GBG_protein_only.pdb"
OUT = os.path.join("md", NAME); os.makedirs(OUT, exist_ok=True)
DT = 0.004  # ps (4 fs with HMR)
SYS_XML = os.path.join(OUT, "system.xml")
EQ_STATE = os.path.join(OUT, "equilibrated.xml")
CHK = os.path.join(OUT, "checkpoint.chk")

def build():
    print("Building system (one-time) ...")
    fixer = PDBFixer(filename=PROTEIN)
    fixer.findMissingResidues(); fixer.findMissingAtoms()
    fixer.addMissingAtoms(); fixer.addMissingHydrogens(7.4)
    lig = Molecule.from_file(LIG_SDF)
    model = [m for m in list_available_nagl_models() if "am1bcc" in str(m).lower()][-1]
    lig.assign_partial_charges(str(model), toolkit_registry=NAGLToolkitWrapper())
    sysgen = SystemGenerator(
        forcefields=["amber14-all.xml", "amber14/tip3p.xml"],
        small_molecule_forcefield="openff-2.2.0", molecules=[lig],
        forcefield_kwargs={"constraints": app.HBonds, "rigidWater": True,
                           "removeCMMotion": True, "hydrogenMass": 1.5*unit.amu},
        periodic_forcefield_kwargs={"nonbondedMethod": app.PME})
    modeller = app.Modeller(fixer.topology, fixer.positions)
    modeller.add(lig.to_topology().to_openmm(), lig.conformers[0].to_openmm())
    modeller.addSolvent(sysgen.forcefield, model="tip3p", padding=1.0*unit.nanometer,
                        ionicStrength=0.15*unit.molar, neutralize=True)
    system = sysgen.create_system(modeller.topology)
    system.addForce(MonteCarloBarostat(1*unit.bar, 300*unit.kelvin, 25))
    app.PDBFile.writeFile(modeller.topology, modeller.positions,
                          open(os.path.join(OUT, "system.pdb"), "w"))
    with open(SYS_XML, "w") as f: f.write(XmlSerializer.serialize(system))
    # minimize + equilibrate
    integ = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, DT*unit.picoseconds)
    sim = make_sim(modeller.topology, system, integ)
    sim.context.setPositions(modeller.positions)
    sim.minimizeEnergy()
    sim.context.setVelocitiesToTemperature(300*unit.kelvin)
    sim.step(int(100/DT))  # 100 ps equilibration
    sim.saveState(EQ_STATE)
    print("Equilibration done.")
    return modeller.topology, system

def make_sim(topology, system, integrator):
    plat = Platform.getPlatformByName("OpenCL")
    props = {"OpenCLPlatformIndex": "0", "OpenCLDeviceIndex": "0", "Precision": "mixed"}
    return app.Simulation(topology, system, integrator, plat, props)

# --- load or build ---
top = app.PDBFile(os.path.join(OUT, "system.pdb")).topology if os.path.exists(SYS_XML) else None
if top is not None:
    with open(SYS_XML) as f: system = XmlSerializer.deserialize(f.read())
    print("Loaded existing system.")
else:
    top, system = build()

integ = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, DT*unit.picoseconds)
sim = make_sim(top, system, integ)

total_steps = int(TOTAL_NS * 1000 / DT)
save_every  = int(250 / DT)   # checkpoint every 250 ps

if os.path.exists(CHK):
    sim.loadCheckpoint(CHK)
    done = sim.context.getStepCount()
    print("Resuming from checkpoint at %.1f ns (%d/%d steps)."
          % (done*DT/1000, done, total_steps))
else:
    sim.loadState(EQ_STATE)
    sim.context.setStepCount(0); done = 0
    print("Starting production from equilibrated state.")

append = os.path.exists(CHK)
sim.reporters.append(app.DCDReporter(os.path.join(OUT, "traj.dcd"), save_every, append=append))
sim.reporters.append(app.StateDataReporter(
    os.path.join(OUT, "production_log.csv"), 5000, step=True, time=True,
    potentialEnergy=True, temperature=True, density=True, speed=True, append=append))
sim.reporters.append(app.CheckpointReporter(CHK, save_every))

remaining = total_steps - done
print("Running %d steps (%.1f ns) ..." % (remaining, remaining*DT/1000))
# run in chunks so a checkpoint is always recent
chunk = save_every
while sim.context.getStepCount() < total_steps:
    sim.step(min(chunk, total_steps - sim.context.getStepCount()))
sim.saveCheckpoint(CHK)
print("PRODUCTION COMPLETE: %.1f ns. Trajectory: %s" % (TOTAL_NS, os.path.join(OUT, "traj.dcd")))
