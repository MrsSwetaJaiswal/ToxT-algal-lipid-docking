from pymol import cmd

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1)
cmd.set('ray_shadows', 0)
cmd.set('antialias', 2)
cmd.set('ambient_occlusion_mode', 1)
cmd.set('ambient_occlusion_scale', 12)
cmd.set('cartoon_transparency', 0.55)
cmd.set('stick_radius', 0.16)
cmd.set('label_size', 20)
cmd.set('label_color', 'black')
cmd.set('label_outline_color', 'white')
cmd.set('float_labels', 1)
cmd.set('dash_color', 'grey40')
cmd.set('dash_width', 2.5)

# pocket residues grouped by chemistry (crystal 3GBG numbering)
AROM = [12, 20, 22, 33, 69, 266]
BASIC = [13, 31, 230]
HYDRO = [25, 61, 71, 81, 83, 226, 259, 261, 269]
LABEL = [12, 20, 22, 31, 33, 69, 230, 266]

cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
cmd.hide('everything')
cmd.show('cartoon', 'ToxT')
cmd.color('grey90', 'ToxT')

def sticks(resis, color, name):
    sel = 'ToxT and resi ' + '+'.join(map(str, resis))
    cmd.show('sticks', sel + ' and not (name C+N+O)')
    cmd.color(color, sel)
    cmd.util.cnc(sel)

sticks(AROM, 'orange', 'arom')
sticks(BASIC, 'marine', 'basic')
sticks(HYDRO, 'grey60', 'hydro')
for r in LABEL:
    cmd.label('ToxT and resi %d and name CA' % r, '"%s%s" % (resn, resi)')

# ligand (native palmitoleate)
cmd.load('prepared_structures/pam_ref.pdb', 'PAM')
cmd.show('sticks', 'PAM')
cmd.color('yellow', 'PAM')
cmd.util.cnc('PAM')

# polar contacts from basic residues to the ligand carboxylate
cmd.distance('saltbridge', 'ToxT and resi 13+31+230 and (name NZ+NH1+NH2+NE)',
             'PAM and name O*', 3.6)
cmd.hide('labels', 'saltbridge')
cmd.color('grey30', 'saltbridge')

cmd.orient('ToxT and resi ' + '+'.join(map(str, LABEL)))
cmd.zoom('ToxT and resi ' + '+'.join(map(str, LABEL)), 6)
cmd.ray(1800, 1400)
cmd.png('figures/fig8c_pocket_improved.png', dpi=200)
print('wrote improved pocket figure')
