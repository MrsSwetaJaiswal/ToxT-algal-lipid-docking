"""SI figure: blind-docking pose gallery -- every Vina mode for each of the 5
whole-protein blind-docked ligands, coloured by in-pocket (<8 A of the PAM
reference centroid, matching Methods 2.10) vs out-of-pocket.

PyMOL's PDBQT loader only reads the first MODEL block of a multi-model file
(confirmed: loading a 15-model file gives count_states==1, natoms matching
just model 1) -- so each MODEL/ENDMDL block is split out to its own temp
PDBQT file first and loaded individually.

Run (viz env):  conda run -n viz pymol -cq render_si_blind_docking_gallery.py
Outputs: figures/si_blind/<ligand>_blind_poses.png
"""
from pymol import cmd
import os, glob, shutil

LIGANDS = [
    ("cis_5_8_11_14_17_eicosapentaenoic_acid", "EPA"),
    ("gamma_linolenic_acid", "gamma-linolenic acid"),
    ("palmitic_acid", "palmitic acid"),
    ("palmitoleic_acid", "palmitoleate (native)"),
    ("glucose", "glucose (decoy)"),
]
POCKET_CUTOFF = 8.0  # Angstrom, matches Methods 2.10 "in pocket" definition
TMP = "si_blind_tmp"

def split_models(pdbqt_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, "*.pdbqt")):
        os.remove(f)
    with open(pdbqt_path) as f:
        lines = f.readlines()
    blocks = []
    cur = []
    in_model = False
    for line in lines:
        if line.startswith("MODEL"):
            in_model = True
            cur = [line]
        elif line.startswith("ENDMDL"):
            cur.append(line)
            blocks.append(cur)
            in_model = False
        elif in_model:
            cur.append(line)
    paths = []
    for i, b in enumerate(blocks, 1):
        p = os.path.join(outdir, "pose_%04d.pdbqt" % i)
        with open(p, "w") as f:
            f.writelines(b)
        paths.append(p)
    return paths

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1)
cmd.set('ray_shadows', 0)
cmd.set('antialias', 2)
cmd.set('stick_radius', 0.12)

os.makedirs('figures/si_blind', exist_ok=True)

for slug, label in LIGANDS:
    cmd.delete('all')
    cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
    cmd.hide('everything')
    cmd.show('cartoon', 'ToxT')
    cmd.color('grey80', 'ToxT')
    cmd.set('cartoon_transparency', 0.35)

    cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
    cmd.show('sticks', 'PAM')
    cmd.color('yellow', 'PAM')
    pocket_com = cmd.centerofmass('PAM')

    src = 'results_blind/%s_blind.pdbqt' % slug
    pose_files = split_models(src, TMP)

    n_in, n_out = 0, 0
    for i, pf in enumerate(pose_files, 1):
        obj = 'pose_%04d' % i
        cmd.load(pf, obj)
        com = cmd.centerofmass(obj)
        d = sum((com[k] - pocket_com[k]) ** 2 for k in range(3)) ** 0.5
        cmd.show('sticks', obj)
        cmd.remove(obj + ' and hydro')
        if d < POCKET_CUTOFF:
            cmd.color('marine', obj)
            n_in += 1
        else:
            cmd.color('firebrick', obj)
            n_out += 1

    cmd.orient('ToxT')
    cmd.ray(1600, 1300)
    out = 'figures/si_blind/%s_blind_poses.png' % slug
    cmd.png(out, dpi=200)
    print('wrote %s -- %d/%d in pocket (<%.0f A, blue), %d out (red)' %
          (out, n_in, len(pose_files), POCKET_CUTOFF, n_out))

shutil.rmtree(TMP, ignore_errors=True)
print('DONE')
