# Findings (preliminary, 2026-10-25 early morning)

Source of every number: `2026/2026-10/2026-10-24/` (01 to 06) and the run folders under `data/`. Effect = change in the collusion index CI(31-60) against the no-swap branch of the same base run, 95% bootstrap interval over base runs. CI = (mean price - 10) / 45; monopoly price 55 gives 1.0. A model/communication cell is analysed only if at least 60% of its base runs have CI(16-30) >= 0.5 (the gate).

## Status of runs when this was written
Done: swap studies on gemma4-12b, deepseek-v4-1-flash, qw38, glm53f; factor cells on gemma and deepseek; known end date on all four; three mixed markets; eight-firm runs; external-agent firm (n=2); temperature and entry ablations on gemma; more seeds for deepseek and glm53f.
Running or not yet written up at this time: glm53f factor cells (announced, communication cut, history none and last round, notes, communication off, clone k=2), gemma family k=2, deepseek entry, awareness probe, LLM newcomer variants, gemma 120-round horizon, number of firms. Fill these in `ROUGH_REPORT.md` section 4 when done (`FINDINGS.md` is refreshed once after the last run).

## Headline findings
1. **Replacing a firm with a fresh copy, a different model or a different family does not break a cartel.** Clone effect is -0.001 (gemma), +0.022 (deepseek), +0.000 (qw38), -0.005 (glm53f, 10 seeds). Newcomers who see the record copy it; a fresh clone converges within a round. A different-family replacement (qwen3-14b for gemma, Qwen for DeepSeek, DeepSeek for Qwen and GLM) is also near zero (-0.00 to +0.06).
2. **One defector dents the cartel, two break it** (positive control works): scripted undercutter replacing 1 firm costs -0.046 (gemma), -0.046 (deepseek), -0.082 (qw38), -0.297 (glm53f); replacing 2 costs -0.317, -0.286, -0.300, -0.346. Lower in every seed.
3. **Messages are how newcomers get recruited.** Without messages neither gemma (1 of 5 base runs pass) nor deepseek (0 of 10) forms a cartel. An existing cartel survives losing its messages at round 30 (no-swap effect about 0), but a fresh clone that joins without messages breaks it: -0.207 (gemma, interval -0.407 to -0.012), -0.222 (deepseek, -0.359 to -0.104). In a mixed market with gemma as one firm the same test gives -0.605 (-0.730 to -0.428).
4. **Fragility depends on the model.** One undercutter costs glm53f -0.297 against -0.03 to -0.09 for the others. A known end date gives an end-game price drop in deepseek (4 of 5 seeds) and glm53f (5 of 5) but not in qw38 (holds 55 to round 60) or gemma.
5. **Announcing a swap roughly doubles an undercutter's damage** (gemma -0.075 vs -0.046; deepseek -0.098 vs -0.046; deepseek 10 more seeds -0.100 vs -0.031). Intervals overlap for gemma; small effect.
6. **Group size matters.** Eight firms (two copies each of four models, seeds 51-53): the cartel formed in 1 of 3 base runs per variant and decayed toward cost.
7. **Mixed markets** (deepseek/qw38/glm53f, seeds 31-35, 5 of 5 gated, no-swap 0.86): clone +0.037, gemma replacing C +0.035, gemma entering as a fourth firm +0.008, undercutter k=1 -0.056, k=2 -0.267, clone after a communication cut -0.170.
8. **Ablations on gemma (seeds 11, 13, 14):** temperature 0.3 / 0.7 / 1.0 leaves the cartel (index 0.84-0.87) and the clone effect (0.000) unchanged; no temperature trend in the undercutter effect. One new gemma firm entering at round 31 changes nothing; two change it in 1 of 5 seeds (0.87 to 0.43).

## Results by model (core cells, full history, hidden swap)
| Model | Gated runs | Clone | Family | Undercutter k=1 | Undercutter k=2 |
|---|---|---:|---:|---:|---:|
| gemma4-12b (local) | 9 of 10 | -0.001 | 0.00 | -0.046 | -0.317 |
| deepseek-v4-1-flash | 10 of 10 (20 with extra seeds) | +0.022 | +0.060 | -0.046 | -0.286 |
| qw38 | 5 of 5 | 0.000 | 0.000 | -0.082 | -0.300 |
| glm53f | 10 of 10 | -0.005 | 0.000 | -0.297 | -0.346 |
| kimi-k3 | 3 of 3 (gate only) | - | - | - | - |

Full per-condition tables (history none/last round, notes, communication cut, announced, known end) are in `README.md` and `06_MORE_CELLS.md`.

## Caveats to state in the report
- Small samples: 9-20 gated runs in main cells, 5 in most factor cells, 3 (eight-firm), 2 (external agent). Descriptive, not confirmatory.
- Everything after the frozen plan (`prereg-v1`) is exploratory and logged in `03_PREREG.md`.
- Hosted endpoints ignore the seed, so hosted runs are independent replicates, not reproducible runs. Local runs are only approximately reproducible.
- Coverage is uneven by model (qw38 lacks announced, cut, history and notes cells; Qwen excluded for cost).
- One game, one stylised swap, a scripted undercutter as the positive control, thinking switched off or set low.
- Gemma's narrow intervals reflect very similar runs (most settle at price 50).
