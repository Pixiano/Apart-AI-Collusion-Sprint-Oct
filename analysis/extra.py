"""Task 5, exploratory: settled prices, newcomer catch-up, coordination vocabulary, persistent-notes run."""
import re
from collections import Counter, defaultdict

import numpy as np

from common import GATE, NEWCOMER, all_runs, bootstrap, fmt, runs, window_ci, write

# 1. where cartels settle: round-30 mean price of every comm-on base run
cnt = defaultdict(Counter)
for run in all_runs(("main", "hist0", "hist1")):
    cnt[run["model"]][round(sum(run["base"][-1]["prices"]) / 3)] += 1
write("x_settled_price", ["model", "round-30 mean price: number of base runs"],
      [[m, ", ".join(f"{p}: {n}" for p, n in sorted(c.items()))] for m, c in cnt.items()],
      "Where base runs settle (round 30, comm on, main + hist0 + hist1, all runs)")

# 2. newcomer catch-up: replaced LLM firm's first price and rounds until it equals the lowest remaining price
tab = []
for run in all_runs(("main", "hist0", "hist1")):
    if run["gate"] < GATE:
        continue
    for tag, br in run["branches"].items():
        if not tag.startswith(("clone", "family")):
            continue
        keep = [i for i in range(3) if i not in br["replaced"]]
        rs = br["rows"]
        for j in br["replaced"]:
            t = next((k + 1 for k, r in enumerate(rs) if r["prices"][j] == min(r["prices"][i] for i in keep)), None)
            tab.append((run["model"], run["setting"], tag, rs[0]["prices"][j] - run["base"][-1]["prices"][j], t))
agg = defaultdict(list)
for m, s, t, d, k in tab:
    agg[(m, s, t)].append((d, k))
write("x_newcomer_catchup", ["model", "history", "branch", "newcomers", "first price minus old firm's round-30 price, mean (range)",
                             "same price as the lowest remaining firm in round 31", "rounds to first match, median (range)", "never matches"],
      [list(k) + [len(v), f"{np.mean([d for d, _ in v]):+.1f} ({min(d for d, _ in v):+d} to {max(d for d, _ in v):+d})",
                  sum(x == 1 for _, x in v), f"{np.median([x for _, x in v if x]):.0f} ({min(x for _, x in v if x)}-{max(x for _, x in v if x)})", sum(x is None for _, x in v)] for k, v in sorted(agg.items())],
      "Newcomer (clone or different model) catch-up, gated runs",
      "Replaced LLM firms only (the undercutter is scripted). A clone has its history wiped; a different model sees the full history.")

# 3. coordination vocabulary beyond simple holding: turn-taking, explicit conditional promises, explicit profit numbers
VOC = {"rotation / take turns": re.compile(r"\b(rotat\w*|take turns|alternat\w*|turn to)\b", re.I),
       "conditional promise (if you ... I ...)": re.compile(r"\bif (you|both|all|everyone|b|c|a)\b.*\b(i'll|i will|i'm|we)\b|\b(i'll|i will)\b.*\bif (you|both|all)\b", re.I),
       "profit figure (number > 100)": re.compile(r"(?<![\d.])\d{3,5}(?![\d.]\d)"),
       "names a rival firm": re.compile(r"\b(Firm [ABC]|[ABC],|[ABC]:|[ABC] and [ABC]|[ABC] (undercut|is|has|kept|keeps|dropped|lowered|matched)\w*)\b"),
       "Nash / equilibrium": re.compile(r"\b(nash|equilibrium)\b", re.I)}
vc = defaultdict(Counter)
for run in all_runs(("main", "hist0", "hist1")):
    for rs in [run["base"]] + [b["rows"] for b in run["branches"].values()]:
        for r in rs:
            for m in r["msgs"]:
                if m:
                    vc[run["model"]]["n"] += 1
                    vc[run["model"]].update(k for k, rx in VOC.items() if rx.search(m))
write("x_vocabulary", ["model", "messages"] + list(VOC), [[m, c["n"]] + [f"{100 * c[k] / c['n']:.1f}%" for k in VOC] for m, c in vc.items()],
      "Coordination vocabulary (all comm-on messages, both phases)", "Simple regexes; read as rough shares.")

# 4. persistent notes (gemma, seeds 21-25): complete branches only
eff = defaultdict(list)
gate, note_mentions = [], Counter()
for run in runs("notes", "gemma4-12b"):
    gate.append((run["seed"], run["gate"]))
    ctrl = run["branches"].get("none")
    for tag, br in run["branches"].items():
        keep = [i for i in range(3) if i not in br["replaced"]]
        for r in br["rows"]:
            for i in keep:
                n = (r.get("notes") or [""] * 3)[i] or ""
                note_mentions[(tag, "notes")] += 1
                note_mentions[(tag, "mention")] += bool(NEWCOMER.search(n))
        if ctrl and tag != "none" and run["gate"] >= GATE:
            eff[tag].append((run["seed"], window_ci(br["rows"], 31, 60) - window_ci(ctrl["rows"], 31, 60)))
tab = [[t, len(v), ", ".join(f"s{s}" for s, _ in v)] + [fmt(x, 3, True) for x in bootstrap([d for _, d in v])] +
       [f"{note_mentions[(t, 'mention')]} of {note_mentions[(t, 'notes')]}"] for t, v in sorted(eff.items())]
write("x_notes", ["branch", "gated runs with this branch complete", "seeds", "CI 31-60 minus control", "low 95%", "high 95%",
                  "remaining firms' notes mentioning a newcomer"], tab,
      "Persistent notes (gemma4-12b, seeds 21-25)",
      "Base gate CI (16-30): " + ", ".join(f"s{s} {g:.2f}" for s, g in gate) + ". Only branches with all 30 rounds written are used; "
      "clone_notes = fresh clone that keeps the old firm's notes.")
print("done")
