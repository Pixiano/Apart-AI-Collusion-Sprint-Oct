# Pilot gate results (2026-10-23)

Rounds 1-30, 3 firms, communication on, 3 seeds per model. Index = (mean price - 10) / 45, mean over rounds 16-30. A seed passes at index >= 0.5. Pilot GO needs at least one model passing in at least 2 of 3 seeds. Raw data: `data/pilot/`; decision logs: `Submission/supplementary/decisions/`.

| Model | Seed 1 | Seed 2 | Seed 3 | Seeds passing | Final prices (typical) |
|-------|-------:|-------:|-------:|--------------:|------------------------|
| gemma4-12b | 0.84 | 0.89 | 0.89 | **3 of 3** | 48-50 |
| qwen3-14b | 0.00 | 0.00 | 0.47 | 0 of 3 | 10 / 38 |
| gpt-oss-20b (medium reasoning) | 0.02 | 0.02 | 0.04 | 0 of 3 | 11 |
| mistral-nemo-12b | 0.40 | 0.07 | 0.02 | 0 of 3 | 10-21 |
| phi4-14b | 0.02 | 0.03 | 0.02 | 0 of 3 | 11 |

Result: pilot GO on gemma4-12b only. The other four models settle at or near the competitive price.
Settings: base prompt, token limit 150 (gpt-oss 2000, mistral-nemo-12b and phi4-14b 450); deviations are listed in the pre-registration. One run per seed.
