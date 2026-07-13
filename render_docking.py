from pymol import cmd
import glob

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1)
cmd.set('ray_shadows', 0)
cmd.set('antialias', 2)
cmd.set('cartoon_transparency', 0.35)
cmd.set('stick_radius', 0.14)

COL = ['cyan','magenta','salmon','marine','splitpea','orange','purple','wheat',
       'slate','limon','deepteal','hotpink','lightblue','olive','firebrick',
       'teal','sand','violet','forest','deepsalmon']

def base():
    cmd.delete('all')
    cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
    cmd.hide('everything')
    cmd.show('cartoon', 'ToxT')
    cmd.color('grey70', 'ToxT')
    cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
    cmd.show('sticks', 'PAM')
    cmd.color('yellow', 'PAM')
    cmd.util.cnc('PAM')

# 1) Overview: whole protein, pocket ligand
base()
cmd.orient('ToxT')
cmd.ray(1600, 1200)
cmd.png('figures/fig8_toxt_overview.png', dpi=200)
print('wrote overview')

# 2/3) Per-species overlays
for org in ['CV', 'CCM']:
    base()
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
