"""Autonomous thermal supervisor for the TRIPLICATE replicate campaign.

Runs 2 additional INDEPENDENT replicates (r2, r3) for each of the 14 base
systems (13 ligands + apo) = 28 runs of 50 ns. Replicate 1 is the original
production run already on disk; r2/r3 use distinct velocity + integrator random
seeds (passed to md_production.py / md_production_apo.py) so each trajectory is
a genuinely independent sample, not a re-run of the same dynamics.

Same thermal policy as md_supervisor.py:
  - poll GPU temp every POLL_S s
  - pause (checkpoint-safe) at HIGH_C or after RUN_CHUNK_MIN of continuous run
  - resume at COOL_C (or after COOLDOWN_MAX_MIN)
  - each pause loses < 250 ps (checkpoint interval)

Idempotent: a run whose checkpoint already reached 50 ns exits immediately as
COMPLETE, so re-launching the supervisor safely skips finished replicates.

A live progress line is appended to md/reps_progress.log after every poll so
`python reps_status.py` (or tail) shows the exact ns/50 of the active run.

Run (background, survives session teardown):
  C:\\Users\\ASUS\\miniforge3\\envs\\md\\python.exe md_supervisor_reps.py
"""
import os, sys, time, subprocess, datetime, glob, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\ASUS\miniforge3\envs\md\python.exe"
LOG = os.path.join(ROOT, "md", "thermal_supervisor_reps.log")
PROG = os.path.join(ROOT, "md", "reps_progress.log")

# --- thermal policy (matches original campaign) ---
HIGH_C = 78
COOL_C = 56
RUN_CHUNK_MIN = 90
COOLDOWN_MAX_MIN = 15
POLL_S = 15
NS = 50
DT = 0.004  # ps/step (must match md_production.py for progress math)
TOTAL_STEPS = int(NS * 1000 / DT)

# base systems: (ligand_sdf or None, base_name, production_script)
# HEADLINE first (abstract claims): EPA, gamma-linolenic, palmitic, apo control.
# These get full triplicate (r2+r3) before any of the REST, so publishable error
# bars on the headline systems land in ~4 days instead of ~2 weeks.
HEADLINE = [
    ("md/epa_pose.sdf",              "epa_50ns",              "md_production.py"),
    ("md/gla_pose.sdf",              "gla_50ns",              "md_production.py"),
    ("md/palmitic_pose.sdf",         "palmitic_50ns",         "md_production.py"),
    (None,                           "apo_toxt_50ns",         "md_production_apo.py"),
]
REST = [
    ("md/methyl_epa_pose.sdf",       "methyl_epa_50ns",       "md_production.py"),
    ("md/epa_deprot_pose.sdf",       "epa_deprot_50ns",       "md_production.py"),
    ("md/gla_ester_pose.sdf",        "gla_ester_50ns",        "md_production.py"),
    ("md/gla_deprot_pose.sdf",       "gla_deprot_50ns",       "md_production.py"),
    ("md/methyl_palmitate_pose.sdf", "methyl_palmitate_50ns", "md_production.py"),
    ("md/palmitic_deprot_pose.sdf",  "palmitic_deprot_50ns",  "md_production.py"),
    ("md/pam_pose.sdf",              "pam_50ns",              "md_production.py"),
    ("md/glucose_pose.sdf",          "glucose_decoy_50ns",    "md_production.py"),
    ("md/pentadecanal_pose.sdf",     "pentadecanal_50ns",     "md_production.py"),
    ("md/tridecanoic_pose.sdf",      "tridecanoic_50ns",      "md_production.py"),
]
BASE = HEADLINE + REST  # kept for reps_status / external references

# Build the 28-run queue with a stable per-system seed (same base_name -> same
# seed regardless of ordering, so reordering never re-seeds a started run).
# HEADLINE r2, HEADLINE r3, REST r2, REST r3.
_SEED = {}
for i, (_, base, _s) in enumerate(BASE, start=1):
    _SEED[base] = i  # 1..14, stable identity

RUNS = []
for group in (HEADLINE, REST):
    for rep, base_seed in ((2, 1000), (3, 2000)):
        for sdf, base, script in group:
            RUNS.append((sdf, "%s_r%d" % (base, rep), script, base_seed + _SEED[base]))

def log(msg):
    line = "[%s] %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def gpu_temp():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            timeout=15).decode().strip().splitlines()[0]
        return int(out)
    except Exception:
        return -1

def steps_done(name):
    """Read current step count from the run's checkpoint-backed log (best effort)."""
    csv = os.path.join(ROOT, "md", name, "production_log.csv")
    try:
        with open(csv) as f:
            last = None
            for last in f:
                pass
        if last and not last.startswith('#') and ',' in last:
            return int(float(last.split(',')[0].strip('"')))
    except Exception:
        pass
    return 0

def progress(active, phase):
    ns_done = steps_done(active) * DT / 1000.0
    done_runs = sum(1 for r in RUNS if _complete(r[1]))
    line = ("[%s] %s | active=%s %.1f/%d ns (%.0f%%) | queue %d/28 done | GPU %dC"
            % (datetime.datetime.now().strftime("%H:%M:%S"), phase, active,
               ns_done, NS, 100.0*ns_done/NS, done_runs, gpu_temp()))
    with open(PROG, "w") as f:  # single-line live status, overwritten each poll
        f.write(line + "\n")

def _complete(name):
    """A replicate is complete when its log's last step >= TOTAL_STEPS."""
    return steps_done(name) >= TOTAL_STEPS - 1

def notify(title, msg):
    ps = ("[void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');"
          "$n=New-Object System.Windows.Forms.NotifyIcon;"
          "$n.Icon=[System.Drawing.SystemIcons]::Information;$n.Visible=$true;"
          "$n.ShowBalloonTip(8000,'%s','%s',"
          "[System.Windows.Forms.ToolTipIcon]::Warning);Start-Sleep 9;$n.Dispose()" % (title, msg))
    try:
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps])
    except Exception:
        pass

MIN_FREE_GB = 5.0   # a 50 ns run needs ~0.2 GB; keep real headroom for Windows

def free_gb():
    try:
        return shutil.disk_usage(ROOT).free / (1024.0 ** 3)
    except Exception:
        return 999.0

def wait_for_disk(name):
    """Block (do NOT consume the queue) while the disk is too full to run safely.
    A full disk previously killed builds/checkpoints and burned 8 runs' retries."""
    while free_gb() < MIN_FREE_GB:
        log("LOW DISK: %.1f GB free (< %.1f) -> holding %s, recheck in 10 min"
            % (free_gb(), MIN_FREE_GB, name))
        notify("MD paused (low disk)", "%.1f GB free - free space to resume" % free_gb())
        time.sleep(600)

def launch(sdf, name, script, seed):
    args = [PY, "-u", script]
    if sdf is not None:
        args += [sdf, name, str(NS), str(seed)]
    else:  # apo: <name> <ns> <seed>
        args += [name, str(NS), str(seed)]
    d = os.path.join(ROOT, "md", name)
    os.makedirs(d, exist_ok=True)
    # Capture child stdout+stderr; previously discarded, which made failures undiagnosable.
    errlog = open(os.path.join(d, "stderr.log"), "a", buffering=1)
    errlog.write("\n=== launch %s seed=%d at %s ===\n"
                 % (name, seed, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    p = subprocess.Popen(args, cwd=ROOT, stdout=errlog, stderr=subprocess.STDOUT)
    p._errlog = errlog
    return p

def run_one(sdf, name, script, seed):
    if _complete(name):
        log("SKIP %s (already at 50 ns)" % name)
        return
    done = False
    failed = False
    fails = 0
    while not done:
        wait_for_disk(name)
        log("START/RESUME %s (seed %d)  (GPU %d C, %.1f GB free)"
            % (name, seed, gpu_temp(), free_gb()))
        p = launch(sdf, name, script, seed)
        t0 = time.time()
        paused = False
        while True:
            time.sleep(POLL_S)
            progress(name, "running")
            rc = p.poll()
            if rc is not None:
                if rc == 0:
                    log("COMPLETE %s" % name); done = True
                else:
                    fails += 1
                    log("EXIT %s rc=%s (failure %d/3)" % (name, rc, fails))
                    if fails >= 3:
                        log("!! FAILED %s after 3 attempts -> leaving INCOMPLETE; "
                            "diagnose md/%s/stderr.log. It will be retried automatically "
                            "on the next supervisor start." % (name, name))
                        notify("MD replicate FAILED", "%s incomplete - see stderr.log" % name)
                        failed = True
                        done = True
                    else:
                        time.sleep(30)
                break
            temp = gpu_temp()
            hot = temp >= HIGH_C
            long_run = (time.time() - t0) >= RUN_CHUNK_MIN * 60
            if hot or long_run:
                reason = ("GPU %d C >= %d" % (temp, HIGH_C)) if hot else \
                         ("ran %d min (duty-cycle cooldown)" % RUN_CHUNK_MIN)
                log("PAUSE %s : %s" % (name, reason))
                progress(name, "cooling")
                notify("MD paused (cooling)", "%s paused: %s" % (name, reason))
                p.terminate()
                try: p.wait(timeout=30)
                except Exception: p.kill()
                paused = True
                cd0 = time.time()
                while True:
                    time.sleep(POLL_S)
                    tt = gpu_temp()
                    if tt <= COOL_C or (time.time() - cd0) >= COOLDOWN_MAX_MIN * 60:
                        log("COOLED to %d C after %d s -> resuming"
                            % (tt, int(time.time() - cd0)))
                        break
                break  # relaunch -> resume from checkpoint
        if paused:
            continue
    # Never report a failed run as DONE - that masked 8 dead runs during the
    # 2026-07-16 disk-full incident.
    log("=== INCOMPLETE %s (needs rerun) ===" % name if failed
        else "=== DONE %s ===" % name)

if __name__ == "__main__":
    log("REPLICATE supervisor started: %d runs (r2+r3 x 14 systems). "
        "Policy: pause@%dC or every %dmin, resume@%dC." % (len(RUNS), HIGH_C, RUN_CHUNK_MIN, COOL_C))
    for sdf, name, script, seed in RUNS:
        run_one(sdf, name, script, seed)
    log("ALL 28 REPLICATES COMPLETE.")
    notify("MD replicates complete", "All 28 replicate runs finished.")
