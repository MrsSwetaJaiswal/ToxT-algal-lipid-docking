# AlphaFold3 submission — ToxT–DNA complex (for the competition model)

You do a ~2-minute web submission; I do all the analysis afterward.

## What we're modelling
ToxT bound to its target promoter DNA (a "toxbox" element). We'll then compare
this DNA-bound conformation to the fatty-acid-bound crystal (3GBG) to assess how
lipid binding in the pocket opposes DNA engagement (the Lowden mechanism).

The DNA is a 34-bp duplex containing **two direct-repeat toxboxes** (the ctxAB/tcpA
arrangement; toxbox consensus yrTTTTwwTwAww; Withey & DiRita 2006). If you have the
exact ctxAB promoter sequence from a reference you prefer, you can substitute it.

---

## Steps

1. Go to **https://alphafoldserver.com** and sign in with a Google account.

2. Click **"+ Add entity"** and build **three** entities:

   **Entity 1 — Protein** (copies: 1)
   Paste the ToxT sequence:
   ```
   MIGKKSFQTNVYRMSKFDTYIFNNLYINDYKMFWIDSGIAKLIDKNCLVSYEINSSSIILLKKNSIQRFSLTSLSDENINVSVITISDSFIRSLKSYILGDLMIRNLYSENKDLLLWNCEHNDIAVLSEVVNGFREINYSDEFLKVFFSGFFSKVEKKYNSIFITDDLDAMEKISCLVKSDITRNWRWADICGELRTNRMILKKELESRGVKFRELINSIRISYSISLMKTGEFKIKQIAYQSGFASVSYFSTVFKSTMNVAPSEYLFMLTGVAEK
   ```

   **Entity 2 — DNA** (copies: 1)
   ```
   GCACATTTTAATAAAATACATTTTAATAAAATGC
   ```

   **Entity 3 — DNA** (copies: 1)
   ```
   GCATTTTATTAAAATGTATTTTATTAAAATGTGC
   ```
   (Entities 2 and 3 are the two complementary strands of the duplex.)

3. Leave ligands/ions empty. Click **"Continue and preview job"** → **"Confirm and submit job."**

4. Wait a few minutes. When it's done, **download the results** (a `.zip`
   containing `.cif` model files and confidence scores).

5. Send me the downloaded file (or put it in the project folder and tell me the
   path). I'll take it from there.

---

## What I'll do with the result
- Pick the top-ranked model; report confidence (pTM/ipTM, PAE for the protein–DNA interface).
- Superpose the **fatty-acid-bound** ToxT (3GBG) onto the **DNA-bound** model.
- Assess whether pocket occupancy is compatible with the DNA-binding-competent
  conformation (the competition/mechanism analysis) and render the figure.

## Honest caveats (will go in the caption)
- AF3 predicts the ToxT–DNA complex; it is a **model**, not an experimental structure.
- AF3 does not include the fatty acid, so the competition is assessed by **comparing
  conformations**, not by co-modelling lipid + DNA.
- The DNA is a toxbox-consensus element; exact promoter geometry may differ.
