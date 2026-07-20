from pymol import cmd

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1); cmd.set('ray_shadows', 0)
cmd.set('antialias', 2); cmd.set('ambient_occlusion_mode', 1)
cmd.set('cartoon_transparency', 0.7); cmd.set('valence', 1); cmd.set('valence_mode', 1)
cmd.set('stick_radius', 0.14)
cmd.set('label_size', 16); cmd.set('label_color', 'black'); cmd.set('label_outline_color', 'white')
cmd.set('float_labels', 1)

AROM = [12, 20, 22, 33, 69, 266]

def scene(lig_sdf, lig_name, lig_color, out):
    cmd.delete('all')
    cmd.load('prepared_structures/3GBG_protein_only.pdb', 'ToxT')
    cmd.hide('everything'); cmd.show('cartoon', 'ToxT'); cmd.color('grey90', 'ToxT')
    sel = 'ToxT and resi ' + '+'.join(map(str, AROM))
    cmd.show('sticks', sel + ' and not (name C+N+O)')
    cmd.color('orange', sel); cmd.util.cnc(sel)
    for r in AROM:
        cmd.label('ToxT and resi %d and name CA' % r, '"%s%s" % (resn, resi)')
    cmd.load(lig_sdf, 'lig')
    cmd.remove('hydro')
    cmd.show('sticks', 'lig'); cmd.color(lig_color, 'lig'); cmd.util.cnc('lig')
    cmd.set('stick_radius', 0.22, 'lig')   # thicker ligand so double bonds read
    cmd.orient('lig'); cmd.zoom('lig', 4.5)
    cmd.ray(1500, 1300)
    cmd.png(out, dpi=200)
    print('wrote', out)

scene('poses_sdf/CV/stearic_acid.sdf', 'stearic', 'grey60', 'figures/pi_stearic.png')
scene('poses_sdf/CV/gamma_linolenic_acid.sdf', 'gla', 'cyan', 'figures/pi_gla.png')
print('DONE')
