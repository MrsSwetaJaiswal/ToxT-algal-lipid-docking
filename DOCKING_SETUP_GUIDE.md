# AutoDock Vina Docking Setup Guide
## ToxT-Lipid Binding Study

---

## Overview

You have 3 lipids to dock against ToxT (PDB: 3GBG) from *Vibrio cholerae*.

**Your Lipids:**
1. **Neophytadiene** (C20H32) - a terpene, found in algae
2. **Methyl 3-cis,9-cis,12-cis-octadecatrienoate** (C19H32O2) - polyunsaturated fatty acid methyl ester (algal lipid)
3. **Palmitic acid** (C16H32O2) - saturated fatty acid (common in algae)

**Protein:** ToxT (TCP Pilus Virulence Regulatory Protein) - PDB: 3GBG
- Resolution: 1.90 Å (excellent quality)
- Crystal structure from Lowden et al. (2010) PNAS
- **Key finding:** This structure was solved with bound fatty acids!
- Known to bind lipids and regulate virulence gene expression

---

## Prerequisites

### Installation Requirements

1. **AutoDock Vina** (free, open-source)
   - Download from: http://vina.scripps.edu/
   - Or via conda: `conda install -c conda-forge autodock-vina`

2. **Meeko** (optional, but recommended)
   - Converts ligand/protein formats to PDBQT
   - Install: `pip install meeko`
   - Or: `conda install -c conda-forge meeko`

3. **Python packages:**
   - pandas: `pip install pandas`
   - biopython: `pip install biopython`
   - rdkit: `pip install rdkit` (or `conda install rdkit`)

4. **Visualization tools (optional):**
   - PyMOL (academic license free): https://pymol.org/
   - Chimera: https://www.rbvi.ucsf.edu/chimera/
   - Jmol (free): http://jmol.sourceforge.net/

### Quick Install (conda, all at once):
```bash
conda create -n docking python=3.10
conda activate docking
conda install -c conda-forge autodock-vina meeko rdkit biopython pandas
```

---

## Step-by-Step Docking Workflow

### Step 1: Prepare Protein (ToxT)

Convert 3GBG.pdb to PDBQT format:

```bash
meeko -protein 3GBG.pdb -o 3GBG_prepared.pdbqt
```

**What this does:**
- Adds hydrogens at physiological pH (7.4)
- Assigns Gasteiger partial charges
- Defines atom types for docking scoring function
- Marks rigid vs. rotatable bonds

### Step 2: Prepare Ligands (Lipids)

Convert each SDF file to PDBQT:

```bash
# Lipid 1: Neophytadiene
meeko -ligand "Conformer3D_COMPOUND_CID_10446 neophytadiene.sdf" \
      -o neophytadiene.pdbqt

# Lipid 2: Polyunsaturated fatty acid ester
meeko -ligand "Conformer3D_COMPOUND_CID_91694372 Methyl 3-cis,9-cis,12-cis-octadecatrienoate.sdf" \
      -o polyunsaturated_ester.pdbqt

# Lipid 3: Palmitic acid
meeko -ligand "Conformer3D_COMPOUND_CID_985- palmitic acid.sdf" \
      -o palmitic_acid.pdbqt
```

### Step 3: Identify Binding Pocket

The ToxT structure has a known fatty acid binding pocket. Run analysis:

```bash
python3 analyze_structure.py
```

This will print the binding pocket center coordinates.

### Step 4: Configure Docking

Create or use the provided configuration files (see `config_*.txt` files).

**Example configuration (for neophytadiene):**

```
receptor = 3GBG_prepared.pdbqt
ligand = neophytadiene.pdbqt

center_x = 24.50
center_y = 18.75
center_z = 19.20

size_x = 24.0
size_y = 24.0
size_z = 24.0

exhaustiveness = 16
num_modes = 20
energy_range = 3.0
seed = 42

cpu = 4
```

**Parameter explanation:**
- `center_x, center_y, center_z`: Coordinates of binding pocket center
- `size_*`: Search box dimensions (24×24×24 Å is good for small molecules/lipids)
- `exhaustiveness`: Search thoroughness (16 is balanced; higher = more accurate but slower)
- `num_modes`: Number of binding poses to return (20 gives good diversity)
- `energy_range`: Only report poses within 3 kcal/mol of the best
- `cpu`: Number of CPUs to use

### Step 5: Run Docking

Single lipid:
```bash
vina --config config_neophytadiene.txt --out neophytadiene_docked.pdbqt --log neophytadiene.log
```

All lipids (batch):
```bash
bash run_all_dockings.sh
```

### Step 6: Analyze Results

Extract binding affinities from log files:
```bash
python3 parse_docking_results.py
```

This generates:
- `docking_results.csv` - Summary of all binding affinities
- `docking_summary.txt` - Interpretation of results

---

## Expected Results & Interpretation

### Binding Affinity Scale (kcal/mol)

| Affinity Range | Interpretation | Ki (approx) |
|---|---|---|
| < -8.0 | Very strong binding (drug-like) | < 100 nM |
| -8.0 to -6.0 | Strong binding | 100 nM - 10 µM |
| -6.0 to -5.0 | Moderate binding | 10 - 100 µM |
| -5.0 to -4.0 | Weak binding | 0.1 - 1 mM |
| > -4.0 | Very weak/no binding | > 1 mM |

### For Your Study

**Expected outcomes:**
1. **All three lipids bind ToxT** - supported by Lowden et al. (2010)
2. **Relative binding strengths** may differ:
   - Saturated fatty acids (palmitic) vs. unsaturated (methyl ester) vs. terpene (neophytadiene)
3. **Strongest binder** is likely the polyunsaturated fatty acid methyl ester
4. **Binding site** should be in the lipid-binding pocket identified in PDB 3GBG

### Validation

The docking results directly test the mechanism from Lowden et al.:
- If lipids bind strongly → supports molecular mechanism of antivirulence
- If binding correlates with your in-vitro/in-vivo results → mechanism validated
- Different binding affinities may explain differential activity

---

## File Organization

```
AutoDock/
├── structures/
│   ├── 3GBG.pdb
│   ├── Conformer3D_COMPOUND_CID_10446 neophytadiene.sdf
│   ├── Conformer3D_COMPOUND_CID_91694372 Methyl 3-cis,9-cis,12-cis-octadecatrienoate.sdf
│   └── Conformer3D_COMPOUND_CID_985- palmitic acid.sdf
│
├── prepared_structures/  ← Will be created
│   ├── 3GBG_prepared.pdbqt
│   ├── neophytadiene.pdbqt
│   ├── polyunsaturated_ester.pdbqt
│   └── palmitic_acid.pdbqt
│
├── docking_configs/
│   ├── config_neophytadiene.txt
│   ├── config_polyunsaturated_ester.txt
│   └── config_palmitic_acid.txt
│
├── docking_results/  ← Will be created
│   ├── neophytadiene_docked.pdbqt
│   ├── neophytadiene.log
│   ├── polyunsaturated_ester_docked.pdbqt
│   ├── polyunsaturated_ester.log
│   ├── palmitic_acid_docked.pdbqt
│   ├── palmitic_acid.log
│   ├── docking_results.csv
│   └── docking_summary.txt
│
└── scripts/
    ├── analyze_structure.py
    ├── parse_docking_results.py
    └── run_all_dockings.sh
```

---

## Provided Scripts

### 1. `analyze_structure.py`
Analyzes the ToxT structure to identify binding pocket center.

### 2. `parse_docking_results.py`
Extracts binding affinities from Vina log files and generates results table.

### 3. `run_all_dockings.sh`
Bash script to run all three dockings sequentially.

### 4. `docking_pipeline.py`
Complete automated pipeline (if you have all dependencies installed).

---

## Troubleshooting

### Issue: "vina: command not found"
**Solution:** Ensure AutoDock Vina is in your PATH
- Check: `which vina`
- If not found: add to PATH or use full path to vina executable

### Issue: "ModuleNotFoundError: No module named 'rdkit'"
**Solution:** Install rdkit
```bash
conda install -c conda-forge rdkit
# OR
pip install rdkit
```

### Issue: "Meeko not found or conversion fails"
**Solution:** Use alternative format conversion
- Try: `obabel -isdf file.sdf -opdbqt -O file.pdbqt`
- Or manually prepare PDBQT using AutoDockTools

### Issue: Docking runs but produces no poses
**Solution:** Adjust search box parameters
- Increase `size_x`, `size_y`, `size_z` to 28-30 Å
- Increase `exhaustiveness` to 32
- Check center coordinates are reasonable

---

## Next Steps After Docking

### 1. Visualize Binding Poses
```bash
# In PyMOL:
load 3GBG_prepared.pdbqt
load neophytadiene_docked.pdbqt
color cartoon
zoom neophytadiene
```

### 2. Analyze Interactions
- Which residues contact each lipid?
- Are they the same pocket across all three lipids?
- Do interactions differ by lipid type?

### 3. Correlate with In Vitro/In Vivo Data
- Does strongest binder (lowest ΔG) correlate with best antivirulence effect?
- Does your experimental activity order match docking predictions?

### 4. Write Up Mechanism
**Hypothesis:** Algal lipids inhibit ToxT binding to virulence gene promoters
**Evidence:** 
- Docking affinities (this study)
- ToxT-lipid binding pocket (Lowden et al. structure)
- Your experimental antivirulence data
- Potential: EMSA assay to confirm ToxT-DNA inhibition

---

## Key References

1. **Lowden et al. (2010)** - Structure of Vibrio cholerae ToxT reveals a mechanism for fatty acid regulation of virulence genes
   - PNAS 107:2860
   - PubMed: 20133655
   - **This is the landmark paper showing ToxT-lipid binding**

2. **AutoDock Vina Documentation**
   - http://vina.scripps.edu/
   - Manual: http://vina.scripps.edu/manual.html

3. **Meeko Documentation**
   - https://github.com/forlilab/meeko

---

## Contact & Questions

For issues with the docking setup or interpretation of results, refer to:
- AutoDock Vina manual: http://vina.scripps.edu/manual.html
- Meeko GitHub: https://github.com/forlilab/meeko
- Your computational biology core facility (if available at your institution)

---

**Good luck with your docking study! Your lipid-ToxT interactions are directly testing the Lowden et al. mechanism. Exciting work!**
