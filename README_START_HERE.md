# 🧬 AutoDock Vina Docking Package - START HERE

## Quick Navigation

**Want to run docking immediately?** → Read: `RUN_DOCKING_NOW.md`

**Need detailed explanation?** → Read: `DOCKING_SETUP_GUIDE.md`

**Have technical issues?** → Check: `DOCKING_SETUP_GUIDE.md` (Troubleshooting section)

---

## What You Have

Complete package for docking your 3 algal lipids against ToxT (*Vibrio cholerae* virulence regulator).

### Your Structures
- **Protein:** ToxT (PDB 3GBG) - High-resolution crystal structure (1.90 Å)
- **Lipids:** 
  1. Neophytadiene (terpene)
  2. Polyunsaturated fatty acid methyl ester
  3. Palmitic acid (saturated C16)

### Scientific Context
Your project directly tests the **Lowden et al. (2010) mechanism:**
- ToxT binds fatty acids to regulate virulence genes
- You've shown Chlorella/Chlorococcum lipids have antivirulence activity
- Docking will reveal IF lipid-ToxT binding explains your experimental results

---

## 5-Minute Quick Start

```bash
# Install tools (first time only)
conda create -n autodock python=3.10 -y && conda activate autodock
conda install -c conda-forge autodock-vina meeko rdkit -y

# Run docking
cd AutoDock
python3 quick_dock.py
```

**Done!** Results in `docking_results/` with CSV summary.

---

## What's in This Package

### 📋 Documentation
| File | Purpose |
|------|---------|
| `README_START_HERE.md` | This file - orientation guide |
| `RUN_DOCKING_NOW.md` | **Quick start** - read this first |
| `DOCKING_SETUP_GUIDE.md` | Detailed guide with explanations |

### 🔬 Input Files
| Directory | Contents |
|-----------|----------|
| `structures/` | Your PDB + 3 SDF lipid files |
| | ✓ 3GBG.pdb (ToxT) |
| | ✓ 3 lipid structure files |

### 🛠️ Scripts
| File | Purpose |
|------|---------|
| `quick_dock.py` | **Recommended**: One-command docking |
| `run_docking_workflow.sh` | Bash workflow (Linux/Mac) |
| `analyze_structure.py` | Analyze ToxT binding pocket |
| `parse_docking_results.py` | Parse results into CSV |
| `docking_pipeline.py` | Full pipeline (if all deps available) |

### ⚙️ Configuration Files
| File | Lipid |
|------|-------|
| `docking_configs/config_neophytadiene.txt` | Neophytadiene |
| `docking_configs/config_polyunsaturated_ester.txt` | Polyunsaturated ester |
| `docking_configs/config_palmitic_acid.txt` | Palmitic acid |

All pre-filled with correct parameters and binding pocket coordinates!

### 📊 Output (Will Be Generated)
| Directory | Contents |
|-----------|----------|
| `prepared_structures/` | PDBQT files (protein + ligands) |
| `docking_results/` | Docked poses + logs |
| | ✓ `*_docked.pdbqt` files |
| | ✓ `*.log` files (with affinities) |
| | ✓ `docking_results.csv` |

---

## 🚀 Three Ways to Run

### Option 1: Fully Automated (Easiest)
```bash
python3 quick_dock.py
```
- Auto-installs missing packages
- Prepares all structures
- Runs all 3 dockings
- Parses results
- **No manual steps needed**

### Option 2: Step-by-Step (Recommended for Learning)
```bash
python3 analyze_structure.py              # See binding pocket
meeko -protein structures/3GBG.pdb -o prepared_structures/3GBG_prepared.pdbqt
meeko -ligand structures/*neophytadiene.sdf -o prepared_structures/neophytadiene.pdbqt
# ... prepare other 2 ligands
vina --config docking_configs/config_neophytadiene.txt --out docking_results/neophytadiene_docked.pdbqt --log docking_results/neophytadiene.log
# ... run other 2 dockings
python3 parse_docking_results.py
```

### Option 3: Bash Script (Linux/Mac)
```bash
bash run_docking_workflow.sh
```
- Does everything steps 2 does
- More readable progress output

---

## Expected Results

After docking, you'll get a CSV like:

```
Ligand,Binding_Affinity_kcal_mol,RMSD_lower_bound,RMSD_upper_bound,Ki_nM,Ki_µM,Ki_mM
neophytadiene,-5.80,0.00,20.20,68300.00,68.30,0.07
polyunsaturated_ester,-6.80,0.00,15.50,5400.00,5.40,0.01
palmitic_acid,-5.20,0.00,28.30,135000.00,135.00,0.14
```

### Interpretation
- **ΔG < -8 kcal/mol** = Very strong (likely mechanism)
- **ΔG -8 to -6** = Strong (probable mechanism)
- **ΔG -6 to -5** = Moderate (possible contribution)
- **ΔG > -5** = Weak (less likely)

**For your study:** Look for ΔG < -6 kcal/mol as evidence of mechanism.

---

## After Docking: What's Next?

### 1. Validate Results
Compare docking affinities to your experimental data:
- Does strongest binder have best antivirulence effect?
- Do relative rankings match your in-vitro activity?

### 2. Visualize Binding Modes
```bash
pymol prepared_structures/3GBG_prepared.pdbqt docking_results/*_docked.pdbqt
```

### 3. Plan Validation Experiments
**Without qPCR, consider:**
- **EMSA assay** (test ToxT-DNA binding inhibition) ⭐ Best option
- **Reporter assay** (GFP under virulence promoter)
- **Western blot** (measure ToxT protein levels)

### 4. Write Your Paper
Use docking results + your experimental data to propose mechanism:
> "AutoDock Vina predictions reveal that algal lipids bind ToxT at the 
> characterized fatty acid pocket, consistent with the computational 
> mechanism proposed by Lowden et al. The binding affinities correlate 
> with our experimental antivirulence rankings, supporting direct 
> inhibition of ToxT-mediated virulence gene expression."

---

## Key Reference

**Lowden et al. (2010)** - The foundational paper for your mechanism:
- **Title:** "Structure of *Vibrio cholerae* ToxT reveals a mechanism for fatty acid regulation of virulence genes"
- **Journal:** PNAS 107:2860
- **PubMed:** 20133655
- **Key Finding:** ToxT binds fatty acids → changes virulence gene expression

**Your contribution:** Testing if this mechanism applies to Chlorella/Chlorococcum lipids.

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| `vina: command not found` | See RUN_DOCKING_NOW.md - Prerequisites |
| Installation too slow | Use `conda` instead of `pip` |
| Docking takes forever | Reduce `exhaustiveness` from 16 to 8 |
| ModuleNotFoundError | Run with `conda` environment |
| Config file paths wrong | Use absolute paths in config files |

Full troubleshooting → See `DOCKING_SETUP_GUIDE.md`

---

## File Organization

```
AutoDock/                          # Root directory
├── README_START_HERE.md           # ← You are here
├── RUN_DOCKING_NOW.md             # ← Read next
├── DOCKING_SETUP_GUIDE.md         # ← For detailed info
│
├── structures/                    # Input files
│   ├── 3GBG.pdb
│   ├── *neophytadiene.sdf
│   ├── *Methyl*.sdf
│   └── *palmitic*.sdf
│
├── prepared_structures/           # Will be created by scripts
│   ├── 3GBG_prepared.pdbqt
│   ├── neophytadiene.pdbqt
│   ├── polyunsaturated_ester.pdbqt
│   └── palmitic_acid.pdbqt
│
├── docking_configs/               # Pre-made config files
│   ├── config_neophytadiene.txt
│   ├── config_polyunsaturated_ester.txt
│   └── config_palmitic_acid.txt
│
├── docking_results/               # Will be created during docking
│   ├── neophytadiene_docked.pdbqt
│   ├── neophytadiene.log
│   ├── polyunsaturated_ester_docked.pdbqt
│   ├── polyunsaturated_ester.log
│   ├── palmitic_acid_docked.pdbqt
│   ├── palmitic_acid.log
│   └── docking_results.csv        # ← YOUR RESULTS HERE
│
└── scripts/
    ├── quick_dock.py              # ← BEST: Run this
    ├── analyze_structure.py
    ├── parse_docking_results.py
    ├── docking_pipeline.py
    └── run_docking_workflow.sh
```

---

## Let's Get Started! 🎯

### Right Now:
1. Open terminal/PowerShell in AutoDock directory
2. Read `RUN_DOCKING_NOW.md`
3. Choose Option 1 (`python3 quick_dock.py`) or Option 3 (bash script)
4. Run it!
5. Check `docking_results/docking_results.csv` for your answers

### Time Required:
- **Setup:** 5 minutes (install conda packages)
- **Docking:** 10-20 minutes (on modern computer)
- **Total:** ~30 minutes to have your binding affinities

---

## Questions?

Each file has detailed explanations:
- **Quick overview:** RUN_DOCKING_NOW.md
- **Detailed guide:** DOCKING_SETUP_GUIDE.md
- **Automation:** quick_dock.py (has comments explaining each step)

---

## Good luck with your research! 🧪

Your docking study is directly testing a landmark mechanism (Lowden et al. 2010). 
Exciting work!

**You have everything you need. Just run it!**

---

*Created: June 2026*  
*For: ToxT-Lipid Binding Study*  
*Structures: Chlorella/Chlorococcum lipids vs. V. cholerae ToxT (PDB 3GBG)*
