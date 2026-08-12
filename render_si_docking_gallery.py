"""SI figure: individual docking pose for every ligand in the CV and CCM panels
(one pocket-zoomed image per organism-ligand pair, labelled with affinity).

Run (viz env):  conda run -n viz pymol -cq render_si_docking_gallery.py
Outputs: figures/si_docking/<org>_<ligand>.png
"""
from pymol import cmd
import glob, csv, os

AFF = {}
for org in ['CV', 'CCM']:
    p = 'results_%s/affinities_%s.csv' % (org, org)
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            AFF[(org, r['ligand'])] = float(r['affinity_kcal_mol'])

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
cmd.set('dash_color', 'grey40'); cmd.set('dash_width', 2.5)

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

os.makedirs('figures/si_docking', exist_ok=True)
n_done = 0
for org in ['CV', 'CCM']:
    files = sorted(glob.glob('poses_sdf/%s/*.sdf' % org))
    for f in files:
        label = os.path.splitext(os.path.basename(f))[0]
        load_prot()
        pocket_sticks()
        cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
        cmd.show('sticks', 'PAM'); cmd.color('yellow', 'PAM'); cmd.util.cnc('PAM')
        cmd.load(f, 'LIG')
        cmd.show('sticks', 'LIG')
        cmd.color('cyan', 'LIG'); cmd.util.cnc('LIG')
        cmd.remove('hydro')
        cmd.orient('LIG')
        cmd.zoom('LIG', 7)
        cmd.ray(1400, 1100)
        out = 'figures/si_docking/%s_%s.png' % (org, label)
        cmd.png(out, dpi=200)
        n_done += 1
        print('wrote', out)
print('DONE', n_done, 'images')
