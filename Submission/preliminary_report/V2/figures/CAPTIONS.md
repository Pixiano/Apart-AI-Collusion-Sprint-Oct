Model key (names used in every plot)
- Gemma = gemma4-12b (local, 12B)
- DeepSeek = DeepSeek V4.1 Flash (hosted)
- Qwen = Qwen3.8-2.4T-A95B (hosted, label qw38)
- GLM = GLM-5.3-Flash (hosted, label glm53f)

# Figure captions (V2 draft; the author rewrites)

Scripts: `make_figures.py` (figures a to e, `../RESULTS_TABLE.md`) and `make_figures2.py` (figures f to p). Run from the repo root with `.venv/Scripts/python.exe -I Submission/preliminary_report/V2/figures/<script>`. They read `data/` only and write the PNGs here.

Plain words used in plots. Collusion index = (average price - 10) / 45, averaged over all firms and the rounds of a block: 0 is the competitive price 10, 1 is the monopoly price 55. A run "formed a cartel" if its collusion index over rounds 16-30 is at least 0.5 (the "gate"); all effects use only such runs, and a model is analysed only if at least 60% of its runs did. "Effect" = collusion index over rounds 31-60 of a branch minus that of the same run's no-swap branch (when messages are cut, compared with the no-swap branch with messages also cut); bars show the average over runs, whiskers the 95% bootstrap interval over runs (10000 resamples, seed 0). Narrow whiskers (Gemma, Qwen) come from near-identical runs and understate the uncertainty. "Fresh copy" = a new firm of the same model with its history wiped (clone). "Other model" = a firm from another model family (family). "Scripted undercutter" = a rule that prices one cent below the lowest price of the last round. "1 / 2 firms replaced" = how many of the three firms are swapped at round 31. Pooling (unless stated): Gemma seeds 11-20 (10 runs, 9 formed a cartel), DeepSeek seeds 11-20 (10 of 10), Qwen seeds 21-25 (5 of 5), GLM seeds 21-30 (10 of 10); the all-seeds pooling appears only in `RESULTS_TABLE.md` Table 2; Gemma seed 31 (unfinished) is never used.

## Main text

**Figure 1 (fig_f_design.png). Study design: one base run, then branches from a checkpoint.** A base run of three firms of one model (rounds 1-30, messages and full history) is saved at round 30. From that checkpoint, branches replay rounds 31-60: no swap, a fresh copy, another model, or a scripted undercutter, with 1 or 2 firms replaced. The note under the diagram lists the other tests. No data.

**Figure 2 (fig_a_price_per_round.png). Average price in each round, by model.** One panel per model, runs that formed a cartel only: Gemma 9, DeepSeek 10, Qwen 5, GLM 10 (n of each branch is the same unless a branch is unfinished). Lines are the average over runs; the shaded bands run from the lowest to the highest run for no swap and for 1 scripted undercutter (before round 31, over all runs). The dotted vertical line is the swap after round 30; grey horizontal lines are the competitive price 10 and the monopoly price 55. GLM starts high because some runs open far above 55 (a three-firm average of up to 89 in round 1, average over runs about 64).

**Figure 3 (fig_b_effects.png). Effect of replacing firms on the collusion index.** Same runs as Figure 2 (9, 10, 5, 10). Bars are the average change in collusion index over rounds 31-60 compared with no swap, with 95% intervals; the value is printed on each bar; a black diamond marks an effect within 0.0015 of zero. Exploratory cells are not in this figure.

**Figure 4 (fig_c_comm_cut.png). Replacing one firm when messages are cut.** Messages are on in rounds 1-30 and off from round 31. Bars compare with the no-swap branch with messages also cut, so the cut itself is removed; n is printed under each bar. Runs that formed a cartel: Gemma 9, DeepSeek 10, GLM 5 (cut cells exist for seeds 21-25 only), the two mixed markets 5 each (seeds 31-35; the second mixed market has Gemma as firm C). Fresh copy: -0.207 (-0.407, -0.062), -0.222 (-0.349, -0.102), -0.325 (-0.355, -0.295), -0.170 (-0.271, -0.069), -0.605 (-0.730, -0.428). The Gemma interval depends on the bootstrap seed (upper end between -0.012 and -0.062) because 3 of 9 runs sit near -0.6; the average is stable. The cut alone, without a swap, changes the index by 0.000 (Gemma), -0.051 (DeepSeek) and -0.003 (GLM).

## Appendix

**Figure A1 (fig_g_gate_comm.png). Cartels with messages on and off.** Share of finished 30-round base runs that formed a cartel. Messages on: Gemma 9 of 10, DeepSeek 10 of 10, GLM 10 of 10. Messages off from round 1: Gemma 1 of 5 (seeds 21-25), DeepSeek 0 of 10 (seeds 21-30), GLM 1 of 5 (seeds 21-25). Different seeds on and off, so the comparison is descriptive.

**Figure A2 (fig_h_heatmap.png). Change in collusion index when firms are replaced.** 22 conditions by 4 models; each cell is the average effect (as defined above) with n below it; blank = not run. The first eight rows use the standard pooling (swap announced and messages cut included). "No history" (firms see no past prices), "Last round only", "With notes" and "Known end date" are separate base runs, seeds 21-25, with runs that formed a cartel chosen within each group. Same numbers as `RESULTS_TABLE.md` Tables 1 and 3.

**Figure A3 (fig_i_newcomers.png). Effect of replacing one firm with a new AI firm.** An AI firm with one of five instructions (short-sighted = myopic, share the market, never collude, own price only, deceptive) replaces firm C with its history wiped. Runs that formed a cartel and finished: Gemma n=5 per instruction (seeds 11, 13-16), DeepSeek n=5, GLM n=5 for short-sighted and n=4 for the others (the hosted credit ran out in seed 25; 21 of 25 branches finished). n is printed under each bar; whiskers are 95% intervals. Effects: FINDINGS item 11.

**Figure A4 (fig_k_entry.png). Effect of new firms joining at round 31.** New firms join without the history. Gemma, DeepSeek and GLM: 1 or 2 new firms of the same model; Gemma only: 1 new firm of another model (qwen3-14b) and 1 new scripted undercutter. n=5 (seeds 11, 13-16 for Gemma and DeepSeek, 21-25 for GLM). Gemma entrants, rounds 31-60 and rounds 46-60: other model -0.007 and +0.000; scripted undercutter -0.027 (-0.037, -0.019) and -0.036 (-0.052, -0.023).

**Figure A5 (fig_j_awareness.png). Do firms notice that a firm was replaced?** After the branch, each firm that was not replaced is asked once whether any firm was replaced since round 30; a reply starting with yes counts. Yes of asked, no swap: Gemma 0/15, DeepSeek 1/15, GLM 0/15; fresh copy 0/10, 1/10, 0/10; scripted undercutter 0/10, 5/10, 0/10. Runs that formed a cartel. The reply is cheap talk (a message), not a price.

**Figure A6 (fig_l_temperature.png). Collusion index at three temperatures.** Left: no-swap collusion index over rounds 31-60; right: change when 1 firm is replaced by a scripted undercutter. Temperature 0.3, 0.7 (the frozen value) and 1.0, seeds 11, 13, 14 only (the 0.7 point uses the same seeds). Dots are single runs that formed a cartel, lines the average. Runs with a finished undercutter branch: Gemma 3, 3, 3; DeepSeek 2, 3, 3 (0.3, 0.7, 1.0). Three runs per point: descriptive. The hosted endpoint ignores the seed, so the DeepSeek seed match is nominal.

**Figure A7 (fig_m_mixed_eight.png). Mixed-model and eight-firm markets.** Left: collusion index of each run in rounds 16-30 (circles) and rounds 31-60 without a swap (squares); hollow = no cartel formed; dashed line = 0.5. Right: change in collusion index for each run (dots, hollow = no cartel formed) and the average of runs that formed a cartel (bars). The two mixed markets (DeepSeek, Qwen and GLM; DeepSeek, Qwen and Gemma): seeds 31-35, 5 of 5 formed a cartel. Eight firms (two copies each of four models): seeds 51-53, 1 of 3 runs formed a cartel in each variant.

**Figure A8 (fig_n_known_end.png). Prices when firms are told the game ends at round 60.** Average price in rounds 31-50 against rounds 51-60 in the no-swap branch; grey = each run, red = average. Seeds 21-25; runs that formed a cartel: Gemma 2 (this cell fails the 60% rule), DeepSeek 5, Qwen 5, GLM 5.

**Figure A9 (fig_d_firms.png). Collusion index by number of firms.** Base-run collusion index over rounds 16-30 by number of identical firms; bars = average, dots = single runs; dashed line = 0.5. For both models, 2, 4 and 5 firms use seeds 41 and 42 (n=2 each) and 3 firms use the main-study seeds 11-20 (n=10). Runs are not filtered by the 0.5 rule here.

**Figure A10 (fig_e_horizon.png). Collusion index in a game of up to 120 rounds.** Collusion index in four blocks (rounds 16-30, 31-60, 61-90, 91-120), no swap against 1 scripted undercutter; thin lines = single runs (faint dotted = no cartel formed), thick = average of runs that formed a cartel. Gemma seeds 11-15 (seed 12 formed no cartel; n=4); DeepSeek seeds 11, 13, 14 (n=3).

**Figure A11 (fig_o_per_seed.png). Gemma: price in each of the ten runs.** Average price per round, no swap against 1 scripted undercutter, seeds 11-20 (titled Run 11 to Run 20). All runs shown; run 12 formed no cartel and is marked. The dotted line is the swap after round 30; grey lines are prices 10 and 55. Shows the spread behind the narrow Gemma intervals.

**Figure A12 (fig_p_message_volume.png). How long the firms' messages are, round by round.** Average words per message in each round (three firms averaged) over the base run and the no-swap branch; thin lines = single runs, thick = average. Gemma n=9, DeepSeek n=10 (runs that formed a cartel).
