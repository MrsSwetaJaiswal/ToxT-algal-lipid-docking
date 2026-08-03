# Data & Code Availability — deposit guide

This file has three parts:
1. the **statement** to paste into the manuscript,
2. the **GitHub** push steps (code + small files),
3. the **Zenodo** upload checklist (large MD data → DOI).

---

## 1. Manuscript "Data and Code Availability" statement (paste-ready)

> **Data and code availability.** All code (docking, molecular-dynamics and
> analysis scripts), input structures, configuration files and small outputs are
> available at https://github.com/MrsSwetaJaiswal/ToxT-algal-lipid-docking
> (v1.0.0, archived at Zenodo, DOI:
> [10.5281/zenodo.21778158](https://doi.org/10.5281/zenodo.21778158)). Full
> molecular-dynamics trajectories, serialized systems and simulation topologies
> (~3.7 GB compressed) are archived separately at Zenodo (DOI:
> [10.5281/zenodo.21767402](https://doi.org/10.5281/zenodo.21767402)). Docking
> is deterministic (random seed = 42). Residue numbering follows PDB 3GBG;
> shared topology files were renumbered to the same scheme. The ToxT structure
> (PDB 3GBG) is available from the RCSB PDB; ligand structures are from PubChem
> (CIDs listed in the Methods).

*(Status 2026-08-03: both DOIs above are real and confirmed — code archive
(v1.0.0 release, Software resource type, CC-BY-4.0) and MD trajectory data
(Dataset resource type). No placeholders remain in this statement; the "link
GitHub to Zenodo" step in Section 3 below is done.)*

---

## 2. GitHub — push the code (you do this; needs your account)

The repository is already organized and a `.gitignore` excludes the large
trajectory files. From the project folder:

```bash
cd "C:/Users/ASUS/Claude/Projects/AutoDock"
git init
git add .
git commit -m "Docking + MD of algal lipids against V. cholerae ToxT"
git branch -M main
# create an empty repo on github.com first, then:
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

Before pushing, sanity-check that big files are excluded:

```bash
git status            # should NOT list any *.dcd, system.xml, .venv/, node_modules/
du -sh .git           # should be tens of MB, not gigabytes
```

If a large file slipped in, it's still in `.gitignore` — re-run `git rm --cached <file>`.

**What ends up on GitHub:** all `*.py` / `*.js` scripts, `structures/`,
`ligands/`, `prepared_structures/`, `docking_configs/`, all `results_*/` CSVs,
`figures/`, per-run `md/*/system_pub.pdb` + logs + `analysis/`, the manuscript,
and the environment spec files.

---

## 3. Zenodo — archive the large MD data (→ DOI)

GitHub can't hold the trajectories (~90 MB each × 14 ≈ 1.5–2 GB). Put them on
Zenodo (free, gives a citable DOI, integrates with GitHub).

**Bundle to upload** (zip these):
- `md/*/traj.dcd` — trajectories (the bulk of the data)
- `md/*/system.xml` — serialized OpenMM systems
- `md/*/system_pub.pdb` and `md/*/system.pdb` — topologies (both numberings)
- `md/*/production_log.csv` — thermodynamic logs
- `md/*/final_state.xml` (optional) — restart states

Suggested command to build the bundle:
```bash
# from the project folder
tar -czf ToxT_MD_data.tar.gz --exclude='md/epa_smoketest/*' md/*/traj.dcd md/*/system*.pdb md/*/system.xml md/*/production_log.csv
```
Use the filename `ToxT_MD_data.tar.gz` exactly — that's the name `.gitignore`
excludes; a different name (e.g. the `ToxT_MD_trajectories.tar.gz` this doc used
to suggest) would NOT be gitignored and risks `git add .` staging a multi-GB file.
The `--exclude` is needed because `epa_smoketest` (a throwaway dev/test run) has
its own `traj.dcd` / `system*.pdb` that would otherwise match. This bundle has
already been built once (2026-08-02/03, 3.68 GB, 215 files, verified) — see
`UPLOAD_2_zenodo.md` for current status; only rebuild it if the MD data changes.

**Steps:**
1. Create a free account at https://zenodo.org.
2. New upload → drag in `ToxT_MD_trajectories.tar.gz`.
3. Fill metadata (title, authors, description, keywords: ToxT, molecular docking,
   molecular dynamics, AutoDock Vina, OpenMM, Vibrio cholerae, algal lipids).
4. (Optional) link your GitHub repo so a release is snapshotted automatically.
5. Publish → copy the **DOI** → paste into the manuscript statement (§1) and README.

---

## Notes
- You do **not** need to write any code — everything is scripted already.
- A permissive license (MIT for code) is recommended; add a `LICENSE` file before
  pushing if the journal or your institution requires one.
- Keep the seed (42) and environment files with the deposit so runs reproduce exactly.
