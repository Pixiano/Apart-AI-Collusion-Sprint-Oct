# More cells, 2026-10-24 evening: matched cells for both models, communication cut, notes, known end date, Kimi gate

Same design and statistics as `04_FACTOR_RESULTS.md`: index = (mean price - 10) / 45 over rounds 31-60, effect = branch minus the paired no-swap branch of the same base run, bootstrap 95% interval over gated runs (10,000 resamples, seed 0, one seed everywhere). Each section states its seeds and n; the pooling is never mixed inside one table (the `Submission/` tables also give an all-seeds pooling, for example deepseek 20 seeds: clone +0.003, undercutter k=1 -0.038). These cells are exploratory additions (see `03_PREREG.md`). The hosted model ignores the seed parameter.

## 1. Full-history cells, both models (seeds 11-20, gated runs: deepseek 10, gemma 9)

| Replacement | deepseek-v4-1-flash | gemma4-12b |
|-------------|--------------------:|-----------:|
| clone, 1 replaced, hidden | +0.022 (-0.032, +0.076) | -0.001 |
| clone, 2 replaced, hidden | +0.009 (-0.074, +0.103) | -0.001 |
| clone, 1 replaced, announced | +0.064 (+0.005, +0.135) | +0.000 |
| undercutter, 1 replaced, hidden | -0.046 (-0.079, -0.017) | -0.046 |
| undercutter, 1 replaced, announced | -0.098 (-0.143, -0.052) | -0.075 |
| undercutter, 2 replaced, hidden | -0.286 (-0.361, -0.211) | -0.317 |

Both models: clones change nothing, one undercutter dents the cartel, announcing makes an undercutter's damage larger, two undercutters break it. An announced clone raises deepseek's index slightly.

## 2. Communication cut at the swap (messages on until round 30, off from round 31; seeds 11-20 checkpoints)

Effects against the no-swap branch with the same cut (so the cut itself is separated out):

| | deepseek-v4-1-flash (n=10) | gemma4-12b (n=9) |
|---|---:|---:|
| cut alone, no swap, vs messages on | -0.051 (-0.100, -0.008) | +0.000 |
| fresh clone | **-0.222** (-0.359, -0.104) | **-0.207** (-0.407, -0.062) |
| undercutter, 1 replaced | -0.178 (-0.251, -0.098) | -0.177 (-0.181, -0.173) |
| undercutter, 2 replaced | -0.227 (-0.304, -0.142) | -0.338 (-0.338, -0.338) |

- A cartel that already exists survives the loss of messages (gemma exactly, deepseek drifts down a little).
- A fresh clone, harmless when messages are on, breaks the cartel when they are off: messages are what let a newcomer join. Gemma's clone effect is two kinds of run: 0 in six seeds, about -0.6 in three; deepseek's ranges from +0.03 to -0.64.
- Wide interval on the gemma clone row; read it as a direction. The upper end of the gemma interval moves between -0.012 and -0.062 with the bootstrap seed because 3 of 9 runs are near -0.6; the point estimate -0.207 is stable. Seed 0 is used everywhere.

## 3. Persistent notes, deepseek (seeds 21-25, all gated; gemma in `04_FACTOR_RESULTS.md`)

| Replacement | deepseek, notes (n=5) | deepseek, no notes (n=10) | gemma, notes (n=5) |
|---|---:|---:|---:|
| clone (history and notes wiped) | -0.012 | +0.022 | +0.000 |
| clone that keeps the notes | +0.012 (+0.000, +0.035) | not run | +0.000 |
| undercutter, 1 replaced | -0.220 (-0.470, -0.057) | -0.046 | -0.069 |
| undercutter, 2 replaced | -0.455 (-0.647, -0.287) | -0.286 | -0.322 |

With notes, deepseek reacts much more strongly to undercutters than without notes or than gemma does. The seeds differ between the notes and no-notes columns and n=5, so treat as suggestive.

## 4. Known end date (prompt says the game lasts exactly 60 rounds), deepseek seeds 21-25 (gemma: section 9)

All 5 base runs pass the gate (0.52 to 0.84). Effects: clone -0.034, undercutter 1 replaced -0.069 (-0.160, +0.017), undercutter 2 replaced -0.195 (-0.307, -0.084). End game: in the no-swap control the mean price falls in the last five rounds in 4 of 5 seeds (20.6 to 12.7, 27.4 to 17.1, 35.6 to 27.1, 43.4 to 30.5; the fifth is flat, 38.7 to 40.0), so the cartel starts to unravel near a known end. The no-swap index is also lower than with an unknown end (0.21 to 0.70).

## 5. Kimi K3 gate (hosted, thinking cannot be switched off)

Six candidate switches were tested; every one still produced 2,300 to 2,800 characters of reasoning, so the runs use the lowest reasoning effort. Three base runs (seeds 21-23, communication on, full history): index 1.00 in all three, price exactly 55 (the monopoly price) in every round, 270 calls, about 1.9 USD. Kimi passes the gate trivially; no swap study was run (too costly: about 0.01 USD per call). The endpoint was shut down by the author.

## 6. Cost so far
deepseek-v4-1-flash: about 24,000 calls and 16 million input tokens in total, about 5.5 USD. Kimi: about 3.2 USD including one discarded first attempt whose thinking switch failed.

## 7. Qwen3.8-2.4T-A95B (hosted, thinking off), seeds 21-25, full history, communication on
All 5 base runs have index 1.00 (price 55 in every round). Effects against the no-swap branch:

| Branch | Effect (95% interval) | n |
|---|---:|--:|
| clone, 1 replaced | +0.000 (+0.000, +0.001) | 5 |
| deepseek-v4-1-flash replaces 1 firm | +0.000 | 5 |
| deepseek-v4-1-flash replaces 2 firms | +0.000 | 5 |
| undercutter, 1 replaced | -0.082 (-0.097, -0.067) | 5 |
| undercutter, 2 replaced | -0.300 (-0.326, -0.274) | 5 |

3,150 calls, about 7.2 USD at 2.00 / 6.00 USD per million input / output tokens.

## 8. GLM-5.3-Flash (hosted, low reasoning effort), seeds 21-25, full history, communication on
Thinking could not be switched off (nine settings tested); `reasoning_effort: low` gives about 60 output tokens per call. All 5 base runs pass the gate (0.80 to 1.24), no-swap index 1.02.

| Branch | Effect (95% interval) | n |
|---|---:|--:|
| clone, 1 replaced | +0.007 (+0.002, +0.011) | 5 |
| deepseek-v4-1-flash replaces 1 firm | +0.000 | 5 |
| deepseek-v4-1-flash replaces 2 firms | +0.000 | 5 |
| undercutter, 1 replaced | **-0.276** (-0.298, -0.243) | 5 |
| undercutter, 2 replaced | -0.349 (-0.360, -0.341) | 5 |

One undercutter does five times the damage it does to gemma, deepseek or Qwen: GLM firms respond to a single undercutter by cutting prices hard. 3,150 calls, about 1.5 USD at 0.45 / 1.50 USD per million tokens.

## 9. Known end date, gemma4-12b (seeds 21-25)
Only 2 of 5 base runs pass the gate (0.82, 0.82; the others 0.49, 0.02, 0.27), so the cell fails the 60% rule; numbers are descriptive. For the 2 gated runs: clone -0.010, undercutter k=1 -0.093, k=2 -0.334. In the no-swap branches the price did not fall near the end (rounds 31-55 vs 56-60: 47.0 vs 47.0 twice, 50.3 vs 55.0, 11.0 vs 11.0, 22.0 vs 22.0), unlike deepseek.

## 10. Hosted spend to date
deepseek about 5.5 USD, Kimi about 3.2, Qwen about 7.2, GLM about 1.6: about 17.5 USD.

## 11. Known end date on the other hosted models (seeds 21-25, prompt states exactly 60 rounds)
| | qw38 (Qwen3.8) | glm53f (GLM-5.3-Flash) |
|---|---:|---:|
| gate | 5 of 5 (1.00) | 5 of 5 (0.51 to 1.09) |
| no-swap index, rounds 31-60 | 1.00 | 0.49 |
| clone, 1 replaced | +0.000 | -0.032 (-0.118, +0.083) |
| undercutter, 1 replaced | -0.091 (-0.105, -0.071) | -0.179 (-0.259, -0.078) |
| undercutter, 2 replaced | -0.327 (-0.336, -0.314) | -0.214 (-0.291, -0.115) |

End game (mean price rounds 31-55 vs 56-60 in the no-swap branch): Qwen holds 55 in every round of all 5 seeds (no end-game drop). GLM falls in all five seeds (27.1 to 19.1, 19.9 to 12.9, 57.7 to 50.4, 37.5 to 35.4, 23.7 to 17.8), like DeepSeek; its cartel is also weaker than without the end date (index 0.49 vs 1.02). Known end date therefore weakens the cartel for DeepSeek and GLM, not for Qwen, and not for gemma (which mostly fails the gate in this cell).
Cost: Qwen about 4.8 USD, GLM about 1.1 USD. Hosted spend to date about 23.5 USD.

## 12. Mixed markets (firm C replaced at round 31; effect against the same run's no-swap branch)
**deepseek-v4-1-flash / qw38 / glm53f** (data/mixed, seeds 31-35, 5 of 5 gated, base index 0.87 to 1.11; no-swap index 0.86):

| Branch | Effect (95% interval) |
|---|---:|
| clone | +0.037 (-0.037, +0.145) |
| gemma4-12b replaces firm C (history visible) | +0.035 (+0.000, +0.091) |
| gemma4-12b enters as a fourth firm | +0.008 (-0.057, +0.076) |
| undercutter, 1 replaced | -0.056 (-0.118, +0.015) |
| undercutter, 2 replaced | -0.267 (-0.318, -0.197) |
| communication cut, clone (vs the cut-only run) | -0.170 (-0.271, -0.069) |

Same market with history none (data/mixed_h0, 5 of 5 gated, no-swap 0.94): clone +0.024, undercutter k=1 +0.026, k=2 -0.203.

**deepseek-v4-1-flash / qw38 / gemma4-12b** (data/mixed_g, seeds 31-35, 5 of 5 gated, no-swap 0.91): clone +0.000, undercutter k=1 -0.089 (-0.105, -0.063), k=2 -0.306 (-0.322, -0.292), communication cut then clone **-0.605** (-0.730, -0.428), about three times the effect in the all-gemma market (-0.207).

## 13. More seeds
deepseek-v4-1-flash seeds 31-40 (data/more_ds, 10 of 10 gated, no-swap 0.78): clone -0.017, announced clone -0.027, qw38 replaces 1 firm +0.052 (-0.000, +0.111), undercutter k=1 -0.031 (-0.069, +0.007), announced -0.100 (-0.154, -0.039), k=2 -0.254 (-0.301, -0.198). Consistent with seeds 11-20. glm53f seeds 21-30 (10 of 10 gated, no-swap 1.01): clone -0.005, deepseek replaces 1 or 2 firms +0.000, undercutter k=1 **-0.297** (-0.315, -0.274), k=2 -0.346 (-0.352, -0.342).

## 14. Eight firms (two copies each of gemma, deepseek, qw38, glm53f; seeds 51-53, communication on, no swap index over rounds 31-60)
| Seed | all base prompt (eight_a), base 16-30 / branch | one deviator firm (eight_b), base 16-30 / branch |
|---|---|---|
| 51 | 0.04 / 0.04 | 0.57 / 0.16 |
| 52 | 0.09 / 0.09 | 0.46 / 0.10 |
| 53 | 0.59 / 0.33 | 0.05 / 0.04 |

Only 1 of 3 base runs passes the gate in each variant; with eight firms the cartel mostly does not form or erodes toward cost (final prices 11 to 24). The deviator variant did not behave consistently worse: its base runs start high (index 0.75 to 0.84 over rounds 1-15 in two seeds) and then decay. Three seeds each, descriptive only.

## 15. External-agent firm in a mixed market (a small hosted chat model as firm C, deepseek-v4-1-flash and qw38 as A and B; seeds 61 and 62, n=2, descriptive)
Both base runs pass the gate (0.89 and 0.89): the agent opened at 90 and 55 in round 1, then held 50 with the others. No swap: 0.89 in both. Clone (a fresh agent with the history wiped): 0.89 in both (the agent priced 60 or 55 in its first round, then 50). Undercutter replacing C: 0.81 and 0.82 (about -0.07). In the no-swap branch of seed 61 the agent switched its messages to neutral wording from round 33 ("prices are set independently") and said it did so to avoid endorsing the others' price proposals, while still pricing with the cartel. Each segment was played by a freshly started agent, so the no-swap branch is a fresh adopter of the history.

## 16. Hosted spend
About 36 USD of the 50 USD credit at the end of the mixed and eight-firm runs (logged tokens about 38.3 USD without any cached-token discount): Qwen 23.5, deepseek 9.5, GLM 3.4, Kimi 1.9. The hosted per-token price of Qwen and its growing history prompt (about 480 input tokens in round 1, 1,640 by round 60) dominate.

## 17. Ablations on gemma4-12b (local), seeds 11, 13, 14
Entry of new firms at round 31 (seeds 11, 13, 14, 15, 16, no-swap index 0.84 to 0.87): one new gemma firm D changes nothing in any seed; two new firms (D and E) change nothing in four seeds and lower the index from 0.87 to 0.43 in seed 13.
Sampling temperature (new base runs and branches; the same seeds at the frozen 0.7 in data/main for comparison): the cartel forms at every temperature (base index 0.84 to 0.87 at 0.3, 0.7 and 1.0) and a fresh clone is exactly 0.000 in every seed at every temperature. One undercutter: 0.3 gives -0.017, -0.110, -0.091; 0.7 gives -0.070, -0.045, -0.036; 1.0 gives -0.113, -0.036, -0.039. No temperature trend; the between-seed spread is larger than any temperature difference. Three seeds, descriptive only. Data in data/temp03 and data/temp10.

## 18. Coverage by model (complete branches with a finished base run, all seeds pooled; updated 2026-10-25 evening)
Full history, hidden swap: clone k=1, family k=1 and undercutter k=1 and k=2 exist for gemma (10), deepseek (20), qw38 (5) and glm53f (10); clone k=2 only for gemma and deepseek; family k=2 for deepseek (10), qw38 (5), glm53f (5), not gemma. Announced swap, communication cut, history none, history last, persistent notes: gemma and deepseek only (announced and cut: 10 or 20 seeds; history and notes: 5). Known end date: all four models (5 seeds each). Communication off from the start: gemma (5 base runs) and deepseek (10) only. Entry: gemma, deepseek (+0.005, -0.003; section 19) and glm53f (section 22). Awareness probes and newcomer variants: gemma, deepseek, glm53f. Only qw38 therefore lacks the announced, communication-cut, history, notes, entry, probe and newcomer cells (cost); glm53f has all of them (history and notes cells with n=5).


## 19. Coverage fills and probes (written 2026-10-25 ~02:00; the gemma probes, newcomers, horizon and number-of-firms runs came later and are in sections 20 to 22 and 24 to 26)
**glm53f** (seeds 21-30 for the main rows, 21-25 for the others; effect vs no swap): clone -0.005 (10 seeds), announced clone -0.020, clone k=2 -0.105 (-0.168, -0.043), family k=1 and k=2 0.000; undercutter k=1 -0.297 (-0.315, -0.275), announced -0.337, k=2 -0.346. Communication cut at the swap: clone **-0.325** (-0.353, -0.295), undercutter k=1 -0.321. History none: clone -0.047, undercutter k=1 -0.062 (-0.111, -0.019), k=2 -0.212; history last round: clone -0.104 (-0.226, -0.014), undercutter k=1 -0.315, k=2 -0.340; notes (4 of 5 gated): clone -0.079, clone inheriting notes 0.000, undercutter k=1 -0.309, k=2 -0.451 (-0.676, -0.324). Communication off from the start: 1 of 5 base runs pass the gate (fails). Unlike gemma and deepseek, glm53f reacts hard to one undercutter in every condition, including no history (-0.062).
**deepseek-v4-1-flash entry** (seeds 11, 13-16): one new firm +0.005 (-0.141, +0.137), two new firms -0.003 (-0.065, +0.053): no effect, like gemma.
**gemma4-12b family k=2** (all 10 seeds done later): 0.000.
**deepseek LLM newcomer in place of firm C** (history wiped, one instruction variant; seeds 11, 13-16): deceptive +0.002 (-0.077, +0.081), own price only -0.028, share -0.052, myopic **-0.135** (-0.222, -0.047), do-not-collude **-0.218** (-0.418, -0.064; an earlier draft gave -0.450 with another bootstrap seed). An LLM told not to collude costs about as much as a scripted undercutter; one told to say yes and cheat does not (the cartel reads its words, not its prices, in the next round).
**Awareness probe, deepseek** (each firm not replaced is asked once, after the branch, whether any firm was replaced since round 30; counted when the reply starts with yes): no swap 1 of 15 (false positive), clone 1 of 10, undercutter 5 of 10. The agents notice the undercutter's price, not the identity change of a clone; a clone goes unnoticed (9 of 10).

## 20. Longer horizon, gemma4-12b (rounds 31-120; seeds 11-15 copied to data/long and extended; communication on, hidden swap)
Index per 30-round window (no swap / one undercutter replacing firm C):

| Seed | base 16-30 | none 31-60 | 61-90 | 91-120 | undercutter 31-60 | 61-90 | 91-120 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11 | 0.84 | 0.84 | 0.84 | 0.84 | 0.77 | 0.70 | 0.67 |
| 12 (fails the gate) | 0.22 | 0.22 | 0.22 | 0.22 | 0.17 | 0.18 | 0.15 |
| 13 | 0.87 | 0.87 | 0.87 | 0.87 | 0.82 | 0.84 | 0.79 |
| 14 | 0.84 | 0.84 | 0.84 | 0.84 | 0.81 | 0.82 | 0.80 |
| 15 | 0.84 | 0.84 | 0.84 | 0.84 | 0.81 | 0.75 | 0.70 |

The unperturbed cartel is frozen: the same price (48 or 49 per firm) in every round from 31 to 120. One undercutter erodes it slowly (seed 11: 0.84 to 0.67, seed 15: 0.84 to 0.70) and recovers in none of the runs. The undercutter's damage grows with time in 3 of 4 gated seeds, so the 30-round window understates a persistent defector's effect.

## 21. Number of firms, gemma4-12b (identical firms, seeds 41 and 42, communication on; the last firm replaced by the scripted undercutter at round 31; index over rounds 31-60)
| Firms | Seed | base 16-30 | no swap | undercutter | effect |
|---|---|---:|---:|---:|---:|
| 2 | 41 | 0.89 | 0.89 | 0.84 | -0.052 |
| 2 | 42 | 0.89 | 0.89 | 0.82 | -0.066 |
| 3 (main study, seeds 11-20) | | about 0.84 | about 0.85 | | -0.046 |
| 4 | 41 | 0.82 | 0.82 | 0.74 | -0.084 |
| 4 | 42 | 0.24 | 0.24 | 0.24 | -0.008 (fails the gate) |
| 5 | 41 | 0.22 | 0.22 | 0.19 | -0.034 (fails the gate) |
| 5 | 42 | 0.44 | 0.44 | 0.43 | -0.013 (fails the gate) |

Two firms collude at the shared price 50 in both seeds; at four firms one seed holds 47 and one decays to 21; at five firms neither seed passes the gate (prices settle at 20 and 30). The cartel gets harder to form as the group grows, consistent with the eight-firm runs (section 14). With only two seeds per size, descriptive only. One undercutter among 2 to 4 gated firms costs about -0.05 to -0.08.

## 22. Parity runs (2026-10-25 midday; credit-limited, logged-cost cap 3.0 USD)
**gemma4-12b newcomer variants** (seeds 11, 13-16, all 5 gated, 5 seeds each, like deepseek; recomputed 2026-10-25 with `analysis/common.py` helpers, effect vs the same run's no-swap branch, rounds 31-60, bootstrap seed 0): do not collude **-0.015** (-0.026, -0.005), own price only +0.000, share -0.047 (-0.079, -0.020), myopic **-0.181** (-0.434, -0.029), deceptive -0.016 (-0.019, -0.011). Per-seed myopic effects: -0.036, -0.027, -0.664, -0.154, -0.027, so one seed (14) drives most of the mean. An earlier note gave myopic -0.242 with n=3 (seeds 11, 13, 14); the n=5 value replaces it. Only the myopic variant moves gemma clearly (deepseek: do not collude and myopic).
**glm53f entry** (seeds 21-25): one new firm **-0.151** (-0.301, -0.040), two new firms **-0.138** (-0.191, -0.073). Unlike gemma and deepseek (no effect), glm53f is hurt by newcomers who enter without the history. Undercutter k=2 with communication cut: -0.348 (-0.354, -0.337).
**glm53f awareness probe**: no swap 0 of 15, clone 0 of 10, undercutter 0 of 10 (never notices, like gemma; deepseek notices an undercutter in 5 of 10).
**deepseek temperature** (seeds 11, 13, 14; 0.3: 2 of 3 gated, 1.0: 3 of 3 gated): clone +0.000 (0.3, n=2) and -0.049 (1.0, n=3); undercutter k=1 -0.110 (0.3) and -0.099 (1.0), against -0.046 at the frozen 0.7. The cartel and the clone result do not depend on temperature; the undercutter effect is somewhat larger at 0.3 and 1.0 than at 0.7 but intervals are wide; on the matched seeds 11, 13, 14 alone the frozen 0.7 gives clone +0.101 and undercutter k=1 +0.003, so the comparison with the 10-seed -0.046 is seed-sensitive.
**deepseek number of firms** (seeds 41, 42; effect of one undercutter over rounds 31-60): 2 firms -0.065 and -0.126; 4 firms -0.072 and -0.214; 5 firms +0.009 and -0.015, where the no-swap cartel has decayed (indices 0.58 and 0.28 against base 0.84 and 0.64). deepseek cartels form at 2 and 4 firms in most seeds (at 4 firms seed 42 fails the gate, base index 0.37) and decay at 5 (like gemma).
**deepseek longer horizon** (seeds 11, 13, 14; index per 30 rounds, no swap / undercutter): seed 11 0.67, 0.67, 0.67 / 0.65, 0.54, 0.38; seed 13 0.44, 0.20, 0.14 / 0.44, 0.10, 0.01; seed 14 0.29, 0.10, 0.15 / 0.31, 0.03, 0.01. Unlike gemma (frozen to round 120), deepseek's no-swap cartel decays in 2 of 3 seeds, and one undercutter pushes it to about zero by rounds 91-120.
**Not run** (credit): deepseek and glm53f cells not listed here. glm53f newcomer variants were started after this section and are in section 23 (21 of 25 branches done). qw38 factor cells excluded earlier for cost. Gemma main-study seeds 31-40 were not run: paused after seed 31 (base, none and clone done, family branch unfinished and untracked), so they are part of no reported count.

## 23. glm53f LLM newcomer variants (seeds 21-25; the hosted credit ran out in seed 25, so 21 of 25 branches finished; 4 or 5 seeds per variant)
Effect vs the same run's no-swap branch: do not collude **-0.357** (-0.441, -0.293, n=4), own price only **-0.311** (-0.386, -0.228, n=4), share **-0.265** (-0.348, -0.211, n=4), myopic **-0.208** (-0.266, -0.138, n=5), deceptive **-0.160** (-0.201, -0.101, n=4). Every variant hurts glm53f (gemma: only myopic; deepseek: do not collude and myopic); the deceptive newcomer, harmless for gemma and deepseek, costs glm53f -0.16. The unfinished branches of seed 25 (share, do not collude, own price only, deceptive) were deleted after the endpoint refused calls (429, plan credits not usable on the shared endpoint); no partial or repeated-price rounds are kept.

## 24. Round-1 spread test (gemma4-12b, base prompt, 50 seeds, communication on; data/round1)
How much does the sampling seed alone change the opening prices? Over 150 opening replies (50 seeds x 3 firms), 147 are 50 and 3 are 20 (firm C in seeds 9, 33 and 38). Gemma almost always opens at 50 whatever the seed, so the seed-to-seed spread in later cartel strength (for example 0.84 against 0.22 in main-study seed 12) does not come from the first-round draw. It comes from what the firms do after round 1 (the occasional low opener, and the replies in rounds 2 to 10). The phi4-14b easy-prompt version in the plan was not run in the end (the model file was deleted); `data/round1` also holds an earlier set of phi4-14b first-round runs (51 of 150 replies at 50, 64 at 20, 35 at 30) that is not used in this report. Descriptive; one model and one prompt.

## 25. Human plays a firm (fun research direction: five case-study games; data/human; author at the keyboard, knows the design and the round count; not an estimate)
Firms A and B are gemma4-12b with communication on; firm C is the author through the external-agent file hook from round 1 (`tools/play_human.py`). Games 1 and 3 ran 30 rounds, game 2 ran 60 (30 rounds plus 30 more in the none branch).
| Game | Style | Rounds | A / B / C profit | Last 10 rounds mean price A, B, C |
|---|---|---:|---|---|
| 1 | serious | 30 | 4,000 / 4,000 / 48,317 | 50.0, 50.0, 49.1 |
| 2 | fun | 60 | 21,619 / 14,899 / 78,299 | 47.9, 49.3, 47.9 |
| 3 | general | 30 | 5,629 / 4,634 / 46,094 | 47.9, 47.9, 47.1 |
Game 1: A and B held 50 in all 30 rounds, even when C priced 15, 25, 30, 40 and 90 in rounds 4 to 10; C then sat at 49 with cooperative messages and earned about 12 times each rival. Game 2: after C's first undercut A and B said "Firm C undercut us", moved to 48, drifted to 44 by round 14, and later returned toward 50 and beyond in the extension; C earned about 3.6 to 5.3 times each rival. Game 3: C played an ordinary firm (one probe at 20 in round 2, then 47 to 50); A and B drifted down from 50 to 48; C earned about 8 to 10 times each rival. In all three games a human who undercut by 1 to 5 cents while sending cooperative messages kept the gemma firms cooperating and took most of the profit. One player, one model, three games: "in these games" only.

Games 4 and 5 (same set-up, other market sizes). Game 4: five firms, four gemma4-12b and the author as firm E, 45 rounds: the gemma firms fell to 21 by round 2, the author sat at 20 from round 3; profits A 1,817, B 617, C 617, D 1,017, E 31,929; no cartel formed. Game 5: ten firms, nine gemma4-12b and the author as firm J, 30 rounds: the nine settled at 22 to 23, the author at 20 to 23 (10 in round 30); profits 666 to 1,303 for each gemma firm, 15,334 for J. Game 5 is exploratory in one more way: the game was stopped by mistake after round 13 and resumed from the logged rounds with firms A and B given a prompt to agree with firm J (rounds 14 to 30; `resume_note.txt` in the run folder, harness switch `RESUME_AGREE`); A and B then held 50 for a stretch and fell back to 22 to 23 once firm J's price was low. After games 4 and 5 each gemma firm was told the game had ended, shown the full price record and the profits, told which firm was the human, and asked for its thoughts (`tools/debrief.py`, saved as `debrief.jsonl`). The replies are free text, all blame the human's "exploitation" of an equilibrium, none of them acted on that during the game, and in game 5 several describe price drops to 10 in the last rounds, which did happen (in round 29 two gemma firms priced 10, in round 30 four gemma firms and the author priced 10), so the debriefs are accurate on that point but remain colour, not evidence.

Status of this section: these five games are a **fun research direction**, not part of the preregistered study and not used for any effect estimate; they are reported as case studies only. One player (the author, who knew the design), one model, communication on.

## 26. Gemma entry variants: a different-family entrant and a scripted-undercutter entrant (seeds 11, 13, 14, 15, 16; index against the same run's no-swap branch, two windows: rounds 31-60 and rounds 46-60)
One new firm D joins at round 31 (hidden, full history from round 31, messages on), as in the earlier entry runs.
| Entrant | Rounds 31-60, all four firms | Rounds 46-60, all four firms | Rounds 46-60, incumbents A to C only |
|---|---|---|---|
| same model (earlier, section 17) | +0.000 | +0.000 | +0.000 |
| qwen3-14b | -0.007 | +0.000 (+0.000, +0.000) | +0.000 |
| scripted undercutter (1 below the lowest price) | -0.027 (-0.037, -0.019) | **-0.036 (-0.052, -0.023)** | -0.029 (-0.046, -0.015) |
The qwen3-14b entrant opens at 10 in its first round (it enters without the history), is not punished, and from round 32 on sits at the incumbents' price (for example 48 in seed 11), so the index over rounds 46-60 is the same as with no entrant in all five seeds (over rounds 31-60 the first rounds cost -0.007). The undercutter entrant lowers the index in every seed (-0.01 to -0.06 in rounds 46-60), about the size of one undercutter swap (-0.046): the cartel absorbs a persistent 1-cent entrant slowly, as it absorbs a swapped-in undercutter. Dropped for time: nothing. A branch that ran while the server was slow was not rerun (the prompts and prices do not depend on timing). The first batch (seeds 11 and 13, plus the seed 14 qwen start) ran with both models loaded and was slow (about 80 s a reply); the rest ran after unloading qwen3-14b for the undercutter branches (about 5 s a reply). Values are deterministic per branch seed either way.

## 27. Human suite: the author plays firm C against two gemma4-12b firms under four information conditions (fun research direction, one game each, 30 rounds, `data/human_suite`, seeds 81 to 84; case studies, not estimates)
| Game | History | Messages | Profit A / B / C | Mean price rounds 1-10 (A, B, C) | Mean price rounds 21-30 (A, B, C) | Index rounds 16-30 |
|---|---|---|---|---|---|---:|
| 81 normal | all | on | 4,310 / 4,317 / 50,565 | 49.7, 49.6, 49.2 | 48.0, 48.0, 47.0 | 0.84 |
| 82 no history | none | on | 3,954 / 663 / 41,686 | 49.6, 49.5, 48.5 | 35.0, 35.3, 34.7 | 0.51 |
| 83 no messages | all | off | 11,980 / 5,170 / 10,521 | 46.3, 46.5, 47.5 | 10.1, 10.1, 18.7 | 0.10 |
| 84 neither | none | off | 1,009 / 875 / 2,241 | 17.6, 18.5, 40.9 | 11.0, 11.0, 21.3 | 0.14 |
Game 81: A and B followed the author down one cent at a time (50 to 48) and never punished; the author earned about 12 times each rival. Game 82: the gemma firms held about 50 for ten rounds, then both fell together to 30 in round 11 and sat there (the author followed to 29), bounced in rounds 26 to 30; the author still earned 10 and 60 times A and B. Game 83: no cartel; both gemma firms slid from 50 to 40 by round 13 and to the floor (10) from round 17, the author's attempts to pull them up (50 in rounds 9 to 13 and 19 to 21) failed, and for the only time in all human games the author did not take most of the profit. Game 84: both gemma firms dropped to 11 or 20 from round 2 and stayed (they saw only their own last price), the author alternated between 49 and 10 to 11 and earned about twice each rival, all at very low profits. One player (the author, who knew the design), one model, one game per cell: the pattern (messages hold the cartel together, history keeps it from sliding, human undercutting works only while the gemma firms can still see and read it) agrees with the base study but is a case study only. Same fun research direction label as section 25.
