# Additional experiments (not part of the preregistered design)

Everything here is exploratory or a plumbing check. None of it enters the pilot gate, the main results or the pooled data. Output goes to `data/dev/` (ignored by git). Anything reported from here is labelled "additional" in the paper.

| # | What | Why | Status |
|---|------|-----|--------|
| A1 | Sanity checks (one firm alone, one-shot three-firm game, token distribution) on all local models above 8B, base prompt and reasoning-field variant | Check the prompt makes each model play at all; thinking cutoff build check | running 2026-10-23 |
| A2 | External agent (small hosted model) as the one firm, 25 rounds, through the file hook | Check the hook; reference for rational play | done: 55 in all 25 rounds (the monopoly price) |
| A3 | Three external agents as firms A, B, C, 30 rounds, communication on, each through its own prompt/reply file | Reference: how do capable agents behave in the same game; second use of the hook | started 2026-10-23 |

Notes: external agents keep their own context between rounds (unlike the stateless local calls), see only the prompt file, and are told not to read anything else. Reasoning-field variant is the one allowed prompt change in the prereg and is not used unless decided and logged in the Deviations section.
