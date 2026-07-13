# Docking and molecular dynamics of algal lipids against *Vibrio cholerae* ToxT

Computational companion to *Jaiswal et al.* — molecular docking and all-atom
molecular-dynamics (MD) analysis of fatty-acid / fatty-acid-methyl-ester lipids
from two green microalgae (**CV** = *Chlorella variabilis*, **CCM** =
*Chlorococcum* sp.) against the *Vibrio cholerae* virulence regulator **ToxT**
(PDB **3GBG**).

This repository contains all code, inputs, configurations and small outputs
needed to reproduce the study. Large MD trajectories are archived separately on
Zenodo (see **Data availability** below).

> **Residue numbering.** All residue numbers follow the deposited crystal
> structure (PDB 3GBG). MD topology files shared here (`md/*/system_pub.pdb`)
> were renumbered to the same scheme so reported residues match the coordinates.

---

## What the study does

1. **Docking** of the CV and CCM lipid panels into the ToxT fatty-acid pocket
   (AutoDock Vina 1.2.7; Meeko preparation; pocket box from the co-crystal ligand).
2. **Validation** — native-ligand (palmitoleate) redocking (RMSD 1.41 Å) and
   **blind docking** over the whole protein (confirms the pocket is preferred).
3. **Structure–property analysis** — unsaturation drives affinity (r = −0.87).
4. **Both forms** — free acid vs. methyl ester (form-insensitive).
5. **Consensus scoring** — Vina vs. Vinardo (Spearman ρ = 0.83).
6. **Molecular dynamics** — 50 ns per system; a 3 fatty-acid × 3 form head-group
   matrix, plus **controls**: native ligand (positive), glucose decoy and apo
   protein (negative), and weak-binder contrasts.

---

## Software / environments

Three environments are used (spec files at the repo root):

| Environment | Purpose | Recreate |
|---|---|---|
| `.venv` (Python 3.13, pip) | Meeko ligand/receptor prep, analysis, figures | `pip install -r requirements-prep.txt` |
| conda env `md` (Python 3.11) | OpenMM MD, OpenFF, PDBFixer | `conda env create -f environment-md.yml` |
| conda env `viz` | PyMOL figures | `conda create -n viz -c conda-forge pymol-open-source` |
| Node.js | Word document generation | `npm install` (uses `package.json`) |

**External binary (not in git):** AutoDock Vina 1.2.7 — download `vina.exe`
(and `vina_split.exe`) from the [ccsb-scripps releases](https://github.com/ccsb-scripps/AutoDock-Vina/releases)
into `tools/`.

---

## Reproduce (outline)

```bash
# 1. Ligand + receptor preparation (Meeko)
.venv/Scripts/python.exe generate_missing_3d.py        # build missing 3D structures
#    mk_prepare_receptor / mk_prepare_ligand -> prepared_structures/, ligands_pdbqt/

# 2. Docking (per organism)
.venv/Scripts/python.exe dock_by_organism.py           # -> results_CV/, results_CCM/
.venv/Scripts/python.exe pam_control.py                # native-ligand redocking (1.41 A)
.venv/Scripts/python.exe blind_dock.py                 # whole-protein blind docking
.venv/Scripts/python.exe pairs_pipeline.py             # acid vs ester
.venv/Scripts/python.exe consensus_scoring.py          # Vina vs Vinardo
.venv/Scripts/python.exe structural_analysis.py        # descriptor / affinity correlations

# 3. Molecular dynamics (conda md env)
conda run -n md python md_production.py md/<ligand>_pose.sdf <name> 50   # one 50 ns run
python md_supervisor.py                                # thermal-managed batch of runs

# 4. Analysis + figures
.venv/Scripts/python.exe md_summary.py                 # per-run stability/binding table
.venv/Scripts/python.exe make_specificity_fig.py       # decoy vs cognate figure
conda run -n viz pymol -cq render_docking4.py          # 3D pocket / overlay figures
```

See `HOW_TO_PREP_WITH_MEEKO.md` and `RUN_STEP_BY_STEP.md` for detailed,
copy-paste Windows instructions.

---

## Repository layout

```
structures/            input PDB (3GBG) and PubChem SDF ligands
ligands/               organism-tagged SDFs + RDKit-generated structures
prepared_structures/   Meeko receptor PDBQT, pocket box, native-ligand reference
ligands_pdbqt/         prepared ligand PDBQT files
docking_configs/       Vina configuration (box, seed)
results_CV/ results_CCM/   per-organism docking affinities
results_blind/         blind (whole-protein) docking
results_pairs/         acid-vs-ester docking
results_vinardo/       consensus (Vinardo) scoring
figures/               all manuscript figures (docking + MD + 3D)
md/<run>/              per-run MD topology (system_pub.pdb), logs, analysis
*.py                   pipeline, analysis, MD and figure scripts
build_docx.js          manuscript Word-document generator
MANUSCRIPT_DRAFT.md    working manuscript
```

---

## Key scripts

| Script | Role |
|---|---|
| `dock_by_organism.py` | per-organism docking |
| `pam_control.py` | native-ligand redocking validation |
| `blind_dock.py` | whole-protein blind docking |
| `pairs_pipeline.py` | acid vs. methyl-ester docking |
| `consensus_scoring.py` | Vina vs. Vinardo consensus |
| `structural_analysis.py` | descriptor–affinity correlations |
| `md_production.py` / `md_production_apo.py` | MD with checkpoint/restart |
| `md_supervisor.py` | thermal-managed sequential MD batches |
| `md_summary.py`, `md_figures.py`, `md_contacts_pbc.py`, `make_specificity_fig.py` | MD analysis + figures |
| `renumber_topology.py` | renumber MD topologies to PDB 3GBG numbering |
| `render_docking4.py`, `compose_figures.py` | 3D molecular figures |

---

## Data availability

- **Code, inputs, configs, small outputs, published-numbered topologies** — this
  repository.
- **Full MD trajectories, serialized systems, checkpoints (~1.5–2 GB)** — archived
  on Zenodo: **[DOI: 10.5281/zenodo.XXXXXXX]** *(placeholder — insert after upload)*.

Docking is deterministic (fixed seed = 42). See `DATA_AVAILABILITY.md` for the
manuscript statement and the Zenodo upload checklist.

## Citation

If you use this code, please cite the associated paper (Jaiswal et al.) and the
underlying tools: AutoDock Vina (Eberhardt et al. 2021), Meeko/RDKit, OpenMM
(Eastman et al.), OpenFF, and the Vinardo scoring function (Quiroga & Villarreal 2016).
