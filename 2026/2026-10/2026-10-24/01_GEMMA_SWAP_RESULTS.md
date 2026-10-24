# Swap study, gemma4-12b (main sweep, seeds 11-20, base prompt, communication on)

Run 2026-10-23 00:01 to 2026-10-24 05:40 IST (paused for about 1.5 hours, resumed from the logged rounds). Data in `data/main/gemma4-12b_common_s11` ... `_s20`. One firm (C) replaced after round 30, hidden. Index = (mean price - 10) / 45, three firms, rounds 31-60 for the branches, rounds 16-30 for the base run.

## Gate
9 of 10 base runs pass (index >= 0.5 over rounds 16-30; main gate needs 60%): 0.84, 0.22, 0.87, 0.84, 0.84, 0.84, 0.89, 0.80, 0.84, 0.89. Only seed 12 stays weak (prices about 20).

## Effect of the replacement (paired with the no-swap control, 9 gated runs, bootstrap 95% interval)
| Branch | Index minus control | Interval |
|--------|--------------------:|----------|
| fresh clone (history wiped) | 0.00 | [0.00, 0.00] |
| different model (qwen3-14b, sees full history) | 0.00 | [0.00, 0.00] |
| scripted undercutter (positive control) | -0.05 | [-0.06, -0.04] |

Means over all 10 runs, rounds 31-60: control 0.79, clone 0.79, different model 0.79, undercutter 0.74. The undercutter lowers the index in every seed (-0.03 to -0.08).

## Checks that the replacement is real (seed 11)
Firm C is a different agent in each branch (models recorded in `calls.jsonl`). The clone opens at 50 against 48 and then matches; the different model copies 48 at once; the undercutter slides one price step per round (47, 47, 46, 46, 45) and the others follow it down slowly (43 at round 60).

## Reading (descriptive, one model, 10 seeds)
- A single replacement did not break the cartel, whoever the newcomer was, because newcomers that see the visible history copy it; a fresh clone also converges within a round.
- The positive control works but is gentle: the cartel erodes slowly, about -0.05 over 30 rounds, not a collapse.
- Caveats: only one firm is replaced and the swap is hidden; two of three replaced, announced swaps and persistent notes are not yet run; one model; the different-model partner (qwen3-14b) copies the history rather than pricing on its own. Not pooled with the pilot runs.
