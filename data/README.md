# Data map

One folder per experiment; each run is `<run>/{meta.json, checkpoint.json, base/, <branch>/}` with `rounds.jsonl` (prices, shares, messages), `calls.jsonl` (every model call) and `branch.json`. Data released under CC BY 4.0. Section numbers refer to `2026/2026-10/2026-10-24/06_MORE_CELLS.md` (MC). "Hosted" models are called through a hosted endpoint, which ignores the seed.

| Folder | Experiment | Used in |
|---|---|---|
| `pilot/`, `pilot_nemotron_off/` | Preregistered pilot gates (local models) | prereg pilot notes |
| `easy/`, `median/` | Easy-prompt and median-price gate checks (local models) | `2026-10-24/02_OTHER_RESULTS.md` |
| `main/` | Main swap study: gemma4-12b, deepseek-v4-1-flash (communication on and off), mistral-nemo-12b, glm53f; seeds 11-25 | MC 1, 2, 18 |
| `hist0/`, `hist1/` | History window ablations (deepseek) | `2026-10-24/04_FACTOR_RESULTS.md` |
| `notes/` | Persistent notes ablation (deepseek, seeds 21-25) | MC 3 |
| `horizon/` | Known end date (deepseek) | MC 4, 11 |
| `kimi/` | Kimi K3 gate only (hosted, thinking cannot be switched off) | MC 5 |
| `qwen/` | qw38 (hosted) full-history cells | MC 7 |
| `glm/` | glm53f cells, including newcomer prompt variants (21 of 25 branches finished) | MC 8, 23 |
| `mixed/`, `mixed_g/`, `mixed_h0/` | Mixed-family markets (firm C replaced at round 31); `mixed_h0` = no history | MC 12 |
| `more_ds/` | More deepseek seeds | MC 13 |
| `eight_a/`, `eight_b/` | Eight-firm markets (seeds 51-53) | MC 14 |
| `external_agent/`, `external_agent_ext*/` | An external agent (a small hosted chat model) as firm C via the prompt/reply file hook, seeds 61 and 62, n=2; `_ext*` hold the agent prompt files | MC 15 |
| `gemma_more/` | Gemma main study on seeds 31-40 (none, clone, family, undercutter k=1 and k=2, announced clone and undercutter, communication-cut cells) and the entry (one and two new firms) and myopic-newcomer cells on the same seeds; pooled with `main/` seeds 11-20 for the 20-seed gemma numbers | MC 28 |
| `gemma_timing/` | Swap timing, gemma, 9 gated seeds of 11-20: swap at round 15 (`_t15`) and 45 (`_t45`); each folder holds a checkpoint cut from the matching `main/` run and the branches none, clone_k1_hid, undercutter_k1_hid (no base run; exploratory, tool `tools/swap_timing.py`) | MC 29 |
| `qwen14_more/` | qwen3-14b as the base model, seeds 51 and up (7 finished when analysed): all firms at the floor price 10 in rounds 16-30, gate fails; none, clone, undercutter and family branches exist but are not analysed (exploratory) | MC 30 |
| `long/`, `long_ds/` | Longer horizon (rounds 31-120, gemma and deepseek) | MC 20 |
| `nfirm/`, `nfirm_ds/` | Number of firms (gemma, deepseek; seeds 41, 42) | MC 21 |
| `temp03/`, `temp10/`, `temp03_ds/`, `temp10_ds/` | Temperature 0.3 and 1.0 (gemma, deepseek) | MC 22 |
| `round1/` | Round-1 spread test: 50 gemma4-12b first-round runs per seed set (147 of 150 = 50), reported in MC 24. Also 50 phi4-14b first-round runs (51 of 150 at 50, 64 at 20, 35 at 30); that model has since been deleted and the set is not used in the report | MC 24 |
| `human/`, `human_ext1..9/` | Five human-firm games (case studies, fun research direction); `_ext*` hold prompt files | MC 25 |
| `human_suite/` | Four human information-condition games (case studies) | MC 27 |
| `additional/` | Early exploratory runs: external-agent trios (`ext3`, `ext3off`) and one-firm sanity checks (`sanity*`); see `additional/README.md` | `2026-10-23/01_ADDITIONAL_EXPERIMENTS.md` |
| `dev/` | Scratch output, gitignored, never used | none |

## Partial, cancelled or not used for results

- `main/mistral-nemo-12b_common_s16/undercutter_k1_hid`: ends at round 44 (incomplete branch).
- `eight_b/..._dev..._common_s53/clone_k1_hid`: 1 round only.
- `easy/gpt-oss-20b_common_s1/base`: 21 rounds, cancelled.
- 13 folders in `additional/` (sanity checks) have no `rounds.jsonl`.
- `gemma_more`: seeds 12, 33 and 38 do not pass the gate (index over rounds 16-30 below 0.5; 12 is in `main/`), so they are left out of every effect.
- `qwen14_more`: the swap branches are not used for results because every base run fails the gate.
- `round1` phi4-14b set: not used.
- `human_ext*`, `external_agent_ext*`: prompt files only, no results.
