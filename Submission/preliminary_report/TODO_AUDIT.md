# Project audit: what is done and what is left (2026-10-25 midday)

## A. Ablations (06_ABLATIONS.md, items 1-12, H, H2)
| # | Item | Status |
|---|---|---|
| 1 | Known end date | DONE, all four models (5 seeds each) |
| 2 | Notes | DONE: gemma, deepseek, glm53f (5 seeds) |
| 3 | History window | DONE as history none and last round (gemma, deepseek, glm53f); the 20-round window was cancelled |
| 4 | Prompt wording (sell more) | Cancelled as low value; partly covered by the "share" newcomer variant and the pilot `hint` prompt |
| 5 | Swap timing (round 15, 45) | CANCELLED by the author |
| 6 | gpt-oss reasoning effort | CANCELLED (gpt-oss never passes the gate) |
| 7 | Replacement strength | DONE as cross-family swaps and mixed markets |
| 8 | Temperature 0.3 and 1.0 | DONE: gemma and deepseek (3 seeds each) |
| 9 | Number of firms 2, 4, 5 | DONE: gemma and deepseek (2 seeds per size), plus the eight-firm runs |
| 10 | Anchor price in the prompt | NOT DONE (cancelled earlier as low value) |
| 11 | Entry of a new firm | DONE for gemma, deepseek, glm53f (5 seeds; entry at round 31 not 40). Both extra entry variants DONE 2026-10-25 (section 26: qwen3-14b entrant +0.000, scripted-undercutter entrant -0.036) |
| 12 | LLM newcomer variants | DONE: gemma, deepseek (5 seeds); glm53f running at 14 of 25 |
| H | Human plays a firm | DONE 2026-10-25 as a fun research direction: five case-study games (3 firms x3, 5 firms, 10 firms), debriefs by the gemma firms; section 25 of 06_MORE_CELLS |
| H2 | External agent firm | DONE as a small hosted chat model, 2 seeds, descriptive |

So the ablations are done except 10 (anchor), H (human) and the two extra entry variants, all by choice.

## B. Other runs
- glm53f newcomer variants: running, ends about 12:35.
- Gemma main-study seeds 31-40: PAUSED (about 6.5 hours to finish); gives 20 gemma seeds like deepseek.
- Qwen3.8 factor cells (announced, cut, history, notes, entry, probes, newcomers): NOT run (cost); say so in the report.
- Round-1 spread test (PLAN.md "Later"): DONE 2026-10-25 (gemma, 50 seeds; section 24 of 06_MORE_CELLS): the seed spread is not from the opening draw.
- Kimi K3 swap studies: not run (gate only).
- Gemma known end date: only 2 of 5 base runs pass the gate (descriptive).

## C. Analysis and documents
- Figures: DONE, 16 figures (a to p) in figures/ with make_figures.py and make_figures2.py; rerun make_figures2.py after the entry variants finish.
- Pooled effect table with intervals across models, in one place: partly in README and 06_MORE_CELLS; one clean table for the report is still to build.
- `2026/2026-10/2026-10-25/00_SUMMARY.md`: NOT written (end-of-day checklist requires one per day; 2026-10-24 exists).
- `01_DISCLOSURE_LOG.md`: add the sprint additions (hosted models, parity runs, preliminary report) with times.
- `PLAN.md`: status sections are stale (the "Next runs" and "Schedule changes" lists predate the overnight runs); update after the last run.
- README snapshot to `general/readme_history/` and the `README` "Status" line after the last run.
- Decision logs for new runs: re-run `tools/export_decisions.py` into `Submission/supplementary/` (supporting material only).
- `tools/models.ini`: three entries point at deleted files (mistral-nemo, phi-4, nemotron); harmless, or remove them.
- Housekeeping: `data/gemma_more` is partly pushed (seed 31 base, none, clone); `data/agent_ext*` holds the agent prompt files, untracked.

## D. Report and submission (author)
- Write the report on the official template, 8 pages or fewer, from `Submission/preliminary_report/` (rough draft, outline, findings). Abstract 150-250 words, written last.
- Limitations and Dual-Use appendix (draft is in ROUGH_REPORT).
- LLM usage statement (reference draft in `_local/ai_usage_statement.md`; edit to what is true).
- Check every reference against its paper before citing; no invented citations.
- Fix the final title (resubmission needs the same title).
- Read the prize terms and privacy policy (you are a minor: age, consent, payout).
- Submission form fields: title, 150-250 word summary, PDF, publish yes or no, tracks (1 and 3), team name, location, name, email (see `Submission/submission_form_checklist.md`).
- Optional: 3-5 minute video, slides, project image (the main figure).
- Git tag `submitted` after submitting; Zenodo upload after submitting; confirm the links open while logged out.
- Deadline: Mon 26 Oct 17:29 IST (Sun 25 Oct 11:59 PM AoE).
