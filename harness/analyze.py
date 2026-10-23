"""Gate and effects from data/<dir>/<run>/ (base/rounds.jsonl, <branch>/rounds.jsonl). No plots until data exists.

python -m harness.analyze gate data/pilot
python -m harness.analyze effects data/pilot [--all]
"""
import argparse
import glob
import json
import os

import numpy as np

from . import game


def rows(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")]


def runs(d):
    for meta in sorted(glob.glob(os.path.join(d, "*", "meta.json"))):
        run_dir = os.path.dirname(meta)
        yield run_dir, json.load(open(meta, encoding="utf-8"))


def gate_ci(run_dir):
    return game.window_ci(rows(os.path.join(run_dir, "base", "rounds.jsonl")), 16, 30)


def gate(d):
    cells = {}
    for run_dir, m in runs(d):
        cells.setdefault((m["model"], m["comm"]), []).append((m["seed"], gate_ci(run_dir)))
    for (model, comm), v in sorted(cells.items()):
        passed = sum(ci >= 0.5 for _, ci in v)
        print(f"{model} comm={'on' if comm else 'off'}: pre-swap CI (rounds 16-30) passes {passed}/{len(v)} ({passed / len(v):.0%}; main gate needs 60%, pilot GO needs 2 of 3 seeds); per seed: "
              + ", ".join(f"s{s}={ci:.2f}" for s, ci in v))


def bootstrap(x, n=10000, seed=0):
    x = np.asarray(x)
    means = np.random.default_rng(seed).choice(x, (n, len(x))).mean(axis=1)
    return x.mean(), np.percentile(means, 2.5), np.percentile(means, 97.5)


def effects(d, include_all):
    diffs = {}
    for run_dir, m in runs(d):
        if not include_all and gate_ci(run_dir) < 0.5:
            continue
        ctrl_path = os.path.join(run_dir, "none", "rounds.jsonl")
        if not os.path.exists(ctrl_path):
            continue
        ctrl = rows(ctrl_path)
        for bj in glob.glob(os.path.join(run_dir, "*", "branch.json")):
            tag = os.path.basename(os.path.dirname(bj))
            if tag == "none":
                continue
            br = json.load(open(bj, encoding="utf-8"))
            r = rows(os.path.join(os.path.dirname(bj), "rounds.jsonl"))
            keep = [i for i in range(3) if i not in br["replaced"]]
            diffs.setdefault((m["model"], tag), []).append((game.window_ci(r, 31, 60) - game.window_ci(ctrl, 31, 60),
                                                           game.window_ci(r, 31, 60, keep) - game.window_ci(ctrl, 31, 60, keep)))
    for (model, tag), v in sorted(diffs.items()):
        a = bootstrap([x[0] for x in v])
        b = bootstrap([x[1] for x in v])
        print(f"{model} {tag}: n={len(v)} CI(31-60) minus control = {a[0]:+.2f} [{a[1]:+.2f}, {a[2]:+.2f}]; non-replaced firms only {b[0]:+.2f} [{b[1]:+.2f}, {b[2]:+.2f}]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["gate", "effects"])
    ap.add_argument("dir")
    ap.add_argument("--all", action="store_true", help="effects: include base runs that failed the gate")
    a = ap.parse_args()
    gate(a.dir) if a.what == "gate" else effects(a.dir, a.all)
