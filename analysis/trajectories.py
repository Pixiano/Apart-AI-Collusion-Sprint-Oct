"""Task 4: per-seed mean price (3 firms) at rounds 30, 40, 50, 60 for every branch. CSV has all settings; the markdown shows
the main sweep for both models, one row per seed, as r30 then r40/r50/r60 per branch."""
from common import GATE, all_runs, write

runs = all_runs(("main", "hist0", "hist1", "commoff"))
mean = lambda r: round(sum(r["prices"]) / 3, 1)
full = []
for run in runs:
    r30 = mean(run["base"][-1])
    for tag, br in sorted(run["branches"].items()):
        rs = {r["round"]: r for r in br["rows"]}
        full.append([run["model"], run["setting"], run["seed"], "yes" if run["gate"] >= GATE else "no", tag, r30] + [mean(rs[k]) for k in (40, 50, 60)])
write("trajectories_all", ["model", "setting", "seed", "gated", "branch", "r30", "r40", "r50", "r60"], full)

HEAD = ["none", "clone_k1_hid", "family_k1_hid", "undercutter_k1_hid", "undercutter_k2_hid", "undercutter_k1_ann"]
tab = []
for run in [r for r in runs if r["setting"] == "main"]:
    cells = [run["model"], run["seed"], f"{run['gate']:.2f}", mean(run["base"][-1])]
    for tag in HEAD:
        br = run["branches"].get(tag)
        cells.append("/".join(str(mean(r)) for r in br["rows"] if r["round"] in (40, 50, 60)) if br else "-")
    tab.append(cells)
write("trajectories", ["model", "seed", "gate CI 16-30", "r30"] + [f"{t} r40/r50/r60" for t in HEAD], tab,
      "Per-seed mean price at rounds 30, 40, 50, 60 (main sweep)",
      "Mean of the three firms' prices in that round. Round 30 is the shared base run. '-' = branch not run for that model. "
      "Gate passes at CI >= 0.5 (gemma seed 12 fails). All settings and branches: trajectories_all.csv.")
