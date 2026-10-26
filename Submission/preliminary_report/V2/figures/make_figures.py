"""V2: builds main-text figures a-e and V2/RESULTS_TABLE.md from data/*/rounds.jsonl (read only).
Run from the repo root: .venv/Scripts/python.exe -I Submission/preliminary_report/V2/figures/make_figures.py
Pooling (state it in every caption): HEADLINE = seeds 11-20 for gemma4-12b and deepseek-v4-1-flash (data/main), qw38 seeds 21-25,
glm53f seeds 21-30. ALL = headline plus deepseek seeds 31-40 (data/more_ds). gemma = seeds 11-20 (data/main) + 31-40 (data/gemma_more), 20 runs.
Figures a, b, c and the headline table all use HEADLINE, so 'n gated' agrees across them.
Gate: base run has 30 rounds and index over rounds 16-30 >= 0.5. Effect: index(branch, rounds 31-60) minus index of the
same run's reference branch (none, or none_nocomm for comm-cut branches), mean over runs, 95% bootstrap interval (10000 resamples, seed 0).
A branch counts only if branch and reference both have exactly 30 rounds."""
import glob, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "Submission/preliminary_report/V2/figures"
D = "data"
MODELS = {  # HEADLINE pooling: label -> glob patterns of run dirs
    "gemma4-12b": [f"{D}/main/gemma4-12b_common_s*", f"{D}/gemma_more/gemma4-12b_common_s*"],  # 20 seeds: 11-20 + 31-40
    "deepseek-v4-1-flash": [f"{D}/main/deepseek-v4-1-flash_common_s*"],
    "qw38": [f"{D}/qwen/qw38_common_s*"],
    "glm53f": [f"{D}/glm/glm53f_common_s*"],
}
FIG_A = MODELS
ALL_MODELS = {**MODELS, "deepseek-v4-1-flash": [f"{D}/main/deepseek-v4-1-flash_common_s*", f"{D}/more_ds/deepseek-v4-1-flash_common_s*"]}
MIXED = {"mixed deepseek/qw38/glm53f": [f"{D}/mixed/*_common_s*"], "mixed deepseek/qw38/gemma4-12b": [f"{D}/mixed_g/*_common_s*"]}
MIXLAB = {"mixed deepseek/qw38/glm53f": "Mixed:\nDeepSeek, Qwen, GLM", "mixed deepseek/qw38/gemma4-12b": "Mixed:\nDeepSeek, Qwen, Gemma"}
DN = {"gemma4-12b": "Gemma", "deepseek-v4-1-flash": "DeepSeek", "qw38": "Qwen", "glm53f": "GLM"}  # short plot names; key in CAPTIONS.md
LAB = {"clone": "fresh copy, 1 firm replaced", "family": "other model, 1 firm replaced", "undercutter k=1": "scripted undercutter, 1 firm replaced",
       "undercutter k=2": "scripted undercutter, 2 firms replaced"}
OI = dict(black="#000000", orange="#E69F00", sky="#56B4E9", green="#009E73", yellow="#F0E442", blue="#0072B2", verm="#D55E00", pink="#CC79A7")


def rows(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
def n_rows(d, t):
    try: return sum(1 for _ in open(f"{d}/{t}/rounds.jsonl", encoding="utf-8"))
    except OSError: return 0
def mp(rs): return [sum(r["prices"]) / len(r["prices"]) for r in rs]
def idx(rs): return (np.mean(mp(rs)) - 10) / 45
def dirs(pats): return [d for p in pats for d in sorted(glob.glob(p)) if os.path.isdir(d)]  # pattern order kept: data/main seeds first, then gemma_more (same order as analysis/new_runs.py)
def gated(ds):
    base = [d for d in ds if n_rows(d, "base") == 30]
    return base, [d for d in base if idx(rows(f"{d}/base/rounds.jsonl")[15:30]) >= 0.5]
def boot(x):
    x = np.asarray(x); m = np.random.default_rng(0).choice(x, (10000, len(x))).mean(axis=1)
    return x.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)
def effect(g, tag, ref="none"):
    ok = [d for d in g if n_rows(d, tag) == 30 and n_rows(d, ref) == 30]
    if not ok: return None
    x = [idx(rows(f"{d}/{tag}/rounds.jsonl")) - idx(rows(f"{d}/{ref}/rounds.jsonl")) for d in ok]
    m, lo, hi = boot(x) if len(x) > 1 else (x[0], x[0], x[0])
    return m, lo, hi, len(ok)

COND = [("clone", "clone_k1_hid", "none"), ("family", "family_k1_hid", "none"), ("undercutter k=1", "undercutter_k1_hid", "none"),
        ("undercutter k=2", "undercutter_k2_hid", "none"), ("announced undercutter k=1", "undercutter_k1_ann", "none"),
        ("comm-cut clone", "clone_k1_hid_nocomm", "none_nocomm")]
G = {m: gated(dirs(p)) for m, p in MODELS.items()}
EFF = {m: {c: effect(G[m][1], t, r) for c, t, r in COND} for m in MODELS}
GA = {m: gated(dirs(p)) for m, p in ALL_MODELS.items()}
EFFA = {m: {c: effect(GA[m][1], t, r) for c, t, r in COND} for m in ALL_MODELS}

# ---- tables
def cell(e):
    if e is None: return "not run"
    m, lo, hi, n = e
    return f"{m:+.3f} ({lo:+.3f}, {hi:+.3f}), n={n}" if n > 1 else f"{m:+.3f}, n=1"
def table(g, eff, models):
    t = ["| | " + " | ".join(models) + " |", "|---|" + "---|" * len(models),
         "| base runs finished / gated | " + " | ".join(f"{len(g[m][0])} / {len(g[m][1])}" for m in models) + " |"]
    ns = {}
    for m in models:
        ok = [d for d in g[m][1] if n_rows(d, "none") == 30]
        ns[m] = f"{np.mean([idx(rows(f'{d}/none/rounds.jsonl')) for d in ok]):.2f} (n={len(ok)})" if ok else "not run"
    t.append("| no-swap index, rounds 31-60 | " + " | ".join(ns[m] for m in models) + " |")
    for c, _, _ in COND:
        t.append(f"| {c} | " + " | ".join(cell(eff[m][c]) for m in models) + " |")
    return t
RULE = ("Index = (mean price - 10) / 45, a price-level measure (10 = competitive price, 55 = monopoly price = 1.0). A run is gated if its base run has 30 rounds and index over rounds 16-30 >= 0.5. "
        "Effect = index over rounds 31-60 of the branch minus the index of the same run's reference branch (no swap; for the comm-cut clone, the no-swap branch with messages also cut), averaged over gated runs whose branch and reference both have exactly 30 rounds. "
        "Interval = 95% percentile bootstrap over base runs, 10000 resamples, seed 0 (the same function as analysis/common.py bootstrap). Narrow intervals (gemma, qw38) reflect near-identical runs and understate uncertainty; "
        "the upper end of the gemma comm-cut interval moves between -0.012 and -0.062 with the bootstrap seed because 3 of 9 runs are near -0.6, the point estimate -0.207 is stable. "
        "Effects are conditional on the 60% gate. Branches are full history, messages on, hidden swap, k = firms replaced, unless named. n=1 cells have no interval. Hosted endpoints ignore the seed parameter.")
L = ["# Results tables (V2)", "", "Generated by `figures/make_figures.py` from `data/*/rounds.jsonl`. " + RULE, "",
     "## Table 1. Headline pooling: seeds 11-20 (gemma4-12b, deepseek-v4-1-flash), 21-25 (qw38), 21-30 (glm53f)", "",
     "Folders: data/main (gemma, deepseek), data/qwen, data/glm. This is the pooling of README.md and of figures a, b, c. Same n in every cell of one column except where a branch is unfinished.", ""]
L += table(G, EFF, list(MODELS))
L += ["", "## Table 2. All seeds: as Table 1 plus deepseek-v4-1-flash seeds 31-40 (data/more_ds), so deepseek n=20", "",
      "Only the deepseek column differs from Table 1; the other columns are repeated for reading convenience. Do not compare cells across Table 1 and Table 2.", ""]
L += table(GA, EFFA, list(ALL_MODELS))
PRE3 = {"gemma4-12b": "gemma4-12b", "deepseek-v4-1-flash": "deepseek-v4-1-flash", "qw38": "qw38", "glm53f": "glm53f"}
L += ["", "## Table 3. Factor cells (new base runs per factor; gate applied to each cell's own base runs; seeds 21-25 for every cell below)", "",
      "History none = firms see no past prices (messages still shown); history last = only the last round; notes = private notes; known end = prompt says exactly 60 rounds. Each cell is a separate set of base runs, so compare with Table 1 with care. n = gated runs with finished branches.", "",
      "| factor | model | base finished / gated | no-swap index | clone | undercutter k=1 | undercutter k=2 |", "|---|---|---|---|---|---|---|"]
for r, lab in [("hist0", "history none"), ("hist1", "history last round"), ("notes", "notes"), ("horizon", "known end")]:
    for m in PRE3:
        ds_ = dirs([f"{D}/{r}/{m}_common_s*"]); b_, g_ = gated(ds_)
        if not b_: continue
        ok = [d for d in g_ if n_rows(d, "none") == 30]
        ni = f"{np.mean([idx(rows(f'{d}/none/rounds.jsonl')) for d in ok]):.2f}" if ok else "-"
        L.append(f"| {lab} | {m} | {len(b_)} / {len(g_)} | {ni} | " + " | ".join(cell(effect(g_, t)) for t in ("clone_k1_hid", "undercutter_k1_hid", "undercutter_k2_hid")) + " |")
open("Submission/preliminary_report/V2/RESULTS_TABLE.md", "w", encoding="utf-8").write(chr(10).join(L) + chr(10))

# ---- style
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "font.size": 10, "axes.grid": True, "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})
SW = [("none", "no swap", OI["black"], "-"), ("clone_k1_hid", "fresh copy (1 replaced)", OI["sky"], "-"), ("family_k1_hid", "other model (1 replaced)", OI["green"], "--"),
      ("undercutter_k1_hid", "scripted undercutter (1 replaced)", OI["orange"], "-"), ("undercutter_k2_hid", "scripted undercutter (2 replaced)", OI["verm"], "-")]
def refs(ax):
    ax.axvline(30.5, color="grey", ls=":"); ax.axhline(10, color="grey", lw=.8); ax.axhline(55, color="grey", lw=.8)

# (a)
fig, axs = plt.subplots(1, 4, figsize=(15, 4.0), sharey=True)
seeds_a = {}
for ax, (m, pats) in zip(axs, FIG_A.items()):
    g = G[m][1]; seeds_a[m] = [os.path.basename(d).rsplit("_s", 1)[1] for d in g]
    basem = np.array([mp(rows(f"{d}/base/rounds.jsonl")) for d in g]); basep = basem.mean(axis=0)
    for tag, lab, col, ls in SW:
        ok = [d for d in g if n_rows(d, tag) == 30]
        if not ok: continue
        arr = np.array([mp(rows(f"{d}/{tag}/rounds.jsonl")) for d in ok])
        y = np.concatenate([basep, arr.mean(axis=0)])
        if tag in ("none", "undercutter_k1_hid"):  # band = min to max over runs (base part: all gated runs)
            lo = np.concatenate([basem.min(axis=0), arr.min(axis=0)]); hi = np.concatenate([basem.max(axis=0), arr.max(axis=0)])
            ax.fill_between(range(1, 61), lo, hi, color=col, alpha=.12, lw=0)
        ax.plot(range(1, 61), y, color=col, ls=ls, lw=1.6, label=lab)
    refs(ax); ax.set_title(f"{DN[m]} ({len(g)} runs)", fontsize=11); ax.set_xlabel("round")
axs[0].set_ylabel("average price (10 = competitive, 55 = monopoly)"); axs[0].set_ylim(5, 92)
axs[3].annotate("some round-1 prices\nup to 89", xy=(1, 64), xytext=(8, 80), fontsize=7, arrowprops=dict(arrowstyle="-", color="grey"))
fig.suptitle("Average price in each round, by model", fontsize=13)
fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=5, fontsize=9, frameon=False)
fig.tight_layout(rect=[0, .07, 1, .95]); fig.savefig(f"{OUT}/fig_a_price_per_round.png", dpi=160); plt.close(fig)

# (b)
conds = COND[:4]; fig, ax = plt.subplots(figsize=(9.5, 4.4)); w = .2
cols = [OI["sky"], OI["green"], OI["orange"], OI["verm"]]
for i, (c, _, _) in enumerate(conds):
    for j, m in enumerate(MODELS):
        e = EFF[m][c]; x = j + (i - 1.5) * w
        if e is None: continue
        ax.bar(x, e[0], w, color=cols[i], label=LAB[c] if j == 0 else None)
        if e[3] > 1: ax.errorbar(x, e[0], yerr=[[e[0] - e[1]], [e[2] - e[0]]], color="black", lw=1, capsize=2)
        if abs(e[0]) < .0015: ax.plot(x, 0, marker="D", color="black", ms=4, zorder=4)  # zero effect marker
        ax.text(x, (e[2] if e[3] > 1 else e[0]) + (.02 if abs(e[0]) < .0015 else .008) if e[0] >= -.0005 else min(e[1], e[0]) - .008, f"{e[0]:+.2f}", ha="center", va="bottom" if e[0] >= -.0005 else "top", fontsize=6.5, rotation=90)
ax.axhline(0, color="black", lw=.8); ax.set_xticks(range(len(MODELS))); ax.set_xticklabels([f"{DN[m]}\n({len(G[m][1])} runs)" for m in MODELS])
ax.set_ylabel("change in collusion index, rounds 31-60\ncompared with no swap"); ax.set_ylim(-.46, .2)
ax.legend(fontsize=8, ncol=2, loc="upper right"); ax.set_title("Effect of replacing firms on the collusion index", fontsize=12)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_b_effects.png", dpi=160); plt.close(fig)

# (c)
MK = {**{m: MODELS[m] for m in ["gemma4-12b", "deepseek-v4-1-flash", "glm53f"]}, **MIXED}
fig, ax = plt.subplots(figsize=(10, 4)); w = .35
cc = [("fresh copy", "clone_k1_hid_nocomm", OI["sky"]), ("scripted undercutter", "undercutter_k1_hid_nocomm", OI["orange"])]
for j, (m, p) in enumerate(MK.items()):
    _, g = gated(dirs(p))
    for i, (lab, t, col) in enumerate(cc):
        e = effect(g, t, "none_nocomm"); x = j + (i - .5) * w
        if e is None: continue
        ax.bar(x, e[0], w, color=col, label=lab if j == 0 else None)
        if e[3] > 1: ax.errorbar(x, e[0], yerr=[[e[0] - e[1]], [e[2] - e[0]]], color="black", lw=1, capsize=2)
        ax.text(x, min(e[0], e[1]) - .02, f"n={e[3]}", ha="center", va="top", fontsize=7)
ax.axhline(0, color="black", lw=.8); ax.set_xticks(range(len(MK))); ax.set_xticklabels([MIXLAB.get(m) or DN[m] for m in MK], fontsize=9)
ax.set_ylabel("change in collusion index, rounds 31-60\ncompared with no swap (messages cut)"); ax.legend(fontsize=8, loc="lower left"); ax.set_ylim(-0.85, 0.05)
ax.set_title("Replacing one firm when messages are cut", fontsize=12); fig.tight_layout(); fig.savefig(f"{OUT}/fig_c_comm_cut.png", dpi=160); plt.close(fig)

# (d)
fig, axs = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True); d_info = {}
for ax, (m, root) in zip(axs, [("gemma4-12b", "nfirm"), ("deepseek-v4-1-flash", "nfirm_ds")]):
    pts = {2: [], 3: [], 4: [], 5: []}
    main = [d for d in dirs([f"{D}/main/{m}_common_s*"]) if 11 <= int(d.rsplit("_s", 1)[1]) <= 20]
    for d in dirs([f"{D}/{root}/*_common_s*"]) + main:
        if n_rows(d, "base") == 30:
            k = os.path.basename(d).split("_common")[0].count("+") + 1 if root in d.replace("\\", "/") else 3
            pts[k].append(idx(rows(f"{d}/base/rounds.jsonl")[15:30]))
    d_info[m] = {k: len(v) for k, v in pts.items()}
    for k, v in pts.items():
        ax.bar(k, np.mean(v), .6, color=OI["sky"], alpha=.6); ax.scatter([k] * len(v), v, color=OI["blue"], s=12, zorder=3)
    ax.axhline(.5, color=OI["verm"], ls="--", lw=1); ax.set_xticks([2, 3, 4, 5]); ax.set_xlabel("number of firms")
    ax.set_title(DN[m], fontsize=11)
axs[0].set_ylabel("collusion index, rounds 16-30"); axs[0].text(2.0, .52, "dashed line = 0.5", color=OI["verm"], ha="left", fontsize=8)
fig.suptitle("Collusion index by number of firms", fontsize=12); fig.tight_layout(rect=[0, 0, 1, .94]); fig.savefig(f"{OUT}/fig_d_firms.png", dpi=160); plt.close(fig)

# (e)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True); e_info = {}
X = [22.5, 45, 75, 105]
for ax, (m, root) in zip(axs, [("gemma4-12b", "long"), ("deepseek-v4-1-flash", "long_ds")]):
    e_info[m] = []; means = {}
    for d in dirs([f"{D}/{root}/*_common_s*"]):
        if n_rows(d, "base") != 30: continue
        b = idx(rows(f"{d}/base/rounds.jsonl")[15:30]); ok = b >= .5
        e_info[m].append(d.rsplit("_s", 1)[1] + ("" if ok else " (fails gate)"))
        for tag, col in [("none", OI["black"]), ("undercutter_k1_hid", OI["orange"])]:
            r = rows(f"{d}/{tag}/rounds.jsonl"); ys = [b] + [idx(r[a:a + 30]) if len(r) >= a + 30 else np.nan for a in (0, 30, 60)]
            ax.plot(X, ys, color=col, alpha=.7 if ok else .3, lw=1, ls="-" if ok else ":")
            if ok: means.setdefault(tag, []).append(ys)
    for tag, col, lab in [("none", OI["black"], "no swap"), ("undercutter_k1_hid", OI["orange"], "scripted undercutter")]:
        if tag in means: ax.plot(X, np.nanmean(means[tag], axis=0), color=col, lw=2.4, label=f"{lab} (average)")
    ax.axvline(30, color="grey", ls=":"); ax.set_title(DN[m], fontsize=11); ax.set_xlabel("round (blocks 16-30, 31-60, 61-90, 91-120)")
axs[0].set_ylabel("collusion index in each block"); fig.suptitle("Collusion index in a game of up to 120 rounds", fontsize=12); fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=2, fontsize=9, frameon=False); fig.tight_layout(rect=[0, .07, 1, .94]); fig.savefig(f"{OUT}/fig_e_horizon.png", dpi=160); plt.close(fig)

print("gemma gated", [os.path.basename(d) for d in G["gemma4-12b"][1]], {c: (None if e is None else tuple(round(float(v),3) for v in e)) for c, e in EFF["gemma4-12b"].items()})
print("done", {m: (len(G[m][0]), len(G[m][1])) for m in MODELS}, "seeds_a", seeds_a, d_info, e_info, sep=chr(10))
