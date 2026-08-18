"""Chai-1 on ToxT + the REAL El Tor ctxAB toxbox DNA (1 protein copy).

DNA = positions -76 to -41 of PctxAB (Dittmer & Withey 2012, J Bacteriol
194:5255, Fig. 1) -- the El Tor-length region containing both functional
toxboxes, matching their fully-functional pJW211 construct. Supersedes the
generic consensus construct used in run_chai.py.

Run (chai env):
  C:\\Users\\ASUS\\miniforge3\\envs\\chai\\python.exe run_chai_eltor.py
"""
from pathlib import Path
from chai_lab.chai1 import run_inference

fasta_path = Path(__file__).parent / "toxt_dna_eltor.fasta"
output_dir = Path(__file__).parent / "output_eltor"

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
