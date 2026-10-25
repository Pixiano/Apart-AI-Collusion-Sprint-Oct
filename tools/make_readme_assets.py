"""Builds the README graphics in assets/ from the run data: banner, human-suite panels, human-vs-ten-firms, and the player-window image.
usage (repo root): .venv\\Scripts\\python.exe -I tools\\make_readme_assets.py"""
import glob
import json
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, FG, GRID = "#0d1117", "#e6edf3", "#30363d"
C = {"A": "#58a6ff", "B": "#3fb950", "H": "#f78166", "none": "#8b949e", "ud": "#d29922"}
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG, "text.color": FG, "axes.labelcolor": FG,
                     "xtick.color": FG, "ytick.color": FG, "axes.edgecolor": GRID, "font.family": "DejaVu Sans"})
os.makedirs("assets", exist_ok=True)


def rows(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def mean_price(r):
    return [sum(x["prices"]) / len(x["prices"]) for x in r]


def banner():
    d = "data/main/gemma4-12b_common_s11"
    base, none, ud = (rows(f"{d}/{p}/rounds.jsonl") for p in ("base", "none", "undercutter_k2_hid"))
    fig, ax = plt.subplots(figsize=(14, 4.2))
    x0 = [r["round"] for r in base]
    x1 = [r["round"] for r in none]
    ax.plot(x0, mean_price(base), color=C["A"], lw=3)
    ax.plot(x1, mean_price(none), color=C["B"], lw=3, label="no swap")
    ax.plot([r["round"] for r in ud], mean_price(ud), color=C["H"], lw=3, label="two scripted undercutters swapped in")
    ax.axvline(30.5, color=GRID, ls="--")
    ax.text(31, 14, "turnover", color="#8b949e", fontsize=11)
    ax.set_ylim(8, 62)
    ax.set_xlim(1, 60)
    ax.set_yticks([10, 55])
    ax.set_yticklabels(["10  competitive", "55  monopoly"])
    ax.set_xlabel("round")
    ax.grid(axis="y", color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="lower left", frameon=False, labelcolor=FG)
    fig.suptitle("Does the cartel survive turnover?", x=0.02, y=0.97, ha="left", fontsize=26, fontweight="bold")
    fig.text(0.02, 0.83, "Repeated pricing game, LLM firms, gemma4-12b, one real run", fontsize=12, color="#8b949e")
    fig.tight_layout(rect=(0, 0, 1, 0.80))
    fig.savefig("assets/banner.png", dpi=110)
    plt.close(fig)


def suite():
    fig, axs = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True)
    for ax, (s, t) in zip(axs, ((81, "normal"), (82, "no history"), (83, "no messages"), (84, "neither"))):
        r = rows(glob.glob(f"data/human_suite/*_s{s}/base/rounds.jsonl")[0])
        x = [q["round"] for q in r]
        for i, (lab, col) in enumerate((("gemma A", C["A"]), ("gemma B", C["B"]), ("you (human)", C["H"]))):
            ax.plot(x, [q["prices"][i] for q in r], color=col, lw=2 if i < 2 else 2.6, alpha=0.9, label=lab)
        ax.set_title(t, fontsize=13)
        ax.set_xlabel("round")
        ax.grid(color=GRID, lw=0.5)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axs[0].set_ylabel("price")
    axs[0].legend(frameon=False, labelcolor=FG, fontsize=9)
    fig.suptitle("Human plays one of three firms: four information conditions (one game each, case studies)", x=0.01, ha="left", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig("assets/human_suite.png", dpi=110)
    plt.close(fig)


def sizes():
    fig, axs = plt.subplots(1, 3, figsize=(15, 3.6), sharey=True)
    for ax, (pat, t) in zip(axs, (("data/human/*_s72", "3 firms (60 rounds)"), ("data/human/*_s74", "5 firms"), ("data/human/*_s75", "10 firms"))):
        d = glob.glob(pat)[0]
        r = rows(d + "/base/rounds.jsonl")
        if pat.endswith("s72"):
            r += rows(d + "/none/rounds.jsonl")
        n = len(r[0]["prices"])
        x = [q["round"] for q in r]
        ai = [sum(q["prices"][:-1]) / (n - 1) for q in r]
        ax.plot(x, ai, color=C["A"], lw=2.4, label="mean of the gemma firms")
        ax.plot(x, [q["prices"][-1] for q in r], color=C["H"], lw=2.4, label="you (human)")
        ax.set_title(t, fontsize=13)
        ax.set_xlabel("round")
        ax.grid(color=GRID, lw=0.5)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axs[0].set_ylabel("price")
    axs[0].legend(frameon=False, labelcolor=FG, fontsize=9)
    fig.suptitle("Human plays one firm against 2, 4 and 9 gemma firms (fun research direction, one game each)", x=0.01, ha="left", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig("assets/human_sizes.png", dpi=110)
    plt.close(fig)


def window():
    t = open("data/human_ext6/human.prompt.txt", encoding="utf-8").read().split("\n\n(File-protocol note")[0]
    rn = int(t[t.index("Round ") + 6:].split(".")[0])
    q = rows(glob.glob("data/human_suite/*_s81/base/rounds.jsonl")[0])[rn - 1]  # the author's real reply to this prompt
    t = t[t.index("Round "):]
    tl = t.split("\n")
    idx = [i for i, l in enumerate(tl) if l[:1].isdigit() and " | " in l]
    drop = set(idx[:-6])  # keep the last six table rows
    lines = []
    for i, l in enumerate(tl):
        if i not in drop:
            lines += textwrap.wrap(l, 96) or [""]
    lines = ["Human firm C   (tools/play_human.py)", "=" * 70] + lines[:40] + ["", f"price (10-100)> {q['prices'][2]}", f"message (max 30 words)> {q['msgs'][2]}"]
    fig = plt.figure(figsize=(11, 0.168 * len(lines) + 0.5))
    fig.patch.set_facecolor("#010409")
    fig.text(0.02, 0.97, "\n".join(lines), family="DejaVu Sans Mono", fontsize=9, va="top", color="#7ee787")
    fig.savefig("assets/player_window.png", dpi=110, facecolor="#010409")
    plt.close(fig)


if __name__ == "__main__":
    banner()
    suite()
    sizes()
    window()
    print("ok", sorted(os.listdir("assets")))
