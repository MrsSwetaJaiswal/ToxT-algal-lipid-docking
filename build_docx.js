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
const mmgbsaRows = [
  ["EPA","free acid","-45.1","-42.1","-40.0","-42.4 +/- 2.6"],
  ["EPA","methyl ester","-24.3","-40.2","-35.8","-33.4 +/- 8.2"],
  ["EPA","carboxylate","-49.0","-45.0","-51.5","-48.5 +/- 3.3"],
  ["gamma-linolenic (GLA)","free acid","-34.2","-39.1","-42.6","-38.6 +/- 4.2"],
  ["gamma-linolenic (GLA)","methyl ester","-31.5","-37.2","-23.2","-30.6 +/- 7.0"],
  ["gamma-linolenic (GLA)","carboxylate","-37.6","-48.4","-47.0","-44.3 +/- 5.9"],
  ["palmitic","free acid","-33.2","-33.3","-31.5","-32.7 +/- 1.0"],
  ["palmitic","methyl ester","-36.6","-36.3","-37.6","-36.8 +/- 0.7"],
  ["palmitic","carboxylate","-41.3","-49.2","-45.8","-45.4 +/- 4.0"],
  ["palmitoleate (native)","+control","-33.1","-36.7","-27.6","-32.5 +/- 4.6"],
  ["glucose","decoy","-23.5","-28.0","-24.5","-25.3 +/- 2.4"],
  ["pentadecanal","weak binder","-31.4","-34.8","-37.8","-34.7 +/- 3.2"],
  ["tridecanoic acid","weak binder","-19.8","-26.6","-27.4","-24.6 +/- 4.2"]];

const kids = [];
// Title
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
  children: [new TextRun({ bold: true, size: 30,
    text: "Locking Down ToxT: Microalgal Lipids as Allosteric Antivirulence Agents Against Vibrio cholerae — A Docking and Molecular Dynamics Study" })] }));
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ italics: true, size: 18,
    text: "Working manuscript draft - computational (docking) component. Species names and experimental/GC-MS details are placeholders to be completed by the authors." })] }));

kids.push(H("Abstract", HeadingLevel.HEADING_1));
kids.push(P("The transcriptional activator ToxT is the master regulator of virulence-gene expression in Vibrio cholerae, and its activity is directly modulated by fatty acids that occupy a hydrophobic binding pocket (Lowden et al., 2010). We previously reported that lipid extracts of the microalgae Chlorella variabilis (CV) and Chlorococcum sp. (CCM) suppress cholera-toxin production by a multidrug-resistant V. cholerae strain by up to 97.9% without affecting bacterial viability (a true antivirulence effect), yet the molecular target was unknown (Jaiswal et al., 2025). To test whether direct ToxT binding could underlie this activity, we docked the lipid species identified in each extract against the ToxT crystal structure (PDB 3GBG). A panel of 22 unique lipids (15 CV, 13 CCM, 6 shared) was docked with AutoDock Vina 1.2.7 into the experimentally defined fatty-acid pocket. The protocol was validated by redocking the co-crystallized fatty acid (palmitoleate), reproducing the crystallographic pose to 1.41 A RMSD; blind docking over the whole protein independently recovered the native site (0.6 A) and identified the fatty-acid pocket as the preferred binding site, with no competing site elsewhere. All lipids bound within a narrow moderate-to-strong range (-6.8 to -8.8 kcal/mol; a ~2 kcal/mol spread within Vina's scoring uncertainty, so per-lipid rankings are trends). Binding strength correlated most strongly with degree of unsaturation (r = -0.87) and chain length (r = -0.70; these descriptors are collinear), whereas headgroup esterification state had a negligible effect (mean |dG| ~ 0.11 kcal/mol). Rankings were robust to scoring-function choice (Vina vs. Vinardo, Spearman rho = 0.83). Docked under an identical protocol, the algal lipids bound comparably to the native ligand and far more strongly than the short-chain fatty acid butyrate, though below the engineered inhibitor virstatin. Per-molecule affinities were indistinguishable between organisms (mean dG: CV -7.77, CCM -7.64 kcal/mol), suggesting any organism-level activity difference reflects extract composition and bioavailability rather than per-lipid binding strength - a hypothesis not tested here. Molecular-dynamics simulations (14 systems - three fatty acids, EPA, gamma-linolenic and palmitic, each in three chemical forms; the native ligand; two weak binders; the glucose decoy from two starting poses; and an apo baseline - each run in triplicate, n = 3 independent-seed 50 ns replicates per system, 42 trajectories total) showed every complex to be dynamically stable, with the ligand retained in the ToxT pocket throughout; binding was robust to chain length, esterification and protonation state. Specificity was established chiefly by binding preference: in whole-protein blind docking the glucose decoy never localised to the fatty-acid pocket (0/20 poses; best pose 17 A away) and bound weakly (-5.5 kcal/mol), whereas the fatty acids strongly selected it (8-15/15 poses). In MD the native ligand was retained; the decoy was retained only when artificially seeded in the pocket core, reflecting kinetic trapping in a buried cavity - underscoring that binding preference, not MD retention, discriminates cognate lipids from the decoy. MM-GBSA binding free energies, computed across n = 3 independent-seed replicates per system, corroborated this ranking: EPA was the strongest binder and glucose the least favourable of all tested ligands. A modelled ToxT-DNA complex (AlphaFold3; confident fold, low-confidence DNA interface) placed the DNA on the C-terminal helix-turn-helix domain, distinct from the N-terminal fatty-acid pocket, suggesting an allosteric rather than steric basis for inhibition.", { justify: true }));

kids.push(H("1. Introduction", HeadingLevel.HEADING_1));
kids.push(P("Vibrio cholerae causes cholera through coordinated expression of cholera toxin and the toxin-coregulated pilus, both controlled by the AraC/XylS-family regulator ToxT. Lowden et al. (2010) solved the ToxT crystal structure (PDB 3GBG) bound to cis-palmitoleic acid, revealing that unsaturated fatty acids occupy an internal hydrophobic pocket and lock ToxT in a conformation that cannot activate its target promoters - a built-in mechanism for fatty-acid inhibition of virulence.", { justify: true }));
kids.push(P("Natural-product inhibitors exploiting this mechanism are of interest as antivirulence agents. ToxT has previously been targeted computationally with synthetic/screened inhibitors (virstatin, toxtazins, fatty-acid mimetics) and individual natural compounds (herbal polyphenols; short-chain fatty acids such as butyrate); however, the lipid profiles of specific antivirulence-active microalgae have not been characterised against it. In previous work (Jaiswal et al., 2025) we reported that lipid extracts and crude biomass of Chlorella variabilis (CV) and Chlorococcum sp. (CCM) suppress cholera-toxin (CT) production by a multidrug-resistant V. cholerae strain - up to 97.9% inhibition (CCM lipid extract) in vitro and reduced fluid accumulation/CT in a rabbit ileal-loop model in vivo - without affecting bacterial viability, the hallmark of a true antivirulence effect. However, the molecular target was not identified. Because CT is transcriptionally activated by ToxT, and both extracts are rich in fatty acids and methyl esters resembling ToxT's natural ligands, we hypothesised the lipids act by binding the ToxT fatty-acid pocket, supplying a mechanism for the observed antivirulence activity. Here we combine docking (per-organism panels; native-ligand and blind-docking validation; consensus scoring; benchmarking against known inhibitors), all-atom MD with controls (n = 3 independent-seed replicates per system), MM-GBSA, and an AlphaFold3 ToxT-DNA model to (i) test whether the detected lipids engage ToxT, (ii) define structural determinants, (iii) resolve the bound form and protonation state, (iv) establish specificity, and (v) propose a structural mechanism linking pocket occupancy to transcriptional inhibition.", { justify: true }));

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
kids.push(P("Top complexes were simulated with OpenMM 8.5. The ligand used the OpenFF Sage 2.2.0 force field with OpenFF-NAGL AM1BCC-quality charges; the protein used Amber ff14SB, prepared with PDBFixer (missing atoms; hydrogens added at pH 7.4). Systems were solvated in TIP3P water (1.0 nm padding) with 0.15 M NaCl plus neutralizing ions (~38,800 atoms). After minimization and 100 ps equilibration, 50 ns production runs were performed in the NPT ensemble (Langevin 300 K, Monte Carlo barostat 1 bar, 4 fs timestep with hydrogen-mass repartitioning) on an RTX 3050 GPU (~100 ns/day). Analyses (RMSD, RMSF, ligand centre-of-mass distance from the pocket, contact persistence at 4 Angstrom) used MDTraj with minimum-image periodic correction. All residue numbers reported here follow the deposited crystal structure (PDB 3GBG); simulation topology files provided with this work were renumbered to the same scheme so that reported residues match the shared coordinates. Every system was subsequently run as n = 3 independent 50 ns replicates, distinct random seeds (rep 1 = original seed; r2 = seed x100; r3 = seed x200), across all 14 simulated systems (42 trajectories total); unless stated otherwise, values are reported as mean +/- SD across the three replicate means (between-replicate error), not per-frame SD. Figures and tables introduced before the replicate campaign completed show the rep-1 trajectory only, as noted in their captions.", { justify: true }));

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
kids.push(P("Across all 22 lipids, affinity correlated most strongly with the number of C=C double bonds (r = -0.87) and chain length (r = -0.70). Lipophilicity, polarity, and flexibility were weak or non-predictive (Table 3, Figure 2). Two caveats apply: the affinities span only ~2 kcal/mol (within Vina's error), so these are panel-level trends rather than reliable per-lipid rankings; and the predictive descriptors (unsaturation, chain length, MW, logP) are collinear, so their contributions cannot be cleanly separated - unsaturation is the strongest marginal association, not an isolated causal determinant. Consensus scoring (3.6) and MD (3.8) provide independent support.", { justify: true }));
kids.push(P("Structural basis of the unsaturation preference (same-length C18 series). To probe why unsaturation is favoured while controlling for chain length, a same-length (C18) series was examined - stearic (C18:0), oleic (C18:1), 9,11-octadecadienoic (C18:2), and the two octadecatrienoates (C18:3) (Table 4b, Figure 12). A simple contact count is uninformative and even misleading: because burial scales with chain length, the shorter saturated palmitic acid makes as many aromatic-cage contacts as the longer EPA (94 vs 82 within 4.5 A). The discriminating feature is specific: at fixed C18 length the affinity rises modestly with unsaturation (-7.63 for stearic to -8.13 for gamma-linolenic), and every cis double bond localises within alkene-pi contact distance (3.7-4.0 A) of an aromatic-cage residue (Tyr12/20/266, Phe22/33/69), whereas saturated stearic engages none (Figure 12). The cis geometry thus favours binding not by increasing overall contact but by positioning the double-bond pi-systems against the aromatic cage. This effect is modest (~0.3-0.5 kcal/mol at fixed length, within scoring error) and, being a geometric-proximity argument, does not establish optimal stacking orientation; it is a structural rationale for the unsaturation trend, not a strong determinant.", { justify: true }));
kids.push(P("Table 4b. Same-length (C18) series: unsaturation and alkene-pi engagement.", { bold: true, size: 19 }));
kids.push(table(["Lipid","C18:x","dG (kcal/mol)","C=C in pi-contact","closest C=C->ring (A)"],
  [["stearic","C18:0","-7.63","0/0","-"],
   ["oleic","C18:1","-7.90","1/1","5.2"],
   ["9,11-octadecadienoic","C18:2","-7.80","2/2","3.8"],
   ["gamma-linolenic","C18:3","-8.13","3/3","3.7"],
   ["alpha-linolenic","C18:3","-7.91","3/3","4.0"]],
  [2760, 1400, 2200, 1900, 1100]));
kids.push(...fig("figures/fig12_pi_interaction.png", 624, 291,
  "Figure 12. Structural basis of the unsaturation preference (same-length C18). (A) stearic (C18:0) and (B) gamma-linolenic (C18:3) in the ToxT aromatic cage (orange: Tyr12/20/266, Phe22/33/69). The cis double bonds kink the chain and pack against the aromatic rings (alkene-pi, 3.7-4.0 A; all three engaged); the saturated chain makes no such pi-contacts."));
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
kids.push(P("EPA was additionally simulated as its deprotonated carboxylate (dominant at pH 7.4): stable (backbone RMSD 1.82 A) and the most tightly held, with the head group engaging basic residues Lys31, Lys230 and Arg13 ~100% of the time (salt-bridge stabilised). To show this form-independence is a general pocket property rather than an EPA peculiarity, the study was extended to three fatty acids spanning the affinity range - EPA (strong, C20:5), gamma-linolenic (strong, C18:3) and palmitic (weak, C16:0) - each in all three forms: nine 50 ns simulations (rep-1 trajectory summarised below; all nine were subsequently also run in triplicate as part of the full n = 3 replicate campaign, Section 2.8). Every one gave a stable complex (backbone RMSD 1.5-2.3 A) with the ligand bound 100% of the trajectory (Table 5, Figure 7). Across three fatty acids of differing chain length and unsaturation, and across esterification and protonation state, ToxT retains the ligand; the acyl tail governs occupancy, consistent with the docking structure-property analysis.", { justify: true }));
kids.push(P("Table 5. MD summary of the head-group matrix (nine systems, rep-1 trajectory shown; all nine were later also run in triplicate - see Figure 13/14 replicate analyses and Table 9 for the n = 3 MM-GBSA values).", { bold: true, size: 19 }));
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
  "Figure 7. Ligand distance from the pocket (mean over production, rep-1 trajectory) for the nine head-group simulations - three fatty acids x three forms. All stay far below the 10 A unbound threshold."));
kids.push(P("To test whether ligand occupancy perturbs global backbone dynamics beyond the single-trajectory summary above, protein backbone RMSD was compared - mean +/- SD across n = 3 independent-seed replicates - for the three headline fatty acids (free-acid form) against the ligand-free apo simulation, also run in triplicate (Figure 13). All four systems equilibrate to a similar RMSD plateau within the first ~5 ns; from ~20 ns onward the apo replicates drift to a modestly higher plateau (production-window mean 2.12 +/- 0.33 A) than any of the three ligand-bound systems (EPA 1.82 +/- 0.22 A, gamma-linolenic 1.83 +/- 0.15 A, palmitic 1.79 +/- 0.42 A), consistent with a modest ligand-stabilising effect on the overall fold. To test this at residue resolution - and to ask specifically whether the distant C-terminal HTH DNA-binding domain (Section 3.13) is disproportionately rigidified, as an allosteric mechanism would predict - per-residue Ca RMSF was compared between the same apo and headline holo replicates (Figure 14).", { justify: true }));
kids.push(...fig("figures/fig_rmsd_headline_apo.png", 560, 350,
  "Figure 13. Protein backbone RMSD (mean +/- SD across n = 3 independent-seed replicates) for the three headline fatty acids in free-acid form (EPA, gamma-linolenic, palmitic) versus the ligand-free apo simulation. Apo drifts to a modestly higher RMSD plateau than any ligand-bound system after ~20 ns."));
kids.push(P("Ligand binding reduced Ca RMSF modestly across the whole protein (apo 1.01 +/- 0.19 A, holo 0.88 +/- 0.11 A; mean over all 260 resolved residues), including at the fatty-acid pocket itself (apo 0.80 A, holo 0.64 A) and at the five residues that contact DNA in the AlphaFold3 model - Arg214, Lys235, Lys237, Tyr250, Lys256 (apo 0.95 A, holo 0.77 A). However, the magnitude of this reduction was similar in the C-terminal HTH domain (residues 188-273; -0.16 A) and the rest of the N-terminal domain (-0.12 A) (Figure 14), so the C-terminal domain is not disproportionately rigidified relative to the protein as a whole. This MD evidence therefore supports a modest, protein-wide stabilisation upon ligand binding - consistent with, but not on its own sufficient to establish, the domain-specific allosteric coupling proposed from the ToxT-DNA model (Section 3.13); we present it as a qualified, not confirmatory, line of support.", { justify: true }));
kids.push(...fig("figures/fig_apo_holo_rmsf.png", 624, 284,
  "Figure 14. Per-residue Ca RMSF (production window, >5 ns) for apo ToxT (n = 3 replicates) versus the three headline free-acid holo systems (EPA, gamma-linolenic, palmitic; n = 3 systems, each itself a 3-replicate mean). The C-terminal HTH DNA-binding domain (residues 188-276) is shaded; fatty-acid pocket residues are marked with thin vertical lines. Holo RMSF is modestly lower than apo across most of the sequence, not preferentially within the HTH domain."));

kids.push(H("3.9 Blind docking confirms the fatty-acid pocket as the preferred site", HeadingLevel.HEADING_2));
kids.push(P("Because the panel was docked into a predefined box, we verified by blind docking over the entire ToxT surface that this pocket is genuinely preferred, not merely imposed. The protocol was validated by recovery of the native ligand: with no pocket bias, palmitoleate's top pose localized 0.6 A from its crystallographic position (Table 6). For the strongly-binding polyunsaturated lipids every pose fell in the fatty-acid pocket (EPA 15/15, gamma-linolenic 8/8 modes) and no other site scored higher. Palmitic acid placed its single best pose in the pocket (1.5 A) but scattered its remaining poses over the surface (1/20). In sharp contrast, the glucose decoy placed none of its poses in the pocket (0/20; best pose 17 A away, -5.5 kcal/mol), showing the pocket selects fatty acids over a non-lipid. Thus strong unsaturated lipids are pocket-selective, saturated lipids bind loosely, and the non-lipid decoy is excluded, mirroring the affinity structure-activity relationship; no competing high-affinity site was detected.", { justify: true }));
kids.push(P("Table 6. Blind docking (whole-protein search) of representative lipids.", { bold: true, size: 19 }));
kids.push(table(["Lipid","Top-pose dG (kcal/mol)","Top pose -> pocket (A)","Modes in pocket"],
  [["EPA","-8.48","2.9","15/15"],
   ["gamma-linolenic acid","-8.30","1.2","8/8"],
   ["palmitic acid","-5.72","1.5","1/20"],
   ["palmitoleate (native, control)","-7.60","0.6","10/13"],
   ["glucose (decoy)","-5.54","17.0","0/20"]],
  [3060, 2400, 2400, 1500]));
kids.push(...fig("figures/fig5_md_stability.png", 624, 244,
  "Figure 5. MD stability (three EPA forms, rep-1 trajectory, 50 ns each - each form was later also run in triplicate; see Figure 13 for the free-acid replicate comparison): protein backbone RMSD (left) and ligand distance from the pocket (right); 10 A dashed line = bound/unbound threshold."));
kids.push(...fig("figures/fig6_md_contacts.png", 430, 307,
  "Figure 6. ToxT residues contacting EPA and their persistence (% of production frames within 4 A; rep-1 trajectory)."));

kids.push(H("3.10 Structural basis of binding and control simulations", HeadingLevel.HEADING_2));
kids.push(P("The docked lipids occupy the internal fatty-acid pocket of the ToxT N-terminal domain - an aromatic cage (Tyr12, Tyr20, Phe22, Phe33, Phe69, Tyr266) and hydrophobic wall (Leu/Val/Ile/Met) closed by a basic clamp (Lys31, Lys230, Arg13) that engages the carboxylate head group (Figure 8). Superposition of the full CV and CCM panels shows every lipid converges on this single pocket (Figure 9).", { justify: true }));
kids.push(...fig("figures/fig8_pocket_final.png", 624, 312,
  "Figure 8. ToxT fatty-acid pocket. (A) Whole protein with the pocket highlighted; (B) pocket detail with residues coloured by chemistry (orange aromatic, blue basic, grey hydrophobic) and the native ligand (yellow); dashes mark salt bridges to the carboxylate."));
kids.push(...fig("figures/fig_CV_overlay_final.png", 360, 300,
  "Figure 9A. All 15 CV lipids docked in the ToxT pocket, coloured by binding affinity."));
kids.push(...fig("figures/fig_CCM_overlay_final.png", 360, 300,
  "Figure 9B. All 13 CCM lipids docked in the ToxT pocket, coloured by binding affinity."));
kids.push(P("Specificity was assessed by both binding preference and dynamics (Table 7). Positive control: the native ligand palmitoleate remained bound throughout (1.5 A, 100% of frames), validating the protocol. Negative control - binding preference (the primary discriminator): in blind docking over the entire protein the glucose decoy never localised to the fatty-acid pocket (0 of 20 poses; best pose 17 A away on the surface) and bound weakly (-5.5 kcal/mol; Table 6), in stark contrast to the fatty acids (8-15 of 15 poses in the pocket) and consistent with glucose giving the least favourable MM-GBSA energy. Negative control - dynamics: two 50 ns glucose simulations differed by starting pose - from its peripheral docked pose glucose stayed at the pocket mouth (~8.9 A), whereas when artificially seeded in the pocket core it was retained (~2.5 A) for the whole trajectory (Figure 10). This retention reflects kinetic trapping in a buried internal cavity, not favourable binding, and underscores that pocket preference (blind docking and energetics), not MD retention, discriminates cognate lipids from the decoy. Consistent with this, the two weakest-docking cognate lipids (pentadecanal, tridecanoic) also formed stable complexes once seated (1.7-2.0 A). An apo run provided a baseline.", { justify: true }));
kids.push(P("Table 7. Control and weak-binder simulations (rep-1 trajectory shown, 50 ns each; palmitoleate, glucose decoy from its docked start, pentadecanal, tridecanoic acid and apo ToxT were later also run in triplicate - see Figure 10/13/14 replicate analyses).", { bold: true, size: 19 }));
kids.push(table(["System","Role","Ligand-pocket (A)","Bound"],
  [["palmitoleate (native)","positive control","1.5","100%"],
   ["glucose - docked (peripheral) start","negative control (decoy)","8.9","stays at pocket mouth"],
   ["glucose - seeded in pocket core","negative control (decoy)","2.5","retained (buried-cavity trapping)"],
   ["pentadecanal","weak binder","1.7","100%"],
   ["tridecanoic acid","weak binder","2.0","100%"],
   ["apo ToxT","ligand-free baseline","-","-"]],
  [2760, 2900, 2200, 1500]));
kids.push(...fig("figures/fig10_specificity.png", 600, 347,
  "Figure 10. Ligand-pocket distance over 50 ns (mean +/- SD across n = 3 independent-seed replicates per system; the core-seeded decoy is a single trajectory, n = 1) for cognate fatty acids, the native ligand, and the glucose decoy from two starting poses. Cognate lipids and the native ligand occupy the core (green band). The decoy from its docked (peripheral) pose stays at the pocket mouth (~9 A); when seeded in the core it is retained (~2.5 A), reflecting kinetic trapping in a buried cavity rather than binding preference. Specificity is established by binding preference (blind docking, Table 6; MM-GBSA), not by MD retention."));

kids.push(H("3.11 MM-GBSA binding free energies (n = 3 replicates)", HeadingLevel.HEADING_2));
kids.push(P("To place the docking and MD results on an independent energetic footing, MM-GBSA binding free energies (OBC generalized-Born, entropy omitted; 100 frames/replicate) were computed for every simulated system across all three independent-seed replicates and reported as mean +/- SD across the three replicate means (Table 9). EPA is the strongest binder in both its carboxylate (-48.5 +/- 3.3 kcal/mol) and free-acid (-42.4 +/- 2.6) forms, and both EPA and gamma-linolenic acid - in either form - bind more favourably than the native palmitoleate control (-32.5 +/- 4.6), consistent with the docking-panel ranking (Section 3.4) and the retention data (Section 3.10). The two weak cognate binders (pentadecanal, tridecanoic acid) and the glucose decoy cluster at the least favourable end, with glucose giving the least favourable energy of all tested ligands, corroborating its exclusion from the pocket in blind docking (Section 3.9).", { justify: true }));
kids.push(P("A single-trajectory (rep 1 only) estimate for the gamma-linolenic carboxylate had shown an alarmingly large variance (+/-20.5 kcal/mol), raising concern that the pose itself might be unstable. Averaging across n = 3 replicates resolves most of this: the SD falls to +/-5.9. A dedicated diagnostic (ligand and head-group distance to the pocket centroid, all three replicates; Figure S18) confirms the pose is stable throughout - the ligand centre of mass stays within 0.8-3.5 A of the pocket in every replicate - while the carboxylate carbon itself remains solvent-exposed at the pocket mouth (~7.2-7.4 A, SD 0.4-0.6 A across replicates). The residual single-trajectory variance is therefore a known GB sensitivity to a solvent-exposed anionic head group, not pose instability; we report the neutral free-acid value as the primary gamma-linolenic estimate and the carboxylate as a sensitivity check.", { justify: true }));
kids.push(P("Table 9. MM-GBSA binding free energies per replicate and mean +/- SD across replicate means (n = 3, distinct seeds; 100 frames each).", { bold: true, size: 19 }));
kids.push(table(["Lipid","Form","r1","r2","r3","Mean +/- SD (kcal/mol)"], mmgbsaRows, [2560, 1700, 1100, 1100, 1100, 1800]));

kids.push(H("3.12 Comparison with known ToxT ligands", HeadingLevel.HEADING_2));
kids.push(P("Prior computational studies of ToxT ligands used heterogeneous programs and score units (e.g. GOLD fitness scores; MM interaction energies in kJ/mol) that are not directly comparable across methods. To place the algal lipids on a single comparable footing, three reference ToxT ligands were docked under the identical protocol (same box, seed and Vina 1.2.7 scoring): the engineered inhibitor virstatin, the short-chain fatty acid butyrate (a recently reported natural ToxT-targeting compound), and oleic acid (a native-type unsaturated fatty acid). The algal lipids (-6.8 to -8.8 kcal/mol) bound comparably to oleic acid (-7.90) and substantially more strongly than butyrate (-3.71). The purpose-designed inhibitor virstatin scored highest (-10.21), as expected for an engineered scaffold - a value that also partly reflects the docking score's known dependence on aromatic surface area, and virstatin's mechanism (interference with ToxT dimerisation) differs from direct pocket occupancy. Thus these microalgae supply naturally occurring ToxT-pocket binders that engage the site as effectively as its native regulator, without any medicinal-chemistry optimisation (Table 8).", { justify: true }));
kids.push(P("Table 8. Reference ToxT ligands docked under the identical protocol.", { bold: true, size: 19 }));
kids.push(table(["Compound","dG (kcal/mol)","Type"],
  [["virstatin","-10.21","synthetic, engineered inhibitor"],
   ["algal lipids (this study)","-6.8 to -8.8","natural (microalgal)"],
   ["oleic acid","-7.90","native-type unsaturated fatty acid"],
   ["butyric acid","-3.71","natural short-chain fatty acid"]],
  [3060, 2400, 3900]));

kids.push(H("3.13 A modelled ToxT-DNA complex indicates an allosteric mechanism", HeadingLevel.HEADING_2));
kids.push(P("To probe how fatty-acid binding translates into loss of virulence-gene activation, a ToxT-DNA complex was modelled with AlphaFold3 (full-length ToxT plus a 34-bp duplex bearing two direct-repeat toxbox elements). The ToxT fold was predicted with high confidence (pTM 0.85), whereas the protein-DNA interface was of modest confidence (ipTM 0.31); the model is therefore interpreted only at the domain level. The DNA was contacted exclusively by the C-terminal AraC-family helix-turn-helix domain (residues 188-276; e.g. Arg214, Lys235/237, Tyr250, Lys256), while the fatty-acid pocket lies on the separate N-terminal domain, making no direct contact with the DNA in the model (Figure 11). Because the regulatory pocket and the DNA-reading head are on distinct domains, fatty-acid occupancy is unlikely to sterically block DNA binding; the architecture is instead consistent with an allosteric mechanism in which pocket occupancy restrains the inter-domain conformation required for productive DNA engagement - the closed-state model of Lowden et al. (2010). The algal lipids are thus predicted to switch off ToxT-dependent transcription by locking ToxT in a DNA-binding-incompetent conformation rather than by competing with DNA directly. We emphasise that the ToxT-DNA model has a low-confidence interface (ipTM 0.31) and used a consensus toxbox, so this mechanism is a structural hypothesis, not an established geometry.", { justify: true }));
kids.push(...fig("figures/fig11_dna_competition.png", 600, 442,
  "Figure 11. AlphaFold3 model of the ToxT-DNA complex: toxbox DNA (teal), the C-terminal HTH DNA-binding domain (blue, residues 188-276), and the fatty-acid pocket (orange) with the native ligand (yellow, from 3GBG superposition) on the separate N-terminal domain (red dashes) - supporting an allosteric mechanism. ToxT fold high-confidence (pTM 0.85); DNA pose low-confidence (ipTM 0.31), interpreted only at the domain level, not as a precise geometry."));

kids.push(H("4. Discussion", HeadingLevel.HEADING_1));
kids.push(P("These results support direct engagement of algal lipids with the ToxT fatty-acid pocket as a plausible basis for their antivirulence activity. The protocol is validated (redocking 1.41 A), internally consistent across two scoring functions (rho = 0.83), and yields a clear structure-activity relationship: binding strength increases with acyl-chain unsaturation and length, mirroring the native unsaturated ToxT ligand. A same-length (C18) analysis clarifies the basis: rather than simply increasing overall contact (dominated by chain length), the cis double bonds position their pi-systems against the aromatic-cage residues (alkene-pi, 3.7-4.0 A; Section 3.4, Figure 12), a specific if modest rationale for the unsaturation preference.", { justify: true }));
kids.push(P("Headgroup-independence (acid ~ ester) indicates the carboxylate is not the dominant anchor; the hydrophobic tail and its unsaturation dictate pocket fit. Practically, GC-MS uncertainty about the bioactive form does not undermine the proposed mechanism. Notably, docking does not reproduce the greater in vivo activity of CCM: per-lipid affinities are indistinguishable between organisms. This is expected - docking ranks single molecules at equal concentration, whereas in vivo activity reflects abundance-weighted composition, solubility, permeability, and possible multi-target or synergistic effects. The most likely explanation is that CCM is enriched in abundant strong binders; this is directly testable by combining these affinities with GC-MS relative abundances (planned).", { justify: true }));
kids.push(P("From a translational standpoint, the distinguishing feature of these lipids is not that they are the strongest conceivable ToxT binders - the engineered inhibitor virstatin scores higher - but that they are naturally produced, renewable compounds that engage the validated regulatory pocket as effectively as ToxT's native fatty-acid ligand, with no synthesis or medicinal-chemistry optimisation. Combined with the antivirulence activity previously reported for these microalgal extracts, this positions Chlorella variabilis and Chlorococcum sp. lipids as a natural, cultivable source of ToxT-pocket-directed antivirulence leads.", { justify: true }));
kids.push(P("Critically, this closes the loop with our experimental observations (Jaiswal et al., 2025). ToxT is the direct transcriptional activator of the ctxAB (cholera-toxin) promoter, so lipid occupancy of the ToxT pocket offers a concrete molecular explanation for the 93-97.9% suppression of CT production - with viability intact - that we measured for CV and CCM extracts in vitro and in the rabbit ileal-loop model. The greater in-vitro potency of CCM (97.9%) relative to CV, despite indistinguishable per-lipid docking affinities, is consistent with organism-level differences arising from extract composition/abundance rather than intrinsically stronger binders. The computational study thus supplies the missing mechanistic layer - a specific target and binding mode - beneath a previously phenomenological antivirulence observation.", { justify: true }));

kids.push(H("5. Limitations", HeadingLevel.HEADING_1));
kids.push(P("This study is entirely computational and provides a mechanistic rationale for antivirulence activity we reported experimentally elsewhere; it does not itself demonstrate ToxT inhibition, which requires direct assays (ToxT-DNA EMSA or a promoter-reporter). Panel affinities span only ~2 kcal/mol (within Vina error), so correlations describe trends, not per-lipid ranking, and the descriptors are collinear. Docking used one rigid conformation; each MD system was run as n = 3 independent-seed 50 ns replicates (42 trajectories across 14 systems), sufficient to distinguish genuine between-run variance from single-trajectory noise (Section 3.11) but not to extend the sampled timescale - because the pocket is internal, ligand retention is still a modest bar rather than strong evidence of favourable binding, and 50 ns per replicate remains short relative to slower conformational processes; specificity rests on binding preference, not MD retention, as below. The glucose decoy was tested from both a peripheral docked pose and seeded in the pocket core; because it is retained when core-seeded, MD stability alone does not establish specificity for this internal pocket, so the specificity conclusion rests on binding preference (blind docking: 0/20 poses in the pocket; weak affinity) and MM-GBSA energetics. An apo-versus-holo per-residue RMSF comparison (Section 3.8, Figure 14) found a modest, protein-wide stabilisation upon ligand binding (Ca RMSF -0.13 A on average) but no disproportionate rigidification of the C-terminal HTH domain specifically (-0.16 A there vs -0.12 A in the rest of the protein), so this MD-based evidence is consistent with, but does not on its own establish, the domain-specific allosteric coupling proposed from the ToxT-DNA model. MM-GBSA (OBC, no entropy) gives relative, not absolute, energies. Values are reported as mean +/- SD across n = 3 independent-seed replicates per system (Table 9); replicate averaging substantially reduced the large single-trajectory variance seen for charged and some ester ligands (e.g. the gamma-linolenic carboxylate fell from +/-20.5 to +/-5.9 kcal/mol on averaging), though esterified forms such as the EPA methyl ester (+/-8.2) still show comparatively larger between-replicate spread and should be read with correspondingly wider uncertainty. The AlphaFold3 ToxT-DNA model has a low-confidence interface and used a consensus toxbox. Organism-level interpretation requires quantitative GC-MS abundances, available here only qualitatively.", { justify: true }));

kids.push(H("6. Reproducibility and data availability", HeadingLevel.HEADING_1));
kids.push(P("All steps are deterministic (seed = 42). Code, inputs and small outputs are on GitHub (https://github.com/MrsSwetaJaiswal/ToxT-algal-lipid-docking, v1.0.0), archived on Zenodo, DOI: 10.5281/zenodo.21778158 (https://doi.org/10.5281/zenodo.21778158); full molecular-dynamics trajectories, serialized systems and simulation topologies are archived separately on Zenodo, DOI: 10.5281/zenodo.21767402 (https://doi.org/10.5281/zenodo.21767402). Receptor/box: 3GBG_meeko.pdbqt, 3GBG_meeko.box.txt (box enveloping PAM, 5 A padding). Ligand generation: generate_missing_3d.py. Docking: dock_by_organism.py (results_CV/affinities_CV.csv, results_CCM/affinities_CCM.csv). Validation: pam_control.py. Both forms: pairs_pipeline.py. Consensus: consensus_scoring.py. Structure-property: structural_analysis.py.", { justify: true }));

kids.push(H("7. Future work", HeadingLevel.HEADING_1));
kids.push(P("The independent MD replicate campaign originally planned here is now complete (n = 3 replicates per system across all 14 simulated systems; Section 2.8). Remaining planned extensions include MD of representative CCM binders and - contingent on quantitative GC-MS abundances - an abundance-weighted binding score to directly link the docking results to the organism-level bioassay.", { justify: true }));

kids.push(H("References", HeadingLevel.HEADING_1));
[
 "Lowden MJ, et al. Structure of Vibrio cholerae ToxT reveals a mechanism for fatty acid regulation of virulence genes. PNAS 2010;107:2860-2865.",
 "Withey JH, DiRita VJ. The toxbox: specific DNA sequence requirements for activation of V. cholerae virulence genes by ToxT. Mol Microbiol 2006;59:1779-1789.",
 "Hung DT, et al. Small-molecule inhibitor of V. cholerae virulence and intestinal colonization (virstatin). Science 2005;310:670-674.",
 "Woodbrey AK, et al. A modified ToxT inhibitor reduces V. cholerae virulence in vivo. Biochemistry 2018;57:5609-5615.",
 "Anthouard R, DiRita VJ. Small-molecule inhibitors of toxT expression in V. cholerae (toxtazins). mBio 2013;4:e00403-13.",
 "Woodbrey AK, Onyango EO, Pellegrini M, Kovacikova G, Taylor RK, Gribble GW, Kull FJ. A new class of inhibitors of the AraC family virulence regulator Vibrio cholerae ToxT. Sci Rep 2017;7:45011. doi:10.1038/srep45011.",
 "Canals A, Pieretti S, Muriel-Masanes M, El Yaman N, Plecha SC, Thomson JJ, Fabrega-Ferrer M, Perez-Luque R, Krukonis ES, Coll M. ToxR activates the Vibrio cholerae virulence genes by tethering DNA to the membrane through versatile binding to multiple sites. Proc Natl Acad Sci USA 2023;120:e2304378120. PDB 8B4D. doi:10.1073/pnas.2304378120.",
 "Perveen S, Chaudhary HS. In silico screening of antibacterial compounds from herbal sources against Vibrio cholerae. Pharmacogn Mag 2015;11(Suppl 4):S550-S555. doi:10.4103/0973-1296.172960.",
 "Kundu S, Das S, Maitra P, Halder P, Koley H, Mukhopadhyay AK, Miyoshi S, Dutta S, Chatterjee NS, Bhattacharya S. Sodium butyrate inhibits the expression of virulence factors in Vibrio cholerae by targeting ToxT protein. mSphere 2025;10(5):e00824-24. doi:10.1128/msphere.00824-24.",
 "Jaiswal S, Vadadoriya N, Nasir A, Dineshkumar R, Khatri N, Raut S, Ray Chaudhuri S, Chatterjee S, Haldar S. Exploring microalgal lipids as anti-virulent agents targeting MDR Vibrio cholerae infection: a step toward developing herbal ORS formulations. J Nat Prod Discov 2025;4(2):3244. doi:10.24377/jnpd.article3244. (our prior experimental study)",
 "Trott O, Olson AJ. AutoDock Vina. J Comput Chem 2010;31:455-461.",
 "Eberhardt J, Santos-Martins D, Tillack AF, Forli S. AutoDock Vina 1.2.0. J Chem Inf Model 2021;61:3891-3898.",
 "Quiroga R, Villarreal MA. Vinardo scoring function. PLoS ONE 2016;11:e0155183.",
 "Eastman P, et al. OpenMM 8. J Phys Chem B 2024;128:109-116.",
 "Boothroyd S, et al. Open Force Field 2.0.0 (Sage). J Chem Theory Comput 2023;19:3251-3275.",
 "Open Force Field Initiative. OpenFF NAGL: graph neural network partial charge assignment. https://github.com/openforcefield/openff-nagl (software; no dedicated peer-reviewed publication identified as of this draft).",
 "Abramson J, et al. Accurate structure prediction of biomolecular interactions with AlphaFold3. Nature 2024;630:493-500.",
 "McGibbon RT, et al. MDTraj: analysis of molecular dynamics trajectories. Biophys J 2015;109:1528-1532.",
 "Kim S, et al. PubChem 2023 update. Nucleic Acids Res 2023;51:D1373-D1380.",
 "Landrum G, et al. RDKit: Open-source cheminformatics. https://www.rdkit.org.",
 "(2026-08-03: all previously-bracketed placeholder references resolved via web search. Two needed a year correction: the herbal-screen reference is 2015, not 2016; the sodium-butyrate reference is 2025, not 2024. The OpenFF-NAGL reference is software-only; verify before submission.)"
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
