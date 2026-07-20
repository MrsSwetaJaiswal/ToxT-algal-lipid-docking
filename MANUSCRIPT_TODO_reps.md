# Manuscript edits pending — apply AFTER the MD triplicate (r1+r2+r3) is complete

Status of campaign: see `md/reps_progress.log` and `md/thermal_supervisor_reps.log`.
Do **one consolidated pass** over BOTH `MANUSCRIPT_DRAFT.md` and `build_docx.js`, then
regenerate the docx (`node build_docx.js`). Keep the two versions in sync.

Rule for this whole batch: **report replicate statistics as mean ± SD across the 3
independent replicate means** (between-run error), not per-frame SD. Three independent
seeds (rep1 = original, r2 = seed 100x, r3 = seed 200x).

---

## 1. MM-GBSA table → convert to n=3
- Recompute MM-GBSA per replicate for each system, then report mean ± SD across the
  three replicate means. Script: `md_mmgbsa_all.py` (run per replicate dir set), 100 frames.
- Current single-trajectory (rep1) values, for reference — WILL be replaced:
  - EPA carboxylate −49.0 ± 3.6 ; EPA free acid −45.1 ± 3.5
  - GLA carboxylate −37.6 ± **20.5** (unreliable — see item 2) ; GLA free acid −34.2 ± 3.9
  - palmitic carboxylate −41.3 ± 14.7 ; palmitic free acid −33.2 ± 2.1
  - palmitoleate (native, +ctrl) −33.1 ± 2.5 ; glucose (decoy) −23.5 ± 4.1
- Expectation to re-check at n=3: EPA remains the strongest binder; both EPA and GLA
  beat the native palmitoleate. Confirm this ranking survives the replicate averaging.

## 2. GLA carboxylate ±20.5 — report free-acid as primary + add caveat + SI figure
DIAGNOSTIC ALREADY DONE (rep1, `gla_deprot_50ns`), script:
`gla_carboxylate_retention.py`, figure: `figures/gla_carboxylate_retention.png`.
Result (49.8 ns, 200 frames):
  - ligand COM → pocket: mean 1.89 Å, sd 0.55, range 0.82–3.42  → **bound entire run**
  - carboxylate C → pocket: mean 7.24 Å, sd **0.37**, excursion only 2.16 Å
    → solvent-exposed at pocket mouth but **geometrically stable** (small SD)
  - ligand RMSD to t0: mean 2.27 ± 0.29 Å  → bounded chain flexibility

INTERPRETATION (precise wording — note it is NOT gross "mobility"):
  The ±20.5 is a **single-trajectory GB artifact for a solvent-exposed −1 charge**, not an
  unstable pose. A permanently exposed anionic head group sits where the GB desolvation
  term is most sensitive, so even small (~2 Å) environmental fluctuations of the charge
  give large per-frame electrostatic swings. The neutral free acid has no such charge
  (sd ±3.9). The pose itself is stable (COM bound for the full 50 ns).

EDITS:
  (a) Report GLA MM-GBSA primary = FREE-ACID value (also more defensible biologically:
      acid/anion coexist at physiological pH). Treat carboxylate as a sensitivity check.
  (b) Add one honest sentence (Results/MM-GBSA or SI), e.g.:
      "The elevated MM-GBSA variance for the γ-linolenate carboxylate (±20.5 kcal/mol)
       arises from its solvent-exposed anionic head group (Fig. Sx; carboxylate 7.2 ± 0.4 Å
       from the pocket centroid throughout, while the ligand centre of mass remains bound,
       1.9 Å, for the full 50 ns) — a known single-trajectory GB sensitivity for surface
       charges rather than pose instability. We therefore report the neutral free-acid
       value as primary."
  (c) Add `figures/gla_carboxylate_retention.png` to the SI.
  (d) FIX FIGURE TITLE before use: current title says "ligand & head-group mobility";
      change "mobility" → "solvent exposure" (the head group barely moves, sd 0.37 Å).
      Edit in `gla_carboxylate_retention.py` and re-run.
  (e) VERIFY across replicates: confirm carboxylate stays bound (COM < ~4 Å) in r2 and r3
      too. rep1 shows a mild COM drift to ~3 Å over 35–50 ns — check it is not progressive
      across replicates. If all 3 stay bound, the "stable pose" claim is solid.

## 3. RMSD / RMSF / retention figures → add replicate error bands
- Regenerate the specificity/retention figure (`make_specificity_fig.py`) and any RMSD/RMSF
  panels using all three replicates; show mean ± SD band per system.
- Headline systems for n=3 error bars: EPA, γ-linolenic, palmitic, apo.

## 4. Apo-vs-holo RMSF (optional, still not done)
- With apo triplicate complete, compute per-residue RMSF apo vs holo to support/qualify
  the allosteric-stabilisation narrative. Offered earlier; user has not confirmed.

## 5. Methods / stats language
- State replicate protocol: "n = 3 independent 50 ns replicates per system, distinct
  random seeds; values reported as mean ± SD across replicate means."
- Update any figure/table captions that currently imply single-trajectory.

## 6. GitHub push — repo out of sync since initial commit
Only one commit exists on `main` (`90beaed`, "Docking + MD of algal lipids against
V. cholerae ToxT") and it is already pushed to
`origin` (https://github.com/MrsSwetaJaiswal/ToxT-algal-lipid-docking.git). Everything
since is local-only. Before pushing:
  - **Do NOT `git add` `ToxT_MD_data.tar.gz`** (1.2 GB, untracked, not covered by
    `.gitignore`) — GitHub hard-rejects files > 100 MB. Either add an explicit
    `.gitignore` line for it or move it out of the repo; it belongs on Zenodo per
    `DATA_AVAILABILITY.md`.
  - Per-replicate MD dirs (`md/*_r2/`, `md/*_r3/`) are safe to add as-is — the large
    per-run artifacts (`traj.dcd`, `system.xml`, `system.pdb`, `checkpoint.chk`,
    `equilibrated.xml`) are already excluded by the existing `md/*/...` gitignore
    patterns; only small files (`production_log.csv`, `stderr.log`) would be staged.
  - Commit, then `git push`, once the replicate campaign (or a checkpoint of it) is
    at a state worth recording. See record below for the current diff.

---

## Execution note
Harness script execution has been blocked in-session recently; the n=3 recompute + figure
regeneration will likely be run by the user (one-liners), output pasted back, then Claude
interprets and writes the consolidated text into `.md` + `build_docx.js`, then
`node build_docx.js`.
