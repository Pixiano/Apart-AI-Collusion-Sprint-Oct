"""Task 1: what the messages say (communication-on runs, both models). Keyword classes are multi-label.

Outputs analysis/out/msg_*.{md,csv}. All runs are used (description, not an effect); gated-only counts are in msg_phase too.
"""
import random
from collections import Counter, defaultdict

from common import CLASSES, NEWCOMER, all_runs, classes, fmt, prices_in, write

CL = ["price"] + list(CLASSES) + ["other"]
runs = all_runs()


def items():
    """(run, phase, branch, firm index, round, msg, own price now, own price next round or None, replaced firms)."""
    for run in runs:
        b = run["base"]
        for k, r in enumerate(b):
            for i, m in enumerate(r["msgs"]):
                nxt = b[k + 1]["prices"][i] if k + 1 < len(b) else None
                yield run, ("1-10" if r["round"] <= 10 else "11-30"), "base", i, r["round"], m, r["prices"][i], nxt, []
        for tag, br in run["branches"].items():
            rs = br["rows"]
            for k, r in enumerate(rs):
                for i, m in enumerate(r["msgs"]):
                    nxt = rs[k + 1]["prices"][i] if k + 1 < len(rs) else None
                    yield run, "31-60", tag, i, r["round"], m, r["prices"][i], nxt, br["replaced"]


data = [x for x in items() if x[5]]  # scripted undercutters send empty messages

# 1. shares by model, setting, phase
cnt = defaultdict(Counter)
for run, ph, tag, i, rd, m, p, nx, rep in data:
    key = (run["model"], run["setting"], ph)
    cnt[key]["n"] += 1
    cnt[key].update(classes(m))
tab = []
for (model, s, ph), c in sorted(cnt.items()):
    tab.append([model, s, ph, c["n"]] + [f"{100 * c[k] / c['n']:.0f}%" for k in CL])
write("msg_phase", ["model", "history", "rounds", "messages"] + CL, tab, "Message classes by phase",
      "Share of messages in each keyword class (multi-label, so rows can sum above 100%). Rounds 31-60 pool all branches. "
      "history: main = full, hist0 = none, hist1 = last round. All runs, gated or not.")

# 2. before vs after the swap, remaining (non-replaced) firms, clone and undercutter branches
ba = defaultdict(Counter)
for run in runs:
    for tag, br in run["branches"].items():
        if not tag.startswith(("clone", "undercutter")):
            continue
        keep = [i for i in range(3) if i not in br["replaced"]]
        for when, rs in (("before (21-30)", [r for r in run["base"] if r["round"] > 20]), ("after (31-60)", br["rows"])):
            c = ba[(run["model"], run["setting"], tag, when)]
            for r in rs:
                for i in keep:
                    if r["msgs"][i]:
                        c["n"] += 1
                        c.update(classes(r["msgs"][i]))
                        c["newcomer"] += bool(NEWCOMER.search(r["msgs"][i]))
tab = [[m, s, t, w, c["n"]] + [f"{100 * c[k] / c['n']:.0f}%" for k in CL + ["newcomer"]] for (m, s, t, w), c in sorted(ba.items())]
write("msg_before_after", ["model", "history", "branch", "window", "messages"] + CL + ["mentions newcomer"], tab,
      "Messages of the remaining firms before and after the swap",
      "Remaining = firms not replaced. 'before' is the same base run, rounds 21-30, counted once per branch so the two windows are paired.")

# 3. does the number in the message match the price set?
mt = defaultdict(Counter)
for run, ph, tag, i, rd, m, p, nx, rep in data:
    ps = prices_in(m)
    if not ps or nx is None:
        continue
    c = mt[(run["model"], run["setting"])]
    c["n"] += 1
    c["first=now"] += ps[0] == p
    c["first=next"] += ps[0] == nx
    c["last=next"] += ps[-1] == nx
    c["last=next+-1"] += abs(ps[-1] - nx) <= 1
    c["any=next"] += nx in ps
    c["now=next"] += p == nx
mk = ["first=now", "first=next", "last=next", "last=next+-1", "any=next", "now=next"]
tab = [[m, s, c["n"]] + [f"{100 * c[k] / c['n']:.0f}%" for k in mk] for (m, s), c in sorted(mt.items())]
write("msg_price_match", ["model", "history", "messages with a price"] + mk, tab, "Message price against the price actually set",
      "first/last = first or last price-like number in the message; now = the firm's own price in the round the message is sent; "
      "next = the same firm's price one round later. now=next is the baseline: how often the firm simply keeps its price.")

# 4. what precedes a rise or a cut of the sender's own price next round
pc = defaultdict(Counter)
for run, ph, tag, i, rd, m, p, nx, rep in data:
    if nx is None:
        continue
    move = "rise" if nx > p else "cut" if nx < p else "same"
    c = pc[(run["model"], move)]
    c["n"] += 1
    c.update(classes(m))
    c["newcomer"] += bool(NEWCOMER.search(m))
tab = [[m, mv, c["n"]] + [f"{100 * c[k] / c['n']:.0f}%" for k in CL] for (m, mv), c in sorted(pc.items())]
write("msg_before_move", ["model", "own price next round", "messages"] + CL, tab, "Message classes before a price rise, cut or no change",
      "All communication-on runs and rounds pooled (main, hist0, hist1). A move is the sender's own price next round against this round.")

# 5. newcomer mentions per cell (awareness self-report, cheap talk)
nc = defaultdict(lambda: [0, 0, set(), set(), []])
for run, ph, tag, i, rd, m, p, nx, rep in data:
    if ph != "31-60" or i in rep:
        continue
    c = nc[(run["model"], run["setting"], tag)]
    c[0] += 1
    c[3].add(run["seed"])
    if NEWCOMER.search(m):
        c[1] += 1
        c[2].add(run["seed"])
        c[4].append(m)
tab = [[m, s, t, c[0], c[1], f"{len(c[2])} of {len(c[3])}"] for (m, s, t), c in sorted(nc.items())]
write("msg_newcomer", ["model", "history", "branch", "messages (remaining firms, 31-60)", "mention newcomer/replacement", "runs with a mention"], tab,
      "Messages that mention a newcomer or replacement",
      "Regex: new firm/agent/player/entrant/competitor, newcomer, replac*, joined, entered, different firm, and similar ('reset' left out: it always meant resetting a price). "
      "The no-swap control (none) gives the false-positive rate. Cheap talk, reported separately from prices.")
with open("analysis/out/msg_newcomer_examples.md", "w", encoding="utf-8") as f:
    f.write("# All matching messages (remaining firms, rounds 31-60), first 6 per cell\n\n")
    for k, c in sorted(nc.items()):
        for m in c[4][:6]:
            f.write(f"- {k[0]} / {k[1]} / {k[2]}: {m}\n")

# 6. verbatim examples per class (under 25 words), messages with exactly one class where possible
random.seed(0)
with open("analysis/out/msg_examples.md", "w", encoding="utf-8") as f:
    f.write("# Example messages per class (random draw, seed 0, under 25 words, distinct)\n\n"
            "Messages whose only class is the one shown, where enough exist; otherwise any message in the class.\n")
    for model in ("gemma4-12b", "deepseek-v4-1-flash"):
        pool = sorted({x[5] for x in data if x[0]["model"] == model and len(x[5].split()) < 25})
        for k in CL:
            pure = [m for m in pool if classes(m) == [k] or (k == "price" and classes(m)[:1] == ["price"] and len(classes(m)) == 1)]
            anyk = [m for m in pool if k in classes(m)]
            src = pure if len(pure) >= 6 else anyk
            f.write(f"\n## {model}, {k} ({len(anyk)} distinct messages in class, {len(pure)} with this class only)\n\n")
            for m in random.sample(src, min(6, len(src))):
                f.write(f"- {m}\n")
print("messages:", len(data))
