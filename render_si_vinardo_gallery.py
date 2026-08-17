"""SI figure: individual Vinardo-scored docking pose for every ligand in the
22-lipid panel (consensus scoring, Section 2.7/3.6). Same rendering
convention as the Vina gallery (Figures S1/S2).

Run (viz env):  conda run -n viz pymol -cq render_si_vinardo_gallery.py
Outputs: figures/si_vinardo/<ligand>.png
"""
from pymol import cmd
import csv, os

SCORES = {}
for r in csv.DictReader(open("results_vinardo/consensus.csv")):
    SCORES[r["ligand"]] = (float(r["vina_kcal_mol"]), float(r["vinardo_kcal_mol"]))

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1)
cmd.set('ray_shadows', 0)
cmd.set('antialias', 2)
cmd.set('ambient_occlusion_mode', 1)
cmd.set('ambient_occlusion_scale', 12)
cmd.set('stick_radius', 0.16)
cmd.set('label_size', 20)
cmd.set('label_color', 'black')
cmd.set('label_outline_color', 'white')
cmd.set('float_labels', 1)

AROM = [12, 20, 22, 33, 69, 266]
BASIC = [13, 31, 230]
HYDRO = [25, 61, 71, 81, 83, 226, 259, 261, 269]
LABEL = [12, 20, 22, 31, 33, 69, 230, 266]

def load_prot():
    cmd.delete('all')
    cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
    cmd.hide('everything')
    cmd.show('cartoon', 'ToxT')
    cmd.color('grey90', 'ToxT')
    cmd.set('cartoon_transparency', 0.55)

def pocket_sticks():
    for resis, color in [(AROM, 'orange'), (BASIC, 'marine'), (HYDRO, 'grey60')]:
        sel = 'ToxT and resi ' + '+'.join(map(str, resis))
        cmd.show('sticks', sel + ' and not (name C+N+O)')
        cmd.color(color, sel); cmd.util.cnc(sel)
    for r in LABEL:
        cmd.label('ToxT and resi %d and name CA' % r, '"%s%s" % (resn, resi)')

os.makedirs('figures/si_vinardo', exist_ok=True)
n_done = 0
for lig in sorted(SCORES):
    f = 'results_vinardo/%s_vinardo.pdbqt' % lig
    if not os.path.exists(f):
        print('SKIP (missing):', f)
        continue
    load_prot()
    pocket_sticks()
    cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
    cmd.show('sticks', 'PAM'); cmd.color('yellow', 'PAM'); cmd.util.cnc('PAM')
    cmd.load(f, 'LIG')
    cmd.show('sticks', 'LIG')
    cmd.color('forest', 'LIG'); cmd.util.cnc('LIG')
    cmd.remove('hydro')
    cmd.orient('LIG')
    cmd.zoom('LIG', 7)
    cmd.ray(1400, 1100)
    out = 'figures/si_vinardo/%s.png' % lig
    cmd.png(out, dpi=200)
    n_done += 1
    print('wrote', out)
print('DONE', n_done, 'images')
