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
| 9 | **Number of firms**: 2, 4 and 5 instead of 3 (a range of 2 to 5, as in Keppo et al.; 6 only if it is cheap, edited 2026-10-23) | Formation (30 rounds, first model only, 5 seeds) | Keppo: more firms delay and weaken collusion; with 5 sellers it did not form within their horizon | Collusion index falls as firms are added; at 5 firms in our short horizon it likely stays near the competitive price. Needs one server slot per firm (5 slots) and a smaller context per slot; collusion and competitive benchmarks stay 55 and 10, ties split N ways |

## Added 2026-10-23: focal-point anchor (idea from Aharon et al.)
| # | Ablation (change vs base) | Kind | Why (source) | Prediction written now |
|---|---|---|---|---|
| 10 | **Anchor price in the prompt**: one innocuous line giving a round reference price, e.g. "your usual list price is 55", in (a) all three prompts, (b) one prompt only, (c) all three with a non-monopoly anchor (e.g. 30), against no anchor | Formation, then persistence | Aharon et al.: agents coordinate on salient numbers without talking; Fish et al.'s prompt already carried a price ceiling hint. Question: can a firm nudge its AI toward a shared price without ever asking it to collude? | (a) prices cluster at or near the anchor, collusion index up; (b) one firm leads and the others follow, as Keppo et al. saw for a larger model; (c) a stable middle price. After a swap: a replacement given the same anchor rejoins faster than one given a different anchor or none. |

Why it fits: it asks the same question as the main study (how fragile is a cartel) from the other side, how little it takes to start one, and it ties into the replacement design (the anchor can differ for the new agent). It is also a plus-factor question for the fallback detector (which prompt cues look like facilitation). Cost: formation runs are cheap (30 rounds). Handling: describe it as a robustness and detection question; the ethics appendix must say what it does and does not show and that it is a toy market, not a recipe for real pricing.

## Added 2026-10-23: a fourth firm enters at round 40
| # | Ablation (change vs base) | Kind | Why (source) | Prediction written now |
|---|---|---|---|---|
| 11 | **Entry**: a fourth firm joins at round 40 (the market grows from 3 to 4; nobody is replaced). Entrant variants: (a) same model, fresh context (rules only, no history); (b) a different model family, fresh context; (c) scripted undercutter (positive control). Compared with the no-entry control from the same round-40 checkpoint | Persistence | Classic cartel-stability question (entry); Keppo et al.: more sellers delay and weaken collusion (4 patient LLMs +11% against +36% for 3); Eschenbaum et al.: an unseen partner breaks learned collusion | (a) the newcomer starts low and incumbents either punish it or pull it up; direction uncertain. (b) like (a), possibly a different price level. (c) collusion breaks by construction. In all cases the index after entry is below the control, and larger than a swap if incumbents also face a fourth set of competing interests. |

How it differs from a swap: a swap keeps three firms and removes one agent's history; entry adds a firm, so the market share per firm drops (ties now split four ways) and each firm's pie shrinks. Keep these apart in the report. Needs four server slots (the same infrastructure as ablation 9) and one extra checkpoint: the control branch is saved at round 40 and both the control and the entry branch continue from that file, so they are paired at round 40. Primary outcome: collusion index over rounds 41 to 60 for all four firms minus the control, with the incumbents' own index reported separately. Cost: a 20-round branch, cheap. Keep it as a toy-market robustness question in the report.

## Final item, always last: a human plays one firm (added 2026-10-23, for fun and as a demo)
| # | Ablation (change vs base) | Kind | Why | Prediction written now |
|---|---|---|---|---|
| H | **Human firm**: the author picks one firm's price each round (same information as an LLM: rules, history, optionally the message line) while the other two are LLMs. Variants: (a) human from round 1; (b) human takes over a firm at round 30, like a swap | Case study | Shows how LLM firms treat a human-like price setter; a vivid example for the report and talk | LLMs read a steady human as a cartel partner; a human who undercuts triggers a price fall; one person cannot give statistics |

Rules: one author, a handful of games, so it is a **case study, not an estimate**: no bootstrap, no claim beyond "in these games". The human knows the design and the round count (disclose), so the LLMs are not compared with the unblinded human on equal terms. No other participants (no consent or age questions). Needs a small interactive mode in the harness (prompt for a price each round, log it like an LLM call, mark the firm as human in `meta.json`). Runs after everything else; skipped if time is short. This row stays last even if more ablations are added above it.

## Not planned (YAGNI)
Telling agents their rivals are AI, other games, other demand shapes, more than three swap timings, human-written prompts per firm. Add only if a result begs for it.

## Rules for running them
- Seeds: 5 per ablation cell (not 10), because these are exploratory. Same seed list as the base cell where possible so differences are paired.
- Report as a small table of effects with bootstrap intervals, marked exploratory. No claim beyond "differs from base in this setup".
- Log the exact prompt text of every variant in the repo (`data/<run_id>/meta.json`). A change here is not a prereg deviation, but anything that touches the base configuration is.
- Priority by cost: 1, 4, 2, 5 first (cheap or directly motivated), then 10, 11, 6, 7, then 3, 8, 9, and H always last.
