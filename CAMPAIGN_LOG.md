# Campaign Log

Running record of notable events, decisions, and fixes for the ToxT MD replicate
campaign and manuscript work — kept because the underlying tool logs
(`md/thermal_supervisor_reps.log`, `md/reps_progress.log`) only capture simulation
events, not the diagnosis/decisions behind them. Newest entries at the bottom.

See also: `MANUSCRIPT_TODO_reps.md` (pending manuscript edits, blocked on campaign
completion), `DATA_AVAILABILITY.md`, `reps_status.py` (live per-system table).

---

## 2026-07-22

**Campaign found stalled.** `methyl_palmitate_50ns_r2` was stuck at 7.4/50 ns
(15%) with no Python/OpenMM process running and no log activity for ~4 hours —
the thermal supervisor's log showed a resume at 17:03:20 with no matching PAUSE
afterward, consistent with the hosting terminal/session being torn down rather
than a code crash (no traceback in `stderr.log`).

**Committed + pushed pending replicate progress.** 12 files (production_log.csv /
stderr.log for apo_toxt r3, gla_deprot r2, methyl_epa r2, palmitic r3, plus the
progress/thermal logs) staged and committed as `52314ca`, pushed to
`origin/main`. Confirmed `ToxT_MD_data.tar.gz` (1.2 GB) and per-run binaries
(traj.dcd, system.xml, checkpoints) stayed untracked/excluded per `.gitignore`.

**Supervisor restarted, then made session-independent.** First restart (plain
background shell) worked but was still tied to this session's process tree.
Relaunched via a Windows Scheduled Task (`AutoDock_MD_Supervisor`) running
`run_supervisor_detached.bat`. First attempt died immediately
(`STATUS_CONTROL_C_EXIT`, literal `^C` in the log) — traced to the task sharing
this session's console, so a Ctrl+C/Break broadcast hit it too. Fixed by having
the batch file launch Python via `start "MD Supervisor" /min ...`, which opens
its own console and fully detaches the process from both this session's job
object and its console group. Confirmed stable afterward (`Get-Process` showed
independent PIDs accumulating CPU time; task's own wrapper exits with
`Last Result: 0` once the detached child is spawned).

**n=3 MM-GBSA recompute — headline free-acid systems.** Backfilled
`system_pub.pdb` for all replicate directories (was only present for r1 runs;
`renumber_topology.py` is idempotent and globs `md/*/system.pdb`, safe to rerun).
Wrote `md_mmgbsa_n3_headline.py` and ran it for EPA / GLA / palmitic free acid
(the only systems with a completed r1+r2+r3 triplicate so far). Results
(`results_mmgbsa/mmgbsa_n3_headline.csv`):

| ligand | r1 | r2 | r3 | n=3 mean ± SD |
|---|---|---|---|---|
| EPA free acid | −45.1 | −42.1 | −40.0 | **−42.4 ± 2.6** |
| GLA free acid | −34.2 | −39.1 | −42.6 | **−38.6 ± 4.2** |
| palmitic free acid | −33.2 | −33.3 | −31.5 | **−32.7 ± 1.0** |

Headline ranking survives replicate averaging (EPA > GLA > palmitic, both beat
native palmitoleate control). Carboxylate/ester forms still need their r3 (or
r2+r3) MD before they can move to n=3.

## 2026-07-22 / 07-23 (overnight)

**GLA free-acid replicate diagnostic — crash investigation.** Wrote
`gla_freeacid_replicate_check.py` (ligand COM→pocket + RMSD across r1/r2/r3) to
check whether GLA free acid's rising MM-GBSA magnitude trend (r1 −34.2 → r2
−39.1 → r3 −42.6) was a real pose-drift artifact or ordinary replicate noise.
Every invocation crashed instantly (exit 127, no traceback) — reproduced with
even a bare `numpy` matmul, no mdtraj involved. Set up a background watcher to
retry during the supervisor's thermal-pause windows (assuming GPU-job resource
contention); **15 attempts across ~8 hours, every single one crashed**,
including during full cooldowns with no GPU job running — ruling out
contention as the cause.

## 2026-07-23

**Root cause found: MKL heap-corruption bug in the `md` conda env.** Windows
Event Log showed the exact same fault signature (`python.exe` / `KERNELBASE.dll`
/ exception `0xc06d007f`) recurring on this machine on unrelated past dates —
the `md` env is Intel MKL-backed (`mkl_core.dll`, `libiomp5md.dll` present), a
known source of this crash class on Windows when a second MKL-linked process
runs. Not specific to this script, this data, or GPU contention.

**Fix: new OpenBLAS-based conda env (`analysis`).** Created via
`conda create -n analysis -c conda-forge python=3.11 "libblas=*=*openblas" numpy
mdtraj matplotlib -y` — confirmed no MKL DLLs present. Ran the GLA diagnostic
there: succeeded on the first try.

Result: ligand stays bound in all 3 replicates (COM→pocket 1.6–3.6 Å, well
inside the pocket envelope; no progressive drift r1→r2→r3). The MM-GBSA
magnitude trend doesn't track pose geometry in any simple way, so the ±4.2
kcal/mol spread reads as legitimate independent-seed variability, not an
artifact. Figure: `figures/gla_freeacid_replicate_check.png`.

**Switched pure-analysis scripts to the `analysis` env by default.** Updated
run-instruction headers in `md_analyze.py`, `gla_carboxylate_retention.py`,
`gla_freeacid_replicate_check.py`, `make_specificity_fig.py`, `md_figures.py`.
Left untouched: MM-GBSA / production / supervisor scripts (need OpenMM/OpenFF,
only in `md` env) and `md_summary.py` / `md_check_binding.py` /
`md_contacts_pbc.py` (already targeted `.venv`, a separate working Python 3.13
env, unaffected by the bug).

**Thermal pattern note.** Between ~06:22 and ~08:23 the supervisor was hitting
the 78°C hard limit every ~7–9 min (vs. the normal 90-min duty-cycle pause) —
roughly 10x faster heat-up than earlier in the run. `nvidia-smi` showed SM
clock throttled to 1425/2100 MHz at 96% utilization, consistent with thermal
throttling (fan speed / power limit aren't exposed on this laptop GPU via
NVML). Pattern eased back to normal 90-min pauses by 11:07 — no action taken,
just flagged in case it recurs.

**Campaign status as of 12:04:** 13/28 new replicates complete (27/42 total
trajectories). Running: `palmitic_deprot_50ns_r2` (10.2/50 ns). Full r1+r2+r3
done for EPA, GLA, palmitic, apo-ToxT. Remaining queue after the current run:
`palmitic_deprot_r3`, then `pam`, `glucose_decoy`, `pentadecanal`,
`tridecanoic` (r2+r3 each) — 15 replicates left.
