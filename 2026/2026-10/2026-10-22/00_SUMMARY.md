# 2026-10-22 (Thu) - Daily summary

Sprint: Apart Research AI Collusion Sprint, starts 2026-10-23. Today is the last pre-sprint day, setup and planning only.

## Done today
- Playground server: 32k context per chat (1 slot; real-run mode keeps 4 slots of 8k), an opt-in `-Lan` switch in `tools/serve.ps1` (off by default, playground only), and the UI sends gpt-oss its native low/medium/high reasoning level instead of a token cap. Tooling only.
- Wrote a pre-registration draft (`../2026-10-21/03_PREREG.md`: fixed game, gate, outcomes, exclusions). No code or data.
- Re-read the sprint page: found the report template, starter repos and Oct 22 talks. The three starter repos (LLMCartel, focal-points, LLM-Trust-Breaking) have no license, so none of their code is used (see the disclosure log, `../2026-10-21/01_DISCLOSURE_LOG.md`).
- Project Python environment (`.venv`, gitignored) with openai, numpy, pandas, matplotlib. No game code.
- Wrote the report skeleton (`01_REPORT_SKELETON.md`) from the official template's section list, then added the judging rubric, the 8-page maximum and the required ethics appendix after reading the sprint page Guidelines tab.
- Downloaded six related papers (kept locally, not committed; list in `papers/README.md`), read abstracts and introductions, wrote `02_LITERATURE_NOTES.md` (closest work: Keppo et al. 2026, which uses fixed heterogeneity, not replacement mid-run).
- Read the design sections of the papers and wrote `04_PAPER_INSIGHTS.md` (theory, methods and risks drawn from them; expectations written before any data, labelled exploratory). Changed the harness spec: the agents are not told the number of rounds, long-run-profit prompt, one-firm and one-shot sanity checks.
- Wrote the harness spec on paper (`03_HARNESS_SPEC.md`). No code.
- Fixed `02_PLAN.md`: abstract is 150 to 250 words (the plan said 150 or fewer).
- Froze the pre-registration (`prereg-v1` tag) and refreshed the `pre-sprint` tag.

## NOT done today (important for the prior-work disclosure)
- No experiment code, simulations, model runs, results or data.
- No starter repos cloned or run.

## Open items
- Author: review and freeze the pre-registration; copy the official report template; confirm the submission form is live (page shows both "Starts Oct 23" and "submission window has closed").

## Files in this folder
- 00_SUMMARY.md - this file
- 01_REPORT_SKELETON.md - report outline following the official template
- 02_LITERATURE_NOTES.md - what the six related papers did and how this differs
- 03_HARNESS_SPEC.md - how to build the harness (paper only)
- 04_PAPER_INSIGHTS.md - what the papers give us: theory, methods, risks, expectations
