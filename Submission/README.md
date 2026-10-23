# Submission folder

- `report/`: the report draft (written by the author, on the official template). Only the final PDF is uploaded to the sprint.
- `supplementary/decisions/`: raw per-run logs of every model decision (round, firm, price, message, reasoning), one CSV per run. Supporting material only, not part of the sprint upload.
- The official template PDF is kept here for reference.

Regenerate the decision logs after new runs: `python tools/export_decisions.py Submission/supplementary/decisions <run_dir> [...]`. Raw JSON logs live in `data/pilot/` and `data/additional/`.
