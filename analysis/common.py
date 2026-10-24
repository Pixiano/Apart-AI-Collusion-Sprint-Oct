"""Shared loaders for the analysis scripts. Reads data/ only, never writes there. stdlib + numpy.

Run every script from the repo root, e.g. .venv\\Scripts\\python.exe analysis\\messages.py
"""
import csv
import glob
import json
import os
import re

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "analysis", "out")
MODELS = ("gemma4-12b", "deepseek-v4-1-flash")
SETTINGS = {  # name -> folder pattern; comm on unless named
    "main": "data/main/{m}_common_s*",
    "hist0": "data/hist0/{m}_common_s*",
    "hist1": "data/hist1/{m}_common_s*",
    "commoff": "data/main/{m}_commoff_s*",
    "notes": "data/notes/{m}_common_s*",
}
GATE = 0.5
SWAP = 30
# branches covered by this analysis; others (e.g. *_nocomm, added later) are skipped so new runs do not leak in
BRANCHES = {"none", "clone_k1_hid", "family_k1_hid", "undercutter_k1_hid", "clone_k2_hid", "undercutter_k2_hid",
            "clone_k1_ann", "undercutter_k1_ann", "clone_notes_k1_hid"}


def rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def ci(p):
    return (p - 10) / 45


def window_ci(rs, lo, hi, firms=None):
    v = [p for r in rs if lo <= r["round"] <= hi for i, p in enumerate(r["prices"]) if firms is None or i in firms]
    return ci(sum(v) / len(v)) if v else float("nan")


def runs(setting, model):
    """Yields one dict per run with complete base (30 rounds) and only complete branches (30 rounds)."""
    for d in sorted(glob.glob(os.path.join(ROOT, SETTINGS[setting].format(m=model)))):
        bp = os.path.join(d, "base", "rounds.jsonl")
        if not os.path.exists(bp):
            continue
        base = rows(bp)
        if len(base) < SWAP:
            continue
        run = {"setting": setting, "model": model, "seed": int(d.rsplit("_s", 1)[1]), "dir": d,
               "base": base, "gate": window_ci(base, 16, 30), "branches": {}}
        for bj in sorted(glob.glob(os.path.join(d, "*", "branch.json"))):
            bd = os.path.dirname(bj)
            if os.path.basename(bd) not in BRANCHES:
                continue
            rp = os.path.join(bd, "rounds.jsonl")
            r = rows(rp) if os.path.exists(rp) else []
            if len(r) < 30:  # still running or interrupted
                continue
            meta = json.load(open(bj, encoding="utf-8"))
            run["branches"][os.path.basename(bd)] = {"rows": r, "replaced": meta["replaced"], "meta": meta,
                                                     "calls": os.path.join(bd, "calls.jsonl")}
        yield run


def all_runs(settings=("main", "hist0", "hist1"), models=MODELS):
    return [r for s in settings for m in models for r in runs(s, m)]


def bootstrap(x, n=10000, seed=0):
    x = np.asarray([v for v in x if v == v], dtype=float)
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan")
    means = np.random.default_rng(seed).choice(x, (n, len(x))).mean(axis=1)
    return float(x.mean()), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def fmt(v, d=2, sign=False):
    if isinstance(v, str):
        return v
    if v is None or v != v:
        return "n/a"
    return f"{v:+.{d}f}" if sign else f"{v:.{d}f}"


def write(name, header, table, title=None, note=None):
    """Writes analysis/out/<name>.csv and .md with the same rows."""
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(table)
    with open(os.path.join(OUT, name + ".md"), "w", encoding="utf-8") as f:
        if title:
            f.write(f"# {title}\n\n")
        if note:
            f.write(note.strip() + "\n\n")
        f.write("| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n")
        for r in table:
            f.write("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |\n")


# ---- message classes (multi-label: a message can fall in several) ----
_ROUNDREF = re.compile(r"\brounds?\s+\d+(\s*(-|to|and)\s*\d+)?", re.I)
_UNITREF = re.compile(r"\b\d+(\.\d+)?\s*(-?\s*units?|%|rounds?|firms?|percent)\b", re.I)
_NUM = re.compile(r"(?<![\d.])(\d{2,3})(?![\d.]\d)")
CLASSES = {
    "hold": re.compile(r"\b(stay|stays|hold|holding|maintain\w*|keep|keeping|continu\w*|stick|steady|unchanged|stabili[sz]\w*|remain)\b", re.I),
    "match": re.compile(r"\b(match\w*|follow\w*|join|joins|joined|joining|same price)\b", re.I),
    "warn": re.compile(r"\b(undercut\w*|punish\w*|retaliat\w*|price war|race (to|down)\w*|war\b|destructive|ruinous|hurts?|lower(ed|ing)?|cut\w*)\b", re.I),
    "trust": re.compile(r"\b(thank\w*|trust\w*|mutual\w*|collective\w*|shared|together|cooperat\w*|benefit\w*|fair\w*|everyone|all of us|joint)\b", re.I),
}
NEWCOMER = re.compile(r"\b(new (firm|agent|player|entrant|competitor|participant|management|strategy)|newcomer|replac\w*|someone new|"
                      r"new to|just joined|joined|entered|different (firm|agent|player)|changed (hands|strateg\w*)|new here)\b", re.I)


def prices_in(msg):
    """Integers 10-100 in a message, after removing round numbers, unit counts and percentages."""
    s = _UNITREF.sub(" ", _ROUNDREF.sub(" ", msg))
    return [int(x) for x in _NUM.findall(s) if 10 <= int(x) <= 100]


def classes(msg):
    c = [k for k, rx in CLASSES.items() if rx.search(msg)]
    if prices_in(msg):
        c.insert(0, "price")
    return c or ["other"]


if __name__ == "__main__":  # self-check of the message parser
    assert prices_in("Let's stabilize at 23 like rounds 49-50. I'll match 23.") == [23, 23]
    assert prices_in("matching 31 for stable 23-unit split") == [31]
    assert prices_in("39 has been profitable for 30 rounds.") == [39]
    assert classes("I agree. Let's maintain 48.") == ["price", "hold"]
    assert classes("Hello there") == ["other"]
    assert "warn" in classes("Firm C undercut us last round.")
    assert NEWCOMER.search("Firm C was replaced by a new agent") and not NEWCOMER.search("Firm C undercut us")
    print("ok")
