from pymol import cmd
import glob

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1)
cmd.set('ray_shadows', 0)
cmd.set('antialias', 2)
cmd.set('cartoon_transparency', 0.4)
cmd.set('stick_radius', 0.14)
cmd.set('label_size', 18)
cmd.set('label_color', 'black')
cmd.set('label_outline_color', 'white')
cmd.set('float_labels', 1)

# key fatty-acid pocket residues (crystal 3GBG numbering; from proximity to PAM
# and confirmed by MD contact analysis)
KEY = [12, 20, 22, 31, 33, 69, 230, 266]
KEYSEL = 'ToxT and resi ' + '+'.join(map(str, KEY))
COL = ['cyan', 'magenta', 'salmon', 'marine', 'splitpea', 'orange', 'purple',
       'wheat', 'slate', 'limon', 'deepteal', 'hotpink', 'lightblue', 'olive',
       'firebrick', 'teal', 'sand', 'violet', 'forest', 'deepsalmon']

def base(surface=False):
    cmd.delete('all')
    cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
    cmd.hide('everything')
    cmd.show('cartoon', 'ToxT')
    cmd.color('grey80', 'ToxT')
    cmd.show('sticks', KEYSEL + ' and not (name C+N+O)')
    cmd.color('palegreen', KEYSEL)
    cmd.util.cnc(KEYSEL)
    for r in KEY:
        cmd.label('ToxT and resi %d and name CA' % r, '"%s%s" % (resn, resi)')
    if surface:
        cmd.show('surface', 'ToxT')
        cmd.set('transparency', 0.55)
    cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
    cmd.show('sticks', 'PAM')
    cmd.color('yellow', 'PAM')
    cmd.util.cnc('PAM')

# 1a) overview WITH semi-transparent surface
base(surface=True)
cmd.orient(KEYSEL)
cmd.zoom(KEYSEL, 7)
cmd.ray(1700, 1300)
cmd.png('figures/fig8a_toxt_pocket_surface.png', dpi=200)
print('wrote pocket overview (surface)')

# 1b) overview clean cartoon (no surface)
base(surface=False)
cmd.orient(KEYSEL)
cmd.zoom(KEYSEL, 7)
cmd.ray(1700, 1300)
cmd.png('figures/fig8b_toxt_pocket_cartoon.png', dpi=200)
print('wrote pocket overview (cartoon)')

# 2/3) per-species overlays with labelled residues (no surface)
for org in ['CV', 'CCM']:
    base(surface=False)
    files = sorted(glob.glob('poses_sdf/%s/*.sdf' % org))
    for i, f in enumerate(files):
        n = '%s_%d' % (org, i)
        cmd.load(f, n)
        cmd.show('sticks', n)
        cmd.color(COL[i % len(COL)], n)
    cmd.remove('hydro')
    cmd.orient('PAM')
    cmd.zoom('PAM', 9)
    cmd.ray(1700, 1300)
    cmd.png('figures/fig_%s_docked_overlay.png' % org, dpi=200)
    print('wrote %s overlay (%d ligands)' % (org, len(files)))

print('DONE')
