# Molecular docking of *Chlorella* (CV) and *Chlorococcum* (CCM) lipids against the *Vibrio cholerae* virulence regulator ToxT

*Working manuscript draft — computational (docking) component. Generated for internal review prior to molecular-dynamics work. Species names (CV, CCM) and experimental/GC-MS details are placeholders to be completed by the authors.*

---

## Abstract

The transcriptional activator ToxT is the master regulator of virulence-gene expression in *Vibrio cholerae*, and its activity is directly modulated by fatty acids that occupy a hydrophobic binding pocket (Lowden et al., 2010). We previously observed antivirulence activity of lipid extracts from two green microalgae, here abbreviated CV and CCM. To test whether direct ToxT binding could underlie this activity, we performed molecular docking of the lipid species identified in each extract against the ToxT crystal structure (PDB 3GBG). A panel of 22 unique lipids (15 from CV, 13 from CCM, 6 shared) was docked with AutoDock Vina 1.2.7 into the experimentally defined fatty-acid pocket. The protocol was validated by redocking the co-crystallized fatty acid (palmitoleate), which reproduced the crystallographic pose to **1.41 Å RMSD**; blind docking over the whole protein independently recovered the native site (0.6 Å) and identified the fatty-acid pocket as the preferred binding site, with no competing site elsewhere. All lipids bound with moderate-to-strong predicted affinities (−6.8 to −8.8 kcal/mol). Binding strength correlated most strongly with the **degree of unsaturation** (Pearson r = −0.87) and secondarily with **chain length** (r = −0.70), whereas the **headgroup esterification state had a negligible effect** (mean |ΔΔG| ≈ 0.11 kcal/mol between free-acid and methyl-ester forms). Rankings were robust to scoring-function choice (Vina vs. Vinardo, Spearman ρ = 0.83). Per-molecule affinities were statistically indistinguishable between organisms (mean ΔG: CV −7.77, CCM −7.64 kcal/mol), indicating that the superior in vivo activity of CCM is not explained by individual-lipid binding strength alone but more likely by abundance-weighted extract composition and/or bioavailability. Molecular-dynamics simulations — nine 50 ns runs covering three fatty acids (EPA, γ-linolenic and palmitic acid) each in three chemical forms (free acid, methyl ester and deprotonated carboxylate) — confirmed that every complex is dynamically stable, with the ligand remaining bound to the ToxT fatty-acid pocket for 100% of the trajectory through a persistent aromatic/hydrophobic residue network; binding was robust to chain length, esterification and protonation state. Control simulations established specificity: the native ligand remained bound (positive control) while a glucose decoy was expelled to the pocket mouth (negative control), and all cognate lipids — including the weakest binders — formed stable complexes. A modelled ToxT–DNA complex (AlphaFold3) placed the DNA at the C-terminal HTH domain ~30 Å from the fatty-acid pocket, indicating an allosteric rather than steric mechanism of transcriptional inhibition. These results support direct lipid–ToxT engagement as a plausible mechanism and define a clear structure–activity principle: long, polyunsaturated acyl chains are the strongest ToxT binders.

---

## 1. Introduction

*Vibrio cholerae* causes cholera through the coordinated expression of cholera toxin (CT) and the toxin-coregulated pilus (TCP), both controlled by the AraC/XylS-family regulator **ToxT**. Lowden et al. (2010) solved the ToxT crystal structure (PDB 3GBG) bound to *cis*-palmitoleic acid (ligand code PAM), revealing that unsaturated fatty acids occupy an internal hydrophobic pocket and lock ToxT in a conformation incapable of activating its target promoters — a built-in mechanism for fatty-acid inhibition of virulence.

Natural-product inhibitors that exploit this mechanism are of interest as antivirulence agents. We have observed that lipid extracts of two green microalgae (CV and CCM) reduce *V. cholerae* virulence phenotypes. Because both extracts are rich in free fatty acids and fatty-acid methyl esters, we hypothesized that their activity is mediated, at least in part, by direct binding to the ToxT fatty-acid pocket. Here we use molecular docking to (i) test whether the lipid species detected in each extract are predicted to bind ToxT, (ii) identify the structural determinants of binding, (iii) ask whether the free-acid or methyl-ester form is favored, and (iv) compare the two organisms.

---

## 2. Materials and Methods

### 2.1 Receptor preparation
The ToxT crystal structure (PDB **3GBG**, 1.90 Å) was used as the receptor. Crystallographic waters and the co-crystallized fatty acid (PAM) were removed, leaving the protein chain. Missing-atom handling, protonation, assignment of Gasteiger charges, and merging of non-polar hydrogens were performed with **Meeko 0.7.1**, producing the receptor PDBQT.

### 2.2 Ligand sets and 3D structure generation
Lipid species identified in each extract were obtained as 3D conformers from **PubChem** where available (17 compounds). Species lacking a PubChem 3D record were generated from canonical SMILES using **RDKit** with ETKDGv3 embedding followed by MMFF94 energy minimization (fixed random seed = 42); these were: methyl stearate, stearic (octadecanoic) acid, methyl heptadecanoate, methyl heneicosanoate, and methyl 18-fluorooctadecanoate. The final non-redundant panel comprised **22 lipids**: 15 assigned to CV, 13 to CCM, with 6 shared between organisms. Ligand PDBQT files (Gasteiger charges, rotatable-bond detection) were prepared from SDF with **Meeko**.

### 2.3 Binding-site (grid box) definition
To anchor the search to the biologically relevant site, the docking box was defined by **enveloping the co-crystallized palmitoleate (PAM)** with 5 Å padding (Meeko `mk_prepare_receptor --box_enveloping`), yielding a box centered at **(54.65, 44.65, 18.85) Å** with dimensions **15.04 × 19.12 × 15.68 Å**.

### 2.4 Docking
Docking used **AutoDock Vina 1.2.7** with exhaustiveness = 16, up to 20 binding modes, energy range = 3 kcal/mol, and a fixed random seed (42) for determinism. CV and CCM panels were docked as **two independent runs** into the same pocket. The top-ranked (lowest-energy) pose of each ligand was retained.

### 2.5 Protocol validation (native-ligand redocking)
Palmitoleic acid (PAM; PubChem CID 445638) was rebuilt in 3D (RDKit ETKDG/MMFF), docked into the same box, and the top pose was compared to the crystallographic PAM coordinates. The heavy-atom RMSD was computed in the receptor reference frame (no superposition), symmetry-corrected (RDKit `CalcRMS`).

### 2.6 Free-acid vs. methyl-ester ("both forms")
Because GC-MS identifies the lipid species but not the bioactive chemical form, each fatty-acid backbone was docked as **both** its free acid and methyl ester. Counterpart forms were generated by an RDKit reaction transform (acid ⇌ methyl ester), embedded in 3D, and docked identically. Non-carboxyl species (neophytadiene, pentadecanal) were excluded from this comparison.

### 2.7 Consensus scoring
To assess robustness to the scoring function, every ligand was independently re-docked with the **Vinardo** scoring function (the scoring function introduced by SMINA; Quiroga & Villarreal, 2016), available natively in Vina 1.2.7 (`--scoring vinardo`). Agreement between Vina and Vinardo rankings was quantified by the Spearman rank correlation.

### 2.8 Structure–property analysis
Physicochemical descriptors (carbon count, number of C=C double bonds, molecular weight, logP, TPSA, rotatable bonds, headgroup class) were computed with RDKit and correlated (Pearson) with predicted affinity across all 22 ligands.

### 2.9 Molecular dynamics
Top-ranked complexes were subjected to all-atom MD with OpenMM 8.5. The ligand was parameterized with the OpenFF "Sage" 2.2.0 force field; partial charges were assigned by OpenFF-NAGL (a graph neural network reproducing AM1-BCC charges, avoiding semiempirical QM). The protein was described by Amber ff14SB, prepared with PDBFixer (missing atoms added, hydrogens added at pH 7.4). The complex was solvated in a TIP3P water box (1.0 nm padding) with 0.15 M NaCl and neutralizing counter-ions. After energy minimization and 100 ps equilibration, production runs of 50 ns were carried out in the NPT ensemble (Langevin thermostat 300 K, Monte Carlo barostat 1 bar, 4 fs timestep with hydrogen-mass repartitioning, hydrogen bonds constrained) on an NVIDIA RTX 3050 GPU (~100 ns/day). Analyses (backbone/ligand RMSD, per-residue RMSF, ligand center-of-mass distance from the pocket, and contact persistence) used MDTraj with minimum-image (periodic-boundary) correction; a residue was counted "in contact" when any atom was within 4.0 Å of the ligand. All residue numbers reported here follow the deposited crystal structure (PDB 3GBG); the simulation topology files provided with this work were renumbered to the same scheme so that reported residues match the shared coordinates.

### 2.10 Blind docking
To test whether the fatty-acid pocket is the *preferred* binding site rather than an assumed one, blind docking was performed with a search box enclosing the entire receptor (centre 50.6, 50.4, 19.6 Å; dimensions 56 × 60 × 63 Å), with no pocket bias. Four representative ligands — EPA, γ-linolenic acid, palmitic acid, and the native fatty acid palmitoleate — were docked at exhaustiveness 32 (20 modes, seed 42). Each pose's centre of mass was measured against the crystallographic fatty-acid pocket centre; a pose was scored "in pocket" when within 8 Å. For benchmarking, three reference ToxT ligands (virstatin, butyric acid, oleic acid) were retrieved from PubChem, prepared identically (RDKit 3D embedding, Meeko) and docked with the same Vina configuration, enabling comparison on a single scoring scale.

### 2.11 ToxT–DNA modelling
A ToxT–DNA complex was predicted with the AlphaFold3 server using the full-length ToxT sequence and a 34-bp duplex containing two direct-repeat toxbox consensus elements (yrTTTTwwTwAww). The top-ranked model (of five) was analysed; confidence was assessed by pTM and interface ipTM. The fatty-acid-bound crystal (3GBG) was superposed onto the modelled ToxT (Cα) to place the native lipid, and protein–DNA contacts were defined at 5 Å.

### 2.12 Software
AutoDock Vina 1.2.7; Meeko 0.7.1; RDKit 2026.03; OpenMM 8.5.2; OpenFF-Toolkit 0.18 (Sage 2.2.0) + OpenFF-NAGL; PDBFixer; MDTraj; Python 3.11/3.13. Visualization in PyMOL. All input files, configurations (box, seed), scripts, and output poses/trajectories are archived for reproducibility (Section 6).

---

## 3. Results

### 3.1 Validation: the protocol reproduces the crystallographic pose
Redocking palmitoleate into the ToxT pocket reproduced the experimental binding pose to **1.41 Å heavy-atom RMSD** (< 2.0 Å), with a predicted affinity of −7.59 kcal/mol. This confirms that the receptor preparation, box placement, and scoring correctly identify the native fatty-acid binding mode and validates the docking of the lipid panel.

### 3.2 CV lipid panel
All 15 CV lipids docked into the fatty-acid pocket with affinities from −6.90 to −8.78 kcal/mol (Table 1).

**Table 1. CV docking (AutoDock Vina 1.2.7), ranked.**

| Rank | Lipid | ΔG (kcal/mol) |
|---|---|---|
| 1 | *cis*-5,8,11,14,17-eicosapentaenoic acid (EPA) | −8.78 |
| 2 | methyl eicosapentaenoate | −8.48 |
| 3 | methyl 4,7,10,13-hexadecatetraenoate | −8.46 |
| 4 | γ-linolenic acid | −8.13 |
| 5 | 9,12,15-octadecatrienoic acid (ALA) | −7.91 |
| 6 | *cis*-10-heptadecenoic acid | −7.81 |
| 7 | methyl palmitoleate | −7.72 |
| 8 | heptadecanoic acid | −7.68 |
| 9 | stearic acid | −7.63 |
| 10 | methyl heptadecanoate | −7.57 |
| 11 | methyl stearate | −7.57 |
| 12 | methyl palmitate | −7.48 |
| 13 | methyl myristate | −7.31 |
| 14 | methyl pentadecanoate | −7.18 |
| 15 | pentadecanal | −6.90 |

### 3.3 CCM lipid panel
All 13 CCM lipids docked with affinities from −6.84 to −8.13 kcal/mol (Table 2).

**Table 2. CCM docking (AutoDock Vina 1.2.7), ranked.**

| Rank | Lipid | ΔG (kcal/mol) |
|---|---|---|
| 1 | γ-linolenic acid | −8.13 |
| 2 | neophytadiene | −8.12 |
| 3 | methyl 3,9,12-octadecatrienoate | −7.97 |
| 4 | methyl heneicosanoate | −7.84 |
| 5 | *cis*-10-heptadecenoic acid | −7.81 |
| 6 | 9,11-octadecadienoic acid | −7.80 |
| 7 | methyl palmitoleate | −7.72 |
| 8 | methyl stearate | −7.57 |
| 9 | methyl palmitate | −7.48 |
| 10 | methyl 18-fluorostearate | −7.38 |
| 11 | palmitic acid | −7.32 |
| 12 | methyl myristate | −7.31 |
| 13 | tridecanoic acid | −6.84 |

![Figure 1](figures/fig1_affinity_bars.png)

**Figure 1.** Predicted ToxT binding affinities for the CV (blue) and CCM (orange) lipid panels (AutoDock Vina 1.2.7).

### 3.4 Structural determinants of binding
Across all 22 lipids, predicted affinity correlated most strongly with the **number of C=C double bonds** (Pearson r = −0.87) and with **chain length** (carbons, r = −0.70); molecular weight tracked chain length (r = −0.58). Lipophilicity (logP, r = −0.32), polarity (TPSA, r = −0.02), and flexibility (rotatable bonds, r = +0.12) were weak or non-predictive (Table 3).

**Table 3. Descriptor–affinity correlations (n = 22).**

| Descriptor | Pearson r vs. ΔG |
|---|---|
| C=C double bonds | **−0.87** |
| Chain length (C) | −0.70 |
| Molecular weight | −0.58 |
| logP | −0.32 |
| TPSA | −0.02 |
| Rotatable bonds | +0.12 |

The most unsaturated species (EPA, C20:5; hexadecatetraenoate, C16:4; the octadecatrienoates and γ-linolenate, C18:3) were the strongest binders, while fully saturated lipids (tridecanoic, myristate, palmitate) were weakest. The strong-binding outlier neophytadiene (a C20 diterpene, formally 2 C=C) is hydrophobic (logP 7.2) and fits the pocket through shape complementarity rather than a carboxylate interaction.

![Figure 2](figures/fig2_unsaturation.png)

**Figure 2.** Binding affinity vs. number of C=C double bonds (point colour = chain length); dashed line is the linear fit (r = −0.87).

### 3.5 Free-acid vs. methyl-ester form
For every fatty-acid backbone, the free-acid and methyl-ester forms bound with nearly identical affinity (mean |ΔΔG| ≈ 0.11 kcal/mol; maximum 0.42 kcal/mol for ALA), well within Vina's scoring uncertainty (Table 4). ToxT binding is therefore governed by the acyl chain, not the headgroup esterification state, so **both the free acid and the methyl ester are plausible bioactive forms.**

**Table 4. Acid vs. methyl-ester affinity (kcal/mol); Δ = ester − acid (selected backbones).**

| Backbone | C:db | Acid | Ester | Δ |
|---|---|---|---|---|
| EPA | 20:5 | −8.84 | −8.82 | +0.03 |
| hexadecatetraenoate | 16:4 | −8.44 | −8.39 | +0.05 |
| γ-linolenate | 18:3 | −8.24 | −8.35 | −0.11 |
| 9,12,15-octadecatrienoate | 18:3 | −7.89 | −8.31 | −0.42 |
| 9,11-octadecadienoate | 18:2 | −7.91 | −7.89 | +0.01 |
| *cis*-10-heptadecenoate | 17:1 | −7.72 | −7.84 | −0.12 |
| palmitoleate | 16:1 | −7.58 | −7.65 | −0.07 |
| stearate | 18:0 | −7.63 | −7.57 | +0.06 |
| palmitate | 16:0 | −7.29 | −7.41 | −0.12 |
| myristate | 14:0 | −7.14 | −7.31 | −0.17 |
| tridecanoate | 13:0 | −6.82 | −6.85 | −0.03 |

![Figure 4](figures/fig4_acid_vs_ester.png)

**Figure 4.** Free-acid vs. methyl-ester affinity per backbone; points lie on the y = x line (form-insensitive).

### 3.6 Consensus scoring
Re-docking with the Vinardo scoring function gave rankings strongly concordant with the default Vina scoring (**Spearman ρ = 0.83**, n = 22). The top binders (EPA, methyl-EPA, hexadecatetraenoate, γ-linolenate, neophytadiene, the octadecatrienoates) were top-ranked under both functions. The largest disagreement was the long saturated ester methyl heneicosanoate (Vina −7.84, Vinardo −7.19), which Vinardo penalizes more — consistent with the overall unsaturation trend. The ranking is therefore robust to scoring-function choice and unlikely to reflect scoring artifacts.

![Figure 3](figures/fig3_consensus.png)

**Figure 3.** Vina vs. Vinardo affinities (n = 22); dashed line is y = x (Spearman ρ = 0.83).

### 3.7 Organism comparison
Mean predicted affinities were nearly identical between organisms (**CV −7.77 vs. CCM −7.64 kcal/mol**; difference 0.13 kcal/mol, within scoring error), and the best single binders were comparable (CV EPA −8.78; CCM γ-linolenate −8.13). Thus, per-molecule ToxT-binding strength does **not** discriminate the two extracts.

### 3.8 Molecular-dynamics validation of the top complex
To test whether the docked poses are dynamically stable, the top binder EPA was simulated in both its free-acid and methyl-ester forms (50 ns each; ~38,800-atom solvated systems). Both complexes were stable: the protein backbone RMSD plateaued rapidly and remained low (1.87 ± 0.27 Å for the acid, 1.66 ± 0.22 Å for the ester), and the radius of gyration was constant, indicating a well-folded receptor throughout (Figure 5, left).

Crucially, the ligand never left the pocket. The ligand centre-of-mass remained 2–4 Å from the pocket centre (minimum-image corrected) for the entire trajectory — **bound in 100% of frames** for both forms (Figure 5, right). Binding was mediated by a persistent residue network (residue numbering follows the deposited crystal structure, PDB 3GBG): for the free acid, Tyr12, Phe22, Leu25, Lys31 and Phe33 (among others) maintained contact in ~100% of production frames (Figure 6); the methyl ester engaged an essentially identical set (Tyr12, Tyr20, Phe22, Leu25, Ile27, Phe33, Val81, Tyr266 all ~100%, with Lys31/Arg13 at the head group). This aromatic cage plus hydrophobic wall, capped by the basic Lys31/Arg13 pair, corresponds to the crystallographic fatty-acid pocket and confirms the docked binding mode is dynamically real.

To test the physiological protonation state, EPA was additionally simulated as its deprotonated carboxylate (the dominant form of a free fatty acid at pH 7.4). This complex was likewise stable (backbone RMSD 1.82 ± 0.12 Å) and, if anything, the most tightly held: the ligand centre of mass stayed 1.1–3.0 Å from the pocket centre (mean 2.1 Å), bound in 100% of frames. Consistent with the added negative charge, the deprotonated head engaged the basic pocket residues more persistently, with Lys31 and Lys230 (and Arg13) in contact ~100% of the time, indicating a salt-bridge-stabilised carboxylate.

To establish that this form-independence is a general property of the pocket rather than a peculiarity of EPA, the analysis was extended to **three fatty acids spanning the affinity range** — EPA (strong, C20:5), γ-linolenic acid (strong, C18:3), and palmitic acid (weak, C16:0) — each simulated in all three chemical forms (free acid, methyl ester, deprotonated carboxylate): **nine 50 ns simulations**. Every one produced a stable complex (backbone RMSD 1.5–2.3 Å) with the ligand bound for **100% of the trajectory** in all cases (ligand–pocket distance 1.2–3.4 Å; Table 5, Figure 7).

Thus, across three fatty acids of differing chain length and unsaturation, and across esterification and protonation state, ToxT retains the ligand in the fatty-acid pocket. The binding mode is robust to head-group chemistry; the acyl tail governs occupancy, consistent with the docking structure–property analysis (Section 3.4).

**Table 5. MD summary of the head-group matrix (nine 50 ns simulations).**

| Fatty acid | Form | Backbone RMSD (Å) | Ligand–pocket COM (Å) | Bound |
|---|---|---|---|---|
| EPA (C20:5) | free acid | 1.87 ± 0.27 | 2.6 | 100% |
| EPA | methyl ester | 1.66 ± 0.22 | 2.3 | 100% |
| EPA | carboxylate | 1.82 ± 0.12 | 1.7 | 100% |
| γ-linolenic (C18:3) | free acid | 1.91 ± 0.17 | 1.2 | 100% |
| γ-linolenic | methyl ester | 2.12 ± 0.15 | 2.0 | 100% |
| γ-linolenic | carboxylate | 1.65 ± 0.14 | 1.9 | 100% |
| palmitic (C16:0) | free acid | 1.96 ± 0.20 | 3.4 | 100% |
| palmitic | methyl ester | 2.32 ± 0.18 | 3.0 | 100% |
| palmitic | carboxylate | 1.46 ± 0.13 | 2.2 | 100% |

![Figure 5](figures/fig5_md_stability.png)

**Figure 5.** MD stability of the ToxT–EPA complexes (three forms, 50 ns each): protein backbone RMSD (left) and ligand centre-of-mass distance from the pocket (right); the 10 Å dashed line marks the bound/unbound threshold.

![Figure 6](figures/fig6_md_contacts.png)

**Figure 6.** ToxT residues contacting EPA and their persistence (% of production frames within 4 Å).

![Figure 7](figures/fig7_md_headgroup_matrix.png)

**Figure 7.** Ligand centre-of-mass distance from the pocket (mean over production) for the nine head-group simulations — three fatty acids (EPA, γ-linolenic, palmitic) × three forms (free acid, methyl ester, carboxylate). All remain far below the 10 Å unbound threshold, i.e. bound throughout.

*(A positive control — native palmitoleate; two negative controls — a glucose decoy and apo ToxT; and the two weakest binders, pentadecanal and tridecanoic acid, are currently being simulated and will be added on completion.)*

### 3.9 Blind docking confirms the fatty-acid pocket as the preferred site
Because the panel was docked into a predefined box, we verified — by blind docking over the entire ToxT surface — that this pocket is genuinely preferred and not merely imposed. The protocol was validated by its recovery of the native ligand: with no pocket bias, palmitoleate's top pose localized **0.6 Å** from its crystallographic position (Table 6). For the strongly-binding polyunsaturated lipids, **every** pose fell in the fatty-acid pocket (EPA 15/15, γ-linolenic 8/8 modes), and no site elsewhere on the protein scored higher. The weak binder palmitic acid also placed its single best pose in the pocket (1.5 Å) but distributed its remaining poses over the surface (1/20 in pocket), consistent with weak, non-specific association. Thus strong, unsaturated lipids are pocket-selective, whereas saturated lipids bind loosely — mirroring the affinity structure–activity relationship (Section 3.4). No competing high-affinity binding site was detected.

**Table 6. Blind docking (whole-protein search) of representative lipids.**

| Lipid | Top-pose ΔG (kcal/mol) | Top pose → pocket (Å) | Modes in pocket |
|---|---|---|---|
| EPA | −8.48 | 2.9 | 15/15 |
| γ-linolenic acid | −8.30 | 1.2 | 8/8 |
| palmitic acid | −5.72 | 1.5 | 1/20 |
| palmitoleate (native, control) | −7.60 | 0.6 | 10/13 |

### 3.10 Structural basis of binding and control simulations
The docked lipids occupy the internal fatty-acid pocket of the ToxT N-terminal domain — an aromatic cage (Tyr12, Tyr20, Phe22, Phe33, Phe69, Tyr266) and hydrophobic wall (Leu/Val/Ile/Met) closed by a basic clamp (Lys31, Lys230, Arg13) that engages the carboxylate head group (Figure 8). Superposition of the full CV and CCM panels shows every lipid converges on this single pocket (Figure 9).

![Figure 8](figures/fig8_pocket_final.png)

**Figure 8.** ToxT fatty-acid pocket. (A) Whole protein with the pocket highlighted; (B) pocket detail with residues coloured by chemistry (orange aromatic, blue basic, grey hydrophobic) and the native ligand (yellow); dashes mark salt bridges to the carboxylate.

![Figure 9A](figures/fig_CV_overlay_final.png)
![Figure 9B](figures/fig_CCM_overlay_final.png)

**Figure 9.** All CV (A) and CCM (B) lipids docked in the ToxT pocket, coloured by binding affinity — every species converges on the same site.

Three control simulations tested specificity (Table 7). **Positive control:** the native ligand palmitoleate remained bound throughout (ligand–pocket 1.5 Å, 100% of frames), reproducing the crystallographic mode and validating the protocol. **Negative control:** a glucose decoy docked into the pocket was expelled to the pocket mouth (~8.9 Å) and never occupied the core, whereas all fatty acids stayed 1–3 Å from the pocket centre (Figure 10) — demonstrating the pocket is fatty-acid selective. The two weakest-docking lipids (pentadecanal, tridecanoic acid) nonetheless formed stable complexes once seated (1.7–2.0 Å, 100% bound); thus all cognate lipids are retained, and affinity differences among lipids manifest as reduced pocket-selectivity in blind docking (Section 3.9) rather than reduced MD stability. An apo (ligand-free) run provided a dynamics baseline.

**Table 7. Control and weak-binder simulations (50 ns each).**

| System | Role | Ligand–pocket (Å) | Bound |
|---|---|---|---|
| palmitoleate (native) | positive control | 1.5 | 100% |
| glucose | negative control (decoy) | 8.9 | expelled |
| pentadecanal | weak binder | 1.7 | 100% |
| tridecanoic acid | weak binder | 2.0 | 100% |
| apo ToxT | ligand-free baseline | — | — |

![Figure 10](figures/fig10_specificity.png)

**Figure 10.** Ligand–pocket distance over 50 ns: cognate fatty acids and the native ligand stay in the pocket core (green band), while the glucose decoy is held at the pocket mouth (~9 Å).

### 3.11 Comparison with known ToxT ligands
Prior computational studies of ToxT ligands used heterogeneous programs and score units (e.g. GOLD fitness scores; MM interaction energies in kJ/mol) that are not directly comparable across methods. To place the algal lipids on a single, comparable footing, three reference ToxT ligands were docked under the **identical protocol** (same box, seed and Vina 1.2.7 scoring): the engineered inhibitor **virstatin**, the short-chain fatty acid **butyrate** (a recently reported natural ToxT-targeting compound), and **oleic acid** (a native-type unsaturated fatty acid). The algal lipids (−6.8 to −8.8 kcal/mol) bound comparably to the native-type ligand oleic acid (−7.90) and substantially more strongly than butyrate (−3.71). The purpose-designed inhibitor virstatin scored highest (−10.21), as expected for an engineered scaffold — a value that also partly reflects the docking score's known dependence on aromatic surface area, and virstatin's mechanism (interference with ToxT dimerisation) differs from direct pocket occupancy. Thus these microalgae supply **naturally occurring ToxT-pocket binders that engage the site as effectively as its native regulator, without any medicinal-chemistry optimisation** (Table 8).

**Table 8. Reference ToxT ligands docked under the identical protocol.**

| Compound | ΔG (kcal/mol) | Type |
|---|---|---|
| virstatin | −10.21 | synthetic, engineered inhibitor |
| algal lipids (this study) | −6.8 to −8.8 | natural (microalgal) |
| oleic acid | −7.90 | native-type unsaturated fatty acid |
| butyric acid | −3.71 | natural short-chain fatty acid |

### 3.12 A modeled ToxT–DNA complex indicates an allosteric mechanism
To probe how fatty-acid binding translates into loss of virulence-gene activation, a ToxT–DNA complex was modelled with AlphaFold3 (full-length ToxT plus a 34-bp duplex bearing two direct-repeat toxbox elements). The ToxT fold was predicted with high confidence (pTM 0.85), whereas the protein–DNA interface was of modest confidence (ipTM 0.31); the model is therefore interpreted only at the domain level. The DNA was contacted **exclusively by the C-terminal AraC-family helix–turn–helix domain** (residues 188–276; e.g. Arg214, Lys235/237, Tyr250, Lys256), while the fatty-acid pocket lies in the N-terminal domain **~30 Å away**, making no direct contact with the DNA (nearest approach ~6 Å; Figure 11). Because the regulatory pocket and the DNA-reading head are spatially separated on distinct domains, fatty-acid occupancy **cannot sterically block DNA binding**; the architecture is instead consistent with an **allosteric** mechanism in which pocket occupancy restrains the inter-domain conformation required for productive DNA engagement — the closed-state model proposed by Lowden et al. (2010). The algal lipids are thus predicted to switch off ToxT-dependent transcription not by competing with DNA directly, but by locking ToxT in a DNA-binding-incompetent conformation.

![Figure 11](figures/fig11_dna_competition.png)

**Figure 11.** AlphaFold3 model of the ToxT–DNA complex: toxbox DNA (teal), the C-terminal HTH DNA-binding domain (blue, residues 188–276), and the fatty-acid pocket (orange) with the native ligand (yellow, from 3GBG superposition) ~30 Å away (red dashes). The spatial separation supports an allosteric inhibition mechanism. The ToxT fold is high-confidence (pTM 0.85); the DNA pose is low-confidence (ipTM 0.31) and is interpreted only at the domain level, not as a precise binding geometry.

---

## 4. Discussion

These docking results support direct engagement of algal lipids with the ToxT fatty-acid pocket as a plausible molecular basis for their antivirulence activity. The protocol is validated (native redocking 1.41 Å; blind docking recovers the native site to 0.6 Å), internally consistent across two scoring functions (ρ = 0.83), and yields a clear structure–activity relationship: **binding strength increases with acyl-chain unsaturation and length**, mirroring the natural ToxT ligand and the Lowden mechanism in which *cis* double bonds impose the bent geometry that fits the pocket. Molecular dynamics and a full control set place this on a firmer footing: the pocket is fatty-acid **selective** (native ligand retained, glucose decoy expelled), and all cognate lipids form stable complexes across chain length, unsaturation, esterification and protonation state. The modelled ToxT–DNA complex extends this to function: because the fatty-acid pocket and the DNA-binding HTH domain are ~30 Å apart on separate domains, lipid binding is predicted to inhibit transcription **allosterically** — by locking ToxT in a DNA-incompetent conformation — rather than by directly competing with DNA, providing a plausible structural route from lipid binding to virulence-gene silencing.

The headgroup-independence (acid ≈ ester, confirmed by MD) indicates that the carboxylate is not the dominant anchor; the hydrophobic tail and its unsaturation dictate pocket fit. This means GC-MS uncertainty about the bioactive form does not undermine the proposed mechanism — both forms bind and are stable.

Notably, docking does **not** reproduce the experimental observation that CCM is the more active extract: per-lipid affinities are statistically indistinguishable between CV and CCM. This is expected and informative. Docking ranks single molecules at equal concentration, whereas in vivo activity reflects the **abundance-weighted composition** of a complex mixture, plus solubility, membrane permeability, metabolic stability, and possible multi-target or synergistic effects — none captured by single-ligand docking. The most likely explanation is that CCM is enriched in **abundant** strong binders. This is directly testable by combining these affinities with GC-MS relative abundances into an abundance-weighted binding score (future work).

From a translational standpoint, the distinguishing feature of these lipids is not that they are the strongest conceivable ToxT binders — the engineered inhibitor virstatin scores higher — but that they are **naturally produced, renewable compounds** that engage the validated regulatory pocket as effectively as ToxT's native fatty-acid ligand, and do so with **no synthesis or medicinal-chemistry optimisation**. Combined with the antivirulence activity we previously reported for these microalgal extracts, this positions *Chlorella variabilis* and *Chlorococcum* sp. lipids as a natural, cultivable source of ToxT-pocket-directed antivirulence leads.

## 5. Limitations

- Docking provides relative binding hypotheses, not absolute affinities; Vina scores carry ~±1–2 kcal/mol uncertainty, so within-tier rank differences should not be over-interpreted.
- Docking used a single rigid-receptor conformation; MD confirmed the complexes are stable but did not exhaustively sample induced fit.
- MD covered 13 systems (three fatty acids × three forms, plus positive/negative controls and weak binders) as single 50 ns trajectories; independent replicates and MD of the remaining panel members would further strengthen the statistics.
- The organism-level interpretation requires quantitative GC-MS abundance data, which were available only qualitatively (presence/absence, published Table 2); abundance-weighting therefore remains future work.

## 6. Reproducibility and data availability

All steps are deterministic (fixed seed = 42). Residue numbering follows PDB 3GBG; shared MD topologies were renumbered to match. Code, inputs and small outputs are on GitHub; full trajectories are archived on Zenodo (see `DATA_AVAILABILITY.md`). Key scripts:
- **Receptor/box:** Meeko `mk_prepare_receptor` (box enveloping the crystal PAM, 5 Å padding).
- **Ligand generation:** `generate_missing_3d.py` (RDKit ETKDG/MMFF from SMILES).
- **Docking:** `dock_by_organism.py`; **validation:** `pam_control.py`; **blind:** `blind_dock.py`.
- **Both forms:** `pairs_pipeline.py`; **consensus:** `consensus_scoring.py`; **structure–property:** `structural_analysis.py`.
- **MD:** `md_production.py` / `md_production_apo.py` / `md_supervisor.py`; **analysis/figures:** `md_summary.py`, `md_figures.py`, `make_specificity_fig.py`, `render_docking4.py`.

## References (to be formatted to journal style)
1. Lowden MJ, et al. Structure of *Vibrio cholerae* ToxT reveals a mechanism for fatty acid regulation of virulence genes. *PNAS* 2010;107:2860–2865.
2. Trott O, Olson AJ. AutoDock Vina: improving the speed and accuracy of docking. *J Comput Chem* 2010;31:455–461.
3. Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0: New docking methods, expanded force field, and Python bindings. *J Chem Inf Model* 2021;61:3891–3898.
4. Quiroga R, Villarreal MA. Vinardo: A scoring function based on AutoDock Vina improves scoring, docking, and virtual screening. *PLoS ONE* 2016;11:e0155183.
5. Kim S, et al. PubChem 2023 update. *Nucleic Acids Res* 2023;51:D1373–D1380.
6. Landrum G, et al. RDKit: Open-source cheminformatics. https://www.rdkit.org.
