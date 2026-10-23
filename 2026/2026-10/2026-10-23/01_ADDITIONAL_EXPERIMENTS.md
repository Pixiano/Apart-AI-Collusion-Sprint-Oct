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
Three fresh agents, prices only, 30 rounds, seed 1, `data/dev/ext3off`. The harness already makes each round simultaneous: it writes all three prompts, waits for all three replies, and only then reveals the prices, so no agent sees another's price before choosing. Compare with A3 (messages on). Result to be added below.
