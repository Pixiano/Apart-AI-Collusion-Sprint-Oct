"""Task 2: how the remaining firms react to a scripted undercutter (k1, k2, hidden, announced). Gated runs only.

The undercutter prices at (lowest rival price last round) - 1. Remaining firm i in round r (32-60) is scored against the
undercutter's price in round r-1 (the one it could see): 'below' (punish: priced under it), 'match' (equal), 'above' (holds).
"""
import numpy as np

from common import GATE, all_runs, bootstrap, fmt, write

runs = [r for r in all_runs(("main", "hist0", "hist1", "commoff")) if r["gate"] >= GATE or r["setting"] == "commoff"]
per_run, cells = [], {}
for run in runs:
    ctrl = run["branches"].get("none")
    for tag, br in run["branches"].items():
        if not tag.startswith("undercutter"):
            continue
        rep = br["replaced"]
        keep = [i for i in range(3) if i not in rep]
        rs = br["rows"]
        pre = np.mean([run["base"][-1]["prices"][i] for i in keep])  # remaining firms, round 30
        rem = [np.mean([r["prices"][i] for i in keep]) for r in rs]  # rounds 31-60
        first = next((k + 1 for k, v in enumerate(rem) if v < pre), None)  # rounds after the swap
        sc = {"below": 0, "match": 0, "above": 0}
        for k in range(1, 30):
            u = min(rs[k - 1]["prices"][j] for j in rep)
            for i in keep:
                p = rs[k]["prices"][i]
                sc["below" if p < u else "match" if p == u else "above"] += 1
        n = sum(sc.values())
        slope = np.polyfit(range(31, 61), rem, 1)[0]
        cslope = np.polyfit(range(31, 61), [np.mean([r["prices"][i] for i in keep]) for r in ctrl["rows"]], 1)[0] if ctrl else float("nan")
        row = dict(model=run["model"], setting=run["setting"], branch=tag, seed=run["seed"], pre=pre, first=first,
                   below=sc["below"] / n, match=sc["match"] / n, above=sc["above"] / n, ever_below=sc["below"] > 0,
                   slope=slope, cslope=cslope, end=rem[-1], und_end=min(rs[-1]["prices"][j] for j in rep))
        per_run.append(row)
        cells.setdefault((run["model"], run["setting"], tag), []).append(row)

write("timing_per_run", ["model", "history/comm", "branch", "seed", "remaining price r30", "rounds to first fall", "share below undercutter",
                         "share match", "share above", "slope remaining (per round)", "slope control", "remaining r60", "undercutter r60"],
      [[r["model"], r["setting"], r["branch"], r["seed"], fmt(r["pre"], 1), r["first"] or ">30", fmt(r["below"]), fmt(r["match"]), fmt(r["above"]),
        fmt(r["slope"], 2, True), fmt(r["cslope"], 2, True), fmt(r["end"], 1), r["und_end"]] for r in per_run])

tab = []
for (m, s, t), v in sorted(cells.items()):
    fs = [r["first"] for r in v if r["first"]]
    sl = bootstrap([r["slope"] for r in v])
    tab.append([m, s, t, len(v), f"{np.median(fs):.0f} ({min(fs)}-{max(fs)})" if fs else "n/a",
                f"{sum(r['first'] is None for r in v)}", f"{100 * np.mean([r['below'] for r in v]):.0f}%",
                f"{100 * np.mean([r['match'] for r in v]):.0f}%", f"{100 * np.mean([r['above'] for r in v]):.0f}%",
                f"{sum(r['ever_below'] for r in v)} of {len(v)}",
                f"{fmt(sl[0], 2, True)} ({fmt(sl[1], 2, True)}, {fmt(sl[2], 2, True)})",
                fmt(np.mean([r["cslope"] for r in v]), 2, True), fmt(np.mean([r["end"] for r in v]), 1), fmt(np.mean([r["und_end"] for r in v]), 1)])
write("timing", ["model", "history/comm", "branch", "runs", "rounds to first fall, median (range)", "never fall",
                 "below undercutter", "match", "above", "runs ever below", "slope remaining, price/round (95%)", "slope control",
                 "remaining r60", "undercutter r60"], tab, "Reaction to a scripted undercutter (remaining firms)",
     "Gated runs only, except commoff (comm off), where no base run is gated for deepseek and 1 of 5 for gemma, so all runs are shown "
     "and the row is not an effect. Remaining = firms not replaced (A and B for k1, A for k2). 'rounds to first fall' = rounds after "
     "round 30 until the remaining firms' mean price is first below its round-30 value. below/match/above: remaining firm-rounds 32-60 "
     "against the undercutter's price the round before. Slope = least-squares slope of the remaining firms' mean price over rounds 31-60; "
     "control = same firms in the no-swap branch.")
print(len(per_run), "undercutter branches")
