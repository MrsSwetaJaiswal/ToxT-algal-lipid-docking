# Run the Whole Docking Yourself — Step by Step (Windows)

IMPORTANT: Do NOT use `grep` — that is a Linux command and does not exist on Windows.
Every command below works in either Command Prompt (cmd) or PowerShell.

Always start by going to the project folder:
```
cd "C:\Users\ASUS\Claude\Projects\AutoDock"
```

---

## STEP 1 — Prepare the 3 ligands (SDF -> PDBQT)
Copy each line exactly (the quotes matter because filenames have spaces):

```
.\.venv\Scripts\mk_prepare_ligand.exe -i "structures\Conformer3D_COMPOUND_CID_10446 neophytadiene.sdf" -o "prepared_structures\neophytadiene.pdbqt"

.\.venv\Scripts\mk_prepare_ligand.exe -i "structures\Conformer3D_COMPOUND_CID_91694372 Methyl 3-cis,9-cis,12-cis-octadecatrienoate.sdf" -o "prepared_structures\polyunsaturated_ester.pdbqt"

.\.venv\Scripts\mk_prepare_ligand.exe -i "structures\Conformer3D_COMPOUND_CID_985- palmitic acid.sdf" -o "prepared_structures\palmitic_acid.pdbqt"
```
Each should say:  `PDBQT files written: 1`

---

## STEP 2 — Split the protein and the pocket ligand (replaces grep)
```
.\.venv\Scripts\python.exe split_pdb.py
```
Should print:
```
Wrote prepared_structures/3GBG_protein_only.pdb  (2126 protein lines)
Wrote prepared_structures/pam_ref.pdb  (18 ligand atoms)
```

---

## STEP 3 — Prepare the receptor + auto-make the pocket box
Run this as ONE command. In cmd, paste it on one line (remove the back-ticks).
PowerShell version (the ` lets you wrap lines):
```
.\.venv\Scripts\mk_prepare_receptor.exe `
  --read_pdb prepared_structures\3GBG_protein_only.pdb `
  -o prepared_structures\3GBG_meeko `
  -p -v `
  --box_enveloping prepared_structures\pam_ref.pdb `
  --padding 5
```
cmd version (all on ONE line):
```
.\.venv\Scripts\mk_prepare_receptor.exe --read_pdb prepared_structures\3GBG_protein_only.pdb -o prepared_structures\3GBG_meeko -p -v --box_enveloping prepared_structures\pam_ref.pdb --padding 5
```
Creates:
- `prepared_structures\3GBG_meeko.pdbqt`   (receptor)
- `prepared_structures\3GBG_meeko.box.txt` (the box)

---

## STEP 4 — Dock each ligand (Vina 1.2.7)
```
.\tools\vina.exe --config docking_configs\vina_config.txt --ligand prepared_structures\neophytadiene.pdbqt --out docking_results\neophytadiene_docked.pdbqt

.\tools\vina.exe --config docking_configs\vina_config.txt --ligand prepared_structures\polyunsaturated_ester.pdbqt --out docking_results\poly_ester_docked.pdbqt

.\tools\vina.exe --config docking_configs\vina_config.txt --ligand prepared_structures\palmitic_acid.pdbqt --out docking_results\palmitic_docked.pdbqt
```
The first `REMARK VINA RESULT` line in each output file (or the mode-1 row on screen) is the
binding affinity in kcal/mol.

Expected (reproducible, seed=42):
- neophytadiene        ~ -8.1
- polyunsaturated_ester~ -8.0
- palmitic_acid        ~ -7.3

---

## Notes
- If a command "is not recognized": you probably used a Linux command (grep/awk/cat).
  Use the Windows steps above instead.
- The `.\` at the front means "in this folder" - keep it.
- To type long filenames fast: type the first letters and press Tab.
