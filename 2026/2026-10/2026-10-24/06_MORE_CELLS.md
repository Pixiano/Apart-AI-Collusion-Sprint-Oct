# More cells, 2026-10-24 evening: matched cells for both models, communication cut, notes, known end date, Kimi gate

Same design and statistics as `04_FACTOR_RESULTS.md`: index = (mean price - 10) / 45 over rounds 31-60, effect = branch minus the paired no-swap branch of the same base run, bootstrap 95% interval over gated runs. These cells are exploratory additions (see `03_PREREG.md`). The hosted model ignores the seed parameter.

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
| fresh clone | **-0.222** (-0.359, -0.104) | **-0.207** (-0.407, -0.012) |
| undercutter, 1 replaced | -0.178 (-0.251, -0.098) | -0.177 (-0.181, -0.173) |
| undercutter, 2 replaced | -0.227 (-0.304, -0.142) | -0.338 (-0.338, -0.338) |

- A cartel that already exists survives the loss of messages (gemma exactly, deepseek drifts down a little).
- A fresh clone, harmless when messages are on, breaks the cartel when they are off: messages are what let a newcomer join. Gemma's clone effect is two kinds of run: 0 in six seeds, about -0.6 in three; deepseek's ranges from +0.03 to -0.64.
- Wide interval on the gemma clone row; read it as a direction.

## 3. Persistent notes, deepseek (seeds 21-25, all gated; gemma in `04_FACTOR_RESULTS.md`)

| Replacement | deepseek, notes (n=5) | deepseek, no notes (n=10) | gemma, notes (n=5) |
|---|---:|---:|---:|
| clone (history and notes wiped) | -0.012 | +0.022 | +0.000 |
| clone that keeps the notes | +0.012 (+0.000, +0.035) | not run | +0.000 |
| undercutter, 1 replaced | -0.220 (-0.470, -0.057) | -0.046 | -0.069 |
| undercutter, 2 replaced | -0.455 (-0.647, -0.287) | -0.286 | -0.322 |

With notes, deepseek reacts much more strongly to undercutters than without notes or than gemma does. The seeds differ between the notes and no-notes columns and n=5, so treat as suggestive.

## 4. Known end date (prompt says the game lasts exactly 60 rounds), deepseek seeds 21-25 (gemma partly run, not reported yet)

All 5 base runs pass the gate (0.52 to 0.84). Effects: clone -0.034, undercutter 1 replaced -0.069 (-0.160, +0.017), undercutter 2 replaced -0.195 (-0.307, -0.084). End game: in the no-swap control the mean price falls in the last five rounds in 4 of 5 seeds (20.6 to 12.7, 27.4 to 17.1, 35.6 to 27.1, 43.4 to 30.5; the fifth is flat, 38.7 to 40.0), so the cartel starts to unravel near a known end. The no-swap index is also lower than with an unknown end (0.21 to 0.70).

## 5. Kimi K3 gate (hosted, thinking cannot be switched off)

Six candidate switches were tested; every one still produced 2,300 to 2,800 characters of reasoning, so the runs use the lowest reasoning effort. Three base runs (seeds 21-23, communication on, full history): index 1.00 in all three, price exactly 55 (the monopoly price) in every round, 270 calls, about 1.9 USD. Kimi passes the gate trivially; no swap study was run (too costly: about 0.01 USD per call). The endpoint was shut down by the author.

## 6. Cost so far
deepseek-v4-1-flash: about 24,000 calls and 16 million input tokens in total, about 5.5 USD. Kimi: about 3.2 USD including one discarded first attempt whose thinking switch failed.
