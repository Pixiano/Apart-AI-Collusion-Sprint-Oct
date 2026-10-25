# Figure captions (V2 draft; the author rewrites)

Scripts: `make_figures.py` (figures a to e, `../RESULTS_TABLE.md`) and `make_figures2.py` (figures f to p). Run from the repo root with `.venv/Scripts/python.exe -I Submission/preliminary_report/V2/figures/<script>`. They read `data/` only and write the PNGs here.

Common definitions (repeat the short form in every caption).
- Collusion index, a price-level measure: CI = (mean price - 10) / 45, averaged over all firms and the rounds of a window. 0 is the competitive price 10, 1 is the monopoly price 55. "Cartel-like pricing" means CI near 1. It says nothing about intent or about how the price was reached.
- Gate: a base run counts only if CI over rounds 16-30 is at least 0.5. A model and communication setting is analysed only if at least 60% of its base runs pass. All effects are conditional on the gate.
- Effect: CI over rounds 31-60 of a branch minus CI of the same base run's no-swap branch (for comm-cut branches, the no-swap branch with messages also cut). Mean over gated runs; interval = 95% percentile bootstrap over base runs, 10000 resamples, seed 0. Narrow intervals (gemma, qw38) come from near-identical runs and understate uncertainty.
- Headline pooling (figures a, b, c and every other figure unless stated): gemma4-12b seeds 11-20 (data/main, 10 base runs, 9 gated), deepseek-v4-1-flash seeds 11-20 (data/main, 10 of 10 gated), qw38 seeds 21-25 (5 of 5), glm53f seeds 21-30 (10 of 10). The all-seeds pooling (deepseek also seeds 31-40, n=20) appears only in `RESULTS_TABLE.md` Table 2. gemma seed 31 (unfinished) is never used.

## Main text

**Figure 1 (fig_f_design.png). Design.** One base run (rounds 1-30, three firms of one model, messages and full history) is saved as a checkpoint. From the same checkpoint, branches replay rounds 31-60: no swap, a fresh clone (history wiped), a family model, a scripted undercutter (one cent below the lowest last price), with one or two firms replaced. Variants (announced swap, messages cut, history none or last round, notes, known end, entry, LLM newcomers) are listed under the diagram. Gate: CI(16-30) >= 0.5. No data.

**Figure 2 (fig_a_price_per_round.png). Mean price per round.** One panel per model, headline pooling, gated runs only: gemma4-12b n=9, deepseek-v4-1-flash n=10, qw38 n=5, glm53f n=10. Lines are means over runs; the shaded bands run from the lowest to the highest run for the no-swap and undercutter k=1 branches (and over all gated base runs before round 31). The dotted line marks the swap after round 30; grey lines are the competitive price 10 and the monopoly price 55. The glm53f panel starts high because some glm53f runs open far above the monopoly price (a three-firm mean of up to 89 in round 1, mean over runs about 64); the axis now shows it.

**Figure 3 (fig_b_effects.png). Effects of replacing firms.** Headline pooling; same n gated as Figure 2 (9, 10, 5, 10). Bars are the mean change in CI over rounds 31-60 against the same run's no-swap branch, with 95% bootstrap intervals over runs. The value is printed on each bar; a black diamond marks an effect within 0.0015 of zero, so that zero effects are visible. n per bar equals the gated n in every cell (clone, family, undercutter k=1 and k=2). Exploratory cells are not in this figure.

**Figure 4 (fig_c_comm_cut.png). Messages cut at the swap.** Messages are on in rounds 1-30 and off from round 31. Bars are effects against the no-swap branch with messages also cut (so the cut itself is removed). Headline pooling, gated runs: gemma4-12b n=9, deepseek-v4-1-flash n=10, glm53f n=5 (the cut cells exist for seeds 21-25 only), mixed markets n=5 each (seeds 31-35; the mixed deepseek, qw38, gemma market has gemma as firm C). Clone: -0.207 (-0.407, -0.062), -0.222 (-0.349, -0.102), -0.325 (-0.355, -0.295), -0.170 (-0.271, -0.069), -0.605 (-0.730, -0.428). The gemma interval depends on the bootstrap seed (upper end between -0.012 and -0.062) because 3 of 9 runs sit near -0.6; the point estimate is stable. The cut alone, without a swap, changes CI by 0.000 (gemma), -0.051 (deepseek) and -0.003 (glm53f).

## Appendix

**Figure A1 (fig_g_gate_comm.png). Gate with messages on and off.** Share of finished 30-round base runs with CI(16-30) >= 0.5. Messages on: gemma 9 of 10, deepseek 10 of 10, glm53f 10 of 10. Messages off from round 1: gemma 1 of 5 (seeds 21-25), deepseek 0 of 10 (seeds 21-30), glm53f 1 of 5 (seeds 21-25). Different seeds on and off, so the comparison is descriptive.

**Figure A2 (fig_h_heatmap.png). All effects.** 22 conditions by 4 models, headline pooling for the standard, announced and comm-cut rows (data/main, qwen, glm); history none, history last round, notes and known end are separate base runs, seeds 21-25, with the gate applied to each group's own base runs. n is printed in each cell; blank = not run. Same numbers as `RESULTS_TABLE.md` Tables 1 and 3.

**Figure A3 (fig_i_newcomers.png). LLM newcomers.** An LLM firm with one instruction variant (myopic, share, no-collude, own-price, deceptive) replaces firm C with the history wiped. Headline pooling, gated runs with finished branches: gemma n=5 per variant (seeds 11, 13-16), deepseek n=5, glm53f n=5 for myopic and n=4 for the others (the hosted credit ran out in seed 25; 21 of 25 branches finished). Effects: FINDINGS item 11.

**Figure A4 (fig_k_entry.png). Entry of new firms.** New firms join at round 31 without the history. Gemma, deepseek and glm53f: one or two new firms of the same model; gemma only: one new qwen3-14b firm (a different family) and one new scripted undercutter. n=5 (seeds 11, 13-16 for gemma and deepseek, 21-25 for glm53f). The figure uses CI over rounds 31-60. Gemma entrants, rounds 31-60 and rounds 46-60: qwen3-14b -0.007 and +0.000; scripted undercutter -0.027 (-0.037, -0.019) and -0.036 (-0.052, -0.023).

**Figure A5 (fig_j_awareness.png). Awareness probe.** After the branch, each firm that was not replaced is asked once whether any firm was replaced since round 30; a reply that starts with yes counts. Yes of asked: no swap gemma 0/15, deepseek 1/15, glm53f 0/15; clone 0/10, 1/10, 0/10; undercutter k=1 0/10, 5/10, 0/10. Headline pooling, gated runs. The reply is cheap talk (a message), not a price.

**Figure A6 (fig_l_temperature.png). Temperature.** No-swap CI and the undercutter k=1 effect at sampling temperature 0.3, 0.7 (frozen value) and 1.0, seeds 11, 13, 14 only (the 0.7 point uses the same seeds). Dots are gated runs, lines are means. Gated runs with a finished undercutter branch: gemma 3, 3, 3; deepseek 2, 3, 3 (0.3, 0.7, 1.0). Three runs per point: descriptive. The hosted endpoint ignores the seed, so the deepseek seed match is nominal.

**Figure A7 (fig_m_mixed_eight.png). Mixed and eight-firm markets.** Left: per-run base CI (rounds 16-30) and no-swap CI (rounds 31-60); hollow = fails the gate. Right: per-run effects (dots) and the mean of gated runs (bars). Mixed deepseek, qw38, glm53f and mixed deepseek, qw38, gemma: seeds 31-35, 5 of 5 gated each. Eight firms (two copies each of four models): seeds 51-53, 1 of 3 base runs gated in each variant.

**Figure A8 (fig_n_known_end.png). Known end date.** Mean price in rounds 31-50 against 51-60 in the no-swap branch where the prompt states that the game lasts exactly 60 rounds; grey = runs, red = mean over gated runs. Seeds 21-25. Gated n: gemma 2 (the cell fails the 60% gate), deepseek 5, qw38 5, glm53f 5.

**Figure A9 (fig_d_firms.png). Number of firms.** Base-run CI over rounds 16-30 by number of identical firms; dots = seeds; dashed line = gate 0.5. Gemma and deepseek: 2, 4 and 5 firms use seeds 41 and 42 (n=2 each), 3 firms use the main-study seeds 11-20 (n=10). The gate is not applied here.

**Figure A10 (fig_e_horizon.png). Longer horizon.** CI per window (16-30, 31-60, 61-90, 91-120), no swap against undercutter k=1; thin lines = single runs (faint dotted = fails the gate), thick = mean of gated runs. Gemma seeds 11-15 (seed 12 fails the gate; n=4 gated); deepseek seeds 11, 13, 14 (n=3).

**Figure A11 (fig_o_per_seed.png). Seed-to-seed variation.** gemma4-12b, data/main, all ten seeds 11-20, no swap against undercutter k=1; the gate is not applied (seed 12 fails it and is marked in its title). Shows the spread behind the narrow gemma intervals.

**Figure A12 (fig_p_message_volume.png). Message length.** Mean words per message in each round (three firms averaged) over the base run and the no-swap branch; thin lines = gated runs, thick = mean. Gemma n=9, deepseek n=10 (data/main).
