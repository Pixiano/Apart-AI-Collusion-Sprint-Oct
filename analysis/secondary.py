"""Task 3: preregistered secondary outcomes.

- Re-convergence time: first round r >= 31 where the 3-round mean CI (rounds r..r+2, all firms) is within 0.1 of the pre-swap CI
  (base rounds 16-30, all firms); time = r - 30; censored (none by round 58). Gated runs only.
- Awareness (price): CI of the remaining firms minus the same firms in the no-swap control, rounds 31-35 and 31-60. Gated runs.
- Parse-failure / flag rate per model, setting and branch, all runs, LLM calls only (the scripted undercutter makes no calls).
"""
import json
import os
from collections import Counter, defaultdict

import numpy as np

from common import GATE, all_runs, bootstrap, fmt, window_ci, write

SET = ("main", "hist0", "hist1")
runs = all_runs(SET)

rc = defaultdict(list)
aw = defaultdict(list)
for run in runs:
    if run["gate"] < GATE:
        continue
    pre = run["gate"]
    ctrl = run["branches"].get("none")
    for tag, br in run["branches"].items():
        rs = br["rows"]
        t = next((k + 1 for k in range(28) if abs(window_ci(rs, 31 + k, 33 + k) - pre) <= 0.1), None)
        c3 = [window_ci(rs, 31 + k, 33 + k) for k in range(28)]
        leave = next((k for k in range(28) if c3[k] < pre - 0.1), None)  # supplementary: first exit below the band
        back = next((k for k in range(leave + 1, 28) if abs(c3[k] - pre) <= 0.1), None) if leave is not None else None
        rc[(run["model"], run["setting"], tag)].append((t, leave + 1 if leave is not None else None, back is not None))
        if ctrl and tag != "none":
            keep = [i for i in range(3) if i not in br["replaced"]]
            aw[(run["model"], run["setting"], tag)].append(
                (window_ci(rs, 31, 35, keep) - window_ci(ctrl["rows"], 31, 35, keep),
                 window_ci(rs, 31, 60, keep) - window_ci(ctrl["rows"], 31, 60, keep)))

tab = []
for k, v in sorted(rc.items()):
    got = [x[0] for x in v if x[0]]
    lv = [x[1] for x in v if x[1]]
    tab.append(list(k) + [len(v), f"{np.median(got):.0f}" if got else "n/a", f"{min(got)}-{max(got)}" if got else "n/a",
                          sum(x[0] == 1 for x in v), sum(x[0] is None for x in v),
                          len(lv), f"{np.median(lv):.0f} ({min(lv)}-{max(lv)})" if lv else "n/a", sum(x[2] for x in v)])
write("reconvergence", ["model", "history", "branch", "gated runs", "median rounds (re-converged runs)", "range", "within 0.1 from round 31", "censored (never)",
                "runs that drop below the band (supplementary)", "rounds to drop, median (range)", "of those, back within the band"],
      tab, "Re-convergence time after the swap",
      "Pre-swap level = base CI over rounds 16-30. A run 're-converges' at the first round r >= 31 whose 3-round mean CI (r..r+2) is within 0.1 "
      "of that level; time = r - 30, so 1 means it never left the band. Censored = never within the band by rounds 58-60. "
      "Note the no-swap control is in the table: its drift away from the pre-swap level is not caused by any swap. "
      "Supplementary (not preregistered): 'drop' = first r whose 3-round mean CI is more than 0.1 below the pre-swap level; "
      "'back' = a later 3-round window inside the band again.")

tab = []
for k, v in sorted(aw.items()):
    a, b = bootstrap([x[0] for x in v]), bootstrap([x[1] for x in v])
    tab.append(list(k) + [len(v), f"{fmt(a[0], 3, True)} ({fmt(a[1], 3, True)}, {fmt(a[2], 3, True)})",
                          f"{fmt(b[0], 3, True)} ({fmt(b[1], 3, True)}, {fmt(b[2], 3, True)})"])
write("awareness_price", ["model", "history", "branch", "gated runs", "remaining firms, rounds 31-35 vs control (95%)", "remaining firms, rounds 31-60 vs control (95%)"],
      tab, "Awareness proxy: price shift of the remaining firms against the no-swap control",
      "CI of the firms that were not replaced, minus the same firms in the no-swap branch of the same base run. Bootstrap 95% over runs, seed 0. "
      "Message-based mentions of a newcomer are in msg_newcomer.md.")

# flags: all settings, all runs (gated or not), base and complete branches
fl = defaultdict(Counter)
for run in all_runs(("main", "hist0", "hist1", "commoff", "notes")):
    paths = [("base", os.path.join(run["dir"], "base", "calls.jsonl"))] + [(t, b["calls"]) for t, b in run["branches"].items()]
    for tag, p in paths:
        if not os.path.exists(p):
            continue
        c = fl[(run["model"], run["setting"], tag)]
        seen = Counter()
        for line in open(p, encoding="utf-8"):
            x = json.loads(line)
            if x["model"] == "undercutter":
                continue
            c["calls"] += 1
            seen[(x["round"], x["firm"])] += 1
            c["flagged"] += bool(x["flags"])
            c.update("flag:" + f for f in x["flags"])
            c["not stop"] += x["finish"] != "stop"
            c["empty msg"] += run["setting"] != "commoff" and not x["message"]
        c["repeat calls"] += sum(n - 1 for n in seen.values())
ftypes = sorted({k for c in fl.values() for k in c if k.startswith("flag:")})
tab = [list(k) + [c["calls"], c["flagged"], f"{100 * c['flagged'] / c['calls']:.2f}%"] + [c[f] for f in ftypes] + [c["not stop"], c["empty msg"], c["repeat calls"]]
       for k, c in sorted(fl.items())]
tot = defaultdict(Counter)
for (m, s, t), c in fl.items():
    tot[m].update(c)
tab += [[m, "all", "all", c["calls"], c["flagged"], f"{100 * c['flagged'] / c['calls']:.2f}%"] + [c[f] for f in ftypes] + [c["not stop"], c["empty msg"], c["repeat calls"]]
        for m, c in sorted(tot.items())]
write("flags", ["model", "setting", "branch", "LLM calls", "flagged", "rate"] + ftypes + ["finish not stop", "empty message (comm on)", "repeat calls same round/firm"],
      tab, "Parse-failure and flag rate per model and condition",
      "From calls.jsonl, LLM calls only. Settings: main, hist0, hist1, commoff (comm off), notes (complete branches only). Only the branch names listed in common.py are read. "
      "Flag names are the harness's own.")
print("done")
