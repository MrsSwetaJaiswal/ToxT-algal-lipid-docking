"""Batch summary of completed MD runs: backbone RMSD, ligand-pocket COM (min-image),
bound fraction. Writes md/md_summary.csv. Run in .venv."""
import os, csv, numpy as np, mdtraj as md

RUNS = [
    ("epa_50ns", "EPA", "free acid"), ("methyl_epa_50ns", "EPA", "methyl ester"),
    ("epa_deprot_50ns", "EPA", "carboxylate"),
    ("gla_50ns", "GLA", "free acid"), ("gla_ester_50ns", "GLA", "methyl ester"),
    ("gla_deprot_50ns", "GLA", "carboxylate"),
    ("palmitic_50ns", "palmitic", "free acid"), ("methyl_palmitate_50ns", "palmitic", "methyl ester"),
    ("palmitic_deprot_50ns", "palmitic", "carboxylate"),
    ("pam_50ns", "palmitoleate (PAM)", "free acid [+ctrl]"),
    ("glucose_decoy_50ns", "glucose", "decoy [-ctrl]"),
    ("pentadecanal_50ns", "pentadecanal", "aldehyde [weak]"),
    ("tridecanoic_50ns", "tridecanoic", "free acid [weak]"),
]
POCKET = [9,10,11,17,19,22,28,30,68,78,213,246,248,253]
ppf = 250.0
rows = []
for name, lipid, form in RUNS:
    D = "md/" + name
    if not os.path.exists(D + "/traj.dcd"):
        continue
    try:
        t = md.load(D + "/traj.dcd", top=D + "/system.pdb")
    except Exception as e:
        print("skip", name, e); continue
    if t.n_frames < 5:
        continue
    start = int(5000 / ppf)
    lig = t.topology.select("resname UNK")
    sel = " or ".join("(residue %d and name CA)" % r for r in POCKET)
    pocket = t.topology.select(sel)
    com = np.zeros(t.n_frames)
    if len(lig):
        for i in range(t.n_frames):
            xyz = t.xyz[i]; box = t.unitcell_lengths[i]
            d = xyz[lig].mean(0) - xyz[pocket].mean(0)
            d -= box * np.round(d / box)
            com[i] = np.linalg.norm(d) * 10.0
    bb = t.topology.select("protein and backbone")
    t.superpose(t, 0, atom_indices=bb)
    rmsd = md.rmsd(t, t, 0, atom_indices=bb) * 10.0
    prod = slice(start, t.n_frames)
    commean = float(com[prod].mean()) if len(lig) else float("nan")
    bound = float((com[prod] < 10).mean() * 100) if len(lig) else float("nan")
    rows.append({"run": name, "lipid": lipid, "form": form,
                 "ns": round(t.n_frames * ppf / 1000, 1),
                 "bb_rmsd": round(float(rmsd[prod].mean()), 2),
                 "bb_rmsd_sd": round(float(rmsd[prod].std()), 2),
                 "com_A": round(commean, 1) if len(lig) else "",
                 "bound_pct": round(bound) if len(lig) else ""})
    print("%-22s %-9s %-14s bbRMSD %.2f  COM %s  bound %s" %
          (name, lipid, form, rmsd[prod].mean(),
           "%.1f" % commean if len(lig) else "n/a",
           "%.0f%%" % bound if len(lig) else "n/a"))

with open("md/md_summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["run","lipid","form","ns","bb_rmsd","bb_rmsd_sd","com_A","bound_pct"])
    w.writeheader(); w.writerows(rows)
print("\nWrote md/md_summary.csv (%d runs)" % len(rows))
