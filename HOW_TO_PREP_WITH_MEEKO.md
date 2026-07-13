# How to Prepare Inputs with Meeko & Define the Pocket Box

Everything below runs from the project root:
```powershell
cd "C:\Users\ASUS\Claude\Projects\AutoDock"
```

---

## 0. One-time environment setup
Meeko is a Python tool, installed in an isolated virtual environment (uses your Python 3.13):
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install meeko rdkit scipy numpy
```
The tools then live at:
- `.venv\Scripts\mk_prepare_ligand.exe`  (ligand prep, reads SDF directly)
- `.venv\Scripts\mk_prepare_receptor.exe` (receptor prep + box generation)

Optional: activate the env so you can type the short names (`mk_prepare_ligand`):
```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 1. Ligand PDBQT (from SDF)
Use the FULL real filenames (they contain spaces, so keep the double quotes):
```powershell
.\.venv\Scripts\mk_prepare_ligand.exe -i "structures\Conformer3D_COMPOUND_CID_10446 neophytadiene.sdf" -o "prepared_structures\neophytadiene.pdbqt"

.\.venv\Scripts\mk_prepare_ligand.exe -i "structures\Conformer3D_COMPOUND_CID_91694372 Methyl 3-cis,9-cis,12-cis-octadecatrienoate.sdf" -o "prepared_structures\polyunsaturated_ester.pdbqt"

.\.venv\Scripts\mk_prepare_ligand.exe -i "structures\Conformer3D_COMPOUND_CID_985- palmitic acid.sdf" -o "prepared_structures\palmitic_acid.pdbqt"
```
- `-i` : input SDF (must have 3D coordinates + hydrogens; PubChem SDFs do)
- `-o` : output PDBQT
- Meeko auto-assigns AutoDock atom types, Gasteiger charges, and rotatable bonds.
- TIP: type the start of the path and press Tab to auto-complete long filenames.

---

## 2. Clean the protein (receptor = protein only)
Vina needs protein with NO water and NO bound ligand. Split the PDB:
```bash
# protein only (removes HOH waters and the PAM ligand)
grep -E "^(ATOM|TER)" structures/3GBG.pdb > prepared_structures/3GBG_protein_only.pdb

# the co-crystallized fatty acid (palmitoleic acid), used to locate the pocket
grep "^HETATM" structures/3GBG.pdb | grep " PAM " > prepared_structures/pam_ref.pdb
```
(In PowerShell you can use `Select-String` instead of `grep`, or just run these in the Bash shell.)

---

## 3. Receptor PDBQT + pocket box (one command)
```powershell
.\.venv\Scripts\mk_prepare_receptor.exe `
  --read_pdb prepared_structures\3GBG_protein_only.pdb `
  -o prepared_structures\3GBG_meeko `
  -p -v `
  --box_enveloping prepared_structures\pam_ref.pdb `
  --padding 5
```
Flags:
- `--read_pdb` : input protein PDB (no ProDy needed)
- `-o`         : output basename
- `-p`         : write receptor `.pdbqt`
- `-v`         : write Vina box config `.box.txt`
- `--box_enveloping pam_ref.pdb` : build the box around the crystal ligand = the real pocket
- `--padding 5` : add 5 Angstrom margin on each side

Outputs:
- `3GBG_meeko.pdbqt`   <- receptor for Vina
- `3GBG_meeko.box.txt` <- center_x/y/z + size_x/y/z (the docking box)
- `3GBG_meeko.box.pdb` <- box you can load in PyMOL to visualize

### Why this box?
The box must enclose the binding site. By enveloping the crystal fatty acid `PAM`,
the box is anchored to where ToxT actually binds fatty acids (the Lowden pocket),
instead of being guessed. This is the single most important factor for valid results.

---

## 4. Run the docking (Vina 1.2.7)
```powershell
.\tools\vina.exe --config docking_configs\vina_config.txt `
  --ligand prepared_structures\neophytadiene.pdbqt `
  --out docking_results\neophytadiene_docked.pdbqt
```
`vina_config.txt` holds the receptor + box + search settings (exhaustiveness, seed, etc.).
The top pose's affinity is the first `REMARK VINA RESULT` line in the output `.pdbqt`,
or the mode-1 row in the printed table.

Fixed `seed = 42` makes runs reproducible.

---

## Quick reference: finding a pocket box without a crystal ligand
If a structure has NO bound ligand to envelope, alternatives:
- `--box_center X Y Z --box_size X Y Z` : type coordinates manually
- Center on a known catalytic/binding residue's coordinates
- Use a pocket-detection tool (e.g. fpocket) to get coordinates first
