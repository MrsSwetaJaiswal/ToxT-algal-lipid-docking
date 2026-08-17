"""SI figure: AlphaFold3 ToxT-DNA complex confidence metrics (top-ranked
model, model_0 -- matches manuscript pTM 0.85 / ipTM 0.31, verified against
chain_ptm[0] and iptm in the summary_confidences JSON).

Panel A: predicted aligned error (PAE) heatmap, chain boundaries marked.
Panel B: per-residue pLDDT (from mmCIF B-factor column), confidence-banded.

Run (analysis env):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe make_af3_confidence_fig.py
Output: figures/af3_pae_plddt.png
"""
import json, re
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

PREFIX = "af3_toxt_dna/fold_2026_07_13_19_21"

full = json.load(open(PREFIX + "_full_data_0.json"))
summ = json.load(open(PREFIX + "_summary_confidences_0.json"))

pae = np.array(full["pae"])
tchain = full["token_chain_ids"]
n = len(tchain)
# chain boundaries (0-indexed token positions where a new chain starts)
bounds = [0] + [i for i in range(1, n) if tchain[i] != tchain[i - 1]] + [n]
chain_labels = []
for i in range(len(bounds) - 1):
    chain_labels.append((tchain[bounds[i]], bounds[i], bounds[i + 1]))

# --- per-residue pLDDT from the mmCIF B-factor column ---
plddt_by_chain = {}  # chain -> {resnum: [b-factors]}
with open(PREFIX + "_model_0.cif") as f:
    for line in f:
        if not line.startswith("ATOM") and not line.startswith("HETATM"):
            continue
        parts = line.split()
        # columns per header: group_PDB id type_symbol label_atom_id label_alt_id
        # label_comp_id label_asym_id label_entity_id label_seq_id pdbx_PDB_ins_code
        # Cartn_x Cartn_y Cartn_z occupancy B_iso_or_equiv auth_seq_id auth_asym_id model_num
        if len(parts) < 17:
            continue
        b_iso = float(parts[14])
        auth_seq = int(parts[15])
        auth_chain = parts[16]
        plddt_by_chain.setdefault(auth_chain, {}).setdefault(auth_seq, []).append(b_iso)

def chain_plddt_series(chain):
    d = plddt_by_chain.get(chain, {})
    resnums = sorted(d)
    vals = [np.mean(d[r]) for r in resnums]
    return resnums, vals

fig = plt.figure(figsize=(13, 10))
gsA = fig.add_axes([0.10, 0.44, 0.62, 0.46])
gsCB = fig.add_axes([0.74, 0.44, 0.02, 0.46])
gsB = fig.add_axes([0.08, 0.10, 0.86, 0.22])

# --- Panel A: PAE heatmap ---
im = gsA.imshow(pae, cmap="viridis_r", vmin=0, vmax=30, origin="upper")
for cid, s, e in chain_labels:
    gsA.axhline(s - 0.5, color="white", lw=1.2)
    gsA.axvline(s - 0.5, color="white", lw=1.2)
gsA.set_xlim(0, n); gsA.set_ylim(n, 0)
xticks = [(s + e) / 2 for _, s, e in chain_labels]
xlabs = ["chain %s" % cid for cid, _, _ in chain_labels]
gsA.set_xticks(xticks); gsA.set_xticklabels(xlabs, fontsize=10, fontweight="bold")
gsA.set_yticks(xticks); gsA.set_yticklabels(xlabs, fontsize=10, fontweight="bold")
gsA.tick_params(length=0)
gsA.set_title("A. Predicted aligned error (PAE), top-ranked model", fontsize=12, loc="left", pad=10)
cb = fig.colorbar(im, cax=gsCB)
cb.set_label("PAE (\u00c5)", fontsize=10)

fig.text(0.10, 0.385, "pTM (protein, chain A) = %.2f   |   ipTM (complex) = %.2f   |   ranking score = %.2f"
          % (summ["chain_ptm"][0], summ["iptm"], summ["ranking_score"]), fontsize=10)

# --- Panel B: per-residue pLDDT ---
BANDS = [(90, 100, "#106DFF", "very high (>90)"),
         (70, 90, "#63CFD9", "confident (70-90)"),
         (50, 70, "#FFDB13", "low (50-70)"),
         (0, 50, "#FF7D45", "very low (<50)")]

offset = 0
xticks, xlabels = [], []
for cid, s, e in chain_labels:
    resnums, vals = chain_plddt_series(cid)
    xs = np.arange(len(vals)) + offset
    colors = []
    for v in vals:
        for lo, hi, c, _ in BANDS:
            if lo <= v <= hi:
                colors.append(c); break
        else:
            colors.append("#999999")
    gsB.bar(xs, vals, width=1.0, color=colors, edgecolor="none")
    gsB.axvline(offset - 0.5, color="grey", lw=0.8, ls="--")
    xticks.append(offset + len(vals) / 2)
    xlabels.append("chain %s (%d %s)" % (cid, len(vals), "aa" if cid == "A" else "nt"))
    offset += len(vals) + 4

gsB.set_xticks(xticks); gsB.set_xticklabels(xlabels, fontsize=10)
gsB.set_ylabel("pLDDT"); gsB.set_ylim(0, 100)
gsB.set_title("B. Per-residue pLDDT, top-ranked model", fontsize=12, loc="left")
gsB.legend(handles=[Patch(facecolor=c, label=l) for _, _, c, l in BANDS],
           loc="lower center", bbox_to_anchor=(0.5, -0.55), ncol=4, fontsize=9, frameon=False)

fig.suptitle("AlphaFold3 ToxT\u2013DNA complex: confidence metrics (top-ranked model of 5)",
             fontsize=13, y=0.98)
fig.savefig("figures/af3_pae_plddt.png", dpi=200, bbox_inches="tight")
print("Wrote figures/af3_pae_plddt.png")
print("pTM (chain A, protein):", summ["chain_ptm"][0])
print("ipTM (complex):", summ["iptm"])
print("chain_ptm all:", summ["chain_ptm"])
