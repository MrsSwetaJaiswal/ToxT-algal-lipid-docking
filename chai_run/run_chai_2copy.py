"""Run Chai-1 on the ToxT-DNA complex with TWO copies of the ToxT protein
chain (testing whether the tandem two-toxbox DNA site is better engaged by a
ToxT dimer than by a single chain -- the 1-copy run is in ../output/).

Run (chai env):
  C:\\Users\\ASUS\\miniforge3\\envs\\chai\\python.exe run_chai_2copy.py
"""
from pathlib import Path
from chai_lab.chai1 import run_inference

fasta_path = Path(__file__).parent / "toxt_dna_2copy.fasta"
output_dir = Path(__file__).parent / "output_2copy"

candidates = run_inference(
    fasta_file=fasta_path,
    output_dir=output_dir,
    use_esm_embeddings=True,
    use_msa_server=True,       # free ColabFold MSA server -- needs internet
    num_trunk_recycles=3,
    num_diffn_timesteps=200,
    num_diffn_samples=5,
    seed=42,
    low_memory=True,           # needed for the 4GB RTX 3050
)

print("Done. Outputs in:", output_dir)
print("Ranked scores:", candidates.ranking_data)
