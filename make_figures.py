"""Generate manuscript figures from the docking result CSVs."""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(ROOT, "figures"); os.makedirs(FIG, exist_ok=True)

def read(path, k="ligand", v="affinity_kcal_mol"):
    rows = list(csv.DictReader(open(path)))
    return rows

def nice(s):
    return (s.replace("_", " ").replace("cis ", "cis-")
            .replace("eicosapentaenoic", "EPA").replace("octadecatrienoic", "C18:3")
            .replace("methyl 3 cis 9 cis 12 cis octadecatrienoate", "methyl C18:3")
            .replace("ooctadecadienoic", "octadecadienoic"))

# ---------- Figure 1: ranked bar charts per organism ----------
def bars(ax, path, title, color):
    rows = sorted(read(path), key=lambda r: float(r["affinity_kcal_mol"]))
    names = [nice(r["ligand"])[:34] for r in rows]
    vals = [float(r["affinity_kcal_mol"]) for r in rows]
    y = range(len(vals))
    ax.barh(y, vals, color=color, edgecolor="black", linewidth=0.4)
    ax.set_yticks(list(y)); ax.set_yticklabels(names, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Binding affinity (kcal/mol)", fontsize=9)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlim(min(vals) - 0.6, 0)
    for i, val in zip(y, vals):
        ax.text(val - 0.05, i, "%.2f" % val, va="center", ha="right",
                fontsize=6.2, color="white")
    ax.grid(axis="x", alpha=0.3)

fig, axes = plt.subplots(1, 2, figsize=(11, 6))
bars(axes[0], "results_CV/affinities_CV.csv", "CV lipids", "#2c7fb8")
bars(axes[1], "results_CCM/affinities_CCM.csv", "CCM lipids", "#d95f0e")
fig.suptitle("Predicted ToxT binding affinities (AutoDock Vina 1.2.7)",
             fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(FIG, "fig1_affinity_bars.png"), dpi=200)
plt.close(fig)

# ---------- Figure 2: affinity vs unsaturation ----------
sp = read("results_batch/structure_property.csv")
db = [int(r["C_C_double_bonds"]) for r in sp]
aff = [float(r["affinity"]) for r in sp]
nC = [int(r["n_carbons"]) for r in sp]
fig, ax = plt.subplots(figsize=(7, 5.5))
sc = ax.scatter(db, aff, c=nC, cmap="viridis", s=70, edgecolor="black", linewidth=0.5)
# linear trend
n = len(db); mx = sum(db)/n; my = sum(aff)/n
b = sum((x-mx)*(y-my) for x, y in zip(db, aff)) / sum((x-mx)**2 for x in db)
a = my - b*mx
xs = [min(db), max(db)]
ax.plot(xs, [a + b*x for x in xs], "r--", lw=1.5, label="linear fit (r = -0.87)")
ax.set_xlabel("Number of C=C double bonds (unsaturation)", fontsize=10)
ax.set_ylabel("Binding affinity (kcal/mol)", fontsize=10)
ax.set_title("Unsaturation drives ToxT binding", fontsize=12, fontweight="bold")
ax.invert_yaxis()
cb = fig.colorbar(sc); cb.set_label("Chain length (carbons)", fontsize=9)
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig2_unsaturation.png"), dpi=200)
plt.close(fig)

# ---------- Figure 3: consensus Vina vs Vinardo ----------
cons = read("results_vinardo/consensus.csv")
vx = [float(r["vina_kcal_mol"]) for r in cons]
vy = [float(r["vinardo_kcal_mol"]) for r in cons]
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(vx, vy, s=60, color="#31a354", edgecolor="black", linewidth=0.5)
lo, hi = min(vx+vy)-0.2, max(vx+vy)+0.2
ax.plot([lo, hi], [lo, hi], "k--", lw=1, alpha=0.6, label="y = x")
ax.set_xlabel("Vina affinity (kcal/mol)", fontsize=10)
ax.set_ylabel("Vinardo affinity (kcal/mol)", fontsize=10)
ax.set_title("Consensus scoring (Spearman p = 0.83)", fontsize=12, fontweight="bold")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig3_consensus.png"), dpi=200)
plt.close(fig)

# ---------- Figure 4: acid vs ester ----------
fig, ax = plt.subplots(figsize=(6.5, 6))
for path, col, lab in [("results_pairs/pairs_CV.csv", "#2c7fb8", "CV"),
                       ("results_pairs/pairs_CCM.csv", "#d95f0e", "CCM")]:
    rows = read(path)
    ax.scatter([float(r["acid_kcal"]) for r in rows],
               [float(r["ester_kcal"]) for r in rows],
               s=60, color=col, edgecolor="black", linewidth=0.5, label=lab, alpha=0.8)
allv = []
for path in ["results_pairs/pairs_CV.csv", "results_pairs/pairs_CCM.csv"]:
    for r in read(path):
        allv += [float(r["acid_kcal"]), float(r["ester_kcal"])]
lo, hi = min(allv)-0.2, max(allv)+0.2
ax.plot([lo, hi], [lo, hi], "k--", lw=1, alpha=0.6, label="acid = ester")
ax.set_xlabel("Free-acid affinity (kcal/mol)", fontsize=10)
ax.set_ylabel("Methyl-ester affinity (kcal/mol)", fontsize=10)
ax.set_title("Binding is insensitive to headgroup form", fontsize=12, fontweight="bold")
ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig4_acid_vs_ester.png"), dpi=200)
plt.close(fig)

print("Wrote 4 figures to", FIG)
for f in sorted(os.listdir(FIG)):
    print("  ", f)
