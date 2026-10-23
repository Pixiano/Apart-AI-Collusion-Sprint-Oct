# 2026-10-23 (Fri) - Daily summary

Sprint: Apart Research AI Collusion Sprint, 2026-10-23 to 2026-10-25. Author's go ("begin") at 13:15 IST.

## Before the begin marker (reading and planning only)
- Read the seven papers in more depth (Eschenbaum, Fish incl. online appendix, Keppo, Shi, CoopEval appendices); notes in `../2026-10-22/04_PAPER_INSIGHTS.md` and `../2026-10-22/05_COOPEVAL_ANALYSIS.md`.
- Exploratory ablation list (12 configurations plus two case studies), `../../../ABLATIONS.md` and `../2026-10-22/06_ABLATIONS.md`. Not part of the pre-registration.
- No code, no data, no results. The `pre-sprint` tag was moved to the last commit before this marker.

## Build (from about 13:30 IST)
- Harness written per spec v1.0, one job per module: `harness/{game,agents,play,swaps,run,analyze}.py` and `tests/test_game.py` (rules, index, parsing, prompt views, swap plumbing with a fake model; all pass). No model runs yet.
- Spec settled with the author: 150 output tokens, cut replies kept and flagged, verbose prints, units-sold column, clone numbers its rounds from 1. Logged in the prereg Deviations section (token limit, gate time, port).
- Real-mode server moved to port 8082 (8080 is taken by another local service).

## Plan for today
- Write the harness per `../2026-10-22/03_HARNESS_SPEC.md` (game, agents, run, analysis, one test).
- Sanity checks (one-firm price, one-shot), then the pilot; go/no-go gate moved from about 3pm to about 7pm IST (dated note, the pre-registration gives times as approximate).

## Open items
- Author: confirm the submission form is live; claim any compute credits (kept out of the repo docs); write the report text.
