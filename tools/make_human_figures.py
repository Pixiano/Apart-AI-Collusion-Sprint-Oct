"""Figures for the human case studies (supplementary, not in the report). Reads data/human and data/human_suite, writes PNGs to
Submission/supplementary/human_case_studies/.  usage (repo root): .venv\\Scripts\\python.exe -I tools\\make_human_figures.py"""
import glob
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "Submission/supplementary/human_case_studies"
os.makedirs(OUT, exist_ok=True)
BLUE, ORANGE, GREY = "#0072B2", "#D55E00", "#999999"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.3})

GAMES = [  # folder pattern, short title, extra rows file
    ("data/human/*_s71", "Game 1: 3 firms, serious"),
    ("data/human/*_s72", "Game 2: 3 firms, fun (60 rounds)"),
    ("data/human/*_s73", "Game 3: 3 firms, general"),
    ("data/human/*_s74", "Game 4: 5 firms"),
    ("data/human/*_s75", "Game 5: 10 firms"),
    ("data/human_suite/*_s81", "Suite 1: normal"),
    ("data/human_suite/*_s82", "Suite 2: no history"),
    ("data/human_suite/*_s83", "Suite 3: no messages"),
    ("data/human_suite/*_s84", "Suite 4: no history, no messages"),
]


def rows(p):
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def load(pat):
    d = glob.glob(pat)[0]
    r = rows(d + "/base/rounds.jsonl")
    if pat.endswith("s72"):
        r += rows(d + "/none/rounds.jsonl")
    return r


data = [(t, load(p)) for p, t in GAMES]
SHORT = ["Game 1\n3 firms\nserious", "Game 2\n3 firms, fun\n60 rounds", "Game 3\n3 firms\ngeneral", "Game 4\n5 firms", "Game 5\n10 firms",
         "Suite 1\nnormal", "Suite 2\nno history", "Suite 3\nno messages", "Suite 4\nno history,\nno messages"]


def prices_figure():
    fig, axs = plt.subplots(3, 3, figsize=(13, 9), sharey=True)
    for ax, (t, r) in zip(axs.flat, data):
        n = len(r[0]["prices"])
        x = [q["round"] for q in r]
        for i in range(n - 1):
            ax.plot(x, [q["prices"][i] for q in r], color=BLUE, lw=1.2, alpha=0.5)
        ax.plot(x, [q["prices"][-1] for q in r], color=ORANGE, lw=2.4)
        ax.set_title(t, fontsize=11)
        if t.startswith("Game 5"):
            ax.axvline(13.5, color=GREY, ls=":")
            ax.text(14, 95, "two firms told to\nagree with you", fontsize=8, va="top")
    for ax in axs[-1]:
        ax.set_xlabel("round")
    for ax in axs[:, 0]:
        ax.set_ylabel("price")
    fig.suptitle("Price in every round: you in orange, the gemma firms in blue", y=0.995, fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(f"{OUT}/h1_prices_all_games.png", dpi=150)
    plt.close(fig)


def share_figure():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    labs, sh, fair = [], [], []
    for t, r in data:
        n = len(r[0]["prices"])
        tot = [sum(q["profits"][i] for q in r) for i in range(n)]
        labs.append(SHORT[len(labs)])
        sh.append(tot[-1] / sum(tot))
        fair.append(1 / n)
    x = range(len(data))
    ax.bar(x, sh, color=ORANGE, width=0.6, label="your share of all profit")
    ax.scatter(x, fair, color="black", marker="_", s=900, zorder=3, label="equal share (1 / number of firms)")
    for i, v in enumerate(sh):
        ax.text(i, v + 0.02, f"{v:.0%}", ha="center", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labs, fontsize=9)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel("share of all firms' profit")
    ax.set_title("How much of the profit the human took")
    ax.legend(loc="upper center", ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(f"{OUT}/h2_profit_share.png", dpi=150)
    plt.close(fig)


def undercut_figure():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    labs = []
    for k, (t, r) in enumerate(data):
        d = [min(q["prices"][:-1]) - q["prices"][-1] for q in r]
        labs.append(SHORT[len(labs)])
        ax.boxplot([d], positions=[k], widths=0.5, showfliers=True, medianprops=dict(color=ORANGE, lw=2), flierprops=dict(markersize=3, alpha=0.5))
    ax.axhline(0, color="black", lw=1)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labs, fontsize=9)
    ax.set_ylabel("lowest gemma price minus your price")
    ax.set_title("How far below the gemma firms the human priced (above 0 = you were cheaper)")
    fig.tight_layout()
    fig.savefig(f"{OUT}/h3_undercut_size.png", dpi=150)
    plt.close(fig)


def cumulative_figure():
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.8), sharey=False)
    for ax, (t, r) in zip(axs, data[5:]):
        x = [q["round"] for q in r]
        cum = [[sum(q["profits"][i] for q in r[: k + 1]) for k in range(len(r))] for i in range(3)]
        ax.plot(x, cum[0], color=BLUE, alpha=0.6, label="gemma A")
        ax.plot(x, cum[1], color=BLUE, alpha=0.9, ls="--", label="gemma B")
        ax.plot(x, cum[2], color=ORANGE, lw=2.4, label="you")
        ax.set_title(t.split(": ")[1], fontsize=11)
        ax.set_xlabel("round")
    axs[0].set_ylabel("total profit so far")
    axs[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Running total profit in the four information conditions", y=1.0, fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(f"{OUT}/h4_running_profit_suite.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    prices_figure()
    share_figure()
    undercut_figure()
    cumulative_figure()
    print(sorted(os.listdir(OUT)))
