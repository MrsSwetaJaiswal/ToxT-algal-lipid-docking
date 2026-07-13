const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
        WidthType, ShadingType, PageNumber, TableOfContents, PageBreak } = require("docx");

const CW = 9360; // content width (US Letter, 1" margins)
const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };

function P(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120, line: 276 },
    alignment: opts.justify ? AlignmentType.JUSTIFIED : undefined,
    children: [new TextRun({ text, italics: opts.italic, bold: opts.bold, size: opts.size })],
  });
}
function H(text, level) {
  return new Paragraph({ heading: level, children: [new TextRun(text)] });
}
function cell(text, w, { head = false, bold = false } = {}) {
  return new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: head ? { fill: "1F4E79", type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: [new TextRun({
      text, bold: head || bold, color: head ? "FFFFFF" : undefined, size: 19 })] })],
  });
}
function table(headerRow, rows, widths) {
  const trs = [new TableRow({ tableHeader: true,
    children: headerRow.map((t, i) => cell(t, widths[i], { head: true })) })];
  rows.forEach(r => trs.push(new TableRow({
    children: r.map((t, i) => cell(String(t), widths[i], { bold: i === 0 && false })) })));
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}
function fig(file, wPx, hPx, caption) {
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 },
      children: [new ImageRun({ type: "png", data: fs.readFileSync(file),
        transformation: { width: wPx, height: hPx },
        altText: { title: caption, description: caption, name: caption } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({ text: caption, italics: true, size: 18 })] }),
  ];
}

const cvRows = [
  ["1","cis-5,8,11,14,17-eicosapentaenoic acid (EPA)","-8.78"],
  ["2","methyl eicosapentaenoate","-8.48"],
  ["3","methyl 4,7,10,13-hexadecatetraenoate","-8.46"],
  ["4","gamma-linolenic acid","-8.13"],
  ["5","9,12,15-octadecatrienoic acid (ALA)","-7.91"],
  ["6","cis-10-heptadecenoic acid","-7.81"],
  ["7","methyl palmitoleate","-7.72"],
  ["8","heptadecanoic acid","-7.68"],
  ["9","stearic acid","-7.63"],
  ["10","methyl heptadecanoate","-7.57"],
  ["11","methyl stearate","-7.57"],
  ["12","methyl palmitate","-7.48"],
  ["13","methyl myristate","-7.31"],
  ["14","methyl pentadecanoate","-7.18"],
  ["15","pentadecanal","-6.90"]];
const ccmRows = [
  ["1","gamma-linolenic acid","-8.13"],
  ["2","neophytadiene","-8.12"],
  ["3","methyl 3,9,12-octadecatrienoate","-7.97"],
  ["4","methyl heneicosanoate","-7.84"],
  ["5","cis-10-heptadecenoic acid","-7.81"],
  ["6","9,11-octadecadienoic acid","-7.80"],
  ["7","methyl palmitoleate","-7.72"],
  ["8","methyl stearate","-7.57"],
  ["9","methyl palmitate","-7.48"],
  ["10","methyl 18-fluorostearate","-7.38"],
  ["11","palmitic acid","-7.32"],
  ["12","methyl myristate","-7.31"],
  ["13","tridecanoic acid","-6.84"]];
const descRows = [
  ["C=C double bonds","-0.87"],["Chain length (carbons)","-0.70"],
  ["Molecular weight","-0.58"],["logP","-0.32"],
  ["TPSA","-0.02"],["Rotatable bonds","+0.12"]];
const pairRows = [
  ["EPA","20:5","-8.84","-8.82","+0.03"],
  ["hexadecatetraenoate","16:4","-8.44","-8.39","+0.05"],
  ["gamma-linolenate","18:3","-8.24","-8.35","-0.11"],
  ["9,12,15-octadecatrienoate","18:3","-7.89","-8.31","-0.42"],
  ["9,11-octadecadienoate","18:2","-7.91","-7.89","+0.01"],
  ["cis-10-heptadecenoate","17:1","-7.72","-7.84","-0.12"],
  ["palmitoleate","16:1","-7.58","-7.65","-0.07"],
  ["stearate","18:0","-7.63","-7.57","+0.06"],
  ["palmitate","16:0","-7.29","-7.41","-0.12"],
  ["myristate","14:0","-7.14","-7.31","-0.17"],
  ["tridecanoate","13:0","-6.82","-6.85","-0.03"]];

const kids = [];
// Title
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
  children: [new TextRun({ bold: true, size: 30,
    text: "Molecular docking of Chlorella (CV) and Chlorococcum (CCM) lipids against the Vibrio cholerae virulence regulator ToxT" })] }));
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ italics: true, size: 18,
    text: "Working manuscript draft - computational (docking) component. Species names and experimental/GC-MS details are placeholders to be completed by the authors." })] }));

kids.push(H("Abstract", HeadingLevel.HEADING_1));
kids.push(P("The transcriptional activator ToxT is the master regulator of virulence-gene expression in Vibrio cholerae, and its activity is directly modulated by fatty acids that occupy a hydrophobic binding pocket (Lowden et al., 2010). To test whether direct ToxT binding could underlie the observed antivirulence activity of lipid extracts from two green microalgae (CV and CCM), we docked the lipid species identified in each extract against the ToxT crystal structure (PDB 3GBG). A panel of 22 unique lipids (15 CV, 13 CCM, 6 shared) was docked with AutoDock Vina 1.2.7 into the experimentally defined fatty-acid pocket. The protocol was validated by redocking the co-crystallized fatty acid (palmitoleate), reproducing the crystallographic pose to 1.41 A RMSD; blind docking over the whole protein independently recovered the native site (0.6 A) and identified the fatty-acid pocket as the preferred binding site, with no competing site elsewhere. All lipids bound with moderate-to-strong predicted affinities (-6.8 to -8.8 kcal/mol). Binding strength correlated most strongly with degree of unsaturation (r = -0.87) and chain length (r = -0.70), whereas headgroup esterification state had a negligible effect (mean |dG| ~ 0.11 kcal/mol between free-acid and methyl-ester forms). Rankings were robust to scoring-function choice (Vina vs. Vinardo, Spearman rho = 0.83). Per-molecule affinities were statistically indistinguishable between organisms (mean dG: CV -7.77, CCM -7.64 kcal/mol), indicating that the superior in vivo activity of CCM is not explained by individual-lipid binding strength alone but more likely by abundance-weighted extract composition and bioavailability. Molecular-dynamics simulations (nine 50 ns runs: three fatty acids - EPA, gamma-linolenic and palmitic - each as free acid, methyl ester and deprotonated carboxylate) confirmed every complex is dynamically stable, with the ligand bound to the ToxT pocket for 100% of the trajectory; binding was robust to chain length, esterification and protonation state. Control simulations established specificity: the native ligand remained bound (positive control) while a glucose decoy was expelled to the pocket mouth (negative control), and all cognate lipids - including the weakest binders - formed stable complexes. A modelled ToxT-DNA complex (AlphaFold3) placed the DNA at the C-terminal HTH domain ~30 A from the fatty-acid pocket, indicating an allosteric rather than steric mechanism of transcriptional inhibition.", { justify: true }));

kids.push(H("1. Introduction", HeadingLevel.HEADING_1));
kids.push(P("Vibrio cholerae causes cholera through coordinated expression of cholera toxin and the toxin-coregulated pilus, both controlled by the AraC/XylS-family regulator ToxT. Lowden et al. (2010) solved the ToxT crystal structure (PDB 3GBG) bound to cis-palmitoleic acid, revealing that unsaturated fatty acids occupy an internal hydrophobic pocket and lock ToxT in a conformation that cannot activate its target promoters - a built-in mechanism for fatty-acid inhibition of virulence.", { justify: true }));
kids.push(P("Natural-product inhibitors exploiting this mechanism are of interest as antivirulence agents. Lipid extracts of two green microalgae (CV and CCM) reduce V. cholerae virulence phenotypes; because both extracts are rich in free fatty acids and fatty-acid methyl esters, we hypothesized that their activity is mediated, at least in part, by direct binding to the ToxT fatty-acid pocket. Here we use molecular docking to (i) test whether the lipid species detected in each extract are predicted to bind ToxT, (ii) identify the structural determinants of binding, (iii) ask whether the free-acid or methyl-ester form is favored, and (iv) compare the two organisms.", { justify: true }));

kids.push(H("2. Materials and Methods", HeadingLevel.HEADING_1));
kids.push(H("2.1 Receptor preparation", HeadingLevel.HEADING_2));
kids.push(P("The ToxT crystal structure (PDB 3GBG, 1.90 A) was used as the receptor. Crystallographic waters and the co-crystallized fatty acid (PAM) were removed. Protonation, Gasteiger charge assignment, and merging of non-polar hydrogens were performed with Meeko 0.7.1, producing the receptor PDBQT.", { justify: true }));
kids.push(H("2.2 Ligand sets and 3D structure generation", HeadingLevel.HEADING_2));
kids.push(P("Lipid species were obtained as 3D conformers from PubChem where available (17 compounds). Species lacking a PubChem 3D record were generated from canonical SMILES using RDKit (ETKDGv3 embedding + MMFF94 minimization, seed = 42): methyl stearate, stearic acid, methyl heptadecanoate, methyl heneicosanoate, and methyl 18-fluorooctadecanoate. The non-redundant panel comprised 22 lipids (15 CV, 13 CCM, 6 shared). Ligand PDBQT files were prepared from SDF with Meeko.", { justify: true }));
kids.push(H("2.3 Binding-site (grid box) definition", HeadingLevel.HEADING_2));
kids.push(P("To anchor the search to the biologically relevant site, the box was defined by enveloping the co-crystallized palmitoleate (PAM) with 5 A padding, yielding a box centered at (54.65, 44.65, 18.85) A with dimensions 15.04 x 19.12 x 15.68 A.", { justify: true }));
kids.push(H("2.4 Docking", HeadingLevel.HEADING_2));
kids.push(P("Docking used AutoDock Vina 1.2.7 (exhaustiveness = 16, up to 20 modes, energy range = 3 kcal/mol, fixed seed = 42 for determinism). CV and CCM panels were docked as two independent runs into the same pocket; the top-ranked pose of each ligand was retained.", { justify: true }));
kids.push(H("2.5 Protocol validation, both-forms, consensus, and analysis", HeadingLevel.HEADING_2));
kids.push(P("Validation: palmitoleic acid was rebuilt in 3D, redocked, and its top pose compared to the crystallographic PAM coordinates (heavy-atom RMSD in the receptor frame, symmetry-corrected). Both forms: each fatty-acid backbone was docked as both free acid and methyl ester (forms interconverted by an RDKit reaction transform). Consensus: every ligand was re-docked with the Vinardo scoring function (the function introduced by SMINA), available in Vina 1.2.7, and rankings compared by Spearman correlation. Structure-property: RDKit descriptors were correlated (Pearson) with affinity across all 22 ligands. Software: AutoDock Vina 1.2.7, Meeko 0.7.1, RDKit 2026.03, Python 3.13; visualization in PyMOL.", { justify: true }));

kids.push(H("2.6 Blind docking", HeadingLevel.HEADING_2));
kids.push(P("To test whether the fatty-acid pocket is the preferred site rather than an assumed one, blind docking used a box enclosing the entire receptor (centre 50.6, 50.4, 19.6 A; 56 x 60 x 63 A), no pocket bias. Four representative ligands (EPA, gamma-linolenic, palmitic, and native palmitoleate) were docked at exhaustiveness 32. Each pose centre of mass was measured against the crystallographic pocket centre; within 8 A was scored in-pocket. For benchmarking, three reference ToxT ligands (virstatin, butyric acid, oleic acid) were retrieved from PubChem, prepared identically and docked with the same Vina configuration for comparison on a single scale.", { justify: true }));
kids.push(H("2.7 ToxT-DNA modelling", HeadingLevel.HEADING_2));
kids.push(P("A ToxT-DNA complex was predicted with the AlphaFold3 server using the full-length ToxT sequence and a 34-bp duplex containing two direct-repeat toxbox consensus elements. The top-ranked model was analysed (confidence: pTM, interface ipTM); the fatty-acid-bound crystal (3GBG) was superposed onto the modelled ToxT (Ca) to place the native lipid, and protein-DNA contacts defined at 5 A.", { justify: true }));
kids.push(H("2.8 Molecular dynamics", HeadingLevel.HEADING_2));
kids.push(P("Top complexes were simulated with OpenMM 8.5. The ligand used the OpenFF Sage 2.2.0 force field with OpenFF-NAGL AM1BCC-quality charges; the protein used Amber ff14SB, prepared with PDBFixer (missing atoms; hydrogens added at pH 7.4). Systems were solvated in TIP3P water (1.0 nm padding) with 0.15 M NaCl plus neutralizing ions (~38,800 atoms). After minimization and 100 ps equilibration, 50 ns production runs were performed in the NPT ensemble (Langevin 300 K, Monte Carlo barostat 1 bar, 4 fs timestep with hydrogen-mass repartitioning) on an RTX 3050 GPU (~100 ns/day). Analyses (RMSD, RMSF, ligand centre-of-mass distance from the pocket, contact persistence at 4 Angstrom) used MDTraj with minimum-image periodic correction. All residue numbers reported here follow the deposited crystal structure (PDB 3GBG); simulation topology files provided with this work were renumbered to the same scheme so that reported residues match the shared coordinates.", { justify: true }));

kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(H("3. Results", HeadingLevel.HEADING_1));
kids.push(H("3.1 Validation: the protocol reproduces the crystallographic pose", HeadingLevel.HEADING_2));
kids.push(P("Redocking palmitoleate reproduced the experimental binding pose to 1.41 A heavy-atom RMSD (< 2.0 A), with a predicted affinity of -7.59 kcal/mol, validating receptor preparation, box placement, and scoring.", { justify: true }));

kids.push(H("3.2 CV lipid panel", HeadingLevel.HEADING_2));
kids.push(P("All 15 CV lipids docked with affinities from -6.90 to -8.78 kcal/mol (Table 1)."));
kids.push(P("Table 1. CV docking (AutoDock Vina 1.2.7), ranked.", { bold: true, size: 19 }));
kids.push(table(["Rank","Lipid","dG (kcal/mol)"], cvRows, [900, 6660, 1800]));

kids.push(H("3.3 CCM lipid panel", HeadingLevel.HEADING_2));
kids.push(P("All 13 CCM lipids docked with affinities from -6.84 to -8.13 kcal/mol (Table 2)."));
kids.push(P("Table 2. CCM docking (AutoDock Vina 1.2.7), ranked.", { bold: true, size: 19 }));
kids.push(table(["Rank","Lipid","dG (kcal/mol)"], ccmRows, [900, 6660, 1800]));

kids.push(...fig("figures/fig1_affinity_bars.png", 624, 340,
  "Figure 1. Predicted ToxT binding affinities for the CV (blue) and CCM (orange) lipid panels."));

kids.push(H("3.4 Structural determinants of binding", HeadingLevel.HEADING_2));
kids.push(P("Across all 22 lipids, affinity correlated most strongly with the number of C=C double bonds (r = -0.87) and chain length (r = -0.70). Lipophilicity, polarity, and flexibility were weak or non-predictive (Table 3, Figure 2).", { justify: true }));
kids.push(P("Table 3. Descriptor-affinity correlations (n = 22).", { bold: true, size: 19 }));
kids.push(table(["Descriptor","Pearson r vs. dG"], descRows, [5360, 4000]));
kids.push(...fig("figures/fig2_unsaturation.png", 470, 370,
  "Figure 2. Binding affinity vs. unsaturation (point color = chain length)."));

kids.push(H("3.5 Free-acid vs. methyl-ester form", HeadingLevel.HEADING_2));
kids.push(P("For every backbone, the free-acid and methyl-ester forms bound with nearly identical affinity (mean |dG| ~ 0.11 kcal/mol; max 0.42 for ALA), within scoring uncertainty (Table 4, Figure 4). ToxT binding is governed by the acyl chain, not the headgroup esterification state; both forms are plausible bioactive species.", { justify: true }));
kids.push(P("Table 4. Acid vs. methyl-ester affinity (kcal/mol); D = ester - acid.", { bold: true, size: 19 }));
kids.push(table(["Backbone","C:db","Acid","Ester","D"], pairRows, [3360, 1500, 1500, 1500, 1500]));

kids.push(H("3.6 Consensus scoring", HeadingLevel.HEADING_2));
kids.push(P("Re-docking with the Vinardo scoring function gave rankings strongly concordant with default Vina (Spearman rho = 0.83, n = 22; Figure 3). The top binders were top-ranked under both functions; the largest disagreement was the long saturated ester methyl heneicosanoate, which Vinardo penalizes more. The ranking is robust to scoring-function choice.", { justify: true }));
kids.push(...fig("figures/fig3_consensus.png", 410, 410,
  "Figure 3. Vina vs. Vinardo affinities; dashed line is y = x."));
kids.push(...fig("figures/fig4_acid_vs_ester.png", 430, 397,
  "Figure 4. Free-acid vs. methyl-ester affinity per backbone; points lie on the y = x line."));

kids.push(H("3.7 Organism comparison", HeadingLevel.HEADING_2));
kids.push(P("Mean predicted affinities were nearly identical between organisms (CV -7.77 vs. CCM -7.64 kcal/mol; difference within scoring error), and best single binders were comparable (CV EPA -8.78; CCM gamma-linolenate -8.13). Per-molecule ToxT-binding strength does not discriminate the two extracts.", { justify: true }));

kids.push(H("3.8 Molecular-dynamics validation of the top complex", HeadingLevel.HEADING_2));
kids.push(P("The top binder EPA was simulated in both free-acid and methyl-ester forms (50 ns each). Both complexes were stable: protein backbone RMSD plateaued rapidly and stayed low (1.87 +/- 0.27 A acid; 1.66 +/- 0.22 A ester), with constant radius of gyration (Figure 5, left). The ligand never left the pocket - its centre of mass stayed 2-4 A from the pocket centre (minimum-image corrected) and was bound in 100% of frames for both forms (Figure 5, right).", { justify: true }));
kids.push(P("Binding was mediated by a persistent residue network (numbering follows PDB 3GBG). For the free acid, Tyr12, Phe22, Leu25, Lys31 and Phe33 maintained contact in ~100% of production frames (Figure 6); the methyl ester engaged an essentially identical set (Tyr12, Tyr20, Phe22, Leu25, Ile27, Phe33, Val81, Tyr266 at ~100%, with Lys31/Arg13 at the head group). This aromatic cage plus hydrophobic wall, capped by the basic Lys31/Arg13 pair, corresponds to the crystallographic fatty-acid pocket and confirms the docked binding mode is dynamically real.", { justify: true }));
kids.push(P("EPA was additionally simulated as its deprotonated carboxylate (dominant at pH 7.4): stable (backbone RMSD 1.82 A) and the most tightly held, with the head group engaging basic residues Lys31, Lys230 and Arg13 ~100% of the time (salt-bridge stabilised). To show this form-independence is a general pocket property rather than an EPA peculiarity, the study was extended to three fatty acids spanning the affinity range - EPA (strong, C20:5), gamma-linolenic (strong, C18:3) and palmitic (weak, C16:0) - each in all three forms: nine 50 ns simulations. Every one gave a stable complex (backbone RMSD 1.5-2.3 A) with the ligand bound 100% of the trajectory (Table 5, Figure 7). Across three fatty acids of differing chain length and unsaturation, and across esterification and protonation state, ToxT retains the ligand; the acyl tail governs occupancy, consistent with the docking structure-property analysis.", { justify: true }));
kids.push(P("Table 5. MD summary of the head-group matrix (nine 50 ns simulations).", { bold: true, size: 19 }));
kids.push(table(["Fatty acid","Form","Backbone RMSD (A)","COM (A)","Bound"],
  [["EPA (C20:5)","free acid","1.87 +/- 0.27","2.6","100%"],
   ["EPA","methyl ester","1.66 +/- 0.22","2.3","100%"],
   ["EPA","carboxylate","1.82 +/- 0.12","1.7","100%"],
   ["g-linolenic (C18:3)","free acid","1.91 +/- 0.17","1.2","100%"],
   ["g-linolenic","methyl ester","2.12 +/- 0.15","2.0","100%"],
   ["g-linolenic","carboxylate","1.65 +/- 0.14","1.9","100%"],
   ["palmitic (C16:0)","free acid","1.96 +/- 0.20","3.4","100%"],
   ["palmitic","methyl ester","2.32 +/- 0.18","3.0","100%"],
   ["palmitic","carboxylate","1.46 +/- 0.13","2.2","100%"]],
  [2260, 1900, 2300, 1400, 1500]));
kids.push(...fig("figures/fig7_md_headgroup_matrix.png", 560, 336,
  "Figure 7. Ligand distance from the pocket (mean over production) for the nine head-group simulations - three fatty acids x three forms. All stay far below the 10 A unbound threshold."));
kids.push(P("Positive (native palmitoleate), negative (glucose decoy; apo ToxT) and weak-binder (pentadecanal, tridecanoic) control simulations are in progress and will be added on completion.", { italic: true, size: 19 }));

kids.push(H("3.9 Blind docking confirms the fatty-acid pocket as the preferred site", HeadingLevel.HEADING_2));
kids.push(P("Because the panel was docked into a predefined box, we verified by blind docking over the entire ToxT surface that this pocket is genuinely preferred, not merely imposed. The protocol was validated by recovery of the native ligand: with no pocket bias, palmitoleate's top pose localized 0.6 A from its crystallographic position (Table 6). For the strongly-binding polyunsaturated lipids every pose fell in the fatty-acid pocket (EPA 15/15, gamma-linolenic 8/8 modes) and no other site scored higher. Palmitic acid placed its single best pose in the pocket (1.5 A) but scattered its remaining poses over the surface (1/20), consistent with weak, non-specific association. Thus strong unsaturated lipids are pocket-selective while saturated lipids bind loosely, mirroring the affinity structure-activity relationship; no competing high-affinity site was detected.", { justify: true }));
kids.push(P("Table 6. Blind docking (whole-protein search) of representative lipids.", { bold: true, size: 19 }));
kids.push(table(["Lipid","Top-pose dG (kcal/mol)","Top pose -> pocket (A)","Modes in pocket"],
  [["EPA","-8.48","2.9","15/15"],
   ["gamma-linolenic acid","-8.30","1.2","8/8"],
   ["palmitic acid","-5.72","1.5","1/20"],
   ["palmitoleate (native, control)","-7.60","0.6","10/13"]],
  [3060, 2400, 2400, 1500]));
kids.push(...fig("figures/fig5_md_stability.png", 624, 244,
  "Figure 5. MD stability (50 ns): protein backbone RMSD (left) and ligand distance from the pocket (right); 10 A dashed line = bound/unbound threshold."));
kids.push(...fig("figures/fig6_md_contacts.png", 430, 307,
  "Figure 6. ToxT residues contacting EPA and their persistence (% of production frames within 4 A)."));

kids.push(H("3.10 Structural basis of binding and control simulations", HeadingLevel.HEADING_2));
kids.push(P("The docked lipids occupy the internal fatty-acid pocket of the ToxT N-terminal domain - an aromatic cage (Tyr12, Tyr20, Phe22, Phe33, Phe69, Tyr266) and hydrophobic wall (Leu/Val/Ile/Met) closed by a basic clamp (Lys31, Lys230, Arg13) that engages the carboxylate head group (Figure 8). Superposition of the full CV and CCM panels shows every lipid converges on this single pocket (Figure 9).", { justify: true }));
kids.push(...fig("figures/fig8_pocket_final.png", 624, 312,
  "Figure 8. ToxT fatty-acid pocket. (A) Whole protein with the pocket highlighted; (B) pocket detail with residues coloured by chemistry (orange aromatic, blue basic, grey hydrophobic) and the native ligand (yellow); dashes mark salt bridges to the carboxylate."));
kids.push(...fig("figures/fig_CV_overlay_final.png", 360, 300,
  "Figure 9A. All 15 CV lipids docked in the ToxT pocket, coloured by binding affinity."));
kids.push(...fig("figures/fig_CCM_overlay_final.png", 360, 300,
  "Figure 9B. All 13 CCM lipids docked in the ToxT pocket, coloured by binding affinity."));
kids.push(P("Three control simulations tested specificity (Table 7). Positive control: the native ligand palmitoleate remained bound throughout (ligand-pocket 1.5 A, 100% of frames), reproducing the crystallographic mode and validating the protocol. Negative control: a glucose decoy docked into the pocket was expelled to the pocket mouth (~8.9 A) and never occupied the core, whereas all fatty acids stayed 1-3 A from the pocket centre (Figure 10) - demonstrating the pocket is fatty-acid selective. The two weakest-docking lipids (pentadecanal, tridecanoic acid) nonetheless formed stable complexes once seated (1.7-2.0 A, 100% bound); thus all cognate lipids are retained, and affinity differences among lipids manifest as reduced pocket-selectivity in blind docking (Section 3.9) rather than reduced MD stability. An apo (ligand-free) run provided a dynamics baseline.", { justify: true }));
kids.push(P("Table 7. Control and weak-binder simulations (50 ns each).", { bold: true, size: 19 }));
kids.push(table(["System","Role","Ligand-pocket (A)","Bound"],
  [["palmitoleate (native)","positive control","1.5","100%"],
   ["glucose","negative control (decoy)","8.9","expelled"],
   ["pentadecanal","weak binder","1.7","100%"],
   ["tridecanoic acid","weak binder","2.0","100%"],
   ["apo ToxT","ligand-free baseline","-","-"]],
  [2760, 2900, 2200, 1500]));
kids.push(...fig("figures/fig10_specificity.png", 600, 347,
  "Figure 10. Ligand-pocket distance over 50 ns: cognate fatty acids and the native ligand stay in the pocket core (green band), while the glucose decoy is held at the pocket mouth (~9 A)."));

kids.push(H("3.11 Comparison with known ToxT ligands", HeadingLevel.HEADING_2));
kids.push(P("Prior computational studies of ToxT ligands used heterogeneous programs and score units (e.g. GOLD fitness scores; MM interaction energies in kJ/mol) that are not directly comparable across methods. To place the algal lipids on a single comparable footing, three reference ToxT ligands were docked under the identical protocol (same box, seed and Vina 1.2.7 scoring): the engineered inhibitor virstatin, the short-chain fatty acid butyrate (a recently reported natural ToxT-targeting compound), and oleic acid (a native-type unsaturated fatty acid). The algal lipids (-6.8 to -8.8 kcal/mol) bound comparably to oleic acid (-7.90) and substantially more strongly than butyrate (-3.71). The purpose-designed inhibitor virstatin scored highest (-10.21), as expected for an engineered scaffold - a value that also partly reflects the docking score's known dependence on aromatic surface area, and virstatin's mechanism (interference with ToxT dimerisation) differs from direct pocket occupancy. Thus these microalgae supply naturally occurring ToxT-pocket binders that engage the site as effectively as its native regulator, without any medicinal-chemistry optimisation (Table 8).", { justify: true }));
kids.push(P("Table 8. Reference ToxT ligands docked under the identical protocol.", { bold: true, size: 19 }));
kids.push(table(["Compound","dG (kcal/mol)","Type"],
  [["virstatin","-10.21","synthetic, engineered inhibitor"],
   ["algal lipids (this study)","-6.8 to -8.8","natural (microalgal)"],
   ["oleic acid","-7.90","native-type unsaturated fatty acid"],
   ["butyric acid","-3.71","natural short-chain fatty acid"]],
  [3060, 2400, 3900]));

kids.push(H("3.12 A modelled ToxT-DNA complex indicates an allosteric mechanism", HeadingLevel.HEADING_2));
kids.push(P("To probe how fatty-acid binding translates into loss of virulence-gene activation, a ToxT-DNA complex was modelled with AlphaFold3 (full-length ToxT plus a 34-bp duplex bearing two direct-repeat toxbox elements). The ToxT fold was predicted with high confidence (pTM 0.85), whereas the protein-DNA interface was of modest confidence (ipTM 0.31); the model is therefore interpreted only at the domain level. The DNA was contacted exclusively by the C-terminal AraC-family helix-turn-helix domain (residues 188-276; e.g. Arg214, Lys235/237, Tyr250, Lys256), while the fatty-acid pocket lies in the N-terminal domain ~30 A away, making no direct contact with the DNA (nearest approach ~6 A; Figure 11). Because the regulatory pocket and the DNA-reading head are on distinct, spatially separated domains, fatty-acid occupancy cannot sterically block DNA binding; the architecture is instead consistent with an allosteric mechanism in which pocket occupancy restrains the inter-domain conformation required for productive DNA engagement - the closed-state model of Lowden et al. (2010). The algal lipids are thus predicted to switch off ToxT-dependent transcription by locking ToxT in a DNA-binding-incompetent conformation rather than by competing with DNA directly.", { justify: true }));
kids.push(...fig("figures/fig11_dna_competition.png", 600, 442,
  "Figure 11. AlphaFold3 model of the ToxT-DNA complex: toxbox DNA (teal), the C-terminal HTH DNA-binding domain (blue, residues 188-276), and the fatty-acid pocket (orange) with the native ligand (yellow, from 3GBG superposition) ~30 A away (red dashes) - supporting an allosteric mechanism. ToxT fold high-confidence (pTM 0.85); DNA pose low-confidence (ipTM 0.31), interpreted only at the domain level."));

kids.push(H("4. Discussion", HeadingLevel.HEADING_1));
kids.push(P("These results support direct engagement of algal lipids with the ToxT fatty-acid pocket as a plausible basis for their antivirulence activity. The protocol is validated (redocking 1.41 A), internally consistent across two scoring functions (rho = 0.83), and yields a clear structure-activity relationship: binding strength increases with acyl-chain unsaturation and length, mirroring the natural ToxT ligand and the Lowden mechanism in which cis double bonds impose the bent geometry that fits the pocket.", { justify: true }));
kids.push(P("Headgroup-independence (acid ~ ester) indicates the carboxylate is not the dominant anchor; the hydrophobic tail and its unsaturation dictate pocket fit. Practically, GC-MS uncertainty about the bioactive form does not undermine the proposed mechanism. Notably, docking does not reproduce the greater in vivo activity of CCM: per-lipid affinities are indistinguishable between organisms. This is expected - docking ranks single molecules at equal concentration, whereas in vivo activity reflects abundance-weighted composition, solubility, permeability, and possible multi-target or synergistic effects. The most likely explanation is that CCM is enriched in abundant strong binders; this is directly testable by combining these affinities with GC-MS relative abundances (planned).", { justify: true }));
kids.push(P("From a translational standpoint, the distinguishing feature of these lipids is not that they are the strongest conceivable ToxT binders - the engineered inhibitor virstatin scores higher - but that they are naturally produced, renewable compounds that engage the validated regulatory pocket as effectively as ToxT's native fatty-acid ligand, with no synthesis or medicinal-chemistry optimisation. Combined with the antivirulence activity previously reported for these microalgal extracts, this positions Chlorella variabilis and Chlorococcum sp. lipids as a natural, cultivable source of ToxT-pocket-directed antivirulence leads.", { justify: true }));

kids.push(H("5. Limitations", HeadingLevel.HEADING_1));
kids.push(P("Docking provides relative hypotheses, not absolute affinities (Vina ~ +/-1-2 kcal/mol); within-tier rank differences should not be over-interpreted. Docking used a single rigid-receptor conformation; MD (top binder, both forms) confirmed the complex is stable, but induced-fit was not explored for the full panel, and MD was run as single 50 ns trajectories (replicates would strengthen statistics). MD covered 13 systems (three fatty acids x three forms, plus positive/negative controls and weak binders) as single 50 ns trajectories; independent replicates and MD of the remaining panel members would further strengthen the statistics. Organism-level interpretation requires quantitative GC-MS abundances, available here only qualitatively (presence/absence), so abundance-weighting remains future work.", { justify: true }));

kids.push(H("6. Reproducibility and data availability", HeadingLevel.HEADING_1));
kids.push(P("All steps are deterministic (seed = 42). Receptor/box: 3GBG_meeko.pdbqt, 3GBG_meeko.box.txt (box enveloping PAM, 5 A padding). Ligand generation: generate_missing_3d.py. Docking: dock_by_organism.py (results_CV/affinities_CV.csv, results_CCM/affinities_CCM.csv). Validation: pam_control.py. Both forms: pairs_pipeline.py. Consensus: consensus_scoring.py. Structure-property: structural_analysis.py.", { justify: true }));

kids.push(H("7. Future work", HeadingLevel.HEADING_1));
kids.push(P("Planned extensions include independent MD replicates for statistics, MD of representative CCM binders, and - contingent on quantitative GC-MS abundances - an abundance-weighted binding score to directly link the docking results to the organism-level bioassay.", { justify: true }));

kids.push(H("References", HeadingLevel.HEADING_1));
[
 "Lowden MJ, et al. Structure of Vibrio cholerae ToxT reveals a mechanism for fatty acid regulation of virulence genes. PNAS 2010;107:2860-2865.",
 "Trott O, Olson AJ. AutoDock Vina: improving the speed and accuracy of docking. J Comput Chem 2010;31:455-461.",
 "Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0. J Chem Inf Model 2021;61:3891-3898.",
 "Quiroga R, Villarreal MA. Vinardo: A scoring function based on AutoDock Vina. PLoS ONE 2016;11:e0155183.",
 "Kim S, et al. PubChem 2023 update. Nucleic Acids Res 2023;51:D1373-D1380.",
 "Landrum G, et al. RDKit: Open-source cheminformatics. https://www.rdkit.org."
].forEach((r, i) => kids.push(new Paragraph({ spacing: { after: 80 },
  children: [new TextRun({ text: (i+1) + ". " + r, size: 19 })] })));

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "2E5496" },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "ToxT-lipid docking study - draft  |  Page ", size: 16 }),
                 new TextRun({ children: [PageNumber.CURRENT], size: 16 })] })] }) },
    children: kids,
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync("ToxT_docking_manuscript.docx", b);
  console.log("Wrote ToxT_docking_manuscript.docx (" + b.length + " bytes)"); });
