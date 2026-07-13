"""Phase A benchmark: how fast can THIS machine run MD?

Builds a ~30k-atom TIP3P water box (similar scale to a small solvated protein)
and measures ns/day on each available OpenCL device, so we can pick the RTX 3050
and get a realistic time estimate before committing to production runs.
"""
import time
from openmm import app, unit, Platform
import openmm as mm

# build a periodic water box
modeller = app.Modeller(app.Topology(), [])
ff = app.ForceField("amber14/tip3pfb.xml")
modeller.addSolvent(ff, boxSize=mm.Vec3(6.7, 6.7, 6.7) * unit.nanometer,
                    model="tip3p")
n_atoms = modeller.topology.getNumAtoms()
print("Benchmark system: %d atoms (TIP3P water box)\n" % n_atoms)

system = ff.createSystem(modeller.topology, nonbondedMethod=app.PME,
                         nonbondedCutoff=1.0*unit.nanometer,
                         constraints=app.HBonds)

def bench(platform_name, props, label):
    integrator = mm.LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond,
                                             0.004*unit.picoseconds)
    plat = Platform.getPlatformByName(platform_name)
    sim = app.Simulation(modeller.topology, system, integrator, plat, props)
    sim.context.setPositions(modeller.positions)
    sim.minimizeEnergy(maxIterations=200)
    sim.context.setVelocitiesToTemperature(300*unit.kelvin)
    sim.step(500)  # warmup
    nsteps = 3000
    t0 = time.time()
    sim.step(nsteps)
    dt = time.time() - t0
    dev = "?"
    try: dev = plat.getPropertyValue(sim.context, "DeviceName")
    except Exception: pass
    ns = nsteps * 0.004 / 1000.0
    nsday = ns / (dt/86400.0)
    print("%-28s device=%-28s %.1f ns/day" % (label, dev, nsday))
    return nsday

# try each OpenCL platform/device combination, plus CPU for reference
for p in range(4):
    for d in range(3):
        try:
            bench("OpenCL",
                  {"OpenCLPlatformIndex": str(p), "OpenCLDeviceIndex": str(d),
                   "Precision": "mixed"},
                  "OpenCL p%d/d%d" % (p, d))
        except Exception as e:
            if d == 0 and "Illegal" not in str(e) and "out of range" not in str(e).lower():
                pass  # platform p has no device d
            break
try:
    bench("CPU", {}, "CPU (reference)")
except Exception as e:
    print("CPU bench failed:", e)

print("\nNote: a solvated ToxT+lipid system is a similar size (~30-45k atoms).")
print("Estimate for production: time_for_100ns_days = 100 / (ns_per_day).")
