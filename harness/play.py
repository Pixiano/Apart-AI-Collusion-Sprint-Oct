"""The round loop: builds each firm's view, calls the agents, applies the rules, logs. Used by base, branch and sanity runs."""
import concurrent.futures as cf
import hashlib
import json
import os
import sys

from . import agents, game

LABELS = "ABCDE"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # model text can hold non-ASCII; a print must not kill a run


def cseed(seed, tag, r, firm):
    """Per-call seed from (run seed, branch tag, round, firm)."""
    return int(hashlib.sha256(f"{seed}|{tag}|{r}|{firm}".encode()).hexdigest()[:8], 16) % 2**31


def view(firm, hist, r):
    """Rounds a firm may see before round r, numbered from its own first round, and the round number it is told."""
    s = firm["view"]
    return [(k - s + 1, hist[k - 1]) for k in range(s, r)], r - s + 1


def one_call(client, firm, i, labels, hist, r, comm, seed, tag, notice, replaced, horizon):
    if firm["model"] == "undercutter":
        rivals = [p for j, p in enumerate(hist[-1]["prices"]) if j != i]
        return {"price": game.undercutter(rivals), "message": "", "flags": [], "finish": "", "ptok": 0, "ctok": 0, "rchars": 0, "lat": 0.0, "text": ""}
    rows, shown = view(firm, hist, r)
    msgs = hist[r - 2]["msgs"] if comm and r - 1 >= firm["view"] and hist else None
    note = notice if notice and i not in replaced else None
    system = agents.system_prompt(labels[i], len(labels), horizon)
    user = agents.user_prompt(i, labels, rows, shown, comm, msgs, note)
    out = agents.ask(client, firm["model"], system, user, comm, cseed(seed, tag, r, labels[i]))
    out["prompt_hash"] = hashlib.sha256((system + user).encode()).hexdigest()[:10]
    return out


def play(out_dir, tag, firms, hist, r0, r1, comm, seed, client, notice=None, replaced=(), horizon="unknown"):
    """Plays rounds r0..r1, appends round records to hist, writes <out_dir>/<tag>/{rounds,calls}.jsonl. Returns the call records."""
    os.makedirs(os.path.join(out_dir, tag), exist_ok=True)
    rounds_f = open(os.path.join(out_dir, tag, "rounds.jsonl"), "a", encoding="utf-8")
    calls_f = open(os.path.join(out_dir, tag, "calls.jsonl"), "a", encoding="utf-8")
    labels = [f["label"] for f in firms]
    calls = []
    for r in range(r0, r1 + 1):
        with cf.ThreadPoolExecutor(len(firms)) as ex:
            outs = list(ex.map(lambda i: one_call(client, firms[i], i, labels, hist, r, comm, seed, tag, notice, replaced, horizon), range(len(firms))))
        prices = []
        for i, o in enumerate(outs):
            if o["price"] is None:  # prereg: repeat the firm's previous price and flag the round
                o["flags"].append("repeated")
                o["price"] = hist[-1]["prices"][i] if hist else game.PM
                print(f"WARN {tag} r{r} {labels[i]}: no parseable price after retry, repeated {o['price']}; raw={o['text'][:80]!r}")
            prices.append(o["price"])
        units, profits = game.play_round(prices)
        rec = {"round": r, "prices": prices, "units": units, "profits": profits, "msgs": [o["message"] for o in outs], "flags": [o["flags"] for o in outs]}
        hist.append(rec)
        rounds_f.write(json.dumps(rec) + "\n")
        for i, o in enumerate(outs):
            line = {"tag": tag, "round": r, "firm": labels[i], "model": firms[i]["model"], **{k: o.get(k) for k in ("price", "message", "text", "finish", "ptok", "ctok", "rchars", "lat", "flags", "prompt_hash")}}
            calls_f.write(json.dumps(line) + "\n")
            calls.append(line)
            print(f"[{tag} r{r:02d} {labels[i]} {firms[i]['model']}] price={o['price']} words={len(o['message'].split())} ptok={o['ptok']} ctok={o['ctok']} rchars={o['rchars']} fin={o['finish']} {o['lat']:.1f}s flags={','.join(o['flags']) or '-'}")
            for fl, why in (("cut", "reply cut by the token limit (kept if a price parsed)"), ("leak", "reasoning text where it should be off"), ("long", "message over 30 words, trimmed")):
                if fl in o["flags"]:
                    print(f"WARN {tag} r{r} {labels[i]}: {why}")
        print(f"  round {r}: prices={prices} units={[round(u, 1) for u in units]} CI={game.ci(sum(prices) / len(prices)):.2f}")
        rounds_f.flush()
        calls_f.flush()
    rounds_f.close()
    calls_f.close()
    return calls


def summarize(calls, title):
    """Summary block: flag counts, completion-token distribution per model, mean latency."""
    print(f"=== summary: {title} ({len(calls)} calls)")
    flags = {}
    for c in calls:
        for fl in c["flags"] or []:
            flags[fl] = flags.get(fl, 0) + 1
    print("flags:", flags or "none")
    for m in sorted({c["model"] for c in calls}):
        ct = sorted(c["ctok"] for c in calls if c["model"] == m and c["ctok"] is not None)
        lat = [c["lat"] for c in calls if c["model"] == m]
        if ct:
            print(f"{m}: completion tokens max={ct[-1]} p95={ct[int(0.95 * (len(ct) - 1))]} limit={agents.MAX_TOKENS_BY_MODEL.get(m, agents.MAX_TOKENS)}; mean latency {sum(lat) / len(lat):.1f}s")
