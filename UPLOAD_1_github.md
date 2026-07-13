# Upload #1 — GitHub (the code)

**Goes here:** all scripts, input files, settings, small result tables, and figures.
**Size:** ~60 MB.
**You get:** a repository URL to put in the paper.

You do NOT sort files by hand — `.gitignore` automatically skips the big
trajectory files. "Everything except the trajectories" goes to GitHub.

---

## What ends up on GitHub (for reference)
- All `*.py` and `*.js` scripts (docking, MD, analysis, figures)
- `structures/`, `ligands/`, `prepared_structures/`, `ligands_pdbqt/` (inputs)
- `docking_configs/` (settings)
- `results_CV/ results_CCM/ results_blind/ results_pairs/ results_vinardo/ results_batch/` (small CSV outputs)
- `figures/` (all manuscript figures)
- `md/*/system_pub.pdb`, `md/*/production_log.csv`, `md/*/analysis/` (small MD files)
- `README.md`, environment files, the manuscript
- **NOT** the trajectories or `system.xml` (those go to Zenodo — Upload #2)

---

## Steps

1. Go to https://github.com → sign in → **New repository** → give it a name
   (e.g. `ToxT-algal-lipid-docking`) → **Create** (leave it empty, no README).

2. In a terminal, from the project folder, run these lines one by one:

```bash
cd "C:/Users/ASUS/Claude/Projects/AutoDock"
git init
git add .
git commit -m "Docking + MD of algal lipids against V. cholerae ToxT"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
(Replace `<your-username>/<your-repo>` with what GitHub shows you.)

3. **Check the big files were skipped** (should print nothing):
```bash
git ls-files | grep -E "\.dcd$|system\.xml$"
```
If that prints nothing, you're good — the trajectories were correctly excluded.

4. Copy your repo URL (e.g. `https://github.com/you/ToxT-algal-lipid-docking`).
   You'll paste it into the paper's Data Availability statement.

---

Done with GitHub. Next: **Upload #2 — Zenodo** for the big data.
