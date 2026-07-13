load prepared_structures/3GBG_meeko.pdbqt, ToxT
load prepared_structures/pam_ref.pdb, PAM_ref
load docking_results/neophytadiene_docked.pdbqt, neophytadiene
load docking_results/polyunsaturated_ester_docked.pdbqt, poly_ester
load docking_results/palmitic_acid_docked.pdbqt, palmitic
set all_states, off
hide everything
show cartoon, ToxT
color grey80, ToxT
set cartoon_transparency, 0.3, ToxT
show sticks, PAM_ref
color yellow, PAM_ref
show sticks, neophytadiene
color cyan, neophytadiene
show sticks, poly_ester
color magenta, poly_ester
show sticks, palmitic
color green, palmitic
orient PAM_ref
zoom PAM_ref, 12
bg_color white
set ray_shadows, 0
