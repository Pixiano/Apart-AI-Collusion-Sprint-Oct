# Submission folder

- `report/`: the final report PDF goes here (written by the author, on the official template). Only the final PDF is uploaded to the sprint.
- `supplementary/decisions/`: raw per-run logs of every model decision (round, firm, price, message, reasoning), one CSV per run. Supporting material only, not part of the sprint upload.
- The official template PDF is kept here for reference.

Regenerate the decision logs after new runs: `python tools/export_decisions.py Submission/supplementary/decisions <run_dir> [...]`. Raw logs live in `data/`; `data/README.md` lists every folder (main, hist0, hist1, notes, horizon, kimi, qwen, glm, mixed, mixed_g, mixed_h0, more_ds, eight_a, eight_b, external_agent, gemma_more, long, long_ds, nfirm, nfirm_ds, temp03, temp10, temp03_ds, temp10_ds, round1, human, human_suite, pilot, easy, median, additional) and what it is.

Supplementary decision logs (per-run CSVs of every price, message and reasoning text; not part of the sprint upload): `supplementary/decisions` (pilot), `decisions_easy`, `decisions_median`, `decisions_pilot_nemotron_off`, `decisions_main` (swap study).
