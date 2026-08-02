# Manuscript edits pending — apply AFTER the MD triplicate (r1+r2+r3) is complete

Status of campaign: see `md/reps_progress.log` and `md/thermal_supervisor_reps.log`.
Do **one consolidated pass** over BOTH `MANUSCRIPT_DRAFT.md` and `build_docx.js`, then
regenerate the docx (`node build_docx.js`). Keep the two versions in sync.

Rule for this whole batch: **report replicate statistics as mean ± SD across the 3
independent replicate means** (between-run error), not per-frame SD. Three independent
seeds (rep1 = original, r2 = seed 100x, r3 = seed 200x).

---

## 1. MM-GBSA table → convert to n=3 — DONE (2026-08-01/02)
- Recomputed via `md_mmgbsa_n3_headline.py` (free-acid systems, 2026-07-22) and
  `md_mmgbsa_n3_remaining.py` (esters/carboxylates/controls/weak binders, 2026-08-01),
  100 frames/replicate. Results: `results_mmgbsa/mmgbsa_n3_headline.csv`,
  `results_mmgbsa/mmgbsa_n3_remaining.csv`.
- Inserted into `MANUSCRIPT_DRAFT.md` as new **Section 3.11 "MM-GBSA binding free
  energies (n = 3 replicates)"** with **Table 9** (2026-08-02); old 3.11→3.12, 3.12→3.13.
  The stale "(Section 3.11)" cross-reference in Section 3.10 now resolves correctly.
  Abstract and Limitations MM-GBSA sentences also updated from "single-trajectory" to
  n=3 language.
- Final n=3 mean ± SD (kcal/mol): EPA carboxylate −48.5±3.3, EPA free acid −42.4±2.6,
  EPA methyl ester −33.4±8.2; GLA carboxylate −44.3±5.9, GLA free acid −38.6±4.2, GLA
  methyl ester −30.6±7.0; palmitic carboxylate −45.4±4.0, palmitic free acid −32.7±1.0,
  palmitic methyl ester −36.8±0.7; palmitoleate (native, +ctrl) −32.5±4.6; glucose
  (decoy) −25.3±2.4; pentadecanal −34.7±3.2; tridecanoic −24.6±4.2.
- Ranking confirmed: EPA strongest binder overall; both EPA and GLA (either form) beat
  the native palmitoleate control.
- **Consolidated pass done (2026-08-02):** `build_docx.js` synced (new Section 3.11 +
  Table 9, 3.11->3.12, 3.12->3.13 renumbering, abstract/limitations wording) and
  `ToxT_docking_manuscript.docx` regenerated.
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
  (d) DONE (2026-08-02): figure title fixed in `gla_carboxylate_retention.py`
      ("mobility" → "solvent exposure").
  (e) DONE (2026-08-02): verified across all 3 replicates — ligand-COM → pocket stays
      well under 4 Å in every rep (r1: 1.89 Å mean, 0.82–3.42 Å range; r2: 1.66 Å mean,
      0.98–2.75 Å; r3: 1.89 Å mean, 0.94–3.52 Å), no progressive drift across replicates.
      Carboxylate head group consistently solvent-exposed (~7.2–7.4 Å, sd 0.37–0.59 Å) in
      all 3. "Stable pose" claim is solid. Figures: `figures/gla_carboxylate_retention.png`
      (r1), `_r2.png`, `_r3.png`.

## 3. RMSD / RMSF / retention figures → add replicate error bands — DONE (2026-08-02)
- `make_specificity_fig.py` (Figure 10) regenerated: every system with replicates now
  plots mean ± SD across n=3 (core-seeded glucose decoy stays n=1, no other replicates
  exist for that variant). Caption updated in both `MANUSCRIPT_DRAFT.md` and
  `build_docx.js`.
- New script `make_rmsd_headline_fig.py` → `figures/fig_rmsd_headline_apo.png`: backbone
  RMSD mean ± SD across n=3 for the headline systems (EPA, γ-linolenic, palmitic — free
  acid — vs. apo ToxT). Result: apo drifts to a modestly higher RMSD plateau (2.12±0.33 Å)
  than any ligand-bound system after ~20 ns (EPA 1.82±0.22, GLA 1.83±0.15, palmitic
  1.79±0.42 Å) — a global-scale hint of ligand-stabilisation that motivates item 4's
  per-residue RMSF follow-up.
- Inserted as new **Figure 13** in `MANUSCRIPT_DRAFT.md` Section 3.8 (after Table
  5/Figure 7) with a new paragraph; mirrored into `build_docx.js`; docx regenerated.
- Note: Table 5 (nine head-group simulations) intentionally left as-is — it's the
  original single-trajectory summary and converting all 9 systems to full n=3 RMSD
  stats was out of scope for the "headline systems" ask; only the 4 named systems got
  replicate treatment here.

## 4. Apo-vs-holo RMSF — DONE (2026-08-02)
- New script `make_apo_holo_rmsf_fig.py` -> `figures/fig_apo_holo_rmsf.png`. Per-residue
  Cα RMSF (production window >5 ns), apo ToxT (n=3 replicates) vs. holo = EPA/γ-linolenic
  /palmitic free acid (n=3 systems, each itself a 3-replicate mean).
- Result is a **qualification, not a clean confirmation** of domain-specific allostery:
  ligand binding reduces RMSF modestly protein-wide (apo 1.01±0.19 Å vs holo 0.88±0.11 Å),
  including at the pocket (0.80→0.64 Å) and the 5 AlphaFold3 DNA-contact residues
  (0.95→0.77 Å), but the C-terminal HTH domain (188-273) isn't disproportionately
  rigidified relative to the rest of the protein (−0.16 Å there vs −0.12 Å elsewhere).
  Written up honestly as "consistent with, but does not on its own establish" the
  domain-specific allosteric coupling from the ToxT–DNA model.
- Inserted as new **Figure 14** in `MANUSCRIPT_DRAFT.md` Section 3.8 (right after
  Figure 13/RMSD paragraph, replacing the old "future work" pointer) with a new results
  paragraph; Limitations' old "would further test" sentence updated to report the actual
  (qualified) finding. Mirrored into `build_docx.js`; docx regenerated.

## 5. Methods / stats language — DONE (2026-08-02)
- Added the explicit replicate-protocol statement to Methods Section 2.9 (2.8 in docx):
  "n = 3 independent 50 ns replicates per system, distinct random seeds (rep1/r2/r3);
  values reported as mean ± SD across replicate means... 42 trajectories total" across
  all 14 systems.
- Updated Abstract and Introduction MD-overview sentences from "nine 50 ns runs" /
  "single-trajectory MM-GBSA" to state the full 14-system, n=3-replicate, 42-trajectory
  campaign.
- Audited every figure/table caption for single-trajectory implications and annotated
  the ones still showing rep-1-only data (historical, predates the replicate campaign):
  Table 5, Table 7, Figures 5, 6, 7 — each now notes "rep-1 trajectory" and points to
  the later n=3 analyses (Figure 10/13/14, Table 9) where they exist for that system.
- Rewrote the Limitations "single trajectories... independent replicates (in progress)"
  bullet — replicates are done, not in progress; caveat now correctly scoped to
  per-replicate sampling length (50 ns), not replicate count.
- Fixed a docx-only stale item: Section 7 "Future work" (`build_docx.js`) said
  "independent MD replicates for statistics" was still planned — now notes it's
  complete.
- All edits mirrored into `build_docx.js`; docx regenerated.

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
