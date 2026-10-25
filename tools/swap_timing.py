"""Swap timing (exploratory): swap at round 15 or 45 instead of 30, from the gemma main runs that passed the gate.
For each gated seed and time t: a checkpoint is cut from the logged rounds (base, then the no-swap branch for t=45), then branches none, clone and
undercutter run from it. Analyse the first 15 rounds after the swap. Output: data/gemma_timing/<run>_t<t>/
usage (repo root): .venv\Scripts\python.exe -I tools\swap_timing.py [seeds...]"""
import json
import os
import subprocess
import sys

PY = sys.executable
SRC, OUT = "data/main", "data/gemma_timing"


def rows(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def gated(d):
    r = rows(f"{d}/base/rounds.jsonl")[15:30]  # rounds 16-30
    return sum((sum(x["prices"]) / len(x["prices"]) - 10) / 45 for x in r) / len(r) >= 0.5


seeds = [int(a) for a in sys.argv[1:]] or range(11, 21)
for s in seeds:
    d = f"{SRC}/gemma4-12b_common_s{s}"
    if not os.path.exists(f"{d}/none/rounds.jsonl") or not gated(d):
        continue
    ck = json.load(open(f"{d}/checkpoint.json", encoding="utf-8"))
    hist = rows(f"{d}/base/rounds.jsonl") + rows(f"{d}/none/rounds.jsonl")
    for t, last in ((15, 45), (45, 60)):
        run = f"{OUT}/gemma4-12b_common_s{s}_t{t}"
        os.makedirs(run, exist_ok=True)
        json.dump({**ck, "hist": hist[:t], "round": t}, open(f"{run}/checkpoint.json", "w", encoding="utf-8"), indent=1)
        env = {**os.environ, "SWAP_AT": str(t), "BRANCH_ROUNDS": str(last)}
        for w in ("none", "clone", "undercutter"):
            subprocess.run([PY, "-m", "harness.run", "branch", "--run", run, "--swap", w, "--k", "1"], env=env, check=False)
