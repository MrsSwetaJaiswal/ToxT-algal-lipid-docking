"""Blind docking: dock representative lipids over the WHOLE ToxT protein (no
pocket bias) and measure whether their poses land in the known fatty-acid pocket
or elsewhere. Tests whether the FA pocket is the preferred binding site.

Run (.venv):  .venv\\Scripts\\python.exe blind_dock.py
"""
import os, csv, subprocess, math

ROOT = os.path.dirname(os.path.abspath(__file__))
VINA = os.path.join(ROOT, "tools", "vina.exe")
REC = os.path.join(ROOT, "prepared_structures", "3GBG_meeko.pdbqt")
PDBQT_DIR = os.path.join(ROOT, "ligands_pdbqt")
OUT_DIR = os.path.join(ROOT, "results_blind"); os.makedirs(OUT_DIR, exist_ok=True)

# whole-protein box
BOX = dict(cx=50.6, cy=50.4, cz=19.6, sx=56, sy=60, sz=63)
# known fatty-acid pocket centre (Meeko box on crystal PAM)
POCKET = (54.65, 44.65, 18.85)
IN_POCKET_CUTOFF = 8.0  # A

LIGANDS = [
    ("EPA", "cis_5_8_11_14_17_eicosapentaenoic_acid"),
    ("gamma-linolenic", "gamma_linolenic_acid"),
    ("palmitic", "palmitic_acid"),
    ("palmitoleic (native PAM)", "palmitoleic_acid"),
]

def pose_coms(pdbqt):
    """Return list of (affinity, com_xyz) per MODEL."""
    poses = []
    aff = None; xs = ys = zs = 0.0; n = 0
    for line in open(pdbqt):
        if line.startswith("REMARK VINA RESULT"):
            aff = float(line.split()[3])
        elif line.startswith(("ATOM", "HETATM")):
            xs += float(line[30:38]); ys += float(line[38:46]); zs += float(line[46:54]); n += 1
        elif line.startswith("ENDMDL"):
            poses.append((aff, (xs/n, ys/n, zs/n))); aff = None; xs = ys = zs = 0.0; n = 0
    return poses

def dist(a, b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

rows = []
for label, name in LIGANDS:
    lig = os.path.join(PDBQT_DIR, name + ".pdbqt")
    out = os.path.join(OUT_DIR, name + "_blind.pdbqt")
    if not os.path.exists(lig):
        print("MISSING ligand pdbqt:", lig); continue
    if not os.path.exists(out):
        print("Blind docking %s ..." % label, flush=True)
        subprocess.run([VINA, "--receptor", REC, "--ligand", lig,
            "--center_x", str(BOX["cx"]), "--center_y", str(BOX["cy"]), "--center_z", str(BOX["cz"]),
            "--size_x", str(BOX["sx"]), "--size_y", str(BOX["sy"]), "--size_z", str(BOX["sz"]),
            "--exhaustiveness", "32", "--num_modes", "20", "--seed", "42", "--cpu", "4",
            "--out", out], check=True, capture_output=True)
    poses = pose_coms(out)
    top_aff, top_com = poses[0]
    top_d = dist(top_com, POCKET)
    in_pocket = sum(1 for a, c in poses if dist(c, POCKET) < IN_POCKET_CUTOFF)
    rows.append({"ligand": label, "top_affinity": top_aff,
                 "top_pose_dist_to_pocket_A": round(top_d, 1),
                 "top_in_pocket": "YES" if top_d < IN_POCKET_CUTOFF else "NO",
                 "modes_in_pocket": "%d/%d" % (in_pocket, len(poses))})
    print("  %-26s top dG %.2f  top-pose->pocket %.1f A  (%s)  modes in pocket %d/%d"
          % (label, top_aff, top_d, "IN POCKET" if top_d < IN_POCKET_CUTOFF else "ELSEWHERE",
             in_pocket, len(poses)), flush=True)

with open(os.path.join(OUT_DIR, "blind_dock_summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["ligand","top_affinity","top_pose_dist_to_pocket_A",
                                      "top_in_pocket","modes_in_pocket"])
    w.writeheader(); w.writerows(rows)
print("\nWrote results_blind/blind_dock_summary.csv")
