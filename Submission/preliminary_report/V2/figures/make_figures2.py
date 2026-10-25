"""Second figure script: fig_f ... fig_p (captions are in CAPTIONS.md; NOTES printed at the end).
Run from the repo root: .venv/Scripts/python.exe -I Submission/preliminary_report/V2/figures/make_figures2.py
Reads data/ only. Same gate, index, effect and bootstrap rules as make_figures.py (helpers copied)."""
import glob, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch

OUT = "Submission/preliminary_report/V2/figures"
D = "data"
PRE = {"gemma": "gemma4-12b", "deepseek": "deepseek-v4-1-flash", "qw38": "qw38", "glm53f": "glm53f"}
MODELS = {
    "gemma": [f"{D}/main/gemma4-12b_common_s*"],  # headline pooling: seeds 11-20 (gemma seed 31 in data/gemma_more is unfinished, never used)
    "deepseek": [f"{D}/main/deepseek-v4-1-flash_common_s*"],  # seeds 11-20; seeds 31-40 (data/more_ds) are in the all-seeds table only
    "qw38": [f"{D}/qwen/qw38_common_s*"],
    "glm53f": [f"{D}/glm/glm53f_common_s*"],
}
OI = dict(black="#000000", orange="#E69F00", sky="#56B4E9", green="#009E73", yellow="#F0E442", blue="#0072B2", verm="#D55E00", pink="#CC79A7")
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "font.size": 10, "axes.grid": True, "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})


def rows(p): return [json.loads(l) for l in open(p, encoding="utf-8")]
def n_rows(d, t):
    try: return sum(1 for _ in open(f"{d}/{t}/rounds.jsonl", encoding="utf-8"))
    except OSError: return 0
def mp(rs): return [sum(r["prices"]) / len(r["prices"]) for r in rs]
def idx(rs): return (np.mean(mp(rs)) - 10) / 45
def dirs(pats): return sorted(d for p in pats for d in glob.glob(p) if os.path.isdir(d))
def seed(d): return int(d.rsplit("_s", 1)[1])
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
def root(r, m): return [f"{D}/{r}/{PRE[m]}_common_s*"]
def errbar(ax, x, e):
    if e[3] > 1: ax.errorbar(x, e[0], yerr=[[e[0] - e[1]], [e[2] - e[0]]], color="black", lw=1, capsize=2)
def zero_ref(ax): ax.axhline(0, color="black", lw=.8)

G = {m: gated(dirs(p)) for m, p in MODELS.items()}
NOTES = {}  # letter -> README row cells

# ---------------- f) schematic
fig, ax = plt.subplots(figsize=(12, 5.2)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.grid(False)
def box(x, y, w, h, t, c, fs=9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=c, ec="black", lw=1))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
def arrow(a, b): ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color="black", lw=1))
box(.2, 2.4, 3.4, 1.2, "Base run, rounds 1-30\n3 firms, same model,\nmessages + full history", "#E8F1FA")
box(4.2, 2.4, 1.5, 1.2, "Checkpoint\nafter round 30\n(gate: CI 16-30 >= 0.5)", "#FFF3D6", 8)
arrow((3.6, 3), (4.0, 3))
br = [("no swap", "#EEEEEE"), ("clone k=1", "#E3F3FC"), ("family k=1", "#DDF3EA"), ("undercutter k=1", "#FDF0D5"), ("undercutter k=2", "#F9E1D3")]
for i, (t, fc) in enumerate(br):
    y = 4.8 - i * 1.0
    box(6.6, y, 2.6, .75, f"Branch: {t}\nrounds 31-60", fc, 9)
    arrow((5.7, 3), (6.6, y + .375)); arrow((9.2, y + .375), (10.0, 3))
box(10.0, 2.4, 1.8, 1.2, "Round 60\nindex over 31-60\nvs no-swap branch", "#E8F1FA", 8.5)
ax.text(6, .2, "A swap replaces k firms at round 31 by a fresh copy (clone, history wiped), a scripted undercutter, or a family copy; all branches start from the same checkpoint.\n"
        "Variants: announced swap, messages cut, history none / last round, notes, known end date, new firms entering, LLM newcomers.", ha="center", fontsize=8.5)
ax.set_title("Design: one base run, paired branches from a checkpoint", fontsize=11)
fig.savefig(f"{OUT}/fig_f_design.png", dpi=160, bbox_inches="tight"); plt.close(fig)
NOTES["f"] = ("fig_f_design.png", "Schematic of the design: base run rounds 1-30, checkpoint, branches to round 60", "none (diagram)", "n/a", "n/a")

# ---------------- g) gate by comm on / off
OFF = {"gemma": [f"{D}/main/gemma4-12b_commoff_s*"], "deepseek": [f"{D}/main/deepseek-v4-1-flash_commoff_s*"], "glm53f": [f"{D}/glm/glm53f_commoff_s*"]}
fig, ax = plt.subplots(figsize=(7.5, 4)); w = .35; gi = {}
for j, m in enumerate(OFF):
    for i, (lab, pats, col) in enumerate([("messages on", MODELS[m], OI["blue"]), ("messages off", OFF[m], OI["verm"])]):
        b, g = gated(dirs(pats)); gi[(m, lab)] = (len(g), len(b)); x = j + (i - .5) * w
        ax.bar(x, len(g) / len(b), w, color=col, label=lab if j == 0 else None); ax.text(x, len(g) / len(b) + .02, f"{len(g)}/{len(b)}", ha="center", fontsize=8)
ax.set_xticks(range(3)); ax.set_xticklabels(list(OFF)); ax.set_ylim(0, 1.15); ax.set_ylabel("share of base runs with CI(16-30) >= 0.5"); ax.legend(fontsize=8, loc="upper right")
ax.set_title("Gate: how many base runs reach a cartel, messages on vs off")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_g_gate_comm.png", dpi=160); plt.close(fig)
NOTES["g"] = ("fig_g_gate_comm.png", "Share of finished base runs passing the gate, messages on vs off; count printed on bars",
              "on: data/main, data/glm; off: commoff folders of data/main and data/glm",
              "this is the gate rule itself (finished 30-round base run, CI 16-30 >= 0.5)", "gated/finished: " + "; ".join(f"{m} {k} {v[0]}/{v[1]}" for (m, k), v in gi.items()))

# ---------------- h) heatmap
STD = lambda m: MODELS[m]
CONDS = [("clone", STD, "clone_k1_hid", "none"), ("family", STD, "family_k1_hid", "none"), ("undercutter k=1", STD, "undercutter_k1_hid", "none"), ("undercutter k=2", STD, "undercutter_k2_hid", "none"),
         ("announced clone", STD, "clone_k1_ann", "none"), ("announced undercutter", STD, "undercutter_k1_ann", "none"),
         ("comm-cut clone", STD, "clone_k1_hid_nocomm", "none_nocomm"), ("comm-cut undercutter k=1", STD, "undercutter_k1_hid_nocomm", "none_nocomm")]
for r, lab in [("hist0", "history none"), ("hist1", "history last round"), ("notes", "notes"), ("horizon", "known end")]:
    for c, t in [("clone", "clone_k1_hid"), ("undercutter k=1", "undercutter_k1_hid"), ("undercutter k=2", "undercutter_k2_hid")]:
        CONDS.append((f"{lab}: {c}", (lambda m, r=r: root(r, m)), t, "none"))
HM = list(PRE); Z = np.full((len(CONDS), 4), np.nan); NN = np.zeros((len(CONDS), 4), int); gc = {}
for j, m in enumerate(HM):
    for i, (lab, pf, t, ref) in enumerate(CONDS):
        key = (m, tuple(pf(m)))
        if key not in gc: gc[key] = gated(dirs(pf(m)))[1]
        e = effect(gc[key], t, ref)
        if e: Z[i, j], NN[i, j] = e[0], e[3]
fig, ax = plt.subplots(figsize=(8, 10)); ax.grid(False)
im = ax.imshow(Z, cmap="RdBu", vmin=-.5, vmax=.5, aspect="auto")
for i in range(Z.shape[0]):
    for j in range(4):
        if not np.isnan(Z[i, j]): ax.text(j, i, f"{Z[i, j]:+.2f}\nn={NN[i, j]}", ha="center", va="center", fontsize=7.5, color="white" if abs(Z[i, j]) > .33 else "black")
ax.set_xticks(range(4)); ax.set_xticklabels(HM); ax.set_yticks(range(len(CONDS))); ax.set_yticklabels([c[0] for c in CONDS], fontsize=8.5); ax.xaxis.tick_top()
ax.set_title("Effect on index (rounds 31-60) vs same run's no-swap branch\nblank = not run; comm-cut rows vs no-swap with messages cut", fontsize=10, pad=34)
fig.colorbar(im, ax=ax, shrink=.5, label="change in index")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_h_heatmap.png", dpi=160); plt.close(fig)
NOTES["h"] = ("fig_h_heatmap.png", "Heatmap of effects, 22 conditions x 4 models, mean over gated runs, n printed per cell, blank = not run",
              "standard and announced and comm-cut rows: data/main, qwen, glm; history none: data/hist0; history last round: data/hist1; notes: data/notes; known end: data/horizon",
              "gate applied per folder group using that group's own base runs; branch and reference must both have 30 rounds", "seeds as in each folder (11-20, 21-30, 31-40, 21-25); n in cells")

# ---------------- i) LLM newcomers
NC = ["myopic", "share", "nocollude", "ownprice", "deceptive"]; NM = ["gemma", "deepseek", "glm53f"]; MC = [OI["sky"], OI["orange"], OI["verm"]]
fig, ax = plt.subplots(figsize=(10, 4.2)); w = .26; nn = {}
for k, m in enumerate(NM):
    for i, v in enumerate(NC):
        e = effect(G[m][1], f"newcomer_{v}_k1_hid"); x = i + (k - 1) * w
        if e is None: continue
        nn[(m, v)] = e[3]; ax.bar(x, e[0], w, color=MC[k], label=m if i == 0 else None); errbar(ax, x, e)
        ax.text(x, min(e[1], e[0]) - .015, f"n={e[3]}", ha="center", va="top", fontsize=7)
zero_ref(ax); ax.set_xticks(range(5)); ax.set_xticklabels(NC); ax.set_ylabel("change in index, rounds 31-60\nvs same run's no-swap branch"); ax.legend(fontsize=8, loc="lower center"); ax.set_ylim(-.65, .15)
ax.set_title("LLM newcomer in place of firm C (history wiped), by instruction variant; 95% bootstrap interval")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_i_newcomers.png", dpi=160); plt.close(fig)
NOTES["i"] = ("fig_i_newcomers.png", "Effect of an LLM newcomer (myopic, share, nocollude, ownprice, deceptive instruction) replacing firm C; only finished branches (glm53f: finished folders only)",
              "data/main (gemma, deepseek), data/glm", "gated seeds with finished 30-round branches", "n per bar: " + ", ".join(f"{m}/{v}={n}" for (m, v), n in nn.items()))

# ---------------- j) awareness probe
def yes_count(g, tag):
    y = t = 0
    for d in g:
        p = f"{d}/{tag}/probe.jsonl"
        if n_rows(d, tag) == 30 and os.path.exists(p):
            for r in rows(p):
                t += 1; y += r["message"].strip().lstrip("*\"' ").lower().startswith("yes")
    return y, t
PT = [("none", "no swap", OI["black"]), ("clone_k1_hid", "clone", OI["sky"]), ("undercutter_k1_hid", "undercutter k=1", OI["orange"])]
fig, ax = plt.subplots(figsize=(8, 4)); w = .26; pj = {}
for i, (t, lab, col) in enumerate(PT):
    for j, m in enumerate(NM):
        y, n = yes_count(G[m][1], t); pj[(m, lab)] = f"{y}/{n}"; x = j + (i - 1) * w
        if n: ax.bar(x, y / n, w, color=col, label=lab if j == 0 else None); ax.text(x, y / n + .02, f"{y}/{n}", ha="center", fontsize=8)
ax.set_xticks(range(3)); ax.set_xticklabels(NM); ax.set_ylim(0, 1.1); ax.set_ylabel("share of probed firms answering yes"); ax.legend(fontsize=8)
ax.set_title("Awareness probe: 'was any firm replaced since round 30?'")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_j_awareness.png", dpi=160); plt.close(fig)
NOTES["j"] = ("fig_j_awareness.png", "Share of probed firms (not replaced) whose reply starts with yes after the branch; counts on bars",
              "probe.jsonl in none, clone_k1_hid, undercutter_k1_hid of data/main (gemma, deepseek) and data/glm", "gated runs, 30-round branches", "yes/asked: " + ", ".join(f"{m}/{k} {v}" for (m, k), v in pj.items()))

# ---------------- k) entry
ET = [("entry_k1_hid", "one new firm", OI["sky"]), ("entry_k2_hid", "two new firms", OI["blue"]), ("entry-qwen3-14b_k1_hid", "one new qwen3-14b firm", OI["green"]), ("entry-undercutter_k1_hid", "one new undercutter", OI["orange"])]
ET = [e for e in ET if any(n_rows(d, e[0]) == 30 for m in NM for d in G[m][1])]
fig, ax = plt.subplots(figsize=(8, 4.2)); w = .8 / len(ET); en = {}
for i, (t, lab, col) in enumerate(ET):
    for j, m in enumerate(NM):
        e = effect(G[m][1], t)
        if e is None: continue
        en[(m, lab)] = e[3]; x = j + (i - (len(ET) - 1) / 2) * w
        ax.bar(x, e[0], w, color=col); errbar(ax, x, e); ax.text(x, min(e[1], e[0]) - .01, f"n={e[3]}", ha="center", va="top", fontsize=7)
ax.legend([Patch(color=c) for _, _, c in ET], [lb for _, lb, _ in ET], fontsize=8, loc="upper right")
zero_ref(ax); ax.set_xticks(range(3)); ax.set_xticklabels(NM); ax.set_ylabel("change in index, rounds 31-60\nvs no-swap branch"); ax.set_ylim(-.4, .2)
ax.set_title("Entry: new firms join at round 31 without the history (95% bootstrap interval)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_k_entry.png", dpi=160); plt.close(fig)
miss = "entry-undercutter_k1_hid" not in [e[0] for e in ET]
NOTES["k"] = ("fig_k_entry.png", "Effect of one or two new firms entering, plus the qwen3-14b entrant where finished" + ("; the folder entry-undercutter_k1_hid does not exist, so that entrant is skipped" if miss else ""),
              "data/main (gemma, deepseek), data/glm", "gated seeds with finished branches", "n: " + ", ".join(f"{m}/{k} {v}" for (m, k), v in en.items()))

# ---------------- l) temperature
TM = {"gemma": ("gemma4-12b", [("0.3", "temp03"), ("0.7", "main"), ("1.0", "temp10")]), "deepseek": ("deepseek-v4-1-flash", [("0.3", "temp03_ds"), ("0.7", "main"), ("1.0", "temp10_ds")])}
fig, axs = plt.subplots(1, 2, figsize=(10, 4)); tn = {}
for m, (pf, lst) in TM.items():
    col = OI["blue"] if m == "gemma" else OI["verm"]; sh = .015 if m == "deepseek" else -.015
    xs, ys, ex, ey = [], [], [], []
    for T, r in lst:
        g = gated([d for d in dirs([f"{D}/{r}/{pf}_common_s*"]) if seed(d) in (11, 13, 14)])[1]
        ok = [d for d in g if n_rows(d, "none") == 30]
        ni = [idx(rows(f"{d}/none/rounds.jsonl")) for d in ok]
        eff = [d for d in g if n_rows(d, "undercutter_k1_hid") == 30 and n_rows(d, "none") == 30]
        tn[(m, T)] = (len(g), len(eff))
        axs[0].scatter([float(T) + sh] * len(ni), ni, color=col, s=14, alpha=.6)
        if ni: xs.append(float(T)); ys.append(np.mean(ni))
        v = [idx(rows(f"{d}/undercutter_k1_hid/rounds.jsonl")) - idx(rows(f"{d}/none/rounds.jsonl")) for d in eff]
        axs[1].scatter([float(T) + sh] * len(v), v, color=col, s=14, alpha=.6)
        if v: ex.append(float(T)); ey.append(np.mean(v))
    axs[0].plot(xs, ys, color=col, lw=1.8, label=m); axs[1].plot(ex, ey, color=col, lw=1.8, label=m)
for ax, t in zip(axs, ["no-swap index, rounds 31-60", "undercutter k=1 effect, rounds 31-60"]):
    ax.set_xlabel("sampling temperature"); ax.set_ylabel(t); ax.set_xticks([.3, .7, 1.0]); ax.legend(fontsize=8)
zero_ref(axs[1]); axs[0].set_ylim(0, 1); fig.suptitle("Temperature: dots = gated seeds (11, 13, 14), line = mean", y=1.0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_l_temperature.png", dpi=160); plt.close(fig)
NOTES["l"] = ("fig_l_temperature.png", "No-swap index and undercutter k=1 effect at temperature 0.3, 0.7, 1.0; dots = seeds, line = mean",
              "gemma: data/temp03, data/main, data/temp10; deepseek: data/temp03_ds, data/main, data/temp10_ds", "gated; seeds 11, 13, 14 only (so 0.7 uses the same seeds)",
              "(gated runs, runs with finished undercutter branch): " + ", ".join(f"{m}@{T} {v}" for (m, T), v in tn.items()))

# ---------------- m) mixed and eight firms
GR = [("mixed\ndeepseek/qw38/glm53f", [f"{D}/mixed/*_common_s*"]), ("mixed\ndeepseek/qw38/gemma", [f"{D}/mixed_g/*_common_s*"]),
      ("eight firms\nall base prompt", [f"{D}/eight_a/*_common_s*"]), ("eight firms\none deviator", [f"{D}/eight_b/*_common_s*"])]
fig, axs = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw=dict(width_ratios=[1, 1.3])); mi = []
for j, (lab, pats) in enumerate(GR):
    for d in dirs(pats):
        if n_rows(d, "base") != 30 or n_rows(d, "none") != 30: continue
        b = idx(rows(f"{d}/base/rounds.jsonl")[15:30]); ok = b >= .5; n = idx(rows(f"{d}/none/rounds.jsonl"))
        mi.append(f"{lab.replace(chr(10), ' ')} s{seed(d)}: base {b:.2f} none {n:.2f}{'' if ok else ' (fails gate)'}")
        dx = (seed(d) % 10 - 2) * .08
        axs[0].scatter(j + dx - .12, b, marker="o", color=OI["blue"], s=28, facecolors=OI["blue"] if ok else "none", zorder=3, label="base 16-30" if (j, seed(d)) == (0, 31) else None)
        axs[0].scatter(j + dx + .12, n, marker="s", color=OI["black"], s=28, facecolors=OI["black"] if ok else "none", zorder=3, label="no swap 31-60" if (j, seed(d)) == (0, 31) else None)
axs[0].axhline(.5, color=OI["verm"], ls="--", lw=1); axs[0].set_xticks(range(4)); axs[0].set_xticklabels([g[0] for g in GR], fontsize=7.5); axs[0].set_ylabel("collusion index"); axs[0].set_ylim(-.02, 1.2)
axs[0].legend(fontsize=7, loc="upper right"); axs[0].set_title("Per run; hollow = fails the gate (dashed 0.5)", fontsize=9)
ECOND = [("clone", "clone_k1_hid", OI["sky"]), ("undercutter k=1", "undercutter_k1_hid", OI["orange"]), ("undercutter k=2", "undercutter_k2_hid", OI["verm"])]; w = .25; ms = {}
for j, (lab, pats) in enumerate(GR):
    ds = dirs(pats); g = gated(ds)[1]
    for i, (cl, t, col) in enumerate(ECOND):
        x = j + (i - 1) * w
        allr = [d for d in ds if n_rows(d, "base") == 30 and n_rows(d, t) == 30 and n_rows(d, "none") == 30]
        for d in allr:
            axs[1].scatter(x, idx(rows(f"{d}/{t}/rounds.jsonl")) - idx(rows(f"{d}/none/rounds.jsonl")), color=col, s=22, facecolors=col if d in g else "none", zorder=3)
        e = effect(g, t)
        if e: axs[1].bar(x, e[0], w * .9, color=col, alpha=.5, label=cl if j == 0 else None); ms[(lab.replace("\n", " "), cl)] = e[3]
axs[1].axhline(0, color="black", lw=.8); axs[1].set_xticks(range(4)); axs[1].set_xticklabels([g[0] for g in GR], fontsize=7.5); axs[1].set_ylabel("change in index vs no-swap"); axs[1].legend(fontsize=7, loc="lower left")
axs[1].set_title("Effect per run (dots; hollow = fails gate); bars = mean of gated runs", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_m_mixed_eight.png", dpi=160); plt.close(fig)
NOTES["m"] = ("fig_m_mixed_eight.png", "Mixed-model and eight-firm markets: per-run base and no-swap index, and per-run effects (bars = gated mean; the eight-firm groups have few gated runs)",
              "data/mixed (seeds 31-35), data/mixed_g (31-35), data/eight_a, data/eight_b (51-53)", "gate shown by hollow markers; bars use gated runs only", "; ".join(mi))

# ---------------- n) known end
fig, axs = plt.subplots(1, 4, figsize=(13, 3.8), sharey=True); kn = {}
for ax, m in zip(axs, PRE):
    g = [d for d in gated(dirs(root("horizon", m)))[1] if n_rows(d, "none") == 30]; kn[m] = len(g); a = []
    for d in g:
        p = mp(rows(f"{d}/none/rounds.jsonl")); a.append((np.mean(p[:20]), np.mean(p[20:])))
        ax.plot([0, 1], a[-1], color="grey", marker="o", lw=1, alpha=.7)
    if a: ax.plot([0, 1], np.mean(a, axis=0), color=OI["verm"], lw=2.6, marker="s")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["rounds 31-50", "rounds 51-60"]); ax.set_xlim(-.3, 1.3); ax.set_title(f"{m} ({len(g)} gated runs)", fontsize=10)
    ax.axhline(55, color="grey", lw=.8); ax.axhline(10, color="grey", lw=.8)
axs[0].set_ylabel("mean price, no-swap branch\n(competitive 10, monopoly 55)"); fig.suptitle("Known end date (prompt says 60 rounds): grey = single runs, red = mean", y=1.0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_n_known_end.png", dpi=160); plt.close(fig)
NOTES["n"] = ("fig_n_known_end.png", "Mean price in rounds 31-50 vs 51-60 of the no-swap branch where the prompt states the game ends at round 60", "data/horizon (gemma, deepseek, qw38, glm53f)", "gated runs",
              "seeds 21-25; gated n: " + ", ".join(f"{m}={v}" for m, v in kn.items()) + " (gemma fails the 60% rule in this cell)")

# ---------------- o) per-seed gemma main
ds = [d for d in dirs([f"{D}/main/gemma4-12b_common_s*"]) if n_rows(d, "base") == 30 and n_rows(d, "none") == 30 and n_rows(d, "undercutter_k1_hid") == 30]
fig, axs = plt.subplots(2, 5, figsize=(15, 6), sharey=True, sharex=True)
for ax, d in zip(axs.flat, ds):
    b = mp(rows(f"{d}/base/rounds.jsonl")); ok = idx(rows(f"{d}/base/rounds.jsonl")[15:30]) >= .5
    for t, lab, col in [("none", "no swap", OI["black"]), ("undercutter_k1_hid", "undercutter k=1", OI["orange"])]:
        ax.plot(range(1, 61), b + mp(rows(f"{d}/{t}/rounds.jsonl")), color=col, lw=1.5, label=lab)
    ax.axvline(30.5, color="grey", ls=":"); ax.axhline(55, color="grey", lw=.8); ax.axhline(10, color="grey", lw=.8)
    ax.set_title(f"seed {seed(d)}" + ("" if ok else " (fails gate)"), fontsize=9)
for ax in axs[1]: ax.set_xlabel("round")
for ax in axs[:, 0]: ax.set_ylabel("mean price")
axs.flat[0].legend(fontsize=7, loc="lower left"); axs.flat[0].set_ylim(5, 62)
fig.suptitle("gemma4-12b, data/main: seed-to-seed variation (dotted = swap)", y=1.0); fig.tight_layout(); fig.savefig(f"{OUT}/fig_o_per_seed.png", dpi=160); plt.close(fig)
NOTES["o"] = ("fig_o_per_seed.png", "gemma4-12b price per round, no swap vs undercutter k=1, one panel per seed; all seeds shown, ungated marked in title", "data/main gemma4-12b_common",
              "gate not applied (marked in titles)", "seeds " + ", ".join(str(seed(d)) for d in ds) + f"; n={len(ds)} panels")

# ---------------- p) message volume
def words(r): return np.mean([len(m.split()) for m in r["msgs"]]) if r.get("msgs") else np.nan
fig, ax = plt.subplots(figsize=(8, 4)); pn = {}
for m, col in [("gemma", OI["blue"]), ("deepseek", OI["verm"])]:
    g = [d for d in G[m][1] if d.replace("\\", "/").startswith(f"{D}/main/") and n_rows(d, "none") == 30]; pn[m] = len(g)
    ys = np.array([[words(r) for r in rows(f"{d}/base/rounds.jsonl") + rows(f"{d}/none/rounds.jsonl")] for d in g])
    for y in ys: ax.plot(range(1, 61), y, color=col, alpha=.15, lw=.8)
    ax.plot(range(1, 61), np.nanmean(ys, axis=0), color=col, lw=2.2, label=f"{m} (mean of {len(g)} gated runs)")
ax.axvline(30.5, color="grey", ls=":"); ax.set_xlabel("round"); ax.set_ylabel("mean words per message"); ax.legend(fontsize=8); ax.set_ylim(bottom=0)
ax.set_title("Message length over time (base run + no-swap branch)"); fig.tight_layout(); fig.savefig(f"{OUT}/fig_p_message_volume.png", dpi=160); plt.close(fig)
NOTES["p"] = ("fig_p_message_volume.png", "Mean words per message per round (three firms averaged), thin lines = single runs", "data/main gemma4-12b_common and deepseek-v4-1-flash_common, base + none", "gated runs of data/main only", f"n: {pn}")

print("ok", pn, kn, tn, pj, en, sep="\n")
for k in sorted(NOTES): print(k, NOTES[k][4])
