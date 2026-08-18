"""Run Chai-1 structure prediction on the same ToxT-DNA complex used for the
AlphaFold3 model (Section 3.13 / Figure 11), for cross-method comparison.

Run (chai env):
  C:\\Users\\ASUS\\miniforge3\\envs\\chai\\python.exe run_chai.py
"""
from pathlib import Path
from chai_lab.chai1 import run_inference

fasta_path = Path(__file__).parent / "toxt_dna.fasta"
output_dir = Path(__file__).parent / "output"

candidates = run_inference(
    fasta_file=fasta_path,
    output_dir=output_dir,
    use_esm_embeddings=True,
    use_msa_server=True,       # free ColabFold MSA server -- needs internet
    num_trunk_recycles=3,
    num_diffn_timesteps=200,
    num_diffn_samples=5,       # 5 models, matching the AF3 run
    seed=42,
    low_memory=True,           # needed for the 4GB RTX 3050
)

print("Done. Outputs in:", output_dir)
print("Ranked scores:", candidates.ranking_data)
