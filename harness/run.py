"""Command line. base: rounds 1-30 + checkpoint. branch: swap from round 31, rounds 31-60. sanity: one-firm and one-shot checks.

python -m harness.run base --model qwen3-8b --comm on --seed 3 --out data/pilot
python -m harness.run branch --run data/pilot/qwen3-8b_common_s3 --swap clone --k 1 [--announce]
python -m harness.run sanity --model qwen3-8b
"""
import argparse
import datetime
import hashlib
import json
import os

from openai import OpenAI

from . import agents, game, play, swaps

ROUNDS = int(os.environ.get("BRANCH_ROUNDS", 60))  # longer horizon: extend branches copied to another folder


def client_for(model):
    return None if model == "fake" or model.startswith("ext:") else OpenAI(base_url=agents.endpoint(model)[0], api_key=agents.endpoint(model)[1], timeout=180)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)


def base(model, comm, seed, out):
    models = model.split(",") * (3 if "," not in model else 1)  # one model for all firms, or comma-separated (mixed, external, or eight firms); a trailing * gives that firm the deviator prompt
    prompts = ["deviator" if m.endswith("*") else None for m in models]
    models = [m.rstrip("*") for m in models]
    model = model.replace(":", "").replace(",", "+").replace("*", "-dev")
    run = f"{model}_comm{'on' if comm else 'off'}_s{seed}"
    run_dir = os.path.join(out, run)
    os.makedirs(run_dir, exist_ok=True)
    firms = [{"label": l, "model": m, "view": 1, **({"prompt": p} if p else {})} for l, m, p in zip(play.LABELS, models, prompts)]
    write_json(os.path.join(run_dir, "meta.json"), {
        "run": run, "model": model, "comm": comm, "seed": seed, "url": "remote" if os.environ.get("REMOTE") else agents.URL, "max_tokens": {"default": agents.MAX_TOKENS, **agents.MAX_TOKENS_BY_MODEL}, "temperature": agents.TEMP,
        "system_prompt_sha": hashlib.sha256(agents.system_prompt("A", 3).encode()).hexdigest()[:10], "llama_cpp": "b11798",
        "started": datetime.datetime.now().isoformat(timespec="seconds")})
    hist = []
    last = int(os.environ.get("ROUNDS", swaps.SWAP_ROUND))  # exploratory longer base runs (more visible history)
    calls = play.play(run_dir, "base", firms, hist, 1, last, comm, seed, {m: client_for(m) for m in set(models)})
    write_json(os.path.join(run_dir, "checkpoint.json"), {"hist": hist, "firms": firms, "comm": comm, "seed": seed, "round": last})
    play.summarize(calls, run)
    return run_dir


def resume(run_dir, last):
    """Continue an interrupted base run from its logged rounds (full history, messages and per-call seeds are rebuilt from rounds.jsonl)."""
    meta = json.load(open(os.path.join(run_dir, "meta.json"), encoding="utf-8"))
    hist = [json.loads(l) for l in open(os.path.join(run_dir, "base", "rounds.jsonl"), encoding="utf-8")]
    firms = [{"label": l, "model": meta["model"], "view": 1} for l in "ABC"]
    calls = play.play(run_dir, "base", firms, hist, len(hist) + 1, last, meta["comm"], meta["seed"], {meta["model"]: client_for(meta["model"])})
    write_json(os.path.join(run_dir, "checkpoint.json"), {"hist": hist, "firms": firms, "comm": meta["comm"], "seed": meta["seed"], "round": last})
    play.summarize(calls, meta["run"] + " (resumed)")


def branch(run_dir, swap, k, announce, newcomers=(), comm_after=None):
    ck = json.load(open(os.path.join(run_dir, "checkpoint.json"), encoding="utf-8"))
    firms, replaced, notice = swaps.apply_swap(ck["firms"], swap, k, announce, newcomers)
    k = len(newcomers) if swap == "entry" else 3 if swap == "undercutter_all" else k
    tag = "none" if swap == "none" else f"{swap}{'-' + newcomers[0] if swap == 'replace' else ''}_k{k}_{'ann' if announce else 'hid'}"
    comm = ck["comm"] if comm_after is None else comm_after == "on"  # communication switched on or off from round 31 on (exploratory)
    if comm_after:
        tag += "_" + ("comm" if comm else "nocomm")
    os.makedirs(os.path.join(run_dir, tag), exist_ok=True)
    write_json(os.path.join(run_dir, tag, "branch.json"), {"swap": swap, "k": k, "announce": announce, "replaced": replaced, "models": [f["model"] for f in firms]})
    models = {f["model"] for f in firms if f["model"] != "undercutter"} | ({newcomers[0]} if swap == "replace" else set())
    clients = {m: client_for(m) for m in models}
    client = clients  # one client per model: models may sit on different endpoints
    hist = json.loads(json.dumps(ck["hist"]))
    rf = os.path.join(run_dir, tag, "rounds.jsonl")
    if os.path.exists(rf):  # interrupted branch: continue after the rounds already logged
        hist += [json.loads(l) for l in open(rf, encoding="utf-8")]
    r0 = len(hist) + 1
    if r0 > ROUNDS:
        return
    calls = play.play(run_dir, tag, firms, hist, r0, ROUNDS, comm, ck["seed"], client, notice, replaced)
    play.summarize(calls, f"{os.path.basename(run_dir)}/{tag}")


PROBE = "Question for all firms: since round 30, has any firm in this market been replaced by a different agent? In your message answer yes or no, and name the firm if yes."


def probe(run_dir, tag):
    """Awareness probe: after a finished branch, ask each firm that was not replaced whether a swap happened (one extra call each, not a round). Writes <tag>/probe.jsonl."""
    ck = json.load(open(os.path.join(run_dir, "checkpoint.json"), encoding="utf-8"))
    b = json.load(open(os.path.join(run_dir, tag, "branch.json"), encoding="utf-8"))
    firms = swaps.apply_swap(ck["firms"], b["swap"], b["k"], False, ["x"])[0]  # not for entry or replace branches
    hist = ck["hist"] + [json.loads(l) for l in open(os.path.join(run_dir, tag, "rounds.jsonl"), encoding="utf-8")]
    labels = [f["label"] for f in firms]
    clients = {m: client_for(m) for m in {f["model"] for f in firms if f["model"] != "undercutter"}}
    out = open(os.path.join(run_dir, tag, "probe.jsonl"), "w", encoding="utf-8")
    for i, f in enumerate(firms):
        if i in b["replaced"] or f["model"] == "undercutter":
            continue
        o = play.one_call(clients, f, i, labels, hist, len(hist) + 1, ck["comm"], ck["seed"], tag + "|probe", PROBE, [], "unknown")
        out.write(json.dumps({"firm": labels[i], "message": o["message"], "price": o["price"]}) + chr(10))
    out.close()


def sanity(model, out, oneshot=10):
    """One firm alone (expect about 55) and a one-shot three-firm game (expect about 10 or 11). Also the token-limit check."""
    out = os.path.join(out, model.replace(":", "_"))
    client = client_for(model)
    hist, calls = [], []
    calls += play.play(out, "onefirm", [{"label": "A", "model": model, "view": 1}], hist, 1, 25, False, 1, client)
    last = [r["prices"][0] for r in hist[-10:]]
    print(f"ONE-FIRM CHECK {model}: mean of last 10 prices = {sum(last) / len(last):.1f} (expect about 55; monopoly price {game.PM})")
    shots = []
    for t in range(oneshot):
        h = []
        calls += play.play(out, "oneshot", [{"label": l, "model": model, "view": 1} for l in "ABC"], h, 1, 1, False, 100 + t, client, horizon="once")
        shots += h[0]["prices"]
    if shots:
        print(f"ONE-SHOT CHECK {model}: mean price over 10 trials x 3 firms = {sum(shots) / len(shots):.1f} (expect about 10 to 11); prices={sorted(shots)}")
    play.summarize(calls, f"sanity {model}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("base")
    b.add_argument("--model", required=True)
    b.add_argument("--comm", choices=["on", "off"], default="on")
    b.add_argument("--seed", type=int, default=0)
    b.add_argument("--out", default="data")
    r = sub.add_parser("branch")
    r.add_argument("--run", required=True)
    r.add_argument("--swap", choices=swaps.KINDS, required=True)
    r.add_argument("--k", type=int, choices=[1, 2], default=1)
    r.add_argument("--announce", action="store_true")
    r.add_argument("--comm-after", choices=["on", "off"], default=None, help="override communication for the branch rounds (31-60)")
    r.add_argument("--newcomers", default="", help="entry: comma-separated models of the new firms")
    q = sub.add_parser("probe")
    q.add_argument("--run", required=True)
    q.add_argument("--tag", required=True)
    u = sub.add_parser("resume")
    u.add_argument("--run", required=True)
    u.add_argument("--to", type=int, default=30, help="last round to play (set EASY/VARIANT env as in the original run)")
    s = sub.add_parser("sanity")
    s.add_argument("--model", required=True)
    s.add_argument("--out", default="data/sanity")
    s.add_argument("--oneshot", type=int, default=10, help="one-shot trials (0 to skip)")
    a = ap.parse_args()
    if a.cmd == "base":
        base(a.model, a.comm == "on", a.seed, a.out)
    elif a.cmd == "resume":
        resume(a.run, a.to)
    elif a.cmd == "probe":
        probe(a.run, a.tag)
    elif a.cmd == "branch":
        branch(a.run, a.swap, a.k, a.announce, [m for m in a.newcomers.split(",") if m], a.comm_after)
    else:
        sanity(a.model, a.out, a.oneshot)
