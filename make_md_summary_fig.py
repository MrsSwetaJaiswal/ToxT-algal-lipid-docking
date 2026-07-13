"""Figure 7: MD headgroup matrix - ligand-pocket distance for 3 fatty acids x 3 forms."""
import csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rows = list(csv.DictReader(open("md/md_summary.csv")))
lipids = ["EPA", "GLA", "palmitic"]
forms = ["free acid", "methyl ester", "carboxylate"]
colors = {"free acid": "#2c7fb8", "methyl ester": "#d95f0e", "carboxylate": "#31a354"}

data = {(r["lipid"], r["form"]): float(r["com_A"]) for r in rows if r["com_A"] != ""}
x = np.arange(len(lipids)); w = 0.25
fig, ax = plt.subplots(figsize=(8, 4.8))
for j, form in enumerate(forms):
    vals = [data.get((lp, form), np.nan) for lp in lipids]
    bars = ax.bar(x + (j-1)*w, vals, w, label=form, color=colors[form],
                  edgecolor="black", linewidth=0.4)
    for b, v in zip(bars, vals):
        if not np.isnan(v):
            ax.text(b.get_x()+b.get_width()/2, v+0.05, "%.1f" % v,
                    ha="center", va="bottom", fontsize=8)
ax.axhline(10, ls="--", c="grey", alpha=0.7)
ax.text(2.35, 10.2, "unbound threshold", fontsize=8, color="grey", ha="right")
ax.set_xticks(x); ax.set_xticklabels(lipids)
ax.set_ylabel("Ligand-pocket COM distance (A)")
ax.set_ylim(0, 11)
ax.set_title("MD: all fatty-acid forms remain bound to ToxT (50 ns each)", fontweight="bold")
ax.legend(title="Head-group form", fontsize=9)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("figures/fig7_md_headgroup_matrix.png", dpi=200)
print("Wrote figures/fig7_md_headgroup_matrix.png")
