# Supplementary Information

**Unsaturation Drives ToxT Fatty-Acid-Pocket Engagement: Microalgal Lipids as
Antivirulence Agents Against *Vibrio cholerae* — A Docking and Molecular
Dynamics Study**

*Draft — supplementary figures and tables supporting the main manuscript
(`MANUSCRIPT_DRAFT.md`). Figures are numbered S1–S23 and tables S1–S11, in the
order they appear below; the single in-text SI citation in the main manuscript
(Section 3.11, MM-GBSA) now points to Figure S18 by number. Section S.13
(Figure S22, Table S11) presents AlphaFold3 and Chai-1 models of ToxT bound
to the native El Tor *ctxAB* promoter. Section S.14 (Figure S23, Table S10) is a
supplementary-only analysis (not in the main manuscript at all) run to
directly test the allosteric-restraint hypothesis on the existing MD
trajectories; it is a null result — see its note for interpretation.*

---

## Contents

**Figures:**
[S1](#figure-s1-individual-docking-poses--cv-panel-15-lipids) (CV docking poses) ·
[S2](#figure-s2-individual-docking-poses--ccm-panel-13-lipids) (CCM docking poses) ·
[S3–S17](#figures-s3s17--table-s1-individual-md-trajectory-diagnostics-per-system-all-3-replicates) (per-system MD diagnostics, r1–r3) ·
[S18–S19](#figures-s18s19-gla-carboxylate-gb-variance-diagnostic) (GLA carboxylate GB-variance diagnostic) ·
[S20](#figure-s20-blind-docking-pose-galleries-whole-protein-search) (blind-docking pose galleries) ·
[S21](#figure-s21-individual-vinardo-scored-docking-poses-22-lipids) (Vinardo pose gallery) ·
[S22](#section-s13--figure-s22--table-s11-toxtctxab-promoter-models-on-the-native-el-tor-sequence-alphafold3-and-chai-1) (ToxT–*ctxAB* promoter models, native El Tor: AF3 + Chai-1) ·
[S23](#section-s14--figure-s23--table-s10-inter-domain-hinge-angle-analysis-a-direct-null-test-of-the-allosteric-restraint-hypothesis) (inter-domain hinge angle, null result)

**Tables:**
[S1](#table-s1-summary-mean--sd-across-n3-replicates-this-si-pipeline) (replicate MD summary, mean ± SD) ·
[S2–S9](#tables-s2s9-supplementary-data-tables) (full docking/MM-GBSA result CSVs) ·
[S10](#section-s14--figure-s23--table-s10-inter-domain-hinge-angle-analysis-a-direct-null-test-of-the-allosteric-restraint-hypothesis) (inter-domain hinge-angle summary) ·
[S11](#section-s13--figure-s22--table-s11-toxtctxab-promoter-models-on-the-native-el-tor-sequence-alphafold3-and-chai-1) (AlphaFold3 + Chai-1 confidence metrics, all 5 models each)

**Other:** [Remaining open items](#remaining-open-items)

## SI figure/table index

| # | Item | Cited in main text as... |
|---|---|---|
| Figure S1 | CV panel individual docking poses (15) | supports Table 1, Figure 9A |
| Figure S2 | CCM panel individual docking poses (13) | supports Table 2, Figure 9B |
| Figure S3 | EPA free acid — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S4 | EPA deprotonated carboxylate — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S5 | EPA methyl ester — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S6 | GLA free acid — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S7 | GLA deprotonated carboxylate — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S8 | GLA methyl ester — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S9 | Palmitic free acid — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S10 | Palmitic deprotonated carboxylate — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S11 | Palmitic methyl ester — MD diagnostics, r1–r3 | supports Table 5, Figures 5–7 |
| Figure S12 | Palmitoleate (native ligand) — MD diagnostics, r1–r3 | supports Table 7 |
| Figure S13 | Glucose decoy (docked start) — MD diagnostics, r1–r3 | supports Table 7, Figure 10 |
| Figure S14 | Pentadecanal — MD diagnostics, r1–r3 | supports Table 7 |
| Figure S15 | Tridecanoic acid — MD diagnostics, r1–r3 | supports Table 7 |
| Figure S16 | Apo ToxT — MD diagnostics, r1–r3 | supports Figures 13, 14 |
| Figure S17 | Glucose decoy, core-seeded (single trajectory) — MD diagnostics | supports Table 7, Figure 10 |
| Figure S18 | GLA carboxylate GB-variance diagnostic, r1–r3 | **cited in-text**, Section 3.11 ("(Figure S18)") |
| Figure S19 | GLA free-acid replicate check | related to Figure S18, not separately cited |
| Figure S20 | Blind-docking pose galleries, all modes, 5 ligands | supports Table 6, Section 3.9 |
| Figure S21 | Individual Vinardo-scored docking poses (22 lipids) | supports Figure 3, Section 3.6 |
| Figure S22 | AlphaFold3 + Chai-1 ToxT–*ctxAB* promoter models (native El Tor sequence) | Section 3.8 (RMSF) and Discussion/Limitations reference Section S.13 generally |
| Figure S23 | Inter-domain hinge-angle distributions, apo vs. holo (null result) | supplementary-only analysis, not cited in main text |
| Table S1 | Per-system MD replicate summary, mean ± SD (this SI pipeline) | independent cross-check on Figure 13 |
| Table S2 | Full CV panel docking affinities (15) | source for Table 1 |
| Table S3 | Full CCM panel docking affinities (13) | source for Table 2 |
| Table S4 | Blind-docking summary, all poses per ligand | source for Table 6 |
| Table S5 | Vina vs. Vinardo affinity, all 22 ligands | source for Figure 3, Section 3.6 |
| Table S6 | Reference ligand docking (virstatin/butyrate/oleic acid) | source for Table 8 |
| Table S7 | Acid vs. methyl-ester paired affinities, both organisms | source for Table 4 |
| Table S8 | Full descriptor set, all 22 ligands | source for Table 3 |
| Table S9 | Per-replicate MM-GBSA raw values, all 13 systems | source for Table 9 |
| Table S10 | Inter-domain hinge-angle summary, apo vs. 3 holo systems (n=3 replicates each) | source for Figure S23 / Section S.14 |
| Table S11 | AlphaFold3 + Chai-1 confidence metrics, native El Tor promoter (all 5 models each) | source for Figure S22 / Section S.13 |

---

## Figure S1. Individual docking poses — CV panel (15 lipids)

Each panel shows the individual top-ranked AutoDock Vina pose (cyan) superposed
on the ToxT fatty-acid pocket, with the co-crystallized native ligand
palmitoleate (yellow, PDB 3GBG) and pocket residues coloured by chemistry
(orange = aromatic, blue = basic, grey = hydrophobic). Complements the panel
overlay in main-text Figure 9A, at per-ligand resolution. Ranked by affinity
(matches Table 1).

| Rank | Lipid | ΔG (kcal/mol) | Image |
|---|---|---|---|
| 1 | EPA (eicosapentaenoic acid) | −8.78 | `figures/si_docking/CV_cis_5_8_11_14_17_eicosapentaenoic_acid.png` |
| 2 | methyl eicosapentaenoate | −8.48 | `figures/si_docking/CV_methyl_cis_5_8_11_14_17_eicosapntaenoate.png` |
| 3 | methyl 4,7,10,13-hexadecatetraenoate | −8.46 | `figures/si_docking/CV_methyl_4_7_10_13_hexadecatetraenoate.png` |
| 4 | γ-linolenic acid | −8.13 | `figures/si_docking/CV_gamma_linolenic_acid.png` |
| 5 | 9,12,15-octadecatrienoic acid (ALA) | −7.91 | `figures/si_docking/CV_9_12_15_octadecatrienoic_acid.png` |
| 6 | *cis*-10-heptadecenoic acid | −7.81 | `figures/si_docking/CV_cis_10_heptadecenoic_acid.png` |
| 7 | methyl palmitoleate | −7.72 | `figures/si_docking/CV_methyl_palmitoleate.png` |
| 8 | heptadecanoic acid | −7.68 | `figures/si_docking/CV_heptadecanoic_acid.png` |
| 9 | stearic acid | −7.63 | `figures/si_docking/CV_stearic_acid.png` |
| 10 | methyl heptadecanoate | −7.57 | `figures/si_docking/CV_methyl_heptadecanoate.png` |
| 11 | methyl stearate | −7.57 | `figures/si_docking/CV_methyl_stearate.png` |
| 12 | methyl palmitate | −7.48 | `figures/si_docking/CV_methyl_palmitate.png` |
| 13 | methyl myristate | −7.31 | `figures/si_docking/CV_methyl_myristate.png` |
| 14 | methyl pentadecanoate | −7.18 | `figures/si_docking/CV_methyl_pentadecanoate.png` |
| 15 | pentadecanal | −6.90 | `figures/si_docking/CV_pentadecanal.png` |

**Rank 1: EPA (eicosapentaenoic acid) (−8.78 kcal/mol)**

![EPA (eicosapentaenoic acid)](figures/si_docking/CV_cis_5_8_11_14_17_eicosapentaenoic_acid.png)

**Rank 2: methyl eicosapentaenoate (−8.48 kcal/mol)**

![methyl eicosapentaenoate](figures/si_docking/CV_methyl_cis_5_8_11_14_17_eicosapntaenoate.png)

**Rank 3: methyl 4,7,10,13-hexadecatetraenoate (−8.46 kcal/mol)**

![methyl 4,7,10,13-hexadecatetraenoate](figures/si_docking/CV_methyl_4_7_10_13_hexadecatetraenoate.png)

**Rank 4: γ-linolenic acid (−8.13 kcal/mol)**

![γ-linolenic acid](figures/si_docking/CV_gamma_linolenic_acid.png)

**Rank 5: 9,12,15-octadecatrienoic acid (ALA) (−7.91 kcal/mol)**

![9,12,15-octadecatrienoic acid (ALA)](figures/si_docking/CV_9_12_15_octadecatrienoic_acid.png)

**Rank 6: *cis*-10-heptadecenoic acid (−7.81 kcal/mol)**

![*cis*-10-heptadecenoic acid](figures/si_docking/CV_cis_10_heptadecenoic_acid.png)

**Rank 7: methyl palmitoleate (−7.72 kcal/mol)**

![methyl palmitoleate](figures/si_docking/CV_methyl_palmitoleate.png)

**Rank 8: heptadecanoic acid (−7.68 kcal/mol)**

![heptadecanoic acid](figures/si_docking/CV_heptadecanoic_acid.png)

**Rank 9: stearic acid (−7.63 kcal/mol)**

![stearic acid](figures/si_docking/CV_stearic_acid.png)

**Rank 10: methyl heptadecanoate (−7.57 kcal/mol)**

![methyl heptadecanoate](figures/si_docking/CV_methyl_heptadecanoate.png)

**Rank 11: methyl stearate (−7.57 kcal/mol)**

![methyl stearate](figures/si_docking/CV_methyl_stearate.png)

**Rank 12: methyl palmitate (−7.48 kcal/mol)**

![methyl palmitate](figures/si_docking/CV_methyl_palmitate.png)

**Rank 13: methyl myristate (−7.31 kcal/mol)**

![methyl myristate](figures/si_docking/CV_methyl_myristate.png)

**Rank 14: methyl pentadecanoate (−7.18 kcal/mol)**

![methyl pentadecanoate](figures/si_docking/CV_methyl_pentadecanoate.png)

**Rank 15: pentadecanal (−6.90 kcal/mol)**

![pentadecanal](figures/si_docking/CV_pentadecanal.png)


---

## Figure S2. Individual docking poses — CCM panel (13 lipids)

Same rendering convention as Figure S1. Complements main-text Figure 9B
(matches Table 2).

| Rank | Lipid | ΔG (kcal/mol) | Image |
|---|---|---|---|
| 1 | γ-linolenic acid | −8.13 | `figures/si_docking/CCM_gamma_linolenic_acid.png` |
| 2 | neophytadiene | −8.12 | `figures/si_docking/CCM_neophytadiene.png` |
| 3 | methyl 3,9,12-octadecatrienoate | −7.97 | `figures/si_docking/CCM_methyl_3_cis_9_cis_12_cis_octadecatrienoate.png` |
| 4 | methyl heneicosanoate | −7.84 | `figures/si_docking/CCM_methyl_heneicosanoate.png` |
| 5 | *cis*-10-heptadecenoic acid | −7.81 | `figures/si_docking/CCM_cis_10_heptadecenoic_acid.png` |
| 6 | 9,11-octadecadienoic acid | −7.80 | `figures/si_docking/CCM_9_11_ooctadecadienoic_acid.png` |
| 7 | methyl palmitoleate | −7.72 | `figures/si_docking/CCM_methyl_palmitoleate.png` |
| 8 | methyl stearate | −7.57 | `figures/si_docking/CCM_methyl_stearate.png` |
| 9 | methyl palmitate | −7.48 | `figures/si_docking/CCM_methyl_palmitate.png` |
| 10 | methyl 18-fluorostearate | −7.38 | `figures/si_docking/CCM_methyl_18_fluorostearate.png` |
| 11 | palmitic acid | −7.32 | `figures/si_docking/CCM_palmitic_acid.png` |
| 12 | methyl myristate | −7.31 | `figures/si_docking/CCM_methyl_myristate.png` |
| 13 | tridecanoic acid | −6.84 | `figures/si_docking/CCM_tridecanoic_acid.png` |

**Rank 1: γ-linolenic acid (−8.13 kcal/mol)**

![γ-linolenic acid](figures/si_docking/CCM_gamma_linolenic_acid.png)

**Rank 2: neophytadiene (−8.12 kcal/mol)**

![neophytadiene](figures/si_docking/CCM_neophytadiene.png)

**Rank 3: methyl 3,9,12-octadecatrienoate (−7.97 kcal/mol)**

![methyl 3,9,12-octadecatrienoate](figures/si_docking/CCM_methyl_3_cis_9_cis_12_cis_octadecatrienoate.png)

**Rank 4: methyl heneicosanoate (−7.84 kcal/mol)**

![methyl heneicosanoate](figures/si_docking/CCM_methyl_heneicosanoate.png)

**Rank 5: *cis*-10-heptadecenoic acid (−7.81 kcal/mol)**

![*cis*-10-heptadecenoic acid](figures/si_docking/CCM_cis_10_heptadecenoic_acid.png)

**Rank 6: 9,11-octadecadienoic acid (−7.80 kcal/mol)**

![9,11-octadecadienoic acid](figures/si_docking/CCM_9_11_ooctadecadienoic_acid.png)

**Rank 7: methyl palmitoleate (−7.72 kcal/mol)**

![methyl palmitoleate](figures/si_docking/CCM_methyl_palmitoleate.png)

**Rank 8: methyl stearate (−7.57 kcal/mol)**

![methyl stearate](figures/si_docking/CCM_methyl_stearate.png)

**Rank 9: methyl palmitate (−7.48 kcal/mol)**

![methyl palmitate](figures/si_docking/CCM_methyl_palmitate.png)

**Rank 10: methyl 18-fluorostearate (−7.38 kcal/mol)**

![methyl 18-fluorostearate](figures/si_docking/CCM_methyl_18_fluorostearate.png)

**Rank 11: palmitic acid (−7.32 kcal/mol)**

![palmitic acid](figures/si_docking/CCM_palmitic_acid.png)

**Rank 12: methyl myristate (−7.31 kcal/mol)**

![methyl myristate](figures/si_docking/CCM_methyl_myristate.png)

**Rank 13: tridecanoic acid (−6.84 kcal/mol)**

![tridecanoic acid](figures/si_docking/CCM_tridecanoic_acid.png)


*(Note: 6 lipids are shared between the CV and CCM panels — γ-linolenic acid,
*cis*-10-heptadecenoic acid, methyl palmitoleate, methyl stearate, methyl
palmitate, methyl myristate. Each was docked independently per organism run
[README: "CV and CCM panels were docked as two independent runs into the same
pocket"], so both individual poses/images are shown above, one per organism.)*

---

## Figures S3–S17 & Table S1. Individual MD Trajectory Diagnostics, Per System (All 3 Replicates)

For every one of the 14 simulated systems, three per-run diagnostic panels are
available per replicate (produced by `md_analyze.py`, analysis conda env):
**(A)** protein backbone + ligand RMSD vs. time, **(B)** per-residue Cα RMSF
(production window, >5 ns), **(C)** ligand-contact persistence (% of production
frames within 4 Å, top 15 residues; apo has no ligand, so no contacts panel).
These are the per-replicate diagnostics underlying the main-text summary figures
(Table 5, Table 7, Figure 5, Figure 6, Figure 7).

> **Note on a fix applied while generating this SI set:** the original
> `md_analyze.py` had two bugs that would have produced misleading
> supplementary figures: (1) mdtraj's `"protein"` atom selector treats residue
> name `UNK` as a protein placeholder, so the ligand (also named `UNK` by
> OpenFF) was leaking into the protein-residue contact list, producing a
> spurious 100%-persistence "UNK1" self-contact bar on every contacts plot;
> (2) the ligand RMSD trace had no periodic-boundary unwrapping, so a ligand
> that crossed the box edge showed a spurious multi-Å "jump" that read as
> unbinding when it wasn't (confirmed on `gla_deprot_50ns`: apparent ligand
> RMSD 20.2 ± 29.5 Å and a false "drifted" flag before the fix, vs. 3.7 ± 0.6 Å
> and "bound" after — consistent with the independently-diagnosed COM-distance
> result in Figure S18). Both are fixed in the current `md_analyze.py`; all 43
> per-run figure sets (14 systems × 3 replicates, minus apo's contacts panel)
> were regenerated with the fix. This does **not** change any main-text
> number — the headline RMSD/MM-GBSA/contact values reported in the manuscript
> were computed by separate, already-PBC-corrected pipelines
> (`md_summary.py`, `md_contacts_pbc.py`, `md_mmgbsa*.py`, `md_figures.py`
> — the last of which built the actual main-text Figures 5/6 and already had
> both corrections from the start); it only affects the per-run SI diagnostic
> plots generated here.

### Table S1. Summary: mean +/- SD across n=3 replicates (this SI pipeline)

Protein backbone RMSD and ligand RMSD (PBC-corrected, production window >5 ns),
computed independently by `md_analyze.py` per replicate, then averaged as
**mean +/- SD across the 3 replicate means** (matching the manuscript's replicate-
statistics convention, Section 2.9). Protein-backbone values are an independent
cross-check on the main-text headline systems (Figure 13) and agree closely
(e.g. apo 2.12 +/- 0.15 A here vs. 2.12 +/- 0.33 A in Figure 13; EPA free acid
1.83 +/- 0.09 A here vs. 1.82 +/- 0.22 A there). **Ligand RMSD is a different metric**
from the main-text's ligand-to-pocket-centroid COM distance (Table 5/7/9) -- RMSD-to-t0
is sensitive to acyl-chain reorientation even while the ligand stays bound, so it runs
higher than COM distance; read it as a secondary stability check, not a replacement
for the main-text binding-retention numbers.

| System | Protein backbone RMSD, r1/r2/r3 (A) | mean +/- SD | Ligand RMSD, r1/r2/r3 (A) | mean +/- SD |
|---|---|---|---|---|
| EPA (free acid) | 1.87/1.91/1.70 | 1.83 +/- 0.09 | 2.47/2.23/3.17 | 2.62 +/- 0.40 |
| EPA (deprotonated carboxylate) | 1.82/1.61/2.19 | 1.87 +/- 0.24 | 3.12/3.59/3.00 | 3.23 +/- 0.25 |
| EPA (methyl ester) | 1.66/1.85/1.98 | 1.83 +/- 0.13 | 3.61/2.15/2.75 | 2.84 +/- 0.60 |
| GLA / gamma-linolenic acid (free acid) | 1.91/1.74/1.85 | 1.83 +/- 0.07 | 6.52/3.83/3.13 | 4.49 +/- 1.46 |
| GLA (deprotonated carboxylate) | 1.65/1.82/1.98 | 1.82 +/- 0.13 | 3.67/2.16/2.79 | 2.88 +/- 0.62 |
| GLA (methyl ester) | 2.13/2.28/1.78 | 2.06 +/- 0.21 | 4.48/4.76/5.78 | 5.01 +/- 0.56 |
| Palmitic acid (free acid) | 1.96/2.02/1.37 | 1.79 +/- 0.29 | 2.52/4.00/2.46 | 2.99 +/- 0.71 |
| Palmitic acid (deprotonated carboxylate) | 1.46/2.04/1.59 | 1.70 +/- 0.25 | 2.71/1.85/2.07 | 2.21 +/- 0.37 |
| Palmitic acid (methyl ester) | 2.32/1.65/1.68 | 1.88 +/- 0.31 | 3.30/3.08/4.33 | 3.57 +/- 0.54 |
| Palmitoleate -- native ligand, positive control | 1.64/1.58/1.49 | 1.57 +/- 0.06 | 3.11/3.55/3.33 | 3.33 +/- 0.18 |
| Glucose decoy -- docked (peripheral) start, negative control | 2.01/1.72/1.59 | 1.77 +/- 0.17 | 3.01/1.69/1.35 | 2.02 +/- 0.71 |
| Pentadecanal -- weak binder | 2.11/1.61/1.74 | 1.82 +/- 0.21 | 3.15/2.99/3.36 | 3.17 +/- 0.15 |
| Tridecanoic acid -- weak binder | 1.65/1.65/1.59 | 1.63 +/- 0.03 | 4.99/5.94/4.19 | 5.04 +/- 0.72 |
| Apo ToxT -- ligand-free baseline | 2.29/2.14/1.92 | 2.12 +/- 0.15 | n/a | n/a (no ligand) |

*(`glucose_core_50ns`, the core-seeded decoy control, is a single trajectory by
design -- no r2/r3 replicates exist for that variant; see main-text Figure 10 caption.)*

---

### Figure S3. EPA (free acid)

**Replicate 1 (`epa_50ns`)**

![](md/epa_50ns/analysis/rmsd.png)
![](md/epa_50ns/analysis/rmsf.png)
![](md/epa_50ns/analysis/contacts.png)

**Replicate 2 (`epa_50ns_r2`)**

![](md/epa_50ns_r2/analysis/rmsd.png)
![](md/epa_50ns_r2/analysis/rmsf.png)
![](md/epa_50ns_r2/analysis/contacts.png)

**Replicate 3 (`epa_50ns_r3`)**

![](md/epa_50ns_r3/analysis/rmsd.png)
![](md/epa_50ns_r3/analysis/rmsf.png)
![](md/epa_50ns_r3/analysis/contacts.png)

---

### Figure S4. EPA (deprotonated carboxylate)

**Replicate 1 (`epa_deprot_50ns`)**

![](md/epa_deprot_50ns/analysis/rmsd.png)
![](md/epa_deprot_50ns/analysis/rmsf.png)
![](md/epa_deprot_50ns/analysis/contacts.png)

**Replicate 2 (`epa_deprot_50ns_r2`)**

![](md/epa_deprot_50ns_r2/analysis/rmsd.png)
![](md/epa_deprot_50ns_r2/analysis/rmsf.png)
![](md/epa_deprot_50ns_r2/analysis/contacts.png)

**Replicate 3 (`epa_deprot_50ns_r3`)**

![](md/epa_deprot_50ns_r3/analysis/rmsd.png)
![](md/epa_deprot_50ns_r3/analysis/rmsf.png)
![](md/epa_deprot_50ns_r3/analysis/contacts.png)

---

### Figure S5. EPA (methyl ester)

**Replicate 1 (`methyl_epa_50ns`)**

![](md/methyl_epa_50ns/analysis/rmsd.png)
![](md/methyl_epa_50ns/analysis/rmsf.png)
![](md/methyl_epa_50ns/analysis/contacts.png)

**Replicate 2 (`methyl_epa_50ns_r2`)**

![](md/methyl_epa_50ns_r2/analysis/rmsd.png)
![](md/methyl_epa_50ns_r2/analysis/rmsf.png)
![](md/methyl_epa_50ns_r2/analysis/contacts.png)

**Replicate 3 (`methyl_epa_50ns_r3`)**

![](md/methyl_epa_50ns_r3/analysis/rmsd.png)
![](md/methyl_epa_50ns_r3/analysis/rmsf.png)
![](md/methyl_epa_50ns_r3/analysis/contacts.png)

---

### Figure S6. GLA / gamma-linolenic acid (free acid)

**Replicate 1 (`gla_50ns`)**

![](md/gla_50ns/analysis/rmsd.png)
![](md/gla_50ns/analysis/rmsf.png)
![](md/gla_50ns/analysis/contacts.png)

**Replicate 2 (`gla_50ns_r2`)**

![](md/gla_50ns_r2/analysis/rmsd.png)
![](md/gla_50ns_r2/analysis/rmsf.png)
![](md/gla_50ns_r2/analysis/contacts.png)

**Replicate 3 (`gla_50ns_r3`)**

![](md/gla_50ns_r3/analysis/rmsd.png)
![](md/gla_50ns_r3/analysis/rmsf.png)
![](md/gla_50ns_r3/analysis/contacts.png)

---

### Figure S7. GLA (deprotonated carboxylate)

**Replicate 1 (`gla_deprot_50ns`)**

![](md/gla_deprot_50ns/analysis/rmsd.png)
![](md/gla_deprot_50ns/analysis/rmsf.png)
![](md/gla_deprot_50ns/analysis/contacts.png)

**Replicate 2 (`gla_deprot_50ns_r2`)**

![](md/gla_deprot_50ns_r2/analysis/rmsd.png)
![](md/gla_deprot_50ns_r2/analysis/rmsf.png)
![](md/gla_deprot_50ns_r2/analysis/contacts.png)

**Replicate 3 (`gla_deprot_50ns_r3`)**

![](md/gla_deprot_50ns_r3/analysis/rmsd.png)
![](md/gla_deprot_50ns_r3/analysis/rmsf.png)
![](md/gla_deprot_50ns_r3/analysis/contacts.png)

---

### Figure S8. GLA (methyl ester)

**Replicate 1 (`gla_ester_50ns`)**

![](md/gla_ester_50ns/analysis/rmsd.png)
![](md/gla_ester_50ns/analysis/rmsf.png)
![](md/gla_ester_50ns/analysis/contacts.png)

**Replicate 2 (`gla_ester_50ns_r2`)**

![](md/gla_ester_50ns_r2/analysis/rmsd.png)
![](md/gla_ester_50ns_r2/analysis/rmsf.png)
![](md/gla_ester_50ns_r2/analysis/contacts.png)

**Replicate 3 (`gla_ester_50ns_r3`)**

![](md/gla_ester_50ns_r3/analysis/rmsd.png)
![](md/gla_ester_50ns_r3/analysis/rmsf.png)
![](md/gla_ester_50ns_r3/analysis/contacts.png)

---

### Figure S9. Palmitic acid (free acid)

**Replicate 1 (`palmitic_50ns`)**

![](md/palmitic_50ns/analysis/rmsd.png)
![](md/palmitic_50ns/analysis/rmsf.png)
![](md/palmitic_50ns/analysis/contacts.png)

**Replicate 2 (`palmitic_50ns_r2`)**

![](md/palmitic_50ns_r2/analysis/rmsd.png)
![](md/palmitic_50ns_r2/analysis/rmsf.png)
![](md/palmitic_50ns_r2/analysis/contacts.png)

**Replicate 3 (`palmitic_50ns_r3`)**

![](md/palmitic_50ns_r3/analysis/rmsd.png)
![](md/palmitic_50ns_r3/analysis/rmsf.png)
![](md/palmitic_50ns_r3/analysis/contacts.png)

---

### Figure S10. Palmitic acid (deprotonated carboxylate)

**Replicate 1 (`palmitic_deprot_50ns`)**

![](md/palmitic_deprot_50ns/analysis/rmsd.png)
![](md/palmitic_deprot_50ns/analysis/rmsf.png)
![](md/palmitic_deprot_50ns/analysis/contacts.png)

**Replicate 2 (`palmitic_deprot_50ns_r2`)**

![](md/palmitic_deprot_50ns_r2/analysis/rmsd.png)
![](md/palmitic_deprot_50ns_r2/analysis/rmsf.png)
![](md/palmitic_deprot_50ns_r2/analysis/contacts.png)

**Replicate 3 (`palmitic_deprot_50ns_r3`)**

![](md/palmitic_deprot_50ns_r3/analysis/rmsd.png)
![](md/palmitic_deprot_50ns_r3/analysis/rmsf.png)
![](md/palmitic_deprot_50ns_r3/analysis/contacts.png)

---

### Figure S11. Palmitic acid (methyl ester)

**Replicate 1 (`methyl_palmitate_50ns`)**

![](md/methyl_palmitate_50ns/analysis/rmsd.png)
![](md/methyl_palmitate_50ns/analysis/rmsf.png)
![](md/methyl_palmitate_50ns/analysis/contacts.png)

**Replicate 2 (`methyl_palmitate_50ns_r2`)**

![](md/methyl_palmitate_50ns_r2/analysis/rmsd.png)
![](md/methyl_palmitate_50ns_r2/analysis/rmsf.png)
![](md/methyl_palmitate_50ns_r2/analysis/contacts.png)

**Replicate 3 (`methyl_palmitate_50ns_r3`)**

![](md/methyl_palmitate_50ns_r3/analysis/rmsd.png)
![](md/methyl_palmitate_50ns_r3/analysis/rmsf.png)
![](md/methyl_palmitate_50ns_r3/analysis/contacts.png)

---

### Figure S12. Palmitoleate — native ligand, positive control

**Replicate 1 (`pam_50ns`)**

![](md/pam_50ns/analysis/rmsd.png)
![](md/pam_50ns/analysis/rmsf.png)
![](md/pam_50ns/analysis/contacts.png)

**Replicate 2 (`pam_50ns_r2`)**

![](md/pam_50ns_r2/analysis/rmsd.png)
![](md/pam_50ns_r2/analysis/rmsf.png)
![](md/pam_50ns_r2/analysis/contacts.png)

**Replicate 3 (`pam_50ns_r3`)**

![](md/pam_50ns_r3/analysis/rmsd.png)
![](md/pam_50ns_r3/analysis/rmsf.png)
![](md/pam_50ns_r3/analysis/contacts.png)

---

### Figure S13. Glucose decoy — docked (peripheral) start, negative control

**Replicate 1 (`glucose_decoy_50ns`)**

![](md/glucose_decoy_50ns/analysis/rmsd.png)
![](md/glucose_decoy_50ns/analysis/rmsf.png)
![](md/glucose_decoy_50ns/analysis/contacts.png)

**Replicate 2 (`glucose_decoy_50ns_r2`)**

![](md/glucose_decoy_50ns_r2/analysis/rmsd.png)
![](md/glucose_decoy_50ns_r2/analysis/rmsf.png)
![](md/glucose_decoy_50ns_r2/analysis/contacts.png)

**Replicate 3 (`glucose_decoy_50ns_r3`)**

![](md/glucose_decoy_50ns_r3/analysis/rmsd.png)
![](md/glucose_decoy_50ns_r3/analysis/rmsf.png)
![](md/glucose_decoy_50ns_r3/analysis/contacts.png)

---

### Figure S14. Pentadecanal — weak binder

**Replicate 1 (`pentadecanal_50ns`)**

![](md/pentadecanal_50ns/analysis/rmsd.png)
![](md/pentadecanal_50ns/analysis/rmsf.png)
![](md/pentadecanal_50ns/analysis/contacts.png)

**Replicate 2 (`pentadecanal_50ns_r2`)**

![](md/pentadecanal_50ns_r2/analysis/rmsd.png)
![](md/pentadecanal_50ns_r2/analysis/rmsf.png)
![](md/pentadecanal_50ns_r2/analysis/contacts.png)

**Replicate 3 (`pentadecanal_50ns_r3`)**

![](md/pentadecanal_50ns_r3/analysis/rmsd.png)
![](md/pentadecanal_50ns_r3/analysis/rmsf.png)
![](md/pentadecanal_50ns_r3/analysis/contacts.png)

---

### Figure S15. Tridecanoic acid — weak binder

**Replicate 1 (`tridecanoic_50ns`)**

![](md/tridecanoic_50ns/analysis/rmsd.png)
![](md/tridecanoic_50ns/analysis/rmsf.png)
![](md/tridecanoic_50ns/analysis/contacts.png)

**Replicate 2 (`tridecanoic_50ns_r2`)**

![](md/tridecanoic_50ns_r2/analysis/rmsd.png)
![](md/tridecanoic_50ns_r2/analysis/rmsf.png)
![](md/tridecanoic_50ns_r2/analysis/contacts.png)

**Replicate 3 (`tridecanoic_50ns_r3`)**

![](md/tridecanoic_50ns_r3/analysis/rmsd.png)
![](md/tridecanoic_50ns_r3/analysis/rmsf.png)
![](md/tridecanoic_50ns_r3/analysis/contacts.png)

---

### Figure S16. Apo ToxT — ligand-free baseline

**Replicate 1 (`apo_toxt_50ns`)**

![](md/apo_toxt_50ns/analysis/rmsd.png)
![](md/apo_toxt_50ns/analysis/rmsf.png)

**Replicate 2 (`apo_toxt_50ns_r2`)**

![](md/apo_toxt_50ns_r2/analysis/rmsd.png)
![](md/apo_toxt_50ns_r2/analysis/rmsf.png)

**Replicate 3 (`apo_toxt_50ns_r3`)**

![](md/apo_toxt_50ns_r3/analysis/rmsd.png)
![](md/apo_toxt_50ns_r3/analysis/rmsf.png)

---

### Figure S17. Glucose decoy — seeded in pocket core, kinetic-trapping control (single trajectory)

![](md/glucose_core_50ns/analysis/rmsd.png)
![](md/glucose_core_50ns/analysis/rmsf.png)
![](md/glucose_core_50ns/analysis/contacts.png)

*(No r2/r3 -- single trajectory by design, see note above.)*

## Figures S18–S19. GLA Carboxylate GB-Variance Diagnostic

Referenced from main-text Section 3.11 as **"(Figure S18)"**. Shows
ligand-COM → pocket-centroid and carboxylate-C → pocket-centroid distance over
the trajectory, for all three independent-seed replicates of
`gla_deprot_50ns`. Demonstrates the pose stays bound (COM 1.7–1.9 Å mean) in
every replicate while the carboxylate head group is consistently
solvent-exposed (~7.2–7.4 Å) — the structural basis for the large
single-trajectory MM-GBSA variance (±20.5 kcal/mol on rep 1 alone) resolving to
±5.9 kcal/mol once averaged across replicates (Table 9).

**Figure S18.** GLA carboxylate ligand/head-group retention diagnostic, all 3 replicates.

![GLA carboxylate retention, r1](figures/gla_carboxylate_retention.png)
![GLA carboxylate retention, r2](figures/gla_carboxylate_retention_r2.png)
![GLA carboxylate retention, r3](figures/gla_carboxylate_retention_r3.png)

**Figure S19.** GLA free-acid replicate check — the earlier replicate-noise-vs-drift
diagnostic that motivated Figure S18 before it was extended to the carboxylate form.

![GLA free-acid replicate check](figures/gla_freeacid_replicate_check.png)

---

## Figure S20. Blind-docking pose galleries (whole-protein search)

Referenced from main-text Section 3.9 / Table 6. Every Vina binding mode
(model) for each of the 5 whole-protein blind-docked ligands, rendered on
the full ToxT structure. Blue = pose centre of mass within 8 A of the
crystallographic pocket centroid (PAM reference, Methods 2.10, "in
pocket"); red = outside that threshold. Pose counts match Table 6 exactly.

**EPA -- 15/15 in pocket**

![EPA blind docking poses](figures/si_blind/cis_5_8_11_14_17_eicosapentaenoic_acid_blind_poses.png)

**gamma-linolenic acid -- 8/8 in pocket**

![gamma-linolenic acid blind docking poses](figures/si_blind/gamma_linolenic_acid_blind_poses.png)

**palmitic acid -- 1/20 in pocket**

![palmitic acid blind docking poses](figures/si_blind/palmitic_acid_blind_poses.png)

**palmitoleate (native) -- 10/13 in pocket**

![palmitoleate (native) blind docking poses](figures/si_blind/palmitoleic_acid_blind_poses.png)

**glucose (decoy) -- 0/20 in pocket**

![glucose (decoy) blind docking poses](figures/si_blind/glucose_blind_poses.png)

---

## Figure S21. Individual Vinardo-scored docking poses (22 lipids)

Referenced from main-text Section 3.6 / Figure 3 (consensus scoring).
Same rendering convention as Figures S1/S2 (cyan/green pose vs. yellow
native ligand, pocket residues coloured by chemistry) but for the
re-docked Vinardo top pose of each of the 22 panel lipids, rather than
the default-Vina pose. Ranked by Vina affinity for consistency with
Figures S1/S2 (organism-agnostic panel, matches Table 3 ranking).

**cis 5 8 11 14 17 eicosapentaenoic acid -- Vina -8.78 / Vinardo -8.41 kcal/mol**

![cis 5 8 11 14 17 eicosapentaenoic acid Vinardo pose](figures/si_vinardo/cis_5_8_11_14_17_eicosapentaenoic_acid.png)

**methyl cis 5 8 11 14 17 eicosapntaenoate -- Vina -8.48 / Vinardo -8.37 kcal/mol**

![methyl cis 5 8 11 14 17 eicosapntaenoate Vinardo pose](figures/si_vinardo/methyl_cis_5_8_11_14_17_eicosapntaenoate.png)

**methyl 4 7 10 13 hexadecatetraenoate -- Vina -8.46 / Vinardo -8.19 kcal/mol**

![methyl 4 7 10 13 hexadecatetraenoate Vinardo pose](figures/si_vinardo/methyl_4_7_10_13_hexadecatetraenoate.png)

**gamma linolenic acid -- Vina -8.12 / Vinardo -8.25 kcal/mol**

![gamma linolenic acid Vinardo pose](figures/si_vinardo/gamma_linolenic_acid.png)

**neophytadiene -- Vina -8.12 / Vinardo -8.16 kcal/mol**

![neophytadiene Vinardo pose](figures/si_vinardo/neophytadiene.png)

**methyl 3 cis 9 cis 12 cis octadecatrienoate -- Vina -7.97 / Vinardo -8.02 kcal/mol**

![methyl 3 cis 9 cis 12 cis octadecatrienoate Vinardo pose](figures/si_vinardo/methyl_3_cis_9_cis_12_cis_octadecatrienoate.png)

**9 12 15 octadecatrienoic acid -- Vina -7.91 / Vinardo -8.21 kcal/mol**

![9 12 15 octadecatrienoic acid Vinardo pose](figures/si_vinardo/9_12_15_octadecatrienoic_acid.png)

**methyl heneicosanoate -- Vina -7.84 / Vinardo -7.19 kcal/mol**

![methyl heneicosanoate Vinardo pose](figures/si_vinardo/methyl_heneicosanoate.png)

**cis 10 heptadecenoic acid -- Vina -7.81 / Vinardo -7.75 kcal/mol**

![cis 10 heptadecenoic acid Vinardo pose](figures/si_vinardo/cis_10_heptadecenoic_acid.png)

**9 11 ooctadecadienoic acid -- Vina -7.80 / Vinardo -7.92 kcal/mol**

![9 11 ooctadecadienoic acid Vinardo pose](figures/si_vinardo/9_11_ooctadecadienoic_acid.png)

**methyl palmitoleate -- Vina -7.72 / Vinardo -7.46 kcal/mol**

![methyl palmitoleate Vinardo pose](figures/si_vinardo/methyl_palmitoleate.png)

**heptadecanoic acid -- Vina -7.68 / Vinardo -7.84 kcal/mol**

![heptadecanoic acid Vinardo pose](figures/si_vinardo/heptadecanoic_acid.png)

**stearic acid -- Vina -7.63 / Vinardo -7.79 kcal/mol**

![stearic acid Vinardo pose](figures/si_vinardo/stearic_acid.png)

**methyl heptadecanoate -- Vina -7.57 / Vinardo -7.28 kcal/mol**

![methyl heptadecanoate Vinardo pose](figures/si_vinardo/methyl_heptadecanoate.png)

**methyl stearate -- Vina -7.57 / Vinardo -7.21 kcal/mol**

![methyl stearate Vinardo pose](figures/si_vinardo/methyl_stearate.png)

**methyl palmitate -- Vina -7.48 / Vinardo -7.33 kcal/mol**

![methyl palmitate Vinardo pose](figures/si_vinardo/methyl_palmitate.png)

**methyl 18 fluorostearate -- Vina -7.38 / Vinardo -7.12 kcal/mol**

![methyl 18 fluorostearate Vinardo pose](figures/si_vinardo/methyl_18_fluorostearate.png)

**palmitic acid -- Vina -7.32 / Vinardo -7.69 kcal/mol**

![palmitic acid Vinardo pose](figures/si_vinardo/palmitic_acid.png)

**methyl myristate -- Vina -7.31 / Vinardo -7.11 kcal/mol**

![methyl myristate Vinardo pose](figures/si_vinardo/methyl_myristate.png)

**methyl pentadecanoate -- Vina -7.18 / Vinardo -7.40 kcal/mol**

![methyl pentadecanoate Vinardo pose](figures/si_vinardo/methyl_pentadecanoate.png)

**pentadecanal -- Vina -6.90 / Vinardo -7.30 kcal/mol**

![pentadecanal Vinardo pose](figures/si_vinardo/pentadecanal.png)

**tridecanoic acid -- Vina -6.84 / Vinardo -6.93 kcal/mol**

![tridecanoic acid Vinardo pose](figures/si_vinardo/tridecanoic_acid.png)

---

## Section S.13 / Figure S22 / Table S11. ToxT–*ctxAB* promoter models on the native El Tor sequence: AlphaFold3 and Chai-1

To probe how fatty-acid binding relates to virulence-gene activation, a ToxT–DNA complex was modelled independently with **AlphaFold3** and with **Chai-1**, both using the full-length ToxT sequence and the **native El Tor *ctxAB* promoter duplex** (Methods 2.12). Protein–DNA interactions for both models were profiled with **PLIP 3.0.1** (default automatic ligand detection, which identifies hydrogen bonds, salt bridges and hydrophobic contacts from bond geometry rather than a distance cutoff).

**DNA sequence and its provenance.** The duplex used is the 36-bp region spanning positions −76 to −41 of the *ctxAB* promoter:

```
top:    TTTTGATTTTTGATTTTTGATTTCAAATAATACAAA
bottom: TTTGTATTATTTGAAATCAAAAATCAAAAATCAAAA
```

This was transcribed from Dittmer & Withey (2012, *J Bacteriol* 194:5255–5263, Figure 1) and verified three independent ways before use: the `GATTTTT` heptad-repeat count of the parent classical O395 footprint region (6, matching the paper's stated count), the total span length of that region (69 bp, matching the stated −109..−41 span), and the presence of the literal substring `ATTTCAAAT` which the paper gives independently for positions −58..−49. The 36-bp El Tor-relevant subset above was extracted from that verified region: El Tor strains carry only the three promoter-proximal heptad repeats but otherwise share O395's *PctxAB* sequence, and this fragment matches the paper's `pJW211` construct, shown there to be fully ToxT-activated. It spans both experimentally mapped functional toxboxes (toxbox 1, −72..−60, strong copper-phenanthroline footprint; toxbox 2, −58..−46, weaker footprint). The two strands were confirmed to be exact reverse complements, and **both** submitted jobs' own recorded/returned sequences were checked byte-for-byte against these strings before any analysis — protein and DNA exact matches confirmed for both the AlphaFold3 job (via its `job_request.json`) and the Chai-1 job (via the chains extracted from `pred.rank_0.cif`).

**Confidence metrics (Table S11).** AlphaFold3 predicted the ToxT fold with high confidence (chain-A pTM 0.86; overall pTM 0.79) and a modest interface (ipTM 0.48). Chai-1 predicted a **markedly more confident interface** — ipTM 0.671 (aggregate score 0.685) — approaching, though not conclusively reaching, the ~0.7–0.8 range conventionally read as a confident interface. Both tools' top-two-of-five ranked models were near-identical to each other (AlphaFold3: ipTM 0.480/0.480; Chai-1: ipTM 0.671/0.667), indicating convergence rather than a single favourable pose in either case. Neither tool reported a clash.

**Table S11. Confidence metrics, all five ranked models, AlphaFold3 and Chai-1 (same native El Tor DNA input).**

*AlphaFold3:*

| Model | Ranking score | Interface ipTM | pTM | Clash |
|---|---|---|---|---|
| model_0 (analysed) | 0.540 | 0.480 | 0.790 | none |
| model_1 | 0.540 | 0.480 | 0.790 | none |
| model_2 | 0.500 | 0.430 | 0.770 | none |
| model_3 | 0.410 | 0.330 | 0.760 | none |
| model_4 | 0.270 | 0.150 | 0.710 | none |

*Chai-1:*

| Model | Aggregate score | Interface ipTM | ptm | Clash |
|---|---|---|---|---|
| rank_0 (analysed) | 0.685 | 0.671 | 0.744 | none |
| rank_1 | 0.682 | 0.667 | 0.740 | none |
| rank_2 | 0.678 | 0.663 | 0.738 | none |
| rank_3 | 0.631 | 0.622 | 0.668 | none |
| rank_4 | 0.630 | 0.621 | 0.664 | none |

**Where DNA contacts the protein.** Both tools independently place the DNA on the **C-terminal AraC-family helix–turn–helix domain**, away from the N-terminal fatty-acid pocket (Figure S22). AlphaFold3: all 26 residues within 5 Å of DNA fall in the range 188–276, none outside it. Chai-1: 24 of 27 residues within 5 Å fall in the same range; the remaining three (Asn185, Trp186, Arg187) sit immediately adjacent to the 188 domain boundary rather than in the fatty-acid pocket itself — a minor boundary effect, not a contradiction of the domain-separation observation. Neither tool places any fatty-acid pocket residue in contact with DNA. PLIP's bond-level profiling agrees for both: AlphaFold3 finds 21 interactions (12 H-bonds, 7 salt bridges, 2 hydrophobic) over 15 residues, all within the HTH domain; Chai-1 finds 20 interactions (14 H-bonds, 4 salt bridges, 2 hydrophobic) over 11 residues, 10 of which are within the HTH domain (the eleventh, Arg187, is the same boundary-adjacent residue noted above). Contact residues largely overlap between tools (e.g. Lys203, Arg214, Asn218, Ser249, Tyr250, Ser264 identified by both). This places the regulatory pocket and the DNA-reading head on structurally distinct domains in two independent structure-prediction methods, consistent with the domain-separated architecture described by Lowden et al. (2010) — the structural basis cited in the main-text Discussion for why fatty-acid occupancy is unlikely to block DNA binding sterically — and is independently corroborated by the main-text apo/holo RMSF analysis (Section 3.8), which probed this same C-terminal region.

We present this as an exploratory structural check, not an established result: even Chai-1's higher interface confidence does not conclusively clear a confident threshold, and neither model should be read as a validated ToxT–DNA binding geometry. Additional caveats apply regardless of sequence accuracy or which tool is used: the duplex is a 36-bp fragment modelled in isolation, without flanking genomic context, RNA polymerase, or H-NS (which also binds this A/T-rich region and represses *ctxAB*), and the fatty acid is not co-modelled — the native ligand shown in Figure S22 is placed by superposition of the 3GBG crystal structure, not predicted in complex with the DNA. The domain-level observation is in any case independently grounded in the known ToxT domain architecture (Lowden et al., 2010; main-text Discussion), which does not depend on either model.

![Figure S22A](figures/fig_eltor_dna_competition.png)
![Figure S22B](figures/fig_eltor_chai_dna_competition.png)

**Figure S22.** Independent models of ToxT bound to the native El Tor *ctxAB* promoter duplex (−76 to −41): DNA (teal), the C-terminal HTH DNA-binding domain (blue, residues 188–276), and the N-terminal domain (orange) carrying the fatty-acid pocket, with the native ligand (yellow, positioned by 3GBG superposition). Red dashes mark the separation between the fatty-acid pocket and the nearest DNA phosphate. **(A)** AlphaFold3 (chain-A pTM 0.86; interface ipTM 0.48). **(B)** Chai-1 (ptm 0.74; interface ipTM 0.671). Both place all DNA contacts in the C-terminal domain, none in the fatty-acid pocket, despite different underlying methods.

---

## Section S.14 / Figure S23 / Table S10. Inter-domain hinge-angle analysis: a direct, null test of the allosteric-restraint hypothesis

The apo-vs-holo RMSF comparison (main text Section 3.8, Figure 14) found no *domain-specific* rigidification (C-terminal HTH domain −0.16 Å vs. rest of protein −0.12 Å) — but RMSF only measures local fluctuation amplitude, not whether the two domains move in a coordinated, restrained way relative to each other, which is what the allosteric hypothesis actually claims. We therefore ran a more direct test on the same trajectories: the relative geometry between the N-terminal pocket domain and the C-terminal HTH domain (residues 188–273), for apo ToxT and the three headline free-acid holo systems (EPA, γ-linolenic acid, palmitic acid; n = 3 independent-seed 50 ns replicates each, production window >5 ns).

**Method.** Each trajectory was superposed on its own frame 0 using only the N-terminal domain Cα atoms (residues ≤187) as the alignment reference, isolating true inter-domain motion from whole-molecule translation/rotation. Per frame we computed (i) the centroid–centroid distance between the N-domain and HTH-domain Cα atoms, and (ii) the hinge angle at the domain-boundary residue (Cα of residue 188) between vectors to each domain centroid — the standard "elbow angle" construction used for other hinged multi-domain proteins. Per replicate we report the frame-level mean (average relative geometry) and SD (the direct restraint readout: a narrower per-replicate SD in holo than apo would indicate occupancy restrains inter-domain motion, not just local jitter). Apo (n=3 replicate values) was compared against each holo system (n=3 replicate values) by Welch's t-test on both the mean angle and the within-replicate SD, matching the paper's existing replicate-level statistical convention; with n=3 per group these should be read as indicative, not confirmatory.

**Result: no ligand-dependent inter-domain restraint was detected.** Centroid–centroid distance was essentially identical across all four systems (apo 19.1 ± 0.2 Å; EPA 19.2 ± 0.1; GLA 19.3 ± 0.3; palmitic 19.4 ± 0.3 Å). The mean hinge angle did not shift with ligand binding for any system (apo 36.4 ± 1.1°; EPA 36.3 ± 1.1°, p = 0.95; GLA 36.5 ± 1.0°, p = 0.91; palmitic 37.1 ± 0.9°, p = 0.43). The within-replicate angular SD — the direct restraint metric — was unchanged for both strong binders (EPA 1.32 ± 0.18° vs. apo 1.34 ± 0.16°, p = 0.87; GLA 1.22 ± 0.15°, p = 0.37) and only nominally narrower for the weak binder palmitic acid (0.97 ± 0.07°, p = 0.041; Table S10, Figure S23). We do not read this single marginal result as evidence of restraint: if pocket occupancy were driving an affinity-dependent allosteric effect, the two strong binders (EPA, GLA) — not the weak one — would be expected to show it most clearly; the observed pattern runs the opposite way, consistent with a false positive among three comparisons at n = 3.

**Interpretation.** This is a second, independent null result (alongside the RMSF domain-specificity test), obtained with a metric that measures the specific geometric quantity the allosteric hypothesis is about rather than a generic proxy for it. It does not contradict the structural fact that the fatty-acid pocket and the DNA-binding HTH domain sit on separate domains (Lowden et al., 2010) — that observation stands independently of this analysis — but it means we have no positive dynamical evidence, at the 50 ns/replicate timescale sampled here, that ligand occupancy constrains the relative motion of the two domains. Domain-hinge motions in multidomain proteins can occur on slower timescales than 50 ns, so this null result does not rule out the mechanism; it means our data neither support nor refute it beyond the static domain-separation argument.

![Figure S23](figures/fig_interdomain_hinge.png)

**Figure S23.** Inter-domain hinge angle (N-domain centroid — residue 188 Cα — HTH-domain centroid), pooled production frames, apo vs. the three headline holo systems (n = 3 replicates each). Distributions are visually and statistically indistinguishable between apo and the two strong binders (EPA, GLA); see Table S10 for replicate-level statistics.

**Table S10. Inter-domain hinge-angle summary, per system (n = 3 replicates; `interdomain_hinge_summary.csv`).**

| System | Mean hinge angle (deg) | Within-replicate SD (deg) | COM–COM distance (Å) | *p* vs. apo (mean) | *p* vs. apo (SD) |
|---|---|---|---|---|---|
| apo | 36.4 ± 1.1 | 1.34 ± 0.16 | 19.1 ± 0.2 | — | — |
| EPA (free acid) | 36.3 ± 1.1 | 1.32 ± 0.18 | 19.2 ± 0.1 | 0.954 | 0.870 |
| γ-linolenic acid (free acid) | 36.5 ± 1.0 | 1.22 ± 0.15 | 19.3 ± 0.3 | 0.905 | 0.368 |
| palmitic acid (free acid) | 37.1 ± 0.9 | 0.97 ± 0.07 | 19.4 ± 0.3 | 0.433 | 0.041 |

---

## Tables S2–S9. Supplementary Data Tables

Full machine-readable versions of every results table (main-text tables show
selected/ranked subsets); provided as CSV alongside this document.

| Table | File | Rows | Content |
|---|---|---|---|
| Table S2 | `results_CV/affinities_CV.csv` | 15 | Full CV panel docking affinities (source for Table 1) |
| Table S3 | `results_CCM/affinities_CCM.csv` | 13 | Full CCM panel docking affinities (source for Table 2) |
| Table S4 | `results_blind/blind_dock_summary.csv` | 4 | Blind-docking summary, all poses per ligand (source for Table 6) |
| Table S5 | `results_vinardo/consensus.csv` | 22 | Vina vs. Vinardo affinity per ligand, all 22 (source for Fig. 3 / Section 3.6) |
| Table S6 | `results_benchmark/benchmark.csv` | 3 | Virstatin / butyrate / oleic acid reference docking (source for Table 8) |
| Table S7 | `results_pairs/pairs_CV.csv`, `pairs_CCM.csv` | 11 + 10 | Acid vs. methyl-ester paired affinities, per organism (source for Table 4) |
| Table S8 | `results_batch/structure_property.csv` | 22 | Full descriptor set (C count, C=C, MW, logP, TPSA, rotatable bonds) per ligand (source for Table 3) |
| Table S9 | `results_mmgbsa/mmgbsa_n3_headline.csv`, `mmgbsa_n3_remaining.csv` | 3 + 10 | Per-replicate MM-GBSA raw values, all 13 systems (source for Table 9) |

---

## Remaining Open Items

Honest accounting of what this SI draft does **not** yet contain:

*(As of 2026-08-26: none. The previously-listed item — author-supplied CV/CCM
strain designations and GC-MS methodological details — was resolved on
2026-08-25/26 (`MANUSCRIPT_TODO_reps.md` item 7, now fully closed) and does
not require any mirrored detail here; the SI's own content was unaffected.)*

*(Resolved since the previous revision: figure/table numbers are finalised —
Figures S1–S23, Tables S1–S9, cross-referenced in the index above — and the
main manuscript's in-text SI citation reads "(Figure S18)" instead of the
generic "(SI)". A `.docx` export of this document (`SUPPLEMENTARY.docx`) is
generated by `build_supplementary_docx.js`. Full blind-docking pose galleries
(Figure S20, `render_si_blind_docking_gallery.py`), the Vinardo individual
pose gallery (Figure S21, `render_si_vinardo_gallery.py`), and the AlphaFold3
PAE/pLDDT confidence plot (Figure S22, `make_af3_confidence_fig.py`,
cross-validated against the raw AF3 JSON output — chain-A pTM 0.85 and
complex ipTM 0.31 match the main text exactly) are now all included. All
content and scripts are committed to git.)*

*(This revision: the former main-text Section 3.13 / Figure 11 — the
AlphaFold3 ToxT–DNA complex — was moved here in full as Section S.13 /
Figure S23, because its protein–DNA interface confidence (ipTM 0.31) reads
better as a supplementary exploratory check than a main-text finding. The
main manuscript (Abstract, Introduction, Sections 2.11/3.8, Discussion,
Limitations) was updated to reference it as such. No figure file was moved
or renamed on disk (`figures/fig11_dna_competition.png` is unchanged); only
its manuscript section and figure number changed.)*

*(Also this revision: added Section S.14 / Figure S23 / Table S10, a new
inter-domain hinge-angle analysis (`make_interdomain_hinge_analysis.py`,
run on the existing apo + EPA/GLA/palmitic free-acid trajectories, `analysis`
conda env) designed as a more direct test of the allosteric-restraint
hypothesis than the existing RMSF comparison. It returned a null result: no
ligand-dependent shift or narrowing of the inter-domain hinge angle for
either strong binder (EPA, GLA); the one nominally significant value
(palmitic acid, the weak binder, p=0.041 on the SD) runs the wrong
direction for the hypothesis and is presented as a likely false positive,
not a finding. This is supplementary-only — not referenced anywhere in the
main manuscript — added as an additional honest caveat alongside Section
S.13, at the user's request. See that section's Interpretation paragraph
for why this doesn't rule the mechanism out, just fails to detect it at the
50 ns/replicate timescale sampled.)*

*(2026-08-27, first pass: de-escalated the allosteric-mechanism discussion
throughout the main manuscript (Abstract, Introduction aims, Section 3.8,
Discussion, both Limitations bullets) to keep only the one citable fact —
the fatty-acid pocket and DNA-binding domain are structurally separate
(Lowden et al., 2010) — without arguing that this paper's own (largely
null) evidence establishes an allosteric mechanism for these specific
lipids. Also added a Chai-1 monomer ToxT–DNA model alongside a second
AlphaFold3 attempt (same DNA input, different seed), with PLIP-based
interaction profiling for both, as a then-new Section S.15 supplementing
the original Section S.13 AlphaFold3 model. Superseded by the note
immediately below within the same day.)*

*(2026-08-27, second pass, same day: an inaccuracy in the first pass was
caught and corrected. Checking git history (`418e872`) and the actual FASTA
files established that the native El Tor *ctxAB* promoter sequence was never
"unavailable" — it had been transcribed from Dittmer & Withey (2012) and
verified three ways on 2026-08-19, then simply never submitted to any
prediction tool. Every ToxT–DNA model produced up to that point — the
2026-07-13 AlphaFold3 run, the AlphaFold3 rerun, and the Chai-1 run — had
used a synthetic consensus placeholder duplex with no biological
relationship to the study organism. Because that makes those runs
uninformative for this manuscript's purpose regardless of how they compare
to one another, all three were discarded rather than reported.)*

*(2026-08-27, third pass, same day: AlphaFold3 was re-run on the verified
native El Tor promoter duplex, and Section S.13 was rewritten around that
model alone. The submitted job's own recorded input (`job_request.json`)
was checked programmatically against the intended sequences before any
analysis: protein exact match (276 aa), both DNA strands exact match, true
reverse complements, paper landmark substring `ATTTCAAAT` present, and
confirmed not the placeholder. Results: chain-A pTM 0.86 / overall pTM 0.79
/ ipTM 0.48 — the highest interface confidence of any ToxT–DNA run in this
project, with the top two of five ranked models returning identical scores
(convergence rather than a single favourable pose), no clashes, and all 26
DNA-contacting residues (and all 15 PLIP-detected bonding residues) falling
within the C-terminal HTH domain, none in the fatty-acid pocket. Figure S22
is now a single panel (`figures/fig_eltor_dna_competition.png`) and Table
S11 reports confidence metrics for all five ranked models. Raw AlphaFold3
output for this run is archived in `af3_toxt_dna_eltor/`. Superseded assets from the discarded
placeholder runs were removed: `figures/fig_af3_rerun_dna_competition.png`
and `figures/fig_chai_dna_competition.png` were deleted (never committed),
while `figures/fig11_dna_competition.png` and `figures/af3_pae_plddt.png`
remain in git history from earlier commits but are no longer referenced by
any current section. Figure and table numbering is unchanged
from the second pass (Figures S1–S23, Tables S1–S11).)*

*(2026-08-31: Chai-1's server came back online; the user ran it on the same
verified native El Tor sequence and returned the results. Verified
independently before any analysis — extracted the actual chain sequences
from the returned `pred.rank_0.cif` via PyMOL (not assumed from the job
submission) and confirmed byte-for-byte: protein exact match (276 aa), both
DNA strands exact match, true reverse complements, `ATTTCAAAT` landmark
present, confirmed not the placeholder. Result: Chai-1's interface
confidence (ipTM 0.671, aggregate 0.685) is markedly higher than
AlphaFold3's on the same input (ipTM 0.48) — the best ToxT–DNA interface
confidence obtained in this project, though still short of a conclusively
confident threshold. Domain-level placement agrees closely with AlphaFold3:
24 of 27 Chai-1 contact residues fall in the C-terminal HTH domain (188–276),
the remaining three sitting immediately adjacent to the domain boundary
(185–187) rather than in the fatty-acid pocket; PLIP finds 20 interactions
(14 H-bonds, 4 salt bridges, 2 hydrophobic) across 11 residues, 10 of which
are in the HTH domain. Section S.13 rewritten to present both models
together (Table S11 now has two panels, Figure S22 now has two panels).
Rendered `figures/fig_eltor_chai_dna_competition.png` in the same style as
the AlphaFold3 figure. Raw Chai-1 output (top-ranked model + all five
scores.rank_N.json files) archived in `chai_toxt_dna_eltor/`. Methods 2.12,
the Results pointer, Discussion, and Limitations updated in both
`MANUSCRIPT_DRAFT.md` and `build_docx.js` to describe both models. Figure
and table numbering unchanged (still S1–S23, S1–S11) since this extends
existing Figure S22/Table S11 with panels rather than adding new ones.)*
