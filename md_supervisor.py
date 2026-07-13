"""Autonomous thermal supervisor for the MD queue.

Runs the remaining MD jobs sequentially and protects the laptop from heat:
  - polls the GPU temperature every POLL_S seconds
  - PAUSES the run (checkpoint-safe) if the GPU crosses HIGH_C,
    OR after RUN_CHUNK_MIN minutes of continuous running (duty-cycle cooldown)
  - waits until the GPU cools to COOL_C (or COOLDOWN_MAX_MIN elapses)
  - RESUMES automatically from the checkpoint
  - repeats until each run reaches 50 ns, then moves to the next
  - pops a Windows desktop notification and logs every pause/resume event

Because md_production.py checkpoints every 250 ps, every pause loses < 250 ps.

Run (background):
  C:\\Users\\ASUS\\miniforge3\\envs\\md\\python.exe md_supervisor.py
"""
import os, sys, time, subprocess, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\ASUS\miniforge3\envs\md\python.exe"
LOG = os.path.join(ROOT, "md", "thermal_supervisor.log")

# --- thermal policy (adjustable) ---
HIGH_C = 78            # emergency pause if GPU >= this
COOL_C = 56            # resume once GPU <= this
RUN_CHUNK_MIN = 90     # also pause for a cooldown after this much continuous run
COOLDOWN_MAX_MIN = 15  # give up waiting for COOL_C after this long (resume anyway)
POLL_S = 15
NS = 50

# (ligand_sdf or None, run_name, production_script)
RUNS = [
    # --- headgroup matrix: GLA (CCM strongest) ---
    ("md/gla_pose.sdf",              "gla_50ns",             "md_production.py"),  # acid (in progress)
    ("md/gla_ester_pose.sdf",        "gla_ester_50ns",       "md_production.py"),  # methyl ester
    ("md/gla_deprot_pose.sdf",       "gla_deprot_50ns",      "md_production.py"),  # deprotonated
    # --- headgroup matrix: palmitic acid (saturated control) ---
    ("md/palmitic_pose.sdf",         "palmitic_50ns",        "md_production.py"),  # acid
    ("md/methyl_palmitate_pose.sdf", "methyl_palmitate_50ns","md_production.py"),  # methyl ester
    ("md/palmitic_deprot_pose.sdf",  "palmitic_deprot_50ns", "md_production.py"),  # deprotonated
    # --- controls ---
    ("md/pam_pose.sdf",              "pam_50ns",             "md_production.py"),  # positive (native)
    ("md/glucose_pose.sdf",          "glucose_decoy_50ns",   "md_production.py"),  # negative (decoy)
    (None,                           "apo_toxt_50ns",        "md_production_apo.py"),  # negative (apo)
    # --- weak-binder SAR contrast ---
    ("md/pentadecanal_pose.sdf",     "pentadecanal_50ns",    "md_production.py"),  # CV weakest
    ("md/tridecanoic_pose.sdf",      "tridecanoic_50ns",     "md_production.py"),  # CCM weakest
]

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

def launch(sdf, name, script):
    args = [PY, "-u", script]
    if sdf is not None:
        args.append(sdf)
    args += [name, str(NS)]
    return subprocess.Popen(args, cwd=ROOT)

def run_one(sdf, name, script):
    done = False
    fails = 0
    while not done:
        log("START/RESUME %s  (GPU %d C)" % (name, gpu_temp()))
        p = launch(sdf, name, script)
        t0 = time.time()
        paused = False
        while True:
            time.sleep(POLL_S)
            rc = p.poll()
            if rc is not None:
                if rc == 0:
                    log("COMPLETE %s" % name); done = True
                else:
                    fails += 1
                    log("EXIT %s rc=%s (failure %d/3)" % (name, rc, fails))
                    if fails >= 3:
                        log("SKIP %s after %d failures -> moving on" % (name, fails))
                        notify("MD run failed", "%s skipped after 3 failures" % name)
                        done = True
                    else:
                        time.sleep(30)  # brief backoff before retry
                break
            temp = gpu_temp()
            hot = temp >= HIGH_C
            long_run = (time.time() - t0) >= RUN_CHUNK_MIN * 60
            if hot or long_run:
                reason = ("GPU %d C >= %d" % (temp, HIGH_C)) if hot else \
                         ("ran %d min (duty-cycle cooldown)" % RUN_CHUNK_MIN)
                log("PAUSE %s : %s" % (name, reason))
                notify("MD paused (cooling)", "%s paused: %s" % (name, reason))
                p.terminate()
                try: p.wait(timeout=30)
                except Exception: p.kill()
                paused = True
                # cool-down wait
                cd0 = time.time()
                while True:
                    time.sleep(POLL_S)
                    tt = gpu_temp()
                    if tt <= COOL_C or (time.time() - cd0) >= COOLDOWN_MAX_MIN * 60:
                        log("COOLED to %d C after %d s -> resuming"
                            % (tt, int(time.time() - cd0)))
                        notify("MD resuming", "%s cooled to %d C, resuming" % (name, tt))
                        break
                break  # relaunch (resume from checkpoint)
        if paused:
            continue
    log("=== DONE %s ===" % name)

if __name__ == "__main__":
    log("Thermal supervisor started. Policy: pause@%dC or every %dmin, resume@%dC."
        % (HIGH_C, RUN_CHUNK_MIN, COOL_C))
    for sdf, name, script in RUNS:
        run_one(sdf, name, script)
    log("ALL RUNS COMPLETE.")
    notify("MD complete", "All queued MD runs finished.")
