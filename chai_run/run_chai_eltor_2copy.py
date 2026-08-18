"""Chai-1 on ToxT + the REAL El Tor ctxAB toxbox DNA, with TWO ToxT copies.

Same DNA as run_chai_eltor.py (PctxAB -76 to -41, both functional toxboxes)
but modelling two ToxT chains. Tests the two-monomer/dimer hypothesis: Dittmer
& Withey 2012 saw two distinct shifted EMSA species with increasing [ToxT],
consistent with one monomer per toxbox, and suggested binding may be
cooperative via dimerization -- though they also note most ToxT is monomeric
in solution.

Run (chai env):
  C:\\Users\\ASUS\\miniforge3\\envs\\chai\\python.exe run_chai_eltor_2copy.py
"""
from pathlib import Path
from chai_lab.chai1 import run_inference

fasta_path = Path(__file__).parent / "toxt_dna_eltor_2copy.fasta"
output_dir = Path(__file__).parent / "output_eltor_2copy"

candidates = run_inference(
    fasta_file=fasta_path,
    output_dir=output_dir,
    use_esm_embeddings=True,
    use_msa_server=True,
    num_trunk_recycles=3,
    num_diffn_timesteps=200,
    num_diffn_samples=5,
    seed=42,
    low_memory=True,
)

print("Done. Outputs in:", output_dir)
print("Ranked scores:", candidates.ranking_data)
