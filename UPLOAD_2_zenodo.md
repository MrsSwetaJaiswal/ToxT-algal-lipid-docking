# Upload #2 — Zenodo (the big MD data)

**Goes here:** the large molecular-dynamics trajectories and system files that are
too big for GitHub.
**Size:** ~1.2 GB.
**You get:** a permanent **DOI** to cite in the paper.

---

## What goes to Zenodo (for reference)
- `md/*/traj.dcd` — the trajectories (the bulk, ~1.1 GB)
- `md/*/system.xml` — the serialized OpenMM systems (~133 MB)
- `md/*/system.pdb` and `md/*/system_pub.pdb` — topologies (both numberings)
- `md/*/production_log.csv` — thermodynamic logs

Everything else already went to GitHub (Upload #1).

---

## Steps

1. **Make one bundle file.** From the project folder, run:
```bash
cd "C:/Users/ASUS/Claude/Projects/AutoDock"
tar -czf ToxT_MD_data.tar.gz md/*/traj.dcd md/*/system*.pdb md/*/system.xml md/*/production_log.csv
```
This creates a single file, `ToxT_MD_data.tar.gz`, containing all the big data.
*(Or just ask me — I can build this bundle for you.)*

2. Go to https://zenodo.org → sign in (free; you can log in with GitHub or ORCID).

3. Click **New upload** → drag in `ToxT_MD_data.tar.gz`.

4. Fill the form:
   - **Title:** e.g. "Molecular dynamics trajectories: algal lipids bound to *Vibrio cholerae* ToxT"
   - **Authors:** you and co-authors
   - **Description:** one paragraph (what the data is: 50 ns MD of ToxT–lipid complexes, 3GBG)
   - **Keywords:** ToxT, molecular dynamics, AutoDock Vina, OpenMM, Vibrio cholerae, algal lipids
   - **License:** e.g. Creative Commons Attribution (CC-BY)

5. Click **Publish** → Zenodo shows a **DOI** like `10.5281/zenodo.1234567`.

6. Copy that DOI. You'll paste it into the paper's Data Availability statement.

---

## Optional (nice, not required)
On Zenodo you can **link your GitHub repo** so that every GitHub "release"
automatically gets archived with its own DOI. Do this from Zenodo → your
account → GitHub tab.

---

Done. Now paste **both** the GitHub URL and the Zenodo DOI into the manuscript's
Data Availability statement (paste-ready text is in `DATA_AVAILABILITY.md`).
