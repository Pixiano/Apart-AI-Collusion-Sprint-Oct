# 2026-10-22 (Thu) - Daily summary

Sprint: Apart Research AI Collusion Sprint, starts 2026-10-23. Today is the last pre-sprint day, setup and planning only.

## Done today
- Playground server: 32k context per chat (1 slot; real-run mode keeps 4 slots of 8k), an opt-in `-Lan` switch in `tools/serve.ps1` (off by default, playground only), and the UI sends gpt-oss its native low/medium/high reasoning level instead of a token cap. Tooling only.
- Wrote a pre-registration draft (`../2026-10-21/03_PREREG.md`: fixed game, gate, outcomes, exclusions). No code or data.
- Re-read the sprint page: found the report template, starter repos and Oct 22 talks. The three starter repos (LLMCartel, focal-points, LLM-Trust-Breaking) have no license, so none of their code is used (see the disclosure log, `../2026-10-21/01_DISCLOSURE_LOG.md`).
- Project Python environment (`.venv`, gitignored) with openai, numpy, pandas, matplotlib. No game code.
- Wrote the report skeleton (`01_REPORT_SKELETON.md`) from the official template's section list.

## NOT done today (important for the prior-work disclosure)
- No experiment code, simulations, model runs, results or data.
- No starter repos cloned or run.

## Open items
- Author: review and freeze the pre-registration; copy the official report template; confirm the submission form is live (page shows both "Starts Oct 23" and "submission window has closed").
- Refresh the `pre-sprint` tag at the end of today.

## Files in this folder
- 00_SUMMARY.md - this file
- 01_REPORT_SKELETON.md - report outline following the official template
