from pymol import cmd

cmd.bg_color('white')
cmd.set('ray_opaque_background', 1); cmd.set('ray_shadows', 0)
cmd.set('antialias', 2); cmd.set('ambient_occlusion_mode', 1)
cmd.set('cartoon_transparency', 0.0)

# AF3 ToxT-DNA model
cmd.load('af3_toxt_dna/fold_2026_07_13_19_21_model_0.cif', 'af3')
# fatty-acid-bound crystal (protein + PAM), aligned onto AF3 ToxT to place the lipid
cmd.load('structures/3GBG.pdb', 'xtal')
cmd.remove('xtal and (solvent or resn HOH)')
cmd.align('xtal and name CA', 'af3 and chain A and name CA')

cmd.hide('everything')
# ToxT protein (AF3 chain A)
cmd.show('cartoon', 'af3 and chain A')
cmd.color('grey80', 'af3 and chain A')
# DNA (chains B/C)
cmd.show('cartoon', 'af3 and (chain B or chain C)')
cmd.set('cartoon_ring_mode', 3, 'af3 and (chain B or chain C)')
cmd.color('deepteal', 'af3 and (chain B or chain C)')
# DNA-contacting HTH domain residues (188-276) highlighted
cmd.color('marine', 'af3 and chain A and resi 188-276')
# fatty-acid pocket residues (N-terminal domain) + native ligand
POCK = '12+20+22+31+33+69+71+81+226+230+259+261+266'
cmd.color('orange', 'af3 and chain A and resi ' + POCK)
cmd.show('sticks', 'xtal and resn PAM')
cmd.color('yellow', 'xtal and resn PAM'); cmd.util.cnc('xtal and resn PAM')
cmd.show('spheres', 'xtal and resn PAM'); cmd.set('sphere_scale', 0.3, 'xtal and resn PAM')

# distance line: pocket (PAM) to DNA
cmd.pseudoatom('pock_c', selection='xtal and resn PAM')
cmd.pseudoatom('dna_c', selection='af3 and (chain B or chain C)')
cmd.distance('sep', 'pock_c', 'dna_c')
cmd.hide('labels', 'sep'); cmd.color('red', 'sep'); cmd.set('dash_width', 3)

cmd.orient('af3')
cmd.turn('y', 15)
cmd.ray(1900, 1400)
cmd.png('figures/fig11_dna_competition.png', dpi=200)
print('wrote fig11_dna_competition.png')
