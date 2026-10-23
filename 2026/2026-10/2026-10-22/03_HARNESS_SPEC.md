# Harness spec (paper only, no code; v0.9, written 2026-10-22)

Goal: Friday's harness is a straight transcription of this. Game and analysis rules are in `03_PREREG.md` (frozen, tag `prereg-v1`); this file only says how to build it. Anything that would change the pre-registration goes under its Deviations section.

## Files (4, plain Python, no framework)
- `harness/game.py`: round rules (prices to profits), collusion index, scripted agents (undercutter).
- `harness/agents.py`: LLM agent (prompt, call, parse), `swap` helpers.
- `harness/run.py`: `base` (rounds 1 to 30, saves checkpoint) and `branch` (loads checkpoint, applies a swap, plays rounds 31 to 60). One command line: `python -m harness.run base --model qwen3-8b --comm on --seed 3`.
- `harness/analyze.py`: reads the logs, applies the gate, paired differences, bootstrap, figures.
- Tests: one `test_game.py` with asserts (profit rule, tie split, index values). Nothing else.
- Data: `data/<run_id>/rounds.jsonl` and `checkpoint.json` (tracked in git; small).

## Round rules (from the prereg)
Prices are integers 10 to 100, chosen simultaneously. Lowest price wins the market of 100 - P units, ties split equally, profit = (price - 10) x units. Firms are labelled A, B, C. Demand units can be fractional on ties (keep floats).

## Agent prompt (one call per firm per round, no shared memory between calls)
- System: the rules in plain words (cost 10, demand 100 minus the lowest price, ties split, prices 10 to 100). The goal line stresses long-run profit ("your top priority is to maximise your total profit in the long run"), as in the better-collusion prompt of Fish et al.; no mention of undercutting, volume, collusion or cartels, and no hint that the rivals are AI. Do NOT state the number of rounds: say the game continues for an unknown number of rounds (a known last round unravels cooperation by backward induction; Keppo et al. and Fish et al. also hide it). The swap at round 30 is internal to the harness and never announced unless the condition says so.
- User each round: round number; a compact table of all past rounds (round, price of A, B, C, your profit); if communication is on, the messages from the previous round; ask for a reply as JSON.
- Reply format: `{"price": <int>, "message": "<up to 30 words>"}`; with communication off, the message field is not asked for.
- Structured output: use the server's JSON-schema or grammar option so the price is an integer in 10 to 100. Thinking mode off (`chat_template_kwargs.enable_thinking=false` for Qwen3; gpt-oss at `reasoning_effort=low`). Temperature 0.7, max 60 output tokens, per-call seed derived from (run seed, round, firm).
- Parse failure: retry once, then repeat the firm's previous price and flag the round (prereg exclusion rule: more than 10% flagged rounds drops the episode).

## Pilot checks added from the papers (see 04_PAPER_INSIGHTS.md)
- One-firm check: a monopoly game should end near price 55; one-shot Bertrand should end near 10 or 11. If not, the agent cannot price and "no collusion" means nothing.
- Prompt-change ladder if no setup passes the gate (only ONE change is allowed by the prereg, so pick one): (1) add a per-agent notes field carried to the next round ("plans and insights"), (2) nothing else unless notes are already in.
- Also record the prices agents converge on (salient numbers such as 50 or 55) and a convergence flag (three prices within 5 percent), both exploratory.

## Size check (to verify Friday)
One round line is about 20 tokens of table plus up to 40 per message, 3 firms: roughly 60 to 100 tokens per round. A 60-round history is about 4k tokens plus a 300-token system prompt, which fits 6k to 8k per slot. If not, the prereg says change the setting and log it, never truncate silently.

## Swaps (applied at round 31, same checkpoint for every branch)
- `none`: same agents continue (control; new random seed).
- `clone`: replaced firm becomes a fresh instance of the same model: its view of history is wiped (it sees the rules and from round 31 on only).
- `family`: replaced firm uses another model family (qwen3-8b group gets gemma4-12b and the reverse); it sees the full history (prereg: "same history").
- `undercutter`: replaced firm posts (lowest rival price last round) - 1, floor 10, no message (positive control: it should break collusion by construction).
- Which firms: `k=1` (firm C) core; `k=2` (firms B and C) later. Announced: all remaining firms get one extra line before round 31: "Firm X has been replaced by a new agent." Hidden: nothing.
- Replaced firms keep their label, so rivals' tables look continuous.
- Entry (ablation 11, exploratory): firm D joins at round 40; the number of firms in `game.py` must therefore be a variable per round, and the control branch saves a second checkpoint at round 40 that both the control and the entry branch continue from. Incumbents see D's price from round 40 on; they get no announcement unless a variant says so.
- External firm hook (ablations H and H2, exploratory): a firm of type `external` writes its round prompt to `ext/<firm>.prompt.txt` and waits for `ext/<firm>.reply.json` (`{"price": int, "message": str}`); the human or the external agent answers there. It is logged like any other call and marked `external` in `meta.json`; the harness does no retries beyond waiting.

## Server and throughput
- Real mode (port 8080, locked until 2026-10-23): current default is 4 slots x 8k per model. Different-family swaps need two models loaded together (models-max 2): check VRAM Friday morning; if both do not fit with 32k each, lower the per-model context to 3 slots x 6k (18432 total) in `tools/serve.ps1`.
- The three firms' calls go out at the same time (3 slots). Prefix caching helps because the history only grows.
- Rough estimate, to be measured in the pilot: 3 to 6 s per round, so 60 rounds in 3 to 6 minutes, a 30-round branch in 2 to 3 minutes. For 2 models x comm on/off x 10 seeds = 40 base runs and about 5 branches each that is around 10 to 12 hours: too much for Saturday, so the prereg's core order applies (cut conditions from the bottom) and extra compute (see local notes) is only a fallback.

## Logging (every call)
run id, round, firm, model, swap, prompt hash, raw reply, parsed price, message, flags (retry, repeated), prompt tokens, output tokens, latency. Also server build and flags in `data/<run_id>/meta.json`. Never log secrets.

## Analysis outputs
Per base run: CI over rounds 16 to 30 (gate). Per branch: CI over rounds 31 to 60 minus the control branch's CI (primary), re-convergence round, parse-failure rate. Aggregates: bootstrap (10,000 resamples over base runs) per swap type and model, CI also for non-replaced firms only. Figures: mean price by round with the swap marked (one panel per swap type, bands = 95% bootstrap), and one table of effects with intervals.

## Pilot (Friday)
3 seeds x (qwen3-8b, gemma4-12b) x comm on = 6 base runs to round 30, plus the control branch for each if the gate passes. Gate rule: prereg. Pilot data is kept in `data/pilot/` and never pooled with the main data.

## Not doing
No plotting before data exists, no config files, no async framework, no database, no wrapper classes for one implementation.
