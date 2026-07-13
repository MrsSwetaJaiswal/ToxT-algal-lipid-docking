"""Compose final publication molecular figures: two-panel pocket figure with a
chemistry legend, and CV/CCM docked overlays with legend + affinity colorbar."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# chemistry legend handles
LEG = [
    Patch(facecolor='orange', edgecolor='k', label='Aromatic (Tyr/Phe)'),
    Patch(facecolor='#1f6fd0', edgecolor='k', label='Basic (Lys/Arg)'),
    Patch(facecolor='#999999', edgecolor='k', label='Hydrophobic (Leu/Val/Ile/Met)'),
    Patch(facecolor='yellow', edgecolor='k', label='Native ligand (palmitoleate)'),
]
# single-hue affinity colormap (matches PyMOL: light lavender -> deep purple)
AFF_CMAP = LinearSegmentedColormap.from_list('aff', [(0.87,0.82,0.95),(0.36,0.0,0.55)])

# ---- Figure: two-panel pocket ----
fig = plt.figure(figsize=(13, 6.5))
gsA = fig.add_axes([0.01, 0.12, 0.46, 0.85]); gsA.axis('off')
gsB = fig.add_axes([0.49, 0.12, 0.46, 0.85]); gsB.axis('off')
gsA.imshow(mpimg.imread('figures/panelA_whole.png'))
gsB.imshow(mpimg.imread('figures/panelB_pocket.png'))
gsA.text(0.02, 0.98, 'A', transform=gsA.transAxes, fontsize=22, fontweight='bold', va='top')
gsB.text(0.02, 0.98, 'B', transform=gsB.transAxes, fontsize=22, fontweight='bold', va='top')
gsA.set_title('ToxT with the fatty-acid pocket', fontsize=12)
gsB.set_title('Pocket detail (residues coloured by chemistry)', fontsize=12)
fig.legend(handles=LEG, loc='lower center', ncol=4, fontsize=10, frameon=False,
           bbox_to_anchor=(0.5, 0.0))
fig.savefig('figures/fig8_pocket_final.png', dpi=200, bbox_inches='tight')
plt.close(fig)
print('wrote fig8_pocket_final.png')

# ---- Overlays with legend + affinity colorbar ----
for org, title in [('CV', 'C. variabilis (CV) lipids'), ('CCM', 'Chlorococcum (CCM) lipids')]:
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_axes([0.0, 0.10, 0.86, 0.86]); ax.axis('off')
    ax.imshow(mpimg.imread('figures/fig_%s_overlay2.png' % org))
    ax.set_title('%s docked in the ToxT pocket' % title, fontsize=13, fontweight='bold')
    # affinity colorbar
    cax = fig.add_axes([0.88, 0.20, 0.025, 0.6])
    sm = ScalarMappable(norm=Normalize(vmin=-8.8, vmax=-6.8), cmap=AFF_CMAP)
    cb = fig.colorbar(sm, cax=cax)
    cb.set_label('Binding affinity (kcal/mol)', fontsize=10)
    cb.ax.invert_yaxis()  # strong (dark) at top
    fig.legend(handles=LEG, loc='lower center', ncol=2, fontsize=9, frameon=False,
               bbox_to_anchor=(0.43, 0.0))
    fig.savefig('figures/fig_%s_overlay_final.png' % org, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print('wrote fig_%s_overlay_final.png' % org)
print('DONE')
