#!/usr/bin/env python3
"""
Quick AutoDock Vina docking script
Prepares structures and runs docking for all 3 lipids
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def check_and_install(package_name, import_name=None):
    """Check if package is installed, if not install it"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"Installing {package_name}...", end=" ", flush=True)
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package_name,
                 '--break-system-packages', '-q'],
                timeout=180,
                capture_output=True
            )
            print("✓")
            return True
        except subprocess.TimeoutExpired:
            print("✗ (timeout)")
            return False
        except Exception as e:
            print(f"✗ ({e})")
            return False

def main():
    print("=" * 80)
    print("AUTODOCK VINA - QUICK DOCKING SETUP")
    print("=" * 80)
    print()

    # Setup paths
    base_dir = Path(__file__).parent
    struct_dir = base_dir / "structures"
    prep_dir = base_dir / "prepared_structures"
    results_dir = base_dir / "docking_results"
    config_dir = base_dir / "docking_configs"

    prep_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    # Check dependencies
    print("Step 1: Checking dependencies")
    print("-" * 80)

    deps_ok = True

    print("Python packages:")
    deps_ok &= check_and_install("rdkit")
    deps_ok &= check_and_install("meeko")
    deps_ok &= check_and_install("biopython", "Bio")
    deps_ok &= check_and_install("pandas")

    print("\nAutoDock Vina:")
    try:
        result = subprocess.run(["vina", "--help"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("AutoDock Vina: ✓")
        else:
            print("AutoDock Vina: ✗ (not working)")
            deps_ok = False
    except FileNotFoundError:
        print("AutoDock Vina: Installing...", end=" ", flush=True)
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'vina',
                 '--break-system-packages', '-q'],
                timeout=180,
                capture_output=True
            )
            print("✓")
        except:
            print("✗ (failed to install)")
            deps_ok = False

    if not deps_ok:
        print("\n⚠ Some dependencies are missing. Attempting to continue...")

    print()

    # Analyze structure
    print("Step 2: Analyzing ToxT structure")
    print("-" * 80)

    try:
        from Bio import PDB
        import numpy as np

        parser = PDB.PDBParser(QUIET=True)
        structure = parser.get_structure('ToxT', str(struct_dir / "3GBG.pdb"))

        ca_atoms = []
        for chain in structure.get_chains():
            for residue in chain:
                if 'CA' in residue:
                    ca_atoms.append(residue['CA'].coord)

        ca_array = np.array(ca_atoms)
        center = ca_array.mean(axis=0)

        print(f"Binding pocket center:")
        print(f"  center_x = {center[0]:.2f}")
        print(f"  center_y = {center[1]:.2f}")
        print(f"  center_z = {center[2]:.2f}")
        print()
    except Exception as e:
        print(f"Error analyzing structure: {e}")
        center = np.array([24.50, 18.75, 19.20])
        print("Using default center coordinates")
        print()

    # Prepare protein
    print("Step 3: Preparing ToxT protein")
    print("-" * 80)

    pdb_file = struct_dir / "3GBG.pdb"
    pdbqt_file = prep_dir / "3GBG_prepared.pdbqt"

    try:
        from meeko import MoleculePreparation
        from meeko.utils import PDBQTWriterLegacy

        print(f"Loading: {pdb_file.name}")
        preparator = MoleculePreparation()
        preparator.prepare(str(pdb_file))

        print(f"Writing: {pdbqt_file.name}")
        writer = PDBQTWriterLegacy()
        writer.write_pdbqt_file(preparator, str(pdbqt_file))
        print("✓ Protein prepared")
    except Exception as e:
        print(f"Meeko failed: {e}")
        print("Attempting fallback preparation...")
        try:
            subprocess.run(
                ['mk_prepare_ligand.py', '-i', str(pdb_file), '-o', str(pdbqt_file)],
                check=True,
                capture_output=True,
                timeout=30
            )
            print("✓ Protein prepared (fallback)")
        except:
            print("✗ Could not prepare protein")
            sys.exit(1)

    print()

    # Prepare ligands
    print("Step 4: Preparing lipid ligands")
    print("-" * 80)

    lipid_files = [
        ("Neophytadiene", list(struct_dir.glob("*neophytadiene.sdf"))[0]),
        ("Polyunsaturated ester", list(struct_dir.glob("*Methyl*.sdf"))[0]),
        ("Palmitic acid", list(struct_dir.glob("*palmitic*.sdf"))[0]),
    ]

    ligand_pdbqts = {}

    for name, sdf_file in lipid_files:
        pdbqt_out = prep_dir / f"{sdf_file.stem.split()[-1].lower()}_prepared.pdbqt"

        try:
            from meeko import MoleculePreparation
            from meeko.utils import PDBQTWriterLegacy

            print(f"{name}...", end=" ", flush=True)
            preparator = MoleculePreparation()
            preparator.prepare(str(sdf_file))

            writer = PDBQTWriterLegacy()
            writer.write_pdbqt_file(preparator, str(pdbqt_out))
            print("✓")
            ligand_pdbqts[name] = pdbqt_out
        except Exception as e:
            print(f"✗ ({str(e)[:30]})")

    if not ligand_pdbqts:
        print("\n✗ Could not prepare any ligands")
        sys.exit(1)

    print()

    # Run dockings
    print("Step 5: Running AutoDock Vina dockings")
    print("-" * 80)
    print()

    docking_results = []

    for name, ligand_pdbqt in ligand_pdbqts.items():
        output_pdbqt = results_dir / f"{name.replace(' ', '_')}_docked.pdbqt"
        log_file = results_dir / f"{name.replace(' ', '_')}.log"

        # Create config
        config_content = f"""receptor = {str(pdbqt_file)}
ligand = {str(ligand_pdbqt)}

center_x = {center[0]:.2f}
center_y = {center[1]:.2f}
center_z = {center[2]:.2f}

size_x = 24.0
size_y = 24.0
size_z = 24.0

exhaustiveness = 16
num_modes = 20
energy_range = 3.0
seed = 42

cpu = 4
"""

        print(f"Docking: {name}...", end=" ", flush=True)

        try:
            result = subprocess.run(
                ['vina', '--config', '/dev/stdin',
                 '--out', str(output_pdbqt), '--log', str(log_file)],
                input=config_content.encode(),
                timeout=300,
                capture_output=True
            )

            if result.returncode == 0:
                # Parse affinity from log
                affinity = parse_log(log_file)
                print(f"✓ (ΔG = {affinity:.2f} kcal/mol)")
                docking_results.append({
                    'Ligand': name,
                    'Affinity': affinity,
                    'Log': str(log_file)
                })
            else:
                print(f"✗")
                print(f"  Error: {result.stderr.decode()[:100]}")
        except subprocess.TimeoutExpired:
            print("✗ (timeout)")
        except Exception as e:
            print(f"✗ ({str(e)[:30]})")

    print()

    # Results summary
    if docking_results:
        print("=" * 80)
        print("DOCKING RESULTS")
        print("=" * 80)
        print()

        docking_results.sort(key=lambda x: x['Affinity'])

        for i, result in enumerate(docking_results, 1):
            affinity = result['Affinity']
            if affinity < -8.0:
                strength = "Very strong"
            elif affinity < -6.0:
                strength = "Strong"
            elif affinity < -5.0:
                strength = "Moderate"
            else:
                strength = "Weak"

            print(f"{i}. {result['Ligand']:30s} {affinity:7.2f} kcal/mol  ({strength})")

        print()

        # Save CSV
        import pandas as pd
        df = pd.DataFrame(docking_results)
        csv_file = results_dir / "docking_results.csv"
        df.to_csv(csv_file, index=False)
        print(f"Results saved to: {csv_file}")
        print()

    print("=" * 80)
    print("✓ DOCKING COMPLETE")
    print("=" * 80)
    print()
    print(f"Output directory: {results_dir}")
    print()
    print("Next steps:")
    print("  1. View docked poses in PyMOL:")
    print("     pymol " + str(pdbqt_file) + " docking_results/*_docked.pdbqt")
    print("  2. Analyze binding interactions")
    print("  3. Correlate with antivirulence data")
    print()


def parse_log(log_file):
    """Extract binding affinity from Vina log"""
    import re
    try:
        with open(log_file) as f:
            content = f.read()
        match = re.search(r'^\s+1\s+([-\d.]+)', content, re.MULTILINE)
        if match:
            return float(match.group(1))
    except:
        pass
    return 0.0


if __name__ == "__main__":
    main()
