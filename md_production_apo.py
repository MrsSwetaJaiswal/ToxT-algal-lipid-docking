"""Apo (ligand-free) ToxT production MD with checkpoint/restart.

Negative/baseline control: the empty protein, same protocol as the ligand runs
(Amber ff14SB, TIP3P, 0.15 M NaCl, 50 ns NPT), so RMSF/pocket behaviour can be
compared against the ligand-bound simulations.

Usage (conda md env):
  ...python.exe md_production_apo.py <name> <total_ns>
  e.g.  ...python.exe md_production_apo.py apo_toxt_50ns 50
"""
import os, sys
from openmm import app, unit, Platform, MonteCarloBarostat, LangevinMiddleIntegrator, XmlSerializer
from openmmforcefields.generators import SystemGenerator
from pdbfixer import PDBFixer

NAME = sys.argv[1] if len(sys.argv) > 1 else "apo_toxt_50ns"
TOTAL_NS = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
PROTEIN = "prepared_structures/3GBG_protein_only.pdb"
OUT = os.path.join("md", NAME); os.makedirs(OUT, exist_ok=True)
DT = 0.004
SYS_XML = os.path.join(OUT, "system.xml")
EQ_STATE = os.path.join(OUT, "equilibrated.xml")
CHK = os.path.join(OUT, "checkpoint.chk")

def make_sim(topology, system, integrator):
    plat = Platform.getPlatformByName("OpenCL")
    props = {"OpenCLPlatformIndex": "0", "OpenCLDeviceIndex": "0", "Precision": "mixed"}
    return app.Simulation(topology, system, integrator, plat, props)

def build():
    print("Building apo system (one-time) ...")
    fixer = PDBFixer(filename=PROTEIN)
    fixer.findMissingResidues(); fixer.findMissingAtoms()
    fixer.addMissingAtoms(); fixer.addMissingHydrogens(7.4)
    sysgen = SystemGenerator(
        forcefields=["amber14-all.xml", "amber14/tip3p.xml"], molecules=[],
        forcefield_kwargs={"constraints": app.HBonds, "rigidWater": True,
                           "removeCMMotion": True, "hydrogenMass": 1.5*unit.amu},
        periodic_forcefield_kwargs={"nonbondedMethod": app.PME})
    modeller = app.Modeller(fixer.topology, fixer.positions)
    modeller.addSolvent(sysgen.forcefield, model="tip3p", padding=1.0*unit.nanometer,
                        ionicStrength=0.15*unit.molar, neutralize=True)
    system = sysgen.create_system(modeller.topology)
    system.addForce(MonteCarloBarostat(1*unit.bar, 300*unit.kelvin, 25))
    app.PDBFile.writeFile(modeller.topology, modeller.positions,
                          open(os.path.join(OUT, "system.pdb"), "w"))
    with open(SYS_XML, "w") as f: f.write(XmlSerializer.serialize(system))
    integ = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, DT*unit.picoseconds)
    sim = make_sim(modeller.topology, system, integ)
    sim.context.setPositions(modeller.positions)
    sim.minimizeEnergy()
    sim.context.setVelocitiesToTemperature(300*unit.kelvin)
    sim.step(int(100/DT))
    sim.saveState(EQ_STATE)
    print("Equilibration done.")
    return modeller.topology, system

if os.path.exists(SYS_XML):
    top = app.PDBFile(os.path.join(OUT, "system.pdb")).topology
    with open(SYS_XML) as f: system = XmlSerializer.deserialize(f.read())
    print("Loaded existing apo system.")
else:
    top, system = build()

integ = LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, DT*unit.picoseconds)
sim = make_sim(top, system, integ)
total_steps = int(TOTAL_NS * 1000 / DT)
save_every = int(250 / DT)

if os.path.exists(CHK):
    sim.loadCheckpoint(CHK); done = sim.context.getStepCount()
    print("Resuming apo from %.1f ns (%d/%d)." % (done*DT/1000, done, total_steps))
else:
    sim.loadState(EQ_STATE); sim.context.setStepCount(0); done = 0
    print("Starting apo production.")

append = os.path.exists(CHK)
sim.reporters.append(app.DCDReporter(os.path.join(OUT, "traj.dcd"), save_every, append=append))
sim.reporters.append(app.StateDataReporter(
    os.path.join(OUT, "production_log.csv"), 5000, step=True, time=True,
    potentialEnergy=True, temperature=True, density=True, speed=True, append=append))
sim.reporters.append(app.CheckpointReporter(CHK, save_every))
while sim.context.getStepCount() < total_steps:
    sim.step(min(save_every, total_steps - sim.context.getStepCount()))
sim.saveCheckpoint(CHK)
print("APO PRODUCTION COMPLETE: %.1f ns." % TOTAL_NS)
