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

**14:13 — power outage, supervisor stopped gracefully.** User reported a power
outage (running on battery, ~88% charge but only ~80% of original design
capacity, Windows estimating ~64 min runtime under the GPU's heavy draw).
Rather than risk an ungraceful kill when the battery dies mid-write, stopped
both the supervisor (PID 9476) and its active child run (PID 25680,
`palmitic_deprot_50ns_r2`) via `Stop-Process` — same checkpoint-safe mechanism
the supervisor already uses internally for thermal pauses, so at most the last
~250 ps (the checkpoint interval) needs re-simulating. Last recorded state:
`palmitic_deprot_50ns_r2` at 17.2/50 ns (34%), 13/28 new replicates done.
Campaign is fully idle — **needs a manual restart once power is back**
(relaunch `AutoDock_MD_Supervisor` scheduled task, or rerun
`md_supervisor_reps.py` directly; it will skip everything already at 50 ns and
resume `palmitic_deprot_50ns_r2` from its last checkpoint).

**14:35 — power restored, supervisor restarted.** Re-triggered the
`AutoDock_MD_Supervisor` scheduled task. Resumed cleanly: `palmitic_deprot_50ns_r2`
picked back up at 17.2/50 ns (34%), the exact checkpoint it was stopped at — no
progress lost. GPU cold-started at 44-47°C after the idle period.

**~20:29-21:47 — laptop slept on low battery (not a crash).** User reported the
laptop "died" sometime 5-7 PM; verified against Windows' own power event log
rather than assuming. Findings: `LastBootUpTime` unchanged (no reboot), and
`Microsoft-Windows-Power-Troubleshooter` recorded an explicit sleep/wake pair
with **Sleep Reason: Battery** — asleep 20:29:41, woke 21:46:57 (~77 min). This
explains the one anomalous gap in `thermal_supervisor_reps.log`: the run
resumed at 19:08:21 and didn't log its next pause until 21:47:09 — 2h39m later,
well past the normal 90-min duty cycle — because the process was frozen
in-memory by Windows sleep (not killed) for most of that window, then the
supervisor's poll loop caught the elapsed-time jump 11s after wake and logged a
routine-looking "ran 90 min" pause. No checkpoint reload needed this time —
unlike the 14:13 stop, sleep preserves process state in RAM, so it resumed
mid-instruction with zero progress lost, not just checkpoint-safe loss.

## 2026-07-31

**Unexplained ~14-hour stall — genuinely undiagnosed this time.** Found the
process dead with `reps_progress.log` stuck at `[00:38:46] tridecanoic_50ns_r3
41.2/50 ns` while the actual time was 14:41 — a 14-hour gap and no running
Python process at all. Checked thoroughly before restarting:
- `LastBootUpTime` unchanged (still 07-22) — **not** a reboot.
- No Application-log crash event (Id 1000) in the window — **not** a hard crash
  with a traceback.
- No Windows Defender detection/quarantine event — **not** AV intervention
  (as far as its operational log shows).
- No Kernel-Power sleep/wake event this time — **not** the battery-sleep
  pattern seen on 07-23.

`stderr.log` shows the last resume at 00:04:41 with no error, and the run made
~34 more minutes of real progress (38.8 ns checkpoint → 41.2 ns) before going
silent — so it wasn't an immediate failure, something killed it partway
through a normal chunk. Unlike every other incident logged here, this one has
**no identified cause**. Restarted via the `AutoDock_MD_Supervisor` scheduled
task; resumed cleanly from the 41.2/50 ns checkpoint, no progress lost. Worth
watching for a recurrence — if it happens again, worth checking whether the
detached console window itself is getting closed by something (manual or
automated), since that's the one avenue not yet ruled out.

**Campaign status:** 27/28 replicates done, only `tridecanoic_50ns_r3` (the
last one) remaining, resumed at 41.2/50 ns (82%).

**Second unexplained gap (18:24 → 01:28, ~7h vs. the normal 90-min cycle).**
Same signature as the stall above but this time the process was still alive
when caught (`Get-Process` confirmed it running, no restart needed). GPU had
cooled all the way to 40-44°C. Checked Kernel-Power/Power-Troubleshooter events
for this window too — found nothing, unlike the confirmed battery-sleep
incident on 07-23. Possibly a Modern Standby (S0ix) state that doesn't log the
classic sleep/wake events checked for; not confirmed. No data lost either way
— resumed/continued from the correct checkpoint on its own.

## 2026-08-01 — CAMPAIGN COMPLETE

**All 28 replicates done, 42/42 trajectories.** `tridecanoic_50ns_r3` finished
at 02:07:05, closing out the last of the 14 systems' triplicates. Every system
(EPA, methyl-EPA, EPA-carboxylate, GLA, GLA-ester, GLA-carboxylate, palmitic,
methyl-palmitate, palmitic-carboxylate, palmitoleate/PAM, glucose decoy,
pentadecanal, tridecanoic, apo-ToxT) now has independent r1+r2+r3 replicates
(distinct seeds) at 50 ns each. Campaign ran unattended since 2026-07-22 —
about 10 days, surviving two power-loss/stop-resume cycles, a battery-sleep
incident, one fully-unexplained ~14h stall, and one fully-unexplained ~7h gap
(both restarted or self-recovered with zero data loss thanks to checkpointing).

**Next steps (see `MANUSCRIPT_TODO_reps.md`):** recompute MM-GBSA at n=3 for
all remaining forms (carboxylate/ester rows — free-acid headline systems
already done, see 2026-07-22 entry above), finish the GLA carboxylate
diagnostic verification across all 3 reps, add replicate error bands to
RMSD/RMSF/retention figures, update Methods stats language, then the full
Zenodo data upload (see updated Progress section in `UPLOAD_2_zenodo.md`) can
finally happen — this was the one blocker holding it back.

**MM-GBSA n=3 recompute (remaining forms) complete.** Ran
`md_mmgbsa_n3_remaining.py` (100 frames/replicate) for all 10 remaining
carboxylate/ester/weak-binder systems; results in
`results_mmgbsa/mmgbsa_n3_remaining.csv`. Ranking expectation confirmed: EPA
carboxylate is the strongest binder overall (−48.5 ± 3.3 kcal/mol), and both
EPA and GLA (either form) beat the native palmitoleate control (−32.5 ± 4.6).
Notably, GLA carboxylate's SD dropped from the alarming single-trajectory
±20.5 (rep1 only) to **±5.9** once averaged across n=3 replicate means — the
GB-sensitivity artifact documented in `MANUSCRIPT_TODO_reps.md` item 2 is
mostly washed out by replicate averaging, though the COM-retention check
across r2/r3 (item 2e) is still outstanding to confirm the pose itself stays
bound in every replicate. Combined with the free-acid headline results
(`results_mmgbsa/mmgbsa_n3_headline.csv`, 2026-07-22), MM-GBSA item 1 in
`MANUSCRIPT_TODO_reps.md` is now fully done — remaining manuscript work is
items 2(e), 3, 4 (optional), 5, and 6 (GitHub push).

## 2026-08-02

**GLA carboxylate retention verified across all 3 replicates — item 2(e)
done.** Parametrized `gla_carboxylate_retention.py` to take a replicate suffix
and ran it (analysis env) against r1/r2/r3 of `gla_deprot_50ns`. Ligand-COM →
pocket distance stays well under the ~4 Å bound threshold in every replicate
(r1: 1.89 Å mean, max 3.42 Å; r2: 1.66 Å mean, max 2.75 Å; r3: 1.89 Å mean,
max 3.52 Å) with no progressive drift across reps — the mild rep1 excursion
doesn't worsen. Carboxylate head group is consistently solvent-exposed
(~7.2–7.4 Å from pocket, sd 0.37–0.59 Å) in all 3, matching the single-traj
diagnosis. The "stable pose, GB-artifact-not-instability" claim in item 2 is
now solid across replicates, not just rep1. Also fixed the figure title (item
2(d): "mobility" → "solvent exposure") and generated `_r2`/`_r3` versions of
`figures/gla_carboxylate_retention.png`. Item 2 in `MANUSCRIPT_TODO_reps.md`
is now fully done; remaining manuscript work is items 3, 4 (optional), 5, and
6 (GitHub push).

**MM-GBSA n=3 inserted into the manuscript; consolidated docx pass done.**
Added new `MANUSCRIPT_DRAFT.md` Section 3.11 "MM-GBSA binding free energies
(n = 3 replicates)" with Table 9 (all 13 systems, per-replicate values + mean
± SD); renumbered old 3.11→3.12, 3.12→3.13, which incidentally fixed a stale
"(Section 3.11)" cross-reference in Section 3.10 that had never pointed at
real MM-GBSA content. Updated the Abstract and Limitations MM-GBSA sentences
from "single-trajectory" to n=3 language (noting the GLA carboxylate SD drop
from ±20.5 to ±5.9 on replicate averaging, and that EPA methyl ester ±8.2
still carries comparatively wide between-replicate spread). Mirrored all of
this into `build_docx.js` (new Table 9 data/section, renumbering, wording)
and regenerated `ToxT_docking_manuscript.docx` — the two manuscript versions
are back in sync. Item 1 in `MANUSCRIPT_TODO_reps.md` is now fully closed;
remaining manuscript work is items 3, 4 (optional), 5, and 6 (GitHub push).

**Item 3 done: replicate error bands on retention/RMSD figures.** Regenerated
`figures/fig10_specificity.png` (`make_specificity_fig.py`) with mean ± SD
bands across n=3 replicates per system (core-seeded glucose decoy stays n=1 —
no replicates exist for that variant by design). Added a new headline
backbone-RMSD comparison (`make_rmsd_headline_fig.py` →
`figures/fig_rmsd_headline_apo.png`): EPA/GLA/palmitic free-acid vs. apo
ToxT, each mean ± SD across n=3. Notable result — apo drifts to a modestly
higher RMSD plateau (2.12±0.33 Å) than any ligand-bound headline system after
~20 ns (EPA 1.82±0.22, GLA 1.83±0.15, palmitic 1.79±0.42 Å), a global-scale
hint of ligand stabilisation that motivates item 4's still-optional
per-residue RMSF follow-up. Inserted as new Figure 13 in `MANUSCRIPT_DRAFT.md`
Section 3.8, Figure 10's caption updated to note the replicate averaging, both
mirrored into `build_docx.js` and the docx regenerated. Remaining manuscript
work: items 4 (optional), 5, and 6 (GitHub push).

**Item 4 done: apo-vs-holo per-residue RMSF.** New script
`make_apo_holo_rmsf_fig.py` -> `figures/fig_apo_holo_rmsf.png`: Cα RMSF, apo
(n=3 replicates) vs. holo = EPA/γ-linolenic/palmitic free acid (n=3 systems).
Honest result — this qualifies rather than cleanly confirms the allosteric
narrative: ligand binding lowers RMSF modestly everywhere (whole protein
1.01→0.88 Å, pocket 0.80→0.64 Å, AlphaFold3 DNA-contact residues 0.95→0.77 Å),
but the C-terminal HTH domain isn't disproportionately rigidified relative to
the rest of the protein (−0.16 Å there vs −0.12 Å elsewhere) — so it's a
protein-wide stabilisation effect, not clear domain-specific allostery.
Written up as such (not overclaimed) in new Figure 14 + a Section 3.8
paragraph, with the old Limitations "would further test" sentence updated to
report this actual finding. Mirrored into `build_docx.js`, docx regenerated.
Remaining manuscript work: items 5 (Methods/stats language) and 6 (GitHub
push).

**Item 5 done: Methods/stats language pass.** Added an explicit replicate
protocol statement to Methods (n=3 independent 50 ns replicates per system,
distinct seeds, 42 trajectories across 14 systems; mean ± SD across replicate
means). Updated the Abstract and Introduction MD-overview sentences (dropped
the stale "nine 50 ns runs" / "single-trajectory MM-GBSA" framing in favour of
the real 14-system/42-trajectory campaign). Audited every MD-related
figure/table caption and annotated the ones still showing rep-1-only data as
such (Table 5, Table 7, Figures 5/6/7 — historical, predate the replicate
campaign), pointing each to the later n=3 analyses where they exist. Rewrote
the Limitations bullet that said replicates were "in progress" (they're done)
and rescoped its caveat to per-replicate sampling length instead. Also caught
a docx-only stale claim (Section 7 "Future work" still listing MD replicates
as a planned extension) and fixed it. All mirrored into `build_docx.js`, docx
regenerated. **All 5 planned MANUSCRIPT_TODO_reps.md items are now done** —
only item 6 (GitHub push) remains.

**Item 6: committed, push held back per user request.** Reviewed the staging
set with `git add -n .` before touching anything — confirmed it matched the
TODO's predictions exactly (no `traj.dcd`/`system.xml`/checkpoint files, no
`ToxT_MD_data.tar.gz`, ~97 MB total, 92 files). Committed as `562b21c`
("Complete MD replicate campaign (42/42 trajectories); n=3 MM-GBSA;
manuscript updated") covering the whole session's work: campaign completion,
MM-GBSA n=3, GLA carboxylate retention verification, new Figures 13/14,
Figure 10 replicate bands, and the Methods/stats-language pass. Branch is now
2 commits ahead of `origin/main` (`9faaa1a`, `562b21c`). **`git push` was
intentionally not run — the user explicitly asked to hold off**; do not push
without a fresh go-ahead.

## 2026-08-03

**Pushed (`14592be`), then rebuilt the Zenodo upload bundle.** User confirmed
the push (after asking about a PR — clarified none exists here, we push
straight to `main`). Then rebuilt `ToxT_MD_data.tar.gz` since the old one
(Jul 14, 1.2 GB) predated the full triplicate campaign.

Caught and fixed a real bug while doing this: the tar command documented in
both `UPLOAD_2_zenodo.md` and `DATA_AVAILABILITY.md` claimed the `md/*/...`
glob "naturally skips `epa_smoketest`" — true for the `system.xml`/
`production_log.csv` patterns (different filenames there) but **false** for
`traj.dcd`/`system*.pdb` (epa_smoketest has those exact files too, since it's
a real if throwaway run). Running the documented command as-is would have
silently bundled 3 stray dev/test files into the Zenodo deposit. Fixed by
building the file list explicitly (`ls ... | grep -v epa_smoketest`) and
adding `--exclude='md/epa_smoketest/*'` to both docs' commands.

Also found `DATA_AVAILABILITY.md` suggested a *different* bundle filename
(`ToxT_MD_trajectories.tar.gz`) than the one `.gitignore` actually excludes
(`ToxT_MD_data.tar.gz`) — following that doc literally would have produced a
multi-GB file `git add .` wouldn't catch. Fixed to use the correct name.

Rebuilt bundle: `ToxT_MD_data.tar.gz`, **3.68 GB, 215 files**, verified 0
`epa_smoketest` entries. On-disk `md/*/` data is ~5.0 GB uncompressed. Bundle
is ready to drag into Zenodo — see `UPLOAD_2_zenodo.md` for the remaining
manual steps (Zenodo account, metadata, publish, DOI). Not yet uploaded —
that's a manual step for the user.

**Zenodo upload complete — DOI live: 10.5281/zenodo.21767402.** User
published the MD trajectory bundle to Zenodo (resource type Dataset; related
identifier "Continues" -> the JNPD paper DOI 10.24377/jnpd.article3244;
software list = OpenMM/OpenFF-Toolkit+Sage/OpenFF-NAGL/PDBFixer/MDTraj/Python,
matching Methods 2.9). Filled the real DOI into `DATA_AVAILABILITY.md`'s
paste-ready statement (replacing the `YYYYYYY` placeholder) and directly into
`MANUSCRIPT_DRAFT.md` Section 6 + `build_docx.js` (docx regenerated). Also
filled in the GitHub repo URL, which was still a `<user>/<repo>` placeholder.
Only remaining placeholder: the separate code-archive DOI (`XXXXXXX`,
GitHub-repo-to-Zenodo linking) — optional, not blocking.

Separately: 4 of the 5 bracketed reference placeholders in
`MANUSCRIPT_DRAFT.md` (items 6-9: fatty-acid-mimetic ToxT inhibitors, PDB
8B4D, herbal luteolin/catechin screen, sodium butyrate) are still unresolved
— web search was declined each time it was attempted this session, so these
remain open. Item 16 (OpenFF-NAGL) was resolved from memory as a
software-only citation (no journal paper found), not verified by search.

**Code-archive DOI live too — both Zenodo DOIs now complete.** Created GitHub
release `v1.0.0` (tag on `8a522f9`) via `gh release create`; user then linked
the repo to Zenodo and confirmed it picked up the release. Verified via
WebFetch: DOI `10.5281/zenodo.21778158`, resource type Software, references
`v1.0.0` and the correct repo, CC-BY-4.0, published 2026-08-03. Filled into
`DATA_AVAILABILITY.md`'s paste-ready statement (no placeholders left in it now
— both the code DOI and the MD-data DOI `10.5281/zenodo.21767402` are real)
and into `MANUSCRIPT_DRAFT.md` Section 6 + `build_docx.js` (docx
regenerated). All of Upload #1 (GitHub) and Upload #2 (Zenodo data) plus the
optional code-archive DOI are now done.

**ToxT–DNA section (formerly main-text 3.13 / Figure 11) moved to
Supplementary.** Separately from the docking/MD campaign, an exploratory
AF3-monomer-vs-Chai / dimer-vs-DNA comparison this session (new
`fold_toxt_toxbox_1mer/2mer` and Chai runs, distinct from the July
`af3_toxt_dna` run already in the manuscript) turned up real problems with
AI-predicted ToxT quaternary structure: AF3's dimer model has no
protein-protein contact at all (chains 70 Å apart), Chai's dimer has a
genuine backbone clash (K204/M200, unfixable by rotamer repack) and its
contact region doesn't match the literature's actual dimer interface
(helix α3, Lys158–Asp143; Comms Biol 2019). That newer analysis was not
folded into the manuscript — it's chat-only for now. But it did prompt
revisiting whether the *existing*, already-more-conservative July AF3
monomer ToxT–DNA model (pTM 0.85 / ipTM 0.31, Section 3.13/Figure 11) should
be a main-text claim. Decided no: moved it in full to
`SUPPLEMENTARY.md` as new **Section S.13 / Figure S23** (right after the
existing Figure S22 PAE/pLDDT panel it was already paired with). Updated
`MANUSCRIPT_DRAFT.md` in six places to point to it as an exploratory
supplementary check instead of a finding — Abstract, Introduction aims,
Methods 2.11, the Section 3.8 RMSF cross-reference (twice), Discussion, and
Limitations — while keeping the allosteric-mechanism argument itself
grounded in the independent literature (Lowden et al. 2010 domain
architecture), not dependent on our own low-confidence model. Mirrored the
same six edits into `build_docx.js` (hardcoded paragraph builder for the
main manuscript); `build_supplementary_docx.js` needed no manual edit since
it parses `SUPPLEMENTARY.md` generically. Both docx files regenerated
(`ToxT_docking_manuscript.docx`, `SUPPLEMENTARY.docx`). No figure files
moved or renamed on disk — only section/figure numbering changed. Not yet
committed to git.

**Added a direct, purpose-built test of the allosteric-restraint hypothesis
— null result, added to Supplementary as another caveat.** RMSF (Section
3.8) only measures local jitter amplitude, not whether the two domains move
together in a restrained way — a weak proxy for what the allosteric claim
actually predicts. Wrote `make_interdomain_hinge_analysis.py` (analysis
conda env, MDTraj): superposes each of the existing apo + EPA/GLA/palmitic
free-acid trajectories (12 total, n=3 replicates each) onto its own frame 0
using only the N-terminal domain, then measures the N-domain–residue188–HTH-domain
hinge angle and COM-COM distance per frame. Ran it: no ligand-dependent
shift in mean angle for any system, and no narrowing of the angular spread
(the direct "restraint" signal) for either strong binder (EPA p=0.87, GLA
p=0.37); only the weak binder palmitic showed a nominal p=0.041, which runs
backwards from what an affinity-dependent mechanism predicts and reads as a
false positive among three comparisons at n=3. Added in full as new
Section S.14 / Figure S24 / Table S10 in `SUPPLEMENTARY.md` (after Section
S.13), with TOC/index/closing-notes updated and `SUPPLEMENTARY.docx`
regenerated. Not referenced in the main manuscript at all — supplementary-only,
per the user's explicit request. Outputs: `interdomain_hinge_summary.csv`,
`figures/fig_interdomain_hinge.png`.

**Open question raised by the user, not yet resolved: does the manuscript
title still hold up?** The title ("...Microalgal Lipids as *Allosteric*
Antivirulence Agents...") asserts the allosteric mechanism as a
characterization, but every piece of *our own* evidence for it is now
either low-confidence (the AF3 model, already caveated) or a null result
(RMSF domain-specificity; this new hinge-angle test) — the only thing
actually supporting "allosteric" at this point is the literature's
domain-separation argument (Lowden et al. 2010), which establishes
"probably not steric" but doesn't positively establish restraint. User
paused this decision to run the PLIP investigation below instead; still
unresolved.

**Ran PLIP (Protein-Ligand Interaction Profiler) on the AF3/Chai
monomer+dimer ToxT-DNA models — cross-validates the DNA-contact interface,
unrelated to the allosteric/title question above.** Installed `plip` (pip,
analysis env) + bundled `openbabel`. Two gotchas hit and fixed: (1) `--chains`
is peptide/protein-protein mode only and silently excludes nucleotide
residues — default automatic ligand detection (no `--chains`) is what
correctly picks up DNA as a ligand; (2) the pip `openbabel` wheel lacks the
InChI format plugin, crashing PLIP's ligand characterization step — patched
with a try/except around the `self.inchikey = ...` line in the installed
package (cosmetic fix, not a project file). Ran default-mode PLIP on all
four top-ranked models (af3_monomer, af3_dimer, chai_monomer, chai_dimer;
PDBs converted from the earlier-extracted CIFs via PyMOL). Result:
independently confirms (via real H-bond/salt-bridge geometry, not just
proximity) the same ~185–276 DNA-contact residues found earlier by hand
(K212, R214, E215, N218, I236/K237, S249/Y250, S252, K256, S264) across all
four models; also shows Chai's interface is quantitatively denser than
AF3's (14 H-bonds/6 salt bridges vs. 9/3, monomer), consistent with Chai's
higher self-reported ipTM. Chat-only — not written into the manuscript, per
the earlier decision to keep the whole AF3-vs-Chai dimer investigation out
of scope for this paper. Outputs in
`plip_out/{af3_monomer_default,af3_dimer,chai_monomer,chai_dimer}/`.

**User asked for a full strategic "council" analysis of the paper's
direction.** Delivered directly (not via subagents — full session context
made that the better call) rather than spawned. Verdict: the docking/MD/
specificity spine is strong and untouched by anything this session found;
the allosteric mechanism claim in the title is the one live risk, now
undercut by three independent findings this session (dimer/Chai structure
failure, RMSF null, hinge-angle null). Recommended dropping or reframing
"Allosteric" in the title; user has not yet decided (see above).

**Author supplied CV strain accession + full GC-MS methodology — see
`MANUSCRIPT_TODO_reps.md` item 7 for full detail.** Added as new Section
2.1 in `MANUSCRIPT_DRAFT.md` (Methods renumbered 2.1–2.12 → 2.2–2.13;
`build_docx.js`'s own condensed Methods numbering 2.1–2.8 → 2.2–2.9 to
match), title footnote updated, new reference (Kumaran et al., 2023, author
still needs to supply the full citation) added to both files' reference
lists. Both docx regenerated — `ToxT_docking_manuscript.docx` was open in
Word and locked the write; closed the Word process with the user's explicit
go-ahead before regenerating. Still open: CCM's culture-collection
accession, the full Kumaran et al. citation, and a flagged (not resolved)
inconsistency in the supplied peak list where *cis*-10-heptadecenoic acid
appears as organism-specific to both CV and CCM — none of this touched the
existing Tables 1/2 lipid panels, which are unchanged.

**Follow-up same topic, next day: both flagged items resolved by the
author.** CCM genuinely has no culture-collection accession number (not a
missing placeholder) — updated the phrasing in the title footnote and
Section 2.1 of `MANUSCRIPT_DRAFT.md`/`build_docx.js` accordingly. The
*cis*-10-heptadecenoic acid inconsistency was confirmed to be an error in
the original Jaiswal et al. (2025) report, not this manuscript — the
compound is genuinely shared between CV and CCM, which is what Tables 1/2
already had, so no change was needed there (validates the earlier call not
to touch them speculatively). Section 2.1 text and the closing dated
reference-list note updated in both `MANUSCRIPT_DRAFT.md` and
`build_docx.js`; `ToxT_docking_manuscript.docx` regenerated (no Word lock
this time).

**Same thread, final piece: full Kumaran et al. citation supplied.**
Kumaran M, Palanisamy KM, Bhuyar P, Maniam GP, Rahim MHA, Govindan N.,
*Energy Nexus* 2023;9:100169, doi:10.1016/j.nexus.2022.100169 — filled into
ref 11 in `MANUSCRIPT_DRAFT.md` and `build_docx.js`, closing dated notes
updated in both, docx regenerated. **`MANUSCRIPT_TODO_reps.md` item 7 is
now fully closed — no author-supplied content or reference placeholders
remain open anywhere in the manuscript.**

**Title decision resolved.** Talked through the options (pocket-binding
framing, drop-the-word, hedge-with-"candidate", leave-as-is, plus a few
more variants on request); user picked a merge of two — lead with the
actual quantitative finding (unsaturation) rather than a generic
descriptor, name the specific well-supported target site (fatty-acid
pocket) rather than an unproven mechanism — and asked to drop the original
"Locking Down ToxT" hook too, since it echoes the same conformational-lock
claim "Allosteric" did (flagged this myself before the user confirmed).
Final title: **"Unsaturation Drives ToxT Fatty-Acid-Pocket Engagement:
Microalgal Lipids as Antivirulence Agents Against *Vibrio cholerae* — A
Docking and Molecular Dynamics Study."** Updated in `MANUSCRIPT_DRAFT.md`
(H1), `SUPPLEMENTARY.md` (title block), and `build_docx.js`; both docx
regenerated cleanly (no Word lock this time). Confirmed via grep that no
other project markdown file quotes the old title, and that the two
already-published Zenodo records use their own independent, descriptive
dataset titles (not a copy of the manuscript title), so no metadata
mismatch there. Could not check the GitHub repo's own description field
(`gh` not authenticated in this session) — worth a manual look if it
duplicates the old title anywhere.
