# Supplementary documentation

The submitted report is short (8 pages at most). This file points to everything behind it, so anyone who wants more can find it quickly. It is kept up to date in the repository; it is not part of the submission itself and is cited in the report as supplementary documentation.

## Read in this order

| If you want | Read |
|---|---|
| The whole project in 5 minutes | [`README.md`](README.md) (figures, results tables, findings, limitations) |
| The report draft and its numbers | [`Submission/preliminary_report/V2/`](Submission/preliminary_report/V2): [`ROUGH_REPORT.md`](Submission/preliminary_report/V2/ROUGH_REPORT.md), [`FINDINGS.md`](Submission/preliminary_report/V2/FINDINGS.md) (19 numbered results), [`RESULTS_TABLE.md`](Submission/preliminary_report/V2/RESULTS_TABLE.md), [`APPENDIX.md`](Submission/preliminary_report/V2/APPENDIX.md) (prompts, commands, limitations, human games, data map), [`figures/CAPTIONS.md`](Submission/preliminary_report/V2/figures/CAPTIONS.md) |
| Every result, in order, with its source folder | [`2026/2026-10/2026-10-24/06_MORE_CELLS.md`](2026/2026-10/2026-10-24/06_MORE_CELLS.md) (sections 1 to 27) |
| What was planned and what changed | [`03_PREREG.md`](2026/2026-10/2026-10-21/03_PREREG.md) (frozen at tag `prereg-v1`, deviations appended), [`01_DISCLOSURE_LOG.md`](2026/2026-10/2026-10-21/01_DISCLOSURE_LOG.md), [`PLAN.md`](PLAN.md) |
| What each day produced | `2026/2026-10/<day>/00_SUMMARY.md` for 21 to 25 October |
| The raw data | [`data/README.md`](data/README.md) (every folder, the experiment it belongs to, partial and cancelled runs) |
| How to rerun it | README "Reproduce", [`requirements.txt`](requirements.txt), [`tests/`](tests) |
| The first draft of the report | [`Submission/preliminary_report/V1/`](Submission/preliminary_report/V1) (kept as a record; V2 supersedes it) |
| What is still open | [`Submission/preliminary_report/TODO_AUDIT.md`](Submission/preliminary_report/TODO_AUDIT.md) |

## What is in the study

- The main question, a frozen design and a narrow claim: collusion persistence under agent replacement in a repeated three-firm pricing game, with four swap types, hidden or announced, one or two firms replaced.
- Models: gemma4-12b (local), DeepSeek V4.1 Flash, Qwen3.8 and GLM-5.3-Flash (hosted), Kimi K3 (gate only), plus an external agent (a small hosted chat model) and a human as one firm.
- Ablations and extra cells: history window, notes, known end date, temperature, number of firms, horizon, entry of new firms (same model, another family, a scripted undercutter), LLM newcomer prompts, awareness probes, mixed-family markets, eight firms, a round-1 spread test, and a communication cut.
- A fun research direction, outside the preregistered study and never pooled with it: nine games in which the author plays one firm against gemma firms (3, 5 and 10 firms, four information conditions), with the AI firms' own debriefs at the end.

## Quality checks

On 2026-10-25 four read-only auditors (a leak and privacy check, a number-integrity check, a documents-consistency check and a report-readiness check) went over the repository. They found no secrets and no mismatched headline numbers; every stale status line, undisclosed deviation and overclaim they found was fixed or disclosed. The numbers in the README and the results note were recomputed from `data/` with the scripts in [`analysis/`](analysis). The tests in [`tests/test_game.py`](tests/test_game.py) cover the game rules and the harness.

## Conventions used in every document

- Collusion index = (mean price - 10) / 45; effects are branch minus the same base run's no-swap branch, over rounds 31 to 60 unless a table says otherwise; bootstrap over base runs, 10,000 resamples, seed 0.
- Two poolings exist and each table says which it uses: seeds 11 to 20 for the headline cells, all seeds in the appendix tables.
- Everything after the frozen plan is exploratory and logged as a dated deviation.
- Human games and the information suite are case studies (one game per cell, author not blinded), never estimates.
- Hosted models are called hosted endpoints; the hosted endpoint ignores the seed, so hosted runs are replicates and not reproducible bit for bit.

## Maintenance log

| Date | Change |
|---|---|
| 2026-10-25 | Repository audit and clean-up; report remade as V2 (V1 archived); data map, requirements and citation file added; README redesigned with figures; this file added. |
| 2026-10-25 | Gemma runs planned overnight: main-study seeds 31 to 40, plus communication-cut clone, entry (one and two new firms) and the myopic newcomer variant on the same seeds (thin cells found by the coverage check). Results will be added to the results note and this log. |
