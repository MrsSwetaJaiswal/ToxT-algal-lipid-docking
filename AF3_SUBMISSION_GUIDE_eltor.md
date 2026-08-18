# AlphaFold3 submission — ToxT-DNA, **real El Tor ctxAB toxbox sequence**

Supersedes the DNA used in `AF3_SUBMISSION_GUIDE.md` (the original run, already
done, results in `af3_toxt_dna/`). That first run used a *generic synthetic*
construct: two tandem copies of the 13-bp toxbox consensus (yrTTTTwwTwAww) with
GC clamps — a reasonable placeholder, but not a real promoter sequence from any
strain.

**This guide uses the actual experimentally-characterised ctxAB promoter
sequence**, transcribed from Dittmer & Withey 2012 (*J Bacteriol* 194:5255-5263,
"Identification and Characterization of the Functional Toxboxes in the Vibrio
cholerae Cholera Toxin Promoter"), Figure 1.

## Why this sequence

- The ctxAB promoter contains a run of `GATTTTT` heptad repeats. **Classical
  biotype (O395) has 6 perfect repeats + 1 imperfect; El Tor biotype has only
  the 3 promoter-proximal ones**, but "otherwise retain[s] the same DNA sequence
  as that of classical strain O395 at PctxAB" (Dittmer & Withey 2012, Discussion).
  The experimental strain in this study is **El Tor**, so the El Tor-length
  region is the biologically correct input.
- The 36-bp region below spans **position -76 to -41** relative to the
  transcription start site. This exactly matches the paper's `pJW211` construct,
  which they showed is **fully functional** — in fact more strongly
  ToxT-activated than the full-length promoter (their Fig. 3).
- It contains **both functional toxboxes** identified in that paper:
  - **toxbox 1** = positions -72 to -60 (heptad repeats 5 + 6) — strongly
    protected in copper-phenanthroline footprinting
  - **toxbox 2** = positions -58 to -46 (imperfect repeat 7 + downstream A/T-rich
    region; the paper gives -58..-49 verbatim as `ATTTCAAAT`) — more weakly
    protected/less sequence-specific
- Both toxboxes are required: mutating either one severely reduces ToxT
  activation; mutating both abolishes ToxT binding entirely.

### Transcription verification (why this sequence is trusted)
The full classical footprint region (-109 to -41) was transcribed from Fig. 1 and
checked three independent ways before use:
1. Perfect `GATTTTT` repeat count = **6** (matches the paper's stated count; an
   initial transcription attempt gave 5 and was caught and corrected by this check)
2. Total length = **69 bp**, exactly matching the stated -109..-41 inclusive span
3. Contains the literal substring `ATTTCAAAT`, which the paper's text gives
   independently for positions -58 to -49

Classical O395 full region (-109 to -41):
`GTATATTTTGATTTTTGATTTTTGATTTTTGATTTTTGATTTTTGATTTTTGATTTCAAATAATACAAA`

---

## Steps

1. Go to **https://alphafoldserver.com**, sign in.

2. **"+ Add entity"** — build **three** entities:

   **Entity 1 — Protein** (copies: **1** for the baseline run; see below for the
   2-copy variant)
   ```
   MIGKKSFQTNVYRMSKFDTYIFNNLYINDYKMFWIDSGIAKLIDKNCLVSYEINSSSIILLKKNSIQRFSLTSLSDENINVSVITISDSFIRSLKSYILGDLMIRNLYSENKDLLLWNCEHNDIAVLSEVVNGFREINYSDEFLKVFFSGFFSKVEKKYNSIFITDDLDAMEKISCLVKSDITRNWRWADICGELRTNRMILKKELESRGVKFRELINSIRISYSISLMKTGEFKIKQIAYQSGFASVSYFSTVFKSTMNVAPSEYLFMLTGVAEK
   ```

   **Entity 2 — DNA** (copies: 1) — top strand, -76 to -41
   ```
   TTTTGATTTTTGATTTTTGATTTCAAATAATACAAA
   ```

   **Entity 3 — DNA** (copies: 1) — bottom strand (reverse complement, verified)
   ```
   TTTGTATTATTTGAAATCAAAAATCAAAAATCAAAA
   ```

3. Leave ligands/ions empty. **"Continue and preview job"** -> **"Confirm and
   submit job."**

4. Download results, extract to **`af3_toxt_dna_eltor/`** in the project root.

---

## Run this TWICE (the stoichiometry test)

Submit the same job twice, changing only Entity 1's **copies** field:

| Run | Protein copies | Extract to | Question it answers |
|---|---|---|---|
| A | **1** | `af3_toxt_dna_eltor/` | baseline, directly comparable to the original run |
| B | **2** | `af3_toxt_dna_eltor_2copy/` | does a ToxT dimer engage the two-toxbox site better? |

The 2-copy run tests a real hypothesis from the source paper: their EMSAs showed
**two distinct shifted species** as ToxT concentration increased, "consistent
with one ToxT monomer occupying one toxbox... then a second ToxT monomer
occupying the second toxbox," and they note binding "may be cooperative,
potentially by ToxT dimerization." Note the paper also states most ToxT is
monomeric in solution and monomers can bind individual toxboxes — so this is
genuinely open, not a settled question.

---

## What I'll do with the results
- Pull pTM / ipTM / PAE for each run, compare 1-copy vs 2-copy, and compare both
  against the original synthetic-DNA run (pTM 0.85 protein, ipTM 0.31 complex).
- Check geometry: in the 2-copy model, does each ToxT chain sit on a *different*
  toxbox (toxbox 1 vs toxbox 2), as the EMSA two-species result would predict?
- Regenerate the PAE/pLDDT confidence figure (`make_af3_confidence_fig.py`) for
  the new runs, for a side-by-side against Figure S22.

## Honest caveats
- Real promoter sequence now, but still a **36-bp fragment in isolation** — no
  flanking genomic context, no RNA polymerase, no H-NS (which the paper notes
  also binds this A/T-rich region and represses ctxAB).
- AF3 still does not include the fatty acid; the lipid-vs-DNA competition is
  still assessed by comparing conformations, not co-modelling.
- A higher ipTM for 2 copies would *support* the dimer/two-monomer model but
  would not prove it — it is a confidence metric from a prediction, not
  experimental evidence.
