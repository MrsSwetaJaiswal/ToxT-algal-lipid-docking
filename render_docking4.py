from pymol import cmd
import glob, csv, os

# affinity per ligand label (for single-hue gradient colouring of overlays)
AFF = {}
for org in ['CV', 'CCM']:
    p = 'results_%s/affinities_%s.csv' % (org, org)
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            AFF[r['ligand']] = float(r['affinity_kcal_mol'])
# gradient range (strongest = most negative -> darkest)
AMIN, AMAX = -8.8, -6.8
def aff_rgb(a):
    t = max(0.0, min(1.0, (AMAX - a) / (AMAX - AMIN)))  # 0 weak -> 1 strong
    # light lavender -> deep purple (single hue)
    lo = (0.87, 0.82, 0.95); hi = (0.36, 0.0, 0.55)
    return [lo[i] + t * (hi[i] - lo[i]) for i in range(3)]

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
ALLPOCK = AROM + BASIC + HYDRO

def load_prot(transp):
    cmd.delete('all')
    cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
    cmd.hide('everything')
    cmd.show('cartoon', 'ToxT')
    cmd.color('grey90', 'ToxT')
    cmd.set('cartoon_transparency', transp)

def pocket_sticks(labels=True):
    for resis, color in [(AROM, 'orange'), (BASIC, 'marine'), (HYDRO, 'grey60')]:
        sel = 'ToxT and resi ' + '+'.join(map(str, resis))
        cmd.show('sticks', sel + ' and not (name C+N+O)')
        cmd.color(color, sel); cmd.util.cnc(sel)
    if labels:
        for r in LABEL:
            cmd.label('ToxT and resi %d and name CA' % r, '"%s%s" % (resn, resi)')

def add_pam():
    cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
    cmd.show('sticks', 'PAM'); cmd.color('yellow', 'PAM'); cmd.util.cnc('PAM')

def saltbridge():
    cmd.distance('sb', 'ToxT and resi 13+31+230 and (name NZ+NH1+NH2+NE)',
                 'PAM and name O*', 3.6)
    cmd.hide('labels', 'sb'); cmd.color('grey30', 'sb')

# Panel A: whole protein, pocket highlighted (no labels)
load_prot(0.25)
pocket_sticks(labels=False)
add_pam()
cmd.orient('ToxT')
cmd.ray(1500, 1500)
cmd.png('figures/panelA_whole.png', dpi=200)
print('panelA')

# Panel B: zoomed labelled pocket + salt bridges
load_prot(0.55)
pocket_sticks(labels=True)
add_pam()
saltbridge()
cmd.orient('ToxT and resi ' + '+'.join(map(str, LABEL)))
cmd.zoom('ToxT and resi ' + '+'.join(map(str, LABEL)), 6)
cmd.ray(1600, 1500)
cmd.png('figures/panelB_pocket.png', dpi=200)
print('panelB')

# Overlays: uniform-coloured ligands, chemistry-coloured pocket
for org in ['CV', 'CCM']:
    load_prot(0.55)
    pocket_sticks(labels=True)
    add_pam()
    files = sorted(glob.glob('poses_sdf/%s/*.sdf' % org))
    for i, f in enumerate(files):
        label = os.path.splitext(os.path.basename(f))[0]
        n = '%s_%d' % (org, i)
        cmd.load(f, n)
        cmd.show('sticks', n)
        cmd.set('stick_radius', 0.10, n)
        if label in AFF:
            cmd.set_color('c_%s' % n, aff_rgb(AFF[label]))
            cmd.color('c_%s' % n, n)
        else:
            cmd.color('violet', n)
    cmd.remove('hydro')
    cmd.orient('PAM')
    cmd.zoom('PAM', 9)
    cmd.ray(1700, 1400)
    cmd.png('figures/fig_%s_overlay2.png' % org, dpi=200)
    print('overlay', org, len(files))
print('DONE')
