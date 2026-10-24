# Other results gathered 2026-10-23 evening to 2026-10-24 midday (exploratory unless stated)

Index = (mean price - 10) / 45 over three firms; "pass" = 0.5 or more over rounds 16-30. Communication on, one run per seed.

## 1. Opening-price spread, phi4-14b on the easy prompt (profit table), round 1 only, 50 seeds
Data `data/round1/`; script `tools/round1_spread.ps1`. 150 first-round replies: price 20 in 64 (43%), 30 in 35 (23%), 50 in 51 (34%). The opening price is split between three focal points, so the 60-round pilot seeds (0.84 when the opening was 50, 0.22 when it was 20) differ mostly by the opening draw, which the later rounds then copy. Three seeds is a minimum for this model.

## 2. Easy-prompt gate results (profit table in the rules, 60 rounds, data `data/easy`, `data/median`)
| Model | Prompt | Seed indices (16-30) | Seeds passing | Gate |
|-------|--------|----------------------|:-------------:|------|
| phi4-14b | easy | 0.84, 0.22, 0.22 | 1 of 3 | no |
| mistral-nemo-12b | easy | 1.02, 0.69, 0.41 | 2 of 3 | yes (but see 4) |
| mistral-nemo-12b | hint (one sentence) | 0.14, 0.21, 0.93 | 1 of 3 | no |
| gpt-oss-20b | easy | cancelled at round 21 of seed 1 (0.04); dropped by the author 2026-10-24, not needed | | none |
phi4-14b seed 1 stopped at round 49 and was resumed from its logs (note in its `meta.json`).

## 3. Nemotron-Nano-12B-v2, base prompt, thinking off (model's own /no_think switch)
Seeds 1-3: 0.00, 0.24, 0.55 (1 of 3, no gate), no flags, replies at most 12 tokens. Data `data/pilot_nemotron_off`. The thinking-on pilot was not run (sanity: median 1,427 completion tokens, about 36 s per call); limits chosen are logged in `03_PREREG.md`.

## 4. Swap study, mistral-nemo-12b on the easy prompt (seeds 11-16, paused; data `data/main/mistral-nemo-12b_common_s11` ... `_s16`)
Base indices (rounds 16-30), seeds 11-16: 0.46, 0.02, 0.56, 0.15, 0.01, 0.19: only 1 of 6 passes, so the cell cannot reach the 60% main gate (at most 5 of 10) and does not enter the swap analysis. Rounds 31-60 means over the five complete seeds (11-15): control 0.17, clone 0.25, different model 0.18, undercutter 0.15. The control itself moves by 0.1 to 0.2 against the base run without any swap, so these differences are within noise. Reading: with this prompt the model does not collude reliably; the first three easy-prompt seeds (section 2) were a lucky draw. Seed 16 is partial (its undercutter branch has 1 of 30 rounds); the study was paused by the author to gather findings.

## 5. Gemma4-12b swap study: see `01_GEMMA_SWAP_RESULTS.md` (9 of 10 gated; no effect of clone or different-model replacement; undercutter -0.05).

## Not run
Two of three replaced, announced swap, communication off, persistent notes, thinking-on Nemotron. gpt-oss on the easy prompt was dropped (not needed).
