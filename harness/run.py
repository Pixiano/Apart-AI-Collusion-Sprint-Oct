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

ROUNDS = 60


def client_for(model):
    return None if model == "fake" or model.startswith("ext:") else OpenAI(base_url=agents.URL, api_key="none", timeout=180)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)


def base(model, comm, seed, out):
    models = model.split(",") * (3 if "," not in model else 1)  # one model for all firms, or three comma-separated (mixed or external)
    model = model.replace(":", "").replace(",", "+")
    run = f"{model}_comm{'on' if comm else 'off'}_s{seed}"
    run_dir = os.path.join(out, run)
    os.makedirs(run_dir, exist_ok=True)
    firms = [{"label": l, "model": m, "view": 1} for l, m in zip("ABC", models)]
    write_json(os.path.join(run_dir, "meta.json"), {
        "run": run, "model": model, "comm": comm, "seed": seed, "url": agents.URL, "max_tokens": {"default": agents.MAX_TOKENS, **agents.MAX_TOKENS_BY_MODEL}, "temperature": agents.TEMP,
        "system_prompt_sha": hashlib.sha256(agents.system_prompt("A", 3).encode()).hexdigest()[:10], "llama_cpp": "b11798",
        "started": datetime.datetime.now().isoformat(timespec="seconds")})
    hist = []
    calls = play.play(run_dir, "base", firms, hist, 1, swaps.SWAP_ROUND, comm, seed, client_for(models[0]))
    write_json(os.path.join(run_dir, "checkpoint.json"), {"hist": hist, "firms": firms, "comm": comm, "seed": seed, "round": swaps.SWAP_ROUND})
    play.summarize(calls, run)
    return run_dir


def branch(run_dir, swap, k, announce, newcomers=()):
    ck = json.load(open(os.path.join(run_dir, "checkpoint.json"), encoding="utf-8"))
    firms, replaced, notice = swaps.apply_swap(ck["firms"], swap, k, announce, newcomers)
    k = len(newcomers) if swap == "entry" else 3 if swap == "undercutter_all" else k
    tag = "none" if swap == "none" else f"{swap}_k{k}_{'ann' if announce else 'hid'}"
    os.makedirs(os.path.join(run_dir, tag), exist_ok=True)
    write_json(os.path.join(run_dir, tag, "branch.json"), {"swap": swap, "k": k, "announce": announce, "replaced": replaced, "models": [f["model"] for f in firms]})
    models = {f["model"] for f in firms if f["model"] != "undercutter"}
    clients = {m: client_for(m) for m in models}
    # one client is enough: the server routes by model name in the request
    client = next(iter(clients.values()), None)
    hist = json.loads(json.dumps(ck["hist"]))
    calls = play.play(run_dir, tag, firms, hist, swaps.SWAP_ROUND + 1, ROUNDS, ck["comm"], ck["seed"], client, notice, replaced)
    play.summarize(calls, f"{os.path.basename(run_dir)}/{tag}")


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
    r.add_argument("--newcomers", default="", help="entry: comma-separated models of the new firms")
    s = sub.add_parser("sanity")
    s.add_argument("--model", required=True)
    s.add_argument("--out", default="data/sanity")
    s.add_argument("--oneshot", type=int, default=10, help="one-shot trials (0 to skip)")
    a = ap.parse_args()
    if a.cmd == "base":
        base(a.model, a.comm == "on", a.seed, a.out)
    elif a.cmd == "branch":
        branch(a.run, a.swap, a.k, a.announce, [m for m in a.newcomers.split(",") if m])
    else:
        sanity(a.model, a.out, a.oneshot)
