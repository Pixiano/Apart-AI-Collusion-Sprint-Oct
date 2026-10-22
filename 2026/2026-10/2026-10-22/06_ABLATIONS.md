# Ablations and extra configurations (exploratory, written 2026-10-22 before any data)

Status: NOT part of the pre-registration (`prereg-v1`). Run only after the base configuration and the core swaps are done, and label every result from here as exploratory. One factor changes at a time against the base configuration, same seeds, same checkpoint design. Cut from the bottom if time runs out.

## Base configuration (what everything is compared with)
3 firms, 60 rounds, integer prices 10 to 100, agents not told the number of rounds, long-run-profit prompt, full history, no notes field, communication as in the pre-registration, temperature 0.7, thinking off (gpt-oss at low). Details: `03_HARNESS_SPEC.md`.

## Two kinds of ablation (cost differs a lot)
- **Formation ablations** change something that could affect whether collusion forms at all. They need only rounds 1 to 30 (no swap), about 3 to 6 minutes per run. Cheap, so run these first.
- **Persistence ablations** change something that could affect what a swap does. They need branches from a checkpoint, about 2 to 3 minutes each. Run them on the single strongest setup only.

## Candidate list, in priority order
| # | Ablation (change vs base) | Kind | Why (source) | Prediction written now |
|---|---|---|---|---|
| 1 | **Tell the agents the horizon** ("the game lasts 60 rounds") | Formation, then persistence | Backward induction says cooperation unravels near a known end; Keppo and Fish hide the end | Prices fall in the last rounds; a known end also lets agents time a deviation |
| 2 | **Notes field** (each agent writes plans carried to the next round) | Formation, persistence | Fish and Keppo give agents this memory; this is the main candidate prompt change | More collusion; a "fresh clone" then also loses its notes, a clearer replacement |
| 3 | **History window**: last 20 rounds plus summary instead of the full table | Formation | CoopEval: LLMs handle long histories badly | Small or no change; maybe cleaner behaviour late in the run |
| 4 | **Prompt wording**: add a line about selling more by lowering the price | Formation | Fish: this wording lowered prices a lot | Lower prices, less collusion (a manipulation check on the harness) |
| 5 | **Swap timing**: round 15 and round 45 instead of 30 | Persistence | Early swaps hit a cartel before it is settled; late swaps sit near the end | Early swap does less damage (nothing built yet); late swap more |
| 6 | **Reasoning effort** for gpt-oss: low versus high (native setting) | Formation | The model has native levels; costs more tokens | More reasoning gives more strategic play; unclear for collusion |
| 7 | **Replacement strength**: a larger model replaces a smaller one, and the reverse | Persistence | Keppo: the larger model led and stabilised collusion | Stronger replacement keeps or lifts prices; weaker replacement is followed or exploited |
| 8 | **Temperature**: 0.3 and 1.0 | Formation | Randomness may drive accidental undercuts | Lower temperature, steadier prices |
| 9 | **Number of firms**: 2 and 4 instead of 3 | Formation | Keppo: more firms break collusion | 2 firms collude most, 4 least |

## Not planned (YAGNI)
Telling agents their rivals are AI, other games, other demand shapes, more than three swap timings, human-written prompts per firm. Add only if a result begs for it.

## Rules for running them
- Seeds: 5 per ablation cell (not 10), because these are exploratory. Same seed list as the base cell where possible so differences are paired.
- Report as a small table of effects with bootstrap intervals, marked exploratory. No claim beyond "differs from base in this setup".
- Log the exact prompt text of every variant in the repo (`data/<run_id>/meta.json`). A change here is not a prereg deviation, but anything that touches the base configuration is.
- Priority by cost: 1, 4, 2, 5 first (cheap or directly motivated), then 6, 7, then 3, 8, 9.
