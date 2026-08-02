"""Per-residue RMSF, apo vs. holo (ligand-bound), to test/qualify the proposed
allosteric-rigidification narrative (Section 3.13 / Discussion): does fatty-acid
occupancy of the N-terminal pocket restrain motion of the distant C-terminal
HTH DNA-binding domain (residues 188-276, per the AlphaFold3 model)?

apo:  apo_toxt_50ns (+ r2, r3)                          -- n = 3 replicates
holo: epa_50ns, gla_50ns, palmitic_50ns (free acid)      -- n = 3 replicates each,
      averaged per system first, then the 3 system profiles averaged/SD'd
      (n = 3 systems), symmetric with apo's n = 3 replicates.

RMSF computed on CA atoms only, after superposing each trajectory on its own
frame 0 (protein backbone) and restricting to the production window (>5 ns).

Run (conda analysis env -- OpenBLAS-based, avoids the "md" env's MKL crash
on concurrent numpy/mdtraj processes):
  C:\\Users\\ASUS\\miniforge3\\envs\\analysis\\python.exe make_apo_holo_rmsf_fig.py
"""
import os, numpy as np, mdtraj as md
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ppf = 250.0
PROD_START = int(5000 / ppf)  # 5 ns

POCKET = [12, 13, 14, 20, 22, 25, 31, 33, 71, 81, 226, 259, 261, 266]
HTH_CONTACTS = [214, 235, 237, 250, 256]  # DNA-contacting residues, AlphaFold3 model

HOLO_SYSTEMS = ["epa_50ns", "gla_50ns", "palmitic_50ns"]
APO_SYSTEM = "apo_toxt_50ns"

def rmsf_profile(name):
    D = "md/" + name
    top = D + "/system_pub.pdb" if os.path.exists(D + "/system_pub.pdb") else D + "/system.pdb"
    t = md.load(D + "/traj.dcd", top=top)
    bb = t.topology.select("protein and backbone")
    t.superpose(t, 0, atom_indices=bb)
    ca = t.topology.select("protein and name CA")
    resseq = np.array([t.topology.atom(i).residue.resSeq for i in ca])
    xyz = t.xyz[PROD_START:, ca, :]  # (frames, n_res, 3)
    avg = xyz.mean(0)
    rmsf = np.sqrt(((xyz - avg) ** 2).sum(-1).mean(0)) * 10.0  # nm -> A
    return resseq, rmsf

def replicate_mean(base):
    profiles = []
    resseq = None
    for suffix in ("", "_r2", "_r3"):
        name = base + suffix
        if os.path.exists("md/%s/traj.dcd" % name):
            resseq, rmsf = rmsf_profile(name)
            profiles.append(rmsf)
    return resseq, np.array(profiles).mean(0)

# apo: n=3 replicates directly
apo_reps = []
for suffix in ("", "_r2", "_r3"):
    name = APO_SYSTEM + suffix
    resseq, rmsf = rmsf_profile(name)
    apo_reps.append(rmsf)
apo_reps = np.array(apo_reps)
apo_mean, apo_sd = apo_reps.mean(0), apo_reps.std(0, ddof=1)

# holo: per-system replicate-mean, then mean/SD across the 3 systems
holo_system_profiles = []
for base in HOLO_SYSTEMS:
    rs, prof = replicate_mean(base)
    holo_system_profiles.append(prof)
holo_system_profiles = np.array(holo_system_profiles)
holo_mean, holo_sd = holo_system_profiles.mean(0), holo_system_profiles.std(0, ddof=1)

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(resseq, apo_mean, color="#756bb1", lw=1.5, label="apo ToxT (n=3 replicates)")
ax.fill_between(resseq, apo_mean - apo_sd, apo_mean + apo_sd, color="#756bb1", alpha=0.18, lw=0)
ax.plot(resseq, holo_mean, color="#2c7fb8", lw=1.5,
        label="holo: EPA/\u03b3-linolenic/palmitic free acid (n=3 systems)")
ax.fill_between(resseq, holo_mean - holo_sd, holo_mean + holo_sd, color="#2c7fb8", alpha=0.18, lw=0)

ax.axvspan(188, 273, color="#fdd", alpha=0.35, zorder=0)
ax.text(230, ax.get_ylim()[1]*0.92 if ax.get_ylim()[1] > 0 else 1, "C-terminal HTH domain (188-276)",
        fontsize=8, color="#a33", ha="center")
for r in POCKET:
    ax.axvline(r, color="#2d6a2d", alpha=0.15, lw=1, zorder=0)
ax.plot([], [], color="#2d6a2d", alpha=0.5, lw=1, label="fatty-acid pocket residues")

ax.set_xlabel("Residue (crystal/PDB 3GBG numbering)", fontsize=11)
ax.set_ylabel("C\u03b1 RMSF (\u00c5)", fontsize=11)
ax.set_title("Per-residue RMSF, apo vs. ligand-bound ToxT", fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5, loc="upper left", framealpha=0.9)
ax.grid(alpha=0.25)
ax.set_xlim(resseq.min(), resseq.max())
fig.tight_layout()
os.makedirs("figures", exist_ok=True)
fig.savefig("figures/fig_apo_holo_rmsf.png", dpi=200)
print("wrote figures/fig_apo_holo_rmsf.png")

def region_stats(mask, label):
    a = apo_mean[mask]; h = holo_mean[mask]
    print("%-32s apo %.2f +/- %.2f A   holo %.2f +/- %.2f A   (holo-apo %+.2f A, n=%d residues)"
          % (label, a.mean(), apo_sd[mask].mean(), h.mean(), holo_sd[mask].mean(), (h-a).mean(), mask.sum()))

print()
print("=== Region-averaged RMSF (mean over residues; +/- is mean per-residue SD across replicates/systems) ===")
region_stats(np.ones(len(resseq), dtype=bool), "whole protein (%d residues)" % len(resseq))
region_stats(np.isin(resseq, POCKET), "fatty-acid pocket residues")
region_stats(np.isin(resseq, HTH_CONTACTS), "HTH DNA-contact residues")
region_stats((resseq >= 188) & (resseq <= 273), "C-terminal HTH domain (188-273)")
region_stats(resseq < 188, "N-terminal domain (<188)")
