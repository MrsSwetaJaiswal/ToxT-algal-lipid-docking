# Upload #2 — Zenodo (the big MD data)

**Goes here:** the large molecular-dynamics trajectories and system files that are
too big for GitHub.
**Size:** on-disk `md/*/` data ~5.0 GB; the compressed upload bundle was **3.68 GB**
(`ToxT_MD_data.tar.gz`) — the full n=3 replicate campaign is complete.
**You get:** a permanent **DOI** to cite in the paper.

## DONE — published 2026-08-03

**DOI: [10.5281/zenodo.21767402](https://doi.org/10.5281/zenodo.21767402)**

This DOI is now filled into `DATA_AVAILABILITY.md`'s paste-ready statement and
directly into `MANUSCRIPT_DRAFT.md` Section 6 / `build_docx.js` (docx
regenerated). The only related item still outstanding is the separate
*code*-archive DOI (linking the GitHub repo itself to Zenodo, "Optional" section
below) — not required, but nice to have if you want a citable DOI for the code
independent of the data.

---

## Progress (updated as the campaign runs — see `CAMPAIGN_LOG.md` for details)
_Last updated: 2026-08-03 — **UPLOADED, DOI live**: 10.5281/zenodo.21767402._

All 14 systems (EPA, methyl-EPA, EPA-carboxylate, GLA, GLA-ester,
GLA-carboxylate, palmitic, methyl-palmitate, palmitic-carboxylate,
palmitoleate/PAM, glucose decoy, pentadecanal, tridecanoic, apo-ToxT) now have
independent r1+r2+r3 replicates (distinct seeds) at 50 ns each.

Current on-disk data size (all `md/*/` run directories, excluding the empty
`epa_smoketest` dev/test run): **~5.0 GB**. `glucose_core_50ns` (a supplementary
decoy-seeded-in-core control used in `make_specificity_fig.py`) is real data and
included. The compressed, ready-to-upload bundle (`ToxT_MD_data.tar.gz`) is
**3.68 GB**, 215 files — rebuilt from scratch on 2026-08-02/03 against the
now-complete campaign (the previous tarball, from Jul 14, predated the triplicate
replicates and was only ~1.2 GB).

---

## What goes to Zenodo (for reference)
- `md/*/traj.dcd` — the trajectories (the bulk)
- `md/*/system.xml` — the serialized OpenMM systems
- `md/*/system.pdb` and `md/*/system_pub.pdb` — topologies (both numberings)
- `md/*/production_log.csv` — thermodynamic logs

The wildcard `md/*/...` glob in the bundle command below automatically covers
every replicate directory (`_r2`, `_r3`, etc.) as they're produced. `epa_smoketest`
is naturally skipped by the `system.xml` / `production_log.csv` patterns (it uses
different filenames there — `final_state.xml` / `md_log.csv`) but **not** by the
`traj.dcd` / `system*.pdb` patterns, since it does have files with those exact
names (it's a real, if throwaway, run). The `--exclude` flag in the command below
is required to keep it out — confirmed by rebuilding the bundle on 2026-08-02/03
(215 files, 0 smoketest entries; the pre-triplicate Jul 14 tarball predates this
fix and was never checked for it).

Everything else already went to GitHub (Upload #1).

---

## Steps

1. **Make one bundle file.** From the project folder, run:
```bash
cd "C:/Users/ASUS/Claude/Projects/AutoDock"
tar -czf ToxT_MD_data.tar.gz --exclude='md/epa_smoketest/*' md/*/traj.dcd md/*/system*.pdb md/*/system.xml md/*/production_log.csv
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
