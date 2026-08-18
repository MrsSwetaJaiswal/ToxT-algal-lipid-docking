# AlphaFold3 submission — ToxT-DNA complex, 2 ToxT copies (dimer test)

Companion to `AF3_SUBMISSION_GUIDE.md` (the original 1-copy run, already done —
results in `af3_toxt_dna/`). This submission tests whether modelling **two**
copies of ToxT against the same tandem two-toxbox DNA duplex gives a more
confident model (higher ipTM, lower interface PAE) than the single-chain
version. Motivation: the crystal (3GBG) is monomeric *without* DNA present,
but many AraC/XylS-family regulators dimerize specifically upon binding a
tandem-repeat site, and the DNA here has two toxbox repeats — one chain may
not be the right stoichiometry to engage both.

---

## Steps

1. Go to **https://alphafoldserver.com** and sign in with a Google account
   (same account as before is fine — this is a separate, new job).

2. Click **"+ Add entity"** and build **three** entities:

   **Entity 1 — Protein** (copies: **2** <- the only change from the original guide)
   ```
   MIGKKSFQTNVYRMSKFDTYIFNNLYINDYKMFWIDSGIAKLIDKNCLVSYEINSSSIILLKKNSIQRFSLTSLSDENINVSVITISDSFIRSLKSYILGDLMIRNLYSENKDLLLWNCEHNDIAVLSEVVNGFREINYSDEFLKVFFSGFFSKVEKKYNSIFITDDLDAMEKISCLVKSDITRNWRWADICGELRTNRMILKKELESRGVKFRELINSIRISYSISLMKTGEFKIKQIAYQSGFASVSYFSTVFKSTMNVAPSEYLFMLTGVAEK
   ```
   Set the "copies" field to **2** (not 1) — this tells AF3 to model two
   independent ToxT chains in the same complex, rather than pasting the
   sequence twice as separate entities (either works; "copies: 2" on one
   entity is the simpler UI path).

   **Entity 2 — DNA** (copies: 1) — identical to the original run
   ```
   GCACATTTTAATAAAATACATTTTAATAAAATGC
   ```

   **Entity 3 — DNA** (copies: 1) — identical to the original run
   ```
   GCATTTTATTAAAATGTATTTTATTAAAATGTGC
   ```

3. Leave ligands/ions empty. Click **"Continue and preview job"** — the
   preview should now show 4 chains total (2x protein + 2x DNA strand)
   instead of the original 3. **"Confirm and submit job."**

4. Wait a few minutes. **Download the results** (a `.zip` containing `.cif`
   model files and confidence scores), same as before.

5. Put the downloaded/extracted contents in a new folder, e.g.
   `af3_toxt_dna_2copy/` in the project root (parallel to the existing
   `af3_toxt_dna/`), and tell me the path (or just say it's there under that
   name and I'll find it).

---

## What I'll do with the result
- Extract pTM/ipTM/PAE for the top-ranked 2-copy model exactly as done for
  the 1-copy model (`chain_ptm`, `iptm` in `summary_confidences_0.json`).
- Compare directly against the existing 1-copy numbers (pTM 0.85 protein,
  ipTM 0.31 complex) to see whether 2 copies measurably improves confidence
  at the protein-DNA interface.
- Check the actual geometry: does each ToxT chain in the 2-copy model land
  on a *different* toxbox repeat (the dimer hypothesis), or do both chains
  converge on the same site / fail to separate sensibly (which would argue
  against the dimer interpretation regardless of the confidence numbers)?
- Regenerate the PAE/pLDDT confidence figure for the 2-copy model
  (same script, `make_af3_confidence_fig.py`, pointed at the new output) for
  a direct side-by-side with Figure S22.

## Honest caveats (same as the original run, still apply)
- This is still a **consensus toxbox**, not the literal native *ctxAB*
  promoter sequence.
- AF3 does not include the fatty acid — occupancy-vs-DNA-binding competition
  is still assessed by comparing conformations, not co-modelling.
- A higher ipTM for the 2-copy model would support the dimer hypothesis but
  would not by itself *prove* ToxT dimerizes on DNA in vivo — it's evidence
  from a structure-prediction confidence metric, not an experimental result.
