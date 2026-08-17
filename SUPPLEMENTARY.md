# Supplementary Information

**Locking Down ToxT: Microalgal Lipids as Allosteric Antivirulence Agents Against
*Vibrio cholerae* — A Docking and Molecular Dynamics Study**

*Draft — supplementary figures and tables supporting the main manuscript
(`MANUSCRIPT_DRAFT.md`). Figures are numbered S1–S19 and tables S1–S9, in the
order they appear below; the single in-text SI citation in the main manuscript
(Section 3.11, MM-GBSA) now points to Figure S18 by number.*

---

## Contents

**Figures:**
[S1](#figure-s1-individual-docking-poses--cv-panel-15-lipids) (CV docking poses) ·
[S2](#figure-s2-individual-docking-poses--ccm-panel-13-lipids) (CCM docking poses) ·
[S3–S17](#figures-s3s17--table-s1-individual-md-trajectory-diagnostics-per-system-all-3-replicates) (per-system MD diagnostics, r1–r3) ·
[S18–S19](#figures-s18s19-gla-carboxylate-gb-variance-diagnostic) (GLA carboxylate GB-variance diagnostic)

**Tables:**
[S1](#table-s1-summary-mean--sd-across-n3-replicates-this-si-pipeline) (replicate MD summary, mean ± SD) ·
[S2–S9](#tables-s2s9-supplementary-data-tables) (full docking/MM-GBSA result CSVs)

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
| Table S1 | Per-system MD replicate summary, mean ± SD (this SI pipeline) | independent cross-check on Figure 13 |
| Table S2 | Full CV panel docking affinities (15) | source for Table 1 |
| Table S3 | Full CCM panel docking affinities (13) | source for Table 2 |
| Table S4 | Blind-docking summary, all poses per ligand | source for Table 6 |
| Table S5 | Vina vs. Vinardo affinity, all 22 ligands | source for Figure 3, Section 3.6 |
| Table S6 | Reference ligand docking (virstatin/butyrate/oleic acid) | source for Table 8 |
| Table S7 | Acid vs. methyl-ester paired affinities, both organisms | source for Table 4 |
| Table S8 | Full descriptor set, all 22 ligands | source for Table 3 |
| Table S9 | Per-replicate MM-GBSA raw values, all 13 systems | source for Table 9 |

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

1. **Full blind-docking pose-by-pose detail** — Table 6 in the main text
   reports summary statistics (mode counts, top-pose distance); the SI could
   additionally show each of the individual poses (up to 20 per ligand) for
   the 5 blind-docked compounds, which isn't generated yet.
2. **No consensus-scoring (Vinardo) individual pose images** — Figures S1/S2
   render the default-Vina top pose only; a parallel gallery from
   `results_vinardo/*.pdbqt` doesn't exist yet (likely low priority — the
   pose itself rarely differs meaningfully between scoring functions, only
   the ranking).
3. **AlphaFold3 ToxT–DNA model — no dedicated SI figure beyond main-text
   Figure 11.** Could add the raw AF3 confidence plots (PAE/pLDDT) as SI if
   the journal wants the modelling evidence shown explicitly rather than
   just cited by pTM/ipTM numbers.
4. **Author-supplied content still outstanding independent of this SI**
   (carried over from `MANUSCRIPT_TODO_reps.md` item 7): the CV/CCM strain
   culture-collection accession numbers and GC-MS methodological details are
   still placeholders in the main manuscript — once filled in there, check
   whether anything here in the SI needs the same detail (e.g., a
   methods-recap sentence).

*(Resolved since the previous revision: figure/table numbers are now
finalised — Figures S1–S19, Tables S1–S9, cross-referenced in the index above
— and the main manuscript's in-text SI citation now reads "(Figure S18)"
instead of the generic "(SI)". A `.docx` export of this document
(`SUPPLEMENTARY.docx`) is now also generated by `build_supplementary_docx.js`.
All content and scripts are committed to git.)*
