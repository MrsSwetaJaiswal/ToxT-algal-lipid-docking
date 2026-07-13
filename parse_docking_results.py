#!/usr/bin/env python3
"""
Parse AutoDock Vina docking results and generate summary report
"""

import re
import sys
from pathlib import Path
import pandas as pd
import math

def parse_vina_log(log_file):
    """Extract binding affinity and RMSD from Vina log file"""
    try:
        with open(log_file, 'r') as f:
            content = f.read()

        # Pattern: "   1        -7.2      0.000      0.000"
        # Mode, Affinity, RMSD_lb, RMSD_ub
        match = re.search(r'^\s+1\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', content, re.MULTILINE)
        if match:
            affinity = float(match.group(1))
            rmsd_lb = float(match.group(2))
            rmsd_ub = float(match.group(3))
            return affinity, rmsd_lb, rmsd_ub
    except Exception as e:
        print(f"Error parsing {log_file}: {e}")
    return None, None, None


def calculate_ki(binding_affinity_kcal_mol):
    """
    Estimate Ki from binding affinity
    Using: ΔG = RT ln(Ki)
    Where: R = 1.987e-3 kcal/(mol·K), T = 298.15 K
    So: RT = 0.593 kcal/mol
    """
    if binding_affinity_kcal_mol is None:
        return None
    try:
        RT = 0.593
        ki_nm = math.exp(binding_affinity_kcal_mol / RT) * 1e9
        ki_um = ki_nm / 1000
        return ki_um
    except:
        return None


def main():
    results_dir = Path(__file__).parent / "docking_results"

    if not results_dir.exists():
        print(f"Error: {results_dir} not found")
        print("Make sure docking has been completed first")
        sys.exit(1)

    print("=" * 80)
    print("AUTODOCK VINA DOCKING RESULTS SUMMARY")
    print("=" * 80)
    print()

    # Find all log files
    log_files = list(results_dir.glob("*.log"))

    if not log_files:
        print("No log files found in docking_results/")
        sys.exit(1)

    results = []

    print("Parsing log files...\n")

    for log_file in sorted(log_files):
        ligand_name = log_file.stem
        affinity, rmsd_lb, rmsd_ub = parse_vina_log(log_file)

        if affinity is not None:
            ki = calculate_ki(affinity)
            print(f"✓ {ligand_name}")
            print(f"  Binding affinity: {affinity:.2f} kcal/mol")
            print(f"  Ki (estimated): {ki:.2e} M ({ki*1e6:.2f} µM)")
            print(f"  RMSD: {rmsd_lb:.2f} - {rmsd_ub:.2f} Å")
            print()

            results.append({
                'Ligand': ligand_name,
                'Binding_Affinity_kcal_mol': affinity,
                'RMSD_lower_bound': rmsd_lb,
                'RMSD_upper_bound': rmsd_ub,
                'Ki_nM': ki * 1e9,
                'Ki_µM': ki * 1e6,
                'Ki_mM': ki * 1e3
            })
        else:
            print(f"✗ {ligand_name} - Could not parse")
            print()

    if not results:
        print("No valid results found")
        sys.exit(1)

    # Create DataFrame and sort by binding affinity
    df = pd.DataFrame(results)
    df = df.sort_values('Binding_Affinity_kcal_mol')

    print("=" * 80)
    print("RANKING BY BINDING AFFINITY (Strongest to Weakest)")
    print("=" * 80)
    print()

    for idx, (i, row) in enumerate(df.iterrows(), 1):
        print(f"{idx}. {row['Ligand']}")
        print(f"   Binding Affinity: {row['Binding_Affinity_kcal_mol']:8.2f} kcal/mol")
        print(f"   Ki (estimated):   {row['Ki_µM']:8.2f} µM")
        print(f"   Interpretation:  ", end="")

        affinity = row['Binding_Affinity_kcal_mol']
        if affinity < -8.0:
            print("Very strong (drug-like)")
        elif affinity < -6.0:
            print("Strong")
        elif affinity < -5.0:
            print("Moderate")
        elif affinity < -4.0:
            print("Weak")
        else:
            print("Very weak/no binding")
        print()

    # Save to CSV
    csv_file = results_dir / "docking_results.csv"
    df.to_csv(csv_file, index=False)
    print(f"Results saved to: {csv_file}")
    print()

    # Statistical summary
    print("=" * 80)
    print("STATISTICAL SUMMARY")
    print("=" * 80)
    print(f"  Number of ligands: {len(df)}")
    print(f"  Best binding:      {df['Binding_Affinity_kcal_mol'].min():.2f} kcal/mol")
    print(f"  Worst binding:     {df['Binding_Affinity_kcal_mol'].max():.2f} kcal/mol")
    print(f"  Mean affinity:     {df['Binding_Affinity_kcal_mol'].mean():.2f} kcal/mol")
    print(f"  Std deviation:     {df['Binding_Affinity_kcal_mol'].std():.2f} kcal/mol")
    print()

    # Interpretation guide
    print("=" * 80)
    print("BINDING AFFINITY INTERPRETATION")
    print("=" * 80)
    print("""
    < -8.0 kcal/mol  →  Very strong binding (drug-like, Ki < 100 nM)
    -8.0 to -6.0     →  Strong binding (Ki 100 nM - 10 µM)
    -6.0 to -5.0     →  Moderate binding (Ki 10 - 100 µM)
    -5.0 to -4.0     →  Weak binding (Ki 0.1 - 1 mM)
    > -4.0           →  Very weak or no binding (Ki > 1 mM)

    For your study:
    • Strong binding (ΔG < -6 kcal/mol) suggests mechanism of action
    • Weak binding may still be biologically relevant (multiple interactions)
    • Compare affinities to rank lipid potency
    • Correlate with your in-vitro antivirulence data
""")

    print("=" * 80)


if __name__ == "__main__":
    main()
