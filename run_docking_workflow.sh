#!/bin/bash
# Complete AutoDock Vina docking workflow
# Prepares structures and runs all dockings

set -e  # Exit on error

echo "==========================================================================="
echo "AutoDock Vina Docking Workflow - ToxT Lipid Study"
echo "==========================================================================="
echo ""

# Define directories
STRUCT_DIR="./structures"
PREP_DIR="./prepared_structures"
CONFIG_DIR="./docking_configs"
RESULTS_DIR="./docking_results"

# Create output directories
mkdir -p "$PREP_DIR"
mkdir -p "$RESULTS_DIR"

echo "========== STEP 1: Analyze Structure =========="
echo "Analyzing ToxT structure to identify binding pocket..."
python3 analyze_structure.py
echo ""

echo "========== STEP 2: Prepare Protein =========="
echo "Converting ToxT (3GBG.pdb) to PDBQT format..."
echo "Command: meeko -protein structures/3GBG.pdb -o prepared_structures/3GBG_prepared.pdbqt"
meeko -protein "$STRUCT_DIR/3GBG.pdb" -o "$PREP_DIR/3GBG_prepared.pdbqt"
echo "✓ Done"
echo ""

echo "========== STEP 3: Prepare Ligands =========="
echo "Converting lipid ligands to PDBQT format..."
echo ""

echo "Ligand 1: Neophytadiene"
meeko -ligand "$STRUCT_DIR"/*neophytadiene.sdf -o "$PREP_DIR/neophytadiene.pdbqt"
echo "✓ neophytadiene.pdbqt"
echo ""

echo "Ligand 2: Polyunsaturated fatty acid methyl ester"
meeko -ligand "$STRUCT_DIR"/*Methyl*.sdf -o "$PREP_DIR/polyunsaturated_ester.pdbqt"
echo "✓ polyunsaturated_ester.pdbqt"
echo ""

echo "Ligand 3: Palmitic acid"
meeko -ligand "$STRUCT_DIR"/*palmitic*.sdf -o "$PREP_DIR/palmitic_acid.pdbqt"
echo "✓ palmitic_acid.pdbqt"
echo ""

echo "========== STEP 4: Run Dockings =========="
echo ""

# Function to run single docking
run_docking() {
    local config=$1
    local name=$2

    echo "Docking: $name"
    echo "  Config: $config"

    vina --config "$config" \
        --out "$RESULTS_DIR/${name}_docked.pdbqt" \
        --log "$RESULTS_DIR/${name}.log"

    echo "  ✓ Complete"
    echo ""
}

echo "Running AutoDock Vina dockings..."
echo "(This may take 5-20 minutes depending on your hardware)"
echo ""

run_docking "$CONFIG_DIR/config_neophytadiene.txt" "neophytadiene"
run_docking "$CONFIG_DIR/config_polyunsaturated_ester.txt" "polyunsaturated_ester"
run_docking "$CONFIG_DIR/config_palmitic_acid.txt" "palmitic_acid"

echo "========== STEP 5: Parse Results =========="
echo "Analyzing docking results..."
python3 parse_docking_results.py
echo ""

echo "==========================================================================="
echo "✓ DOCKING WORKFLOW COMPLETE!"
echo "==========================================================================="
echo ""
echo "Output files:"
echo "  • prepared_structures/ - PDBQT files for protein and ligands"
echo "  • docking_results/     - Docked poses and log files"
echo "  • docking_results.csv  - Summary table of binding affinities"
echo ""
echo "Next steps:"
echo "  1. Review docking_results.csv for binding affinities"
echo "  2. Visualize poses in PyMOL:"
echo "     load prepared_structures/3GBG_prepared.pdbqt"
echo "     load docking_results/neophytadiene_docked.pdbqt"
echo "  3. Analyze interactions in best binding poses"
echo "  4. Correlate with your in-vitro/in-vivo data"
echo ""
