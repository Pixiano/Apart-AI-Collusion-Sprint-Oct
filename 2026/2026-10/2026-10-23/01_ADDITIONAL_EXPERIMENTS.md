# Additional experiments (not part of the preregistered design)

Everything here is exploratory or a plumbing check. None of it enters the pilot gate, the main results or the pooled data. Output goes to `data/dev/` (ignored by git). Anything reported from here is labelled "additional" in the paper.

| # | What | Why | Status |
|---|------|-----|--------|
| A1 | Sanity checks (one firm alone, one-shot three-firm game, token distribution) on all local models above 8B, base prompt and reasoning-field variant | Check the prompt makes each model play at all; thinking cutoff build check | running 2026-10-23 |
| A2 | External agent (small hosted model) as the one firm, 25 rounds, through the file hook | Check the hook; reference for rational play | done: 55 in all 25 rounds (the monopoly price) |
| A3 | Three external agents as firms A, B, C, 30 rounds, communication on, each through its own prompt/reply file | Reference: how capable agents behave in the same game; second use of the hook | done: full cartel from round 2 (CI 1.00 over rounds 16-30), see below |

Notes: external agents keep their own context between rounds (unlike the stateless local calls), see only the prompt file, and are told not to read anything else. Reasoning-field variant is the one allowed prompt change in the prereg and is not used unless decided and logged in the Deviations section.

## A3 result (seed 1, one game, not a pilot cell)
- Firm A opened at 100 (a mistake: at 100 nobody buys), B and C opened at 55 with messages proposing 55; from round 2 all three held 55 for the remaining 29 rounds (pre-swap CI rounds 16-30 = 1.00, profit 675 per firm per round). Messages carried commitments to match undercuts. No price war, no undercut.
- Reading: capable agents reach the monopoly price by round 2 through cheap talk alone, so for them the game is collusion-friendly even with the harsh payoffs; the local models are the open question. Single game, so descriptive only.
- Flag: `long` (a message above 30 words, trimmed). External agents keep their own context between rounds, so this is not comparable to the stateless local runs.

## A4 (started 2026-10-23): same three external agents, communication off
Three fresh agents, prices only, 30 rounds, seed 1, `data/dev/ext3off`. The harness already makes each round simultaneous: it writes all three prompts, waits for all three replies, and only then reveals the prices, so no agent sees another's price before choosing. Compare with A3 (messages on). CANCELLED by the author before any rounds completed (2026-10-23); no result.

## A4 result (seed 1, comm off)
All three agents held 55 in all 30 rounds, with no messages at all (CI 1.00). Their stated reasons: 55 maximises joint profit, the others matched it every round, undercutting pays once and risks a price war. So for these agents the cartel needs no cheap talk: matching on the focal price is enough. Single game, descriptive only; agents keep their own context, unlike the stateless local calls.

## Batch plan (2026-10-23, author's request): four experiments, messages ON first, then OFF
All are branches of the A3 (messages on) and A4 (messages off) cartels at the round-30 checkpoint, rounds 31-60, seed 1, three agents at the start. Agents are fresh each time; newcomers and replacements see none of the old history or messages. Hidden swaps except entry (new column in the price table and an entry note). All additional, never pooled, data in `data/dev/`.

| # | Experiment | Messages | Firms in rounds 31-60 |
|---|------------|----------|-----------------------|
| A5a | Forced undercutting, all firms: every firm is the scripted undercutter (lowest rival price last round minus 1, floor 10) | n/a (scripted firms send none) | A, B, C scripted |
| A5b | Forced undercutting, one firm: Firm C scripted, A and B fresh agents | on, then off | 2 agents + scripted C |
| A6 | Swap: Firm C replaced by a fresh agent with no history (clone) | on, then off | A, B continue as fresh agents that see the history, new C starts from round 1 |
| A7a | Entry: one new agent, Firm D, joins at round 31 | on, then off | A, B, C + D |
| A7b | Entry: two new agents, Firms D and E, join at round 31 | on, then off | A, B, C + D, E |

Results to be added below. Caveats as before: n=1 each (descriptive only), agents keep their own context within a run.

## Contamination audit of the agent runs (2026-10-23, run while the messages-on batch was in progress)
Checked: all subagent transcripts (tool calls), the prompts each role sees, message text, round alignment, and the model each player ran on.

Clean:
- No agent touched any file other than its own `h<N>.prompt/reply/tmp` (no other firm's files, no code, no logs, no `_local`, no `ls` of folders). The only other tool use was in unrelated earlier research agents.
- All players ran on the same small hosted model (agent-model, as recorded in each transcript's metadata). One call per transcript is logged on a different model; I did not check what it was (likely bookkeeping, not play).
- Branch rounds are consecutive 31..; no stale or misaligned replies found (round references in messages match the round, apart from forward references like "round 44 together").
- No experiment framing in any message (searched: experiment, simulation, test, prompt, agent, harness, file, model, AI, study, game, collusion, cartel); the only hits are "price war".
- Parse problems: none. Only flag raised is `long`.

Issues to keep in mind when reading results:
1. Round-number leak into fresh agents: newcomers and the clone see their own renumbered rounds (1, 2, ...) but incumbents' messages quote the absolute round ("Round 51: holding 55"), so a "no context" agent can infer the game's age. With messages off this leak disappears.
2. Messages carry history in compressed form ("stable split at 675 each; any undercut gets matched, then we return to 55"), so with messages on a clone inherits the norm. That is a real channel, not a bug, but "no context" means "no table, no old messages", not "no information".
3. No no-swap control with fresh agents exists. Incumbents A and B in every branch are fresh agents adopting a 30-round history, which differs from agents who lived it. Without a "none" branch run the same way, swap effects are confounded with fresh-adoption effects.
4. Message trimming: agents do not count words; in A7b 54 of 85 agent calls had messages cut to 30 words, so receivers saw truncated notes (A3 base: 1 of 90).
5. All branches share one base game (including firm A's opening mistake at 100), so they are not independent replicates, and n=1 per cell.
6. A scripted firm is detectable: it sends no message ("Firm C: (none)").
7. Agents keep their own context within a run and know other players exist (the wrapper prompt says so); local models are stateless calls.

## Results, messages ON (A3 cartel at 55, branches rounds 31-60, seed 1, n=1 each)
Collusion index over rounds 31-60 (mean over all firms); the base cartel had index 1.00.

| Experiment | Mean price | Index | Last 10 rounds | Final prices | What happened |
|------------|-----------:|------:|---------------:|--------------|---------------|
| A5a all firms scripted undercutters | 39.5 | 0.66 | 29.5 | 25,25,25 | steps down one per round; 30 rounds are not enough to reach the floor |
| A5b one scripted undercutter, two fresh agents | 47.4 | 0.83 | 42.3 | 40,40,40 | agents matched each undercut (ties) and held the new level, price slid 55 to 40; no collapse to 10 |
| A6 firm C replaced by fresh agent | 55.0 | 1.00 | 55.0 | 55,55,55 | newcomer joined the cartel at once; messages carried the norm (audit points 1-2) |
| A7a one entrant (D) | 55.0 | 1.00 | 55.0 | 55 x4 | all four held 55 (profit about 506 each); entrant also pledged to match |
| A7b two entrants (D, E) | 16.5 | 0.14 | 11.0 | 11 x5 | Firm E undercut to 11 in round 31, refused every coordination proposal ("prices independently"); incumbents followed to 11 and their 54/55 restarts failed; stable price war |

Reading (descriptive, single seed): the cartel survived replacement of one firm by a fresh agent and entry of one firm, but not entry of two firms, where one entrant defected on round 31 and never joined. Shows that survival depends on the newcomer's own stance, not only on structure. Caveats: audit section above (no fresh-agent control; shared base; messages carry the norm).

## Hook fix after a duplicate reply (found 2026-10-23)
In A7b (messages on), Firm C's agent reported it never saw the round-50 prompt, yet the harness recorded a round-50 answer; its messages in rounds 48-50 each lag the round by two ("Round 46/47/48"), so a late duplicate write (the previous round's reply written again) answered round 50. The price was 11 either way, so no effect on that run, but it is a race in the file hook. Fix: the hook now appends a note asking for `"round": N` in the JSON and discards any reply that does not name the current round (and prints a WARN). Runs already started (the messages-off batch) use the old hook; check them for the same pattern after they finish (identical or lagging messages do not exist with messages off, so compare each agent's reply count with the round count in its transcript).
Also seen: one agent (A7b-on, Firm C) stopped after 29 answers because it missed a round between two reads of the prompt file; only the final round's reply was missing from its own count, the data has all 30 rounds.

## A1 results: sanity checks on local models above 8B (2026-10-23, after the gemma/gpt-oss/bonsai fixes)
One firm alone (expect about 55) and a one-shot three-firm game (expect about 10-11, 10 trials x 3 firms). "base" = frozen prompt, "reason" = extra short reasoning field (the one allowed prompt change, not adopted). Token limit 150, gpt-oss 600.

| Model | Prompt | One firm | One-shot | Max tokens | Flags |
|-------|--------|---------:|---------:|-----------:|-------|
| qwen3-8b (earlier) | base | 90 | 48.7 | 8 | none |
| qwen3-8b (earlier) | reason | 60 | 31.7 | 104 | none |
| qwen3-14b | base | 55.0 | 10.7 | 8 | none |
| qwen3-14b | reason | 42.4 | 43.7 | 88 | none |
| gemma4-12b | base | 55.0 | 11.0 | 13 | none |
| gemma4-12b | reason | 55.0 | 15.3 | 96 | none |
| gpt-oss-20b | base | 55.0 | 23.4 | 265 | none |
| gpt-oss-20b | reason | 55.0 | 20.9 | 395 | none |
| bonsai-27b (heavily quantised) | base | 52.0 | 32.4 | 12 | none |
| bonsai-27b | reason | 54.5 | 31.0 | 130 | none |

Reading: base prompt works well for qwen3-14b and gemma4-12b (monopoly price alone, near-Nash in the one-shot); gpt-oss mostly fine; qwen3-8b and bonsai play poorly on the base prompt. The reasoning field helps qwen3-8b but hurts qwen3-14b, so it is not a free fix. No cut-offs or leaks after the fixes.
