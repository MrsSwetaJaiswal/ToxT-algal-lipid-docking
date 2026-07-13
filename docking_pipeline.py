#!/usr/bin/env python3
"""
AutoDock Vina Docking Pipeline
Prepares ToxT protein and lipid ligands, runs docking, and analyzes results
"""

import os
import sys
import subprocess
import re
import pandas as pd
from pathlib import Path
import json

# Define paths
STRUCT_DIR = Path("/sessions/adoring-dazzling-cannon/mnt/AutoDock/structures")
OUTPUT_DIR = Path("/sessions/adoring-dazzling-cannon/mnt/outputs/docking_results")
WORK_DIR = Path("/sessions/adoring-dazzling-cannon/mnt/outputs/docking_work")

# Create working directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

def install_dependencies():
    """Install required Python packages"""
    print("=" * 60)
    print("STEP 1: Installing Dependencies")
    print("=" * 60)

    packages = {
        'rdkit': 'rdkit',
        'meeko': 'meeko',
        'pandas': 'pandas',
        'biopython': 'biopython'
    }

    for import_name, pkg_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {pkg_name} already installed")
        except ImportError:
            print(f"Installing {pkg_name}...", end=" ")
            try:
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', pkg_name,
                     '--break-system-packages', '-q'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("✓")
            except Exception as e:
                print(f"✗ Failed: {e}")
                return False

    # Check for vina
    result = subprocess.run(['which', 'vina'], capture_output=True)
    if result.returncode == 0:
        print("✓ AutoDock Vina installed")
    else:
        print("⚠ AutoDock Vina not found in PATH")
        print("  Installing vina via conda...")
        try:
            subprocess.check_call(
                ['apt-get', 'update'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            subprocess.check_call(
                ['apt-get', 'install', '-y', 'autodock-vina'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✓ AutoDock Vina installed")
        except Exception as e:
            print(f"✗ Could not install Vina: {e}")
            print("  Attempting to install from conda-forge...")
            try:
                subprocess.check_call(
                    ['conda', 'install', '-c', 'conda-forge', 'autodock-vina', '-y'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("✓ AutoDock Vina installed via conda")
            except:
                return False

    print()
    return True


def find_structures():
    """Locate ToxT and lipid files"""
    print("=" * 60)
    print("STEP 2: Locating Structure Files")
    print("=" * 60)

    files = list(STRUCT_DIR.glob("*"))

    toxt_file = None
    lipid_files = []

    for f in files:
        if f.suffix in ['.pdb', '.PDB']:
            toxt_file = f
            print(f"✓ ToxT protein: {f.name}")
        elif f.suffix in ['.sdf', '.SDF', '.mol', '.mol2']:
            lipid_files.append(f)
            print(f"✓ Lipid: {f.name}")

    if not toxt_file:
        print("✗ ERROR: No PDB file found for ToxT")
        return None, []

    if len(lipid_files) == 0:
        print("✗ ERROR: No lipid files found")
        return toxt_file, []

    print()
    return toxt_file, sorted(lipid_files)


def prepare_protein(pdb_file):
    """Convert protein to PDBQT format"""
    print("=" * 60)
    print("STEP 3: Preparing ToxT Protein")
    print("=" * 60)

    try:
        from meeko import MoleculePreparation
        from meeko.utils import PDBQTWriterLegacy
    except ImportError:
        print("✗ meeko import failed. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'meeko',
                              '--break-system-packages', '-q'])
        from meeko import MoleculePreparation
        from meeko.utils import PDBQTWriterLegacy

    pdbqt_file = WORK_DIR / f"{pdb_file.stem}_prepared.pdbqt"

    try:
        print(f"Loading: {pdb_file.name}")
        preparator = MoleculePreparation()
        preparator.prepare(str(pdb_file))

        print(f"Writing: {pdbqt_file.name}")
        writer = PDBQTWriterLegacy()
        writer.write_pdbqt_file(preparator, str(pdbqt_file))

        print(f"✓ ToxT prepared: {pdbqt_file.name}\n")
        return pdbqt_file
    except Exception as e:
        print(f"✗ Error preparing protein: {e}\n")
        # Fallback: convert with meeko command line
        try:
            print("Attempting fallback preparation...")
            subprocess.run(['mk_prepare_ligand.py', '-i', str(pdb_file),
                          '-o', str(pdbqt_file)],
                          capture_output=True, check=True)
            print(f"✓ ToxT prepared (fallback): {pdbqt_file.name}\n")
            return pdbqt_file
        except Exception as e2:
            print(f"✗ Fallback failed: {e2}\n")
            return None


def prepare_ligands(lipid_files):
    """Convert lipids to PDBQT format"""
    print("=" * 60)
    print("STEP 4: Preparing Lipid Ligands")
    print("=" * 60)

    try:
        from meeko import MoleculePreparation
        from meeko.utils import PDBQTWriterLegacy
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'meeko',
                              '--break-system-packages', '-q'])
        from meeko import MoleculePreparation
        from meeko.utils import PDBQTWriterLegacy

    pdbqt_files = {}

    for lipid_file in lipid_files:
        pdbqt_file = WORK_DIR / f"{lipid_file.stem}_prepared.pdbqt"

        try:
            print(f"Loading: {lipid_file.name}", end=" ... ")
            preparator = MoleculePreparation()
            preparator.prepare(str(lipid_file))

            writer = PDBQTWriterLegacy()
            writer.write_pdbqt_file(preparator, str(pdbqt_file))

            print(f"✓")
            pdbqt_files[lipid_file.stem] = pdbqt_file
        except Exception as e:
            print(f"✗ {e}")
            # Fallback: use mk_prepare_ligand.py
            try:
                subprocess.run(['mk_prepare_ligand.py', '-i', str(lipid_file),
                              '-o', str(pdbqt_file)],
                              capture_output=True, check=True, timeout=30)
                print(f"  ✓ Prepared via fallback")
                pdbqt_files[lipid_file.stem] = pdbqt_file
            except Exception as e2:
                print(f"  ✗ Fallback failed: {e2}")

    print()
    return pdbqt_files


def get_binding_pocket(pdb_file):
    """Estimate binding pocket center from protein structure"""
    print("=" * 60)
    print("STEP 5: Identifying Binding Pocket")
    print("=" * 60)

    try:
        from Bio import PDB
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'biopython',
                              '--break-system-packages', '-q'])
        from Bio import PDB

    try:
        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure('protein', str(pdb_file))

        # Get center of mass of all CA atoms
        coords = []
        for chain in structure.get_chains():
            for residue in chain:
                if 'CA' in residue:
                    coords.append(residue['CA'].coord)

        if coords:
            coords = pd.DataFrame(coords)
            center = coords.mean()
            center_x, center_y, center_z = float(center[0]), float(center[1]), float(center[2])

            print(f"Binding pocket center: ({center_x:.2f}, {center_y:.2f}, {center_z:.2f})")
            print()
            return center_x, center_y, center_z
        else:
            print("⚠ Could not parse protein atoms. Using default center (0,0,0)")
            print()
            return 0.0, 0.0, 0.0
    except Exception as e:
        print(f"⚠ Error parsing structure: {e}")
        print("  Using default center (0,0,0)")
        print()
        return 0.0, 0.0, 0.0


def run_docking(receptor_pdbqt, ligand_pdbqt_dict, center_x, center_y, center_z):
    """Run AutoDock Vina for all ligands"""
    print("=" * 60)
    print("STEP 6: Running AutoDock Vina Docking")
    print("=" * 60)

    results = []

    for ligand_name, ligand_pdbqt in ligand_pdbqt_dict.items():
        output_pdbqt = OUTPUT_DIR / f"{ligand_name}_docked.pdbqt"
        log_file = OUTPUT_DIR / f"{ligand_name}_docking.log"
        config_file = WORK_DIR / f"config_{ligand_name}.txt"

        # Create config file
        config_content = f"""receptor = {str(receptor_pdbqt)}
ligand = {str(ligand_pdbqt)}

center_x = {center_x:.2f}
center_y = {center_y:.2f}
center_z = {center_z:.2f}

size_x = 24.0
size_y = 24.0
size_z = 24.0

exhaustiveness = 16
num_modes = 20
energy_range = 3.0
seed = 42

cpu = 4
"""

        with open(config_file, 'w') as f:
            f.write(config_content)

        print(f"Docking {ligand_name}...", end=" ", flush=True)

        try:
            result = subprocess.run(
                ['vina', '--config', str(config_file),
                 '--out', str(output_pdbqt), '--log', str(log_file)],
                capture_output=True,
                timeout=300,
                text=True
            )

            if result.returncode == 0:
                print("✓")
                # Parse binding affinity from log
                affinity = parse_vina_log(log_file)
                results.append({
                    'Lipid': ligand_name,
                    'Binding_Affinity_kcal_mol': affinity,
                    'Output_PDBQT': str(output_pdbqt),
                    'Log_File': str(log_file)
                })
            else:
                print("✗")
                print(f"  Error: {result.stderr[:100]}")
                results.append({
                    'Lipid': ligand_name,
                    'Binding_Affinity_kcal_mol': None,
                    'Output_PDBQT': None,
                    'Error': result.stderr[:100]
                })
        except subprocess.TimeoutExpired:
            print("✗ (timeout)")
            results.append({
                'Lipid': ligand_name,
                'Binding_Affinity_kcal_mol': None,
                'Error': 'Docking timeout'
            })
        except Exception as e:
            print(f"✗ ({str(e)[:50]})")
            results.append({
                'Lipid': ligand_name,
                'Binding_Affinity_kcal_mol': None,
                'Error': str(e)[:100]
            })

    print()
    return results


def parse_vina_log(log_file):
    """Extract best binding affinity from Vina log file"""
    try:
        with open(log_file, 'r') as f:
            content = f.read()
            # Pattern: "   1        -7.2      0.000      0.000"
            match = re.search(r'^\s+1\s+([-\d.]+)', content, re.MULTILINE)
            if match:
                return float(match.group(1))
    except:
        pass
    return None


def analyze_results(results):
    """Analyze and rank docking results"""
    print("=" * 60)
    print("STEP 7: Analyzing Results")
    print("=" * 60)

    df = pd.DataFrame(results)

    # Remove rows with no affinity
    df_valid = df[df['Binding_Affinity_kcal_mol'].notna()].copy()

    if len(df_valid) == 0:
        print("✗ No successful docking runs")
        return df

    # Sort by affinity (more negative = better)
    df_valid = df_valid.sort_values('Binding_Affinity_kcal_mol')

    # Calculate Ki (dissociation constant in µM)
    df_valid['Ki_µM'] = df_valid['Binding_Affinity_kcal_mol'].apply(
        lambda x: exp_estimate_ki(x)
    )

    print("\n📊 DOCKING RESULTS (Ranked by Binding Affinity):\n")
    print(df_valid[['Lipid', 'Binding_Affinity_kcal_mol', 'Ki_µM']].to_string(index=False))
    print()

    # Save to CSV
    csv_file = OUTPUT_DIR / "docking_results.csv"
    df.to_csv(csv_file, index=False)
    print(f"✓ Results saved to: {csv_file}\n")

    return df


def exp_estimate_ki(binding_affinity_kcal_mol):
    """Estimate Ki from binding affinity using exponential approximation"""
    import math
    RT = 0.593  # kcal/(mol·K) × 298K
    try:
        ki_nm = math.exp(binding_affinity_kcal_mol / RT) * 1e9
        ki_um = ki_nm / 1000
        return ki_um
    except:
        return None


def generate_summary_report(results):
    """Generate summary statistics"""
    print("=" * 60)
    print("DOCKING SUMMARY REPORT")
    print("=" * 60)

    df = pd.DataFrame(results)

    successful = len(df[df['Binding_Affinity_kcal_mol'].notna()])
    failed = len(df) - successful

    print(f"\nTotal Lipids Docked: {len(df)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        df_valid = df[df['Binding_Affinity_kcal_mol'].notna()]
        best = df_valid['Binding_Affinity_kcal_mol'].min()
        worst = df_valid['Binding_Affinity_kcal_mol'].max()
        mean = df_valid['Binding_Affinity_kcal_mol'].mean()

        print(f"\nBinding Affinity Statistics (kcal/mol):")
        print(f"  Best:  {best:.2f}")
        print(f"  Worst: {worst:.2f}")
        print(f"  Mean:  {mean:.2f}")

        print(f"\nInterpretation:")
        print(f"  < -8 kcal/mol : Very strong binding")
        print(f"  -8 to -6 kcal/mol : Strong binding (drug-like)")
        print(f"  -6 to -5 kcal/mol : Moderate binding")
        print(f"  > -5 kcal/mol : Weak binding")

    print()


def main():
    print("\n" + "=" * 60)
    print("AUTODOCK VINA LIPID-TOXT DOCKING PIPELINE")
    print("=" * 60 + "\n")

    # Step 1: Install dependencies
    if not install_dependencies():
        print("✗ Failed to install dependencies")
        return

    # Step 2: Find structures
    toxt_file, lipid_files = find_structures()
    if not toxt_file:
        print("✗ Missing required structure files")
        return

    # Step 3: Prepare protein
    receptor_pdbqt = prepare_protein(toxt_file)
    if not receptor_pdbqt:
        print("✗ Failed to prepare protein")
        return

    # Step 4: Prepare ligands
    ligand_pdbqt_dict = prepare_ligands(lipid_files)
    if not ligand_pdbqt_dict:
        print("✗ Failed to prepare ligands")
        return

    # Step 5: Get binding pocket
    center_x, center_y, center_z = get_binding_pocket(toxt_file)

    # Step 6: Run docking
    results = run_docking(receptor_pdbqt, ligand_pdbqt_dict, center_x, center_y, center_z)

    # Step 7: Analyze results
    df_results = analyze_results(results)

    # Summary
    generate_summary_report(results)

    print("=" * 60)
    print("✓ DOCKING COMPLETE")
    print("=" * 60)
    print(f"\nResults saved to: {OUTPUT_DIR}")
    print(f"Working files in: {WORK_DIR}")


if __name__ == "__main__":
    main()
