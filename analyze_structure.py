#!/usr/bin/env python3
"""
Analyze ToxT structure to identify binding pocket
"""

from pathlib import Path
try:
    from Bio import PDB
except ImportError:
    print("Installing biopython...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'biopython', '-q'])
    from Bio import PDB

import pandas as pd
import numpy as np

def analyze_toxt_structure():
    struct_dir = Path(__file__).parent / "structures"
    pdb_file = struct_dir / "3GBG.pdb"

    if not pdb_file.exists():
        print(f"Error: {pdb_file} not found")
        return

    print("=" * 70)
    print("ToxT STRUCTURE ANALYSIS (PDB: 3GBG)")
    print("=" * 70)
    print()

    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('ToxT', str(pdb_file))

    # Extract all CA atoms
    ca_atoms = []
    residue_info = []

    for chain in structure.get_chains():
        print(f"Chain: {chain.id}")

        for residue in chain:
            if 'CA' in residue:
                ca = residue['CA']
                coord = ca.coord
                ca_atoms.append(coord)

                res_name = residue.resname
                res_id = residue.id[1]
                residue_info.append({
                    'residue': res_name,
                    'position': res_id,
                    'x': coord[0],
                    'y': coord[1],
                    'z': coord[2]
                })

    print(f"  Total residues: {len(ca_atoms)}")
    print()

    # Calculate center of mass
    ca_array = np.array(ca_atoms)
    center = ca_array.mean(axis=0)

    print("=" * 70)
    print("BINDING POCKET CENTER (Center of Mass)")
    print("=" * 70)
    print(f"  center_x = {center[0]:.2f}")
    print(f"  center_y = {center[1]:.2f}")
    print(f"  center_z = {center[2]:.2f}")
    print()

    # Calculate dimensions
    min_coords = ca_array.min(axis=0)
    max_coords = ca_array.max(axis=0)
    range_coords = max_coords - min_coords

    print("=" * 70)
    print("PROTEIN DIMENSIONS")
    print("=" * 70)
    print(f"  X range: {min_coords[0]:.2f} to {max_coords[0]:.2f} (span: {range_coords[0]:.2f} Å)")
    print(f"  Y range: {min_coords[1]:.2f} to {max_coords[1]:.2f} (span: {range_coords[1]:.2f} Å)")
    print(f"  Z range: {min_coords[2]:.2f} to {max_coords[2]:.2f} (span: {range_coords[2]:.2f} Å)")
    print()

    # Recommended search box
    print("=" * 70)
    print("RECOMMENDED DOCKING PARAMETERS")
    print("=" * 70)
    print(f"  Search box size: 24 x 24 x 24 Å (appropriate for small lipid molecules)")
    print(f"  Exhaustiveness: 16 (balanced accuracy/speed)")
    print(f"  Number of modes: 20 (diverse binding poses)")
    print(f"  Energy range: 3.0 kcal/mol")
    print()

    print("=" * 70)
    print("USE THESE COORDINATES IN YOUR CONFIG FILES:")
    print("=" * 70)
    print(f"""
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
""")

    # Info about ToxT structure
    print("=" * 70)
    print("ABOUT THIS STRUCTURE (PDB: 3GBG)")
    print("=" * 70)
    print("""
    Reference: Lowden et al. (2010)
    Title: "Structure of Vibrio cholerae ToxT reveals a mechanism for
             fatty acid regulation of virulence genes"
    Journal: PNAS 107:2860
    PubMed: 20133655

    Key Features:
    • X-ray crystal structure at 1.90 Å resolution (excellent quality)
    • ToxT is a DNA-binding transcriptional regulator (AraC family)
    • Binds fatty acids at an allosteric pocket
    • Regulates virulence genes (TCP, CTX, etc.)

    Your lipids:
    1. Neophytadiene (terpene) - natural product of algae
    2. Polyunsaturated fatty acid methyl ester - common algal lipid
    3. Palmitic acid (saturated C16 fatty acid) - ubiquitous in nature

    Expected: All should bind in the characterized fatty acid pocket
""")

    print("=" * 70)

if __name__ == "__main__":
    analyze_toxt_structure()
