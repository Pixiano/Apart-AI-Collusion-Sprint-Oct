# AI_Collusion

Apart Research AI Collusion Sprint entry (2026-10-23 to 2026-10-25).

## Layout
- `YYYY/YYYY-MM/YYYY-MM-DD/` - daily folders, any number of files each
- Every daily folder has `00_SUMMARY.md` that sums up the day (mandatory)
- `general/` - READMEs and anything not tied to one day

## Conventions
- Log pre-sprint vs sprint work in the daily `01_DISCLOSURE_LOG.md` pattern; copy into the report's prior-work note.
- Never fabricate results or references.

## README history
`general/readme_history/` holds a dated snapshot of each README (`README.md`, `general/README.md`) every time a commit changes it, named `YYYY-MM-DD_HHMM_<name>.md`. A local git pre-commit hook (`.git/hooks/pre-commit`, not pushed) makes the snapshot automatically from the staged version, so the newest file is the committed version. If the hook is missing (fresh clone), copy by hand. `git commit --no-verify` skips it. Git history also tracks changes; this folder is the human-readable log.
