"""fig_q_swap_timing.png: gemma, 9 gated seeds (11-20 gate from data/main base), first 15 rounds after the swap, branch minus same checkpoint's no-swap.
Same definitions as analysis/new_runs.py section 5. Run from the repo root: .venv/Scripts/python.exe -I Submission/preliminary_report/V2/figures/make_figures3.py"""
import glob, os, sys
sys.path.insert(0, "analysis")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import bootstrap, rows, window_ci

OUT = "Submission/preliminary_report/V2/figures"
D = "data"
OI = dict(sky="#56B4E9", orange="#E69F00")
main = {int(d.rsplit("_s", 1)[1]): d for d in sorted(glob.glob(f"{D}/main/gemma4-12b_common_s*"))}
gate = [s for s, d in main.items() if len(rows(f"{d}/base/rounds.jsonl")) >= 30 and window_ci(rows(f"{d}/base/rounds.jsonl"), 16, 30) >= .5]
def load(d, t):
    try: return rows(f"{d}/{t}/rounds.jsonl")
    except (OSError, ValueError): return None
def eff(br, t):
    res = []
    for s in gate:
        if t == 30:
            d, lo, hi, need = main[s], 31, 45, 30
        else:
            d, (lo, hi), need = f"{D}/gemma_timing/gemma4-12b_common_s{s}_t{t}", ((16, 30) if t == 15 else (46, 60)), (30 if t == 15 else 15)
        a, r = load(d, br), load(d, "none")
        if a is None or r is None or len(a) != need or len(r) != need: continue
        res.append(window_ci(a, lo, hi) - window_ci(r, lo, hi))
    return res
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "font.size": 10, "axes.grid": True, "grid.alpha": .25, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(8, 4.4)); w = .34; T = (15, 30, 45)
for i, (br, lab, col) in enumerate([("clone_k1_hid", "fresh copy (1 replaced)", OI["sky"]), ("undercutter_k1_hid", "scripted undercutter (1 replaced)", OI["orange"])]):
    for j, t in enumerate(T):
        v = eff(br, t); m, lo, hi = bootstrap(v); x = j + (i - .5) * w
        print(br, "swap at", t, f"{m:+.3f} ({lo:+.3f}, {hi:+.3f}) n={len(v)}")
        ax.bar(x, m, w, color=col, label=lab if j == 0 else None)
        ax.errorbar(x, m, yerr=[[m - lo], [hi - m]], color="black", lw=1, capsize=3)
        ax.text(x, hi + .004 if m > -.005 else lo - .004, f"{m:+.3f}", ha="center", va="bottom" if m > -.005 else "top", fontsize=8)
ax.axhline(0, color="black", lw=.8); ax.set_xticks(range(3)); ax.set_xticklabels([f"swap at round {t}\n(rounds {t + 1}-{t + 15})" for t in T])
ax.set_ylabel("change in collusion index, first 15 rounds\nafter the swap, compared with no swap"); ax.set_ylim(-.075, .02)
ax.legend(fontsize=9, loc="lower right"); ax.set_title("Effect of the swap round on the collusion index (Gemma)", fontsize=12)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_q_swap_timing.png", dpi=160); plt.close(fig)
print("gated seeds", gate)
