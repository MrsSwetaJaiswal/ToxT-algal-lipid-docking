# Upload #2 — Zenodo (the big MD data)

**Goes here:** the large molecular-dynamics trajectories and system files that are
too big for GitHub.
**Size:** **~4.4 GB, final** — the full n=3 replicate campaign is complete.
**You get:** a permanent **DOI** to cite in the paper.

**Ready to upload now.** The replicate campaign finished 2026-08-01 (all 28
replicates, 42/42 trajectories) — this is the complete, final dataset. No need
to wait any further; proceed with the steps below whenever convenient.

---

## Progress (updated as the campaign runs — see `CAMPAIGN_LOG.md` for details)
_Last updated: 2026-08-01 — **CAMPAIGN COMPLETE**, 28/28 replicates, 42/42 total trajectories._

All 14 systems (EPA, methyl-EPA, EPA-carboxylate, GLA, GLA-ester,
GLA-carboxylate, palmitic, methyl-palmitate, palmitic-carboxylate,
palmitoleate/PAM, glucose decoy, pentadecanal, tridecanoic, apo-ToxT) now have
independent r1+r2+r3 replicates (distinct seeds) at 50 ns each.

Current on-disk data size (all `md/*/` run directories, excluding the empty
`epa_smoketest` dev/test run): **~4.4 GB**. `glucose_core_50ns` (a supplementary
decoy-seeded-in-core control used in `make_specificity_fig.py`) is real data and
included.

---

## What goes to Zenodo (for reference)
- `md/*/traj.dcd` — the trajectories (the bulk)
- `md/*/system.xml` — the serialized OpenMM systems
- `md/*/system.pdb` and `md/*/system_pub.pdb` — topologies (both numberings)
- `md/*/production_log.csv` — thermodynamic logs

The wildcard `md/*/...` glob in the bundle command below automatically covers
every replicate directory (`_r2`, `_r3`, etc.) as they're produced, and
naturally skips `epa_smoketest` since its files use different names
(`final_state.xml` / `md_log.csv`, not `system.xml` / `production_log.csv`).

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
