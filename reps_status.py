"""Print a snapshot of the 28-replicate campaign. Run anytime (any python):
   python reps_status.py
Reads each run's production_log.csv (no dependencies, no GPU needed)."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
DT = 0.004
TOTAL = int(50 * 1000 / DT)

BASE = ["epa_50ns","methyl_epa_50ns","epa_deprot_50ns","gla_50ns","gla_ester_50ns",
        "gla_deprot_50ns","palmitic_50ns","methyl_palmitate_50ns","palmitic_deprot_50ns",
        "pam_50ns","glucose_decoy_50ns","pentadecanal_50ns","tridecanoic_50ns","apo_toxt_50ns"]

def ns(name):
    csv = os.path.join(ROOT, "md", name, "production_log.csv")
    try:
        with open(csv) as f:
            last = None
            for last in f:
                pass
        if last and not last.startswith('#') and ',' in last:
            return int(float(last.split(',')[0].strip('"'))) * DT / 1000.0
    except Exception:
        pass
    return None

print("%-24s %8s %8s %8s" % ("system", "r1", "r2", "r3"))
print("-" * 52)
done = 0; total_reps = 0
for b in BASE:
    cells = []
    for suf in ("", "_r2", "_r3"):
        v = ns(b + suf)
        total_reps += 1
        if v is None:
            cells.append("  --  ")
        elif v >= 49.9:
            cells.append(" 50 OK"); done += 1
        else:
            cells.append("%5.1f " % v)
    print("%-24s %8s %8s %8s" % (b, *cells))
print("-" * 52)
prog = os.path.join(ROOT, "md", "reps_progress.log")
if os.path.exists(prog):
    print("live:", open(prog).read().strip())
print("completed %d / %d trajectories (%d/28 new replicates)" % (done, total_reps, max(0, done - 14)))
