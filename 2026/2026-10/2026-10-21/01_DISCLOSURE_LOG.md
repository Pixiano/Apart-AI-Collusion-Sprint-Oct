# Prior-work disclosure and log

Purpose: show what existed before the sprint (2026-10-23) versus what was built during it. Copy the "Pre-sprint" section into the report's "Prior work and setup" note.

## Pre-sprint (before 2026-10-23)
- Planning and question selection only (see 02_PLAN.md).
- Hardware and tooling inventory: local GGUF models already on disk (LM Studio), API keys for hosted endpoint and hosted endpoint.
- This documentation folder.
- No experiment code, no runs, no results, no paper text.
- Starter code to be used, to be listed here when chosen (unverified names from planning: luciasauer/algorithmic_pricing_llms, andyjliu/llm-agent-collusion).

## Log (append new entries, newest last; use date and time)
| Date/time (local) | What | Pre-sprint or sprint |
|---|---|---|
| 2026-10-21 | Read sprint page and rules | Pre-sprint |
| 2026-10-21 | Hardware/tooling inventory | Pre-sprint |
| 2026-10-21 | Question chosen via two-agent debate; plan written | Pre-sprint |
| 2026-10-21 | Doc structure created | Pre-sprint |
| 2026-10-21 | Local git repo (main), README, LICENSE, .gitignore, tag `pre-sprint` | Pre-sprint |
| 2026-10-21 | README history log and snapshot hook; phased schedule and gate rule drafted | Pre-sprint |
| 2026-10-21 | First push to GitHub (main + `pre-sprint` tag) and later push of docs | Pre-sprint |
| 2026-10-21 | Decision: local-only compute; sprint sign-up completed | Pre-sprint |
| 2026-10-21 | Third-party tool installed: llama.cpp build b11798 (prebuilt CUDA 13.4 Windows release, outside the repo) | Pre-sprint |
| 2026-10-21 | `tools/serve.ps1` launcher for a local model server (playground and real modes); no game or experiment code | Pre-sprint |
| 2026-10-21 | `tools/models.ini` model presets (router mode, 7 local models); playground web UI is a locally renamed copy of the llama.cpp built-in web UI (third-party, kept outside the repo) | Pre-sprint |
| 2026-10-21 | `tools/playground/shortcuts.js`: keyboard shortcuts script for the playground UI; no game or experiment code | Pre-sprint |
| 2026-10-22 | `tools/serve.ps1` `-Lan` option and 32k context settings in `tools/models.ini`; UI copy patched to send gpt-oss its native reasoning level; no game or experiment code | Pre-sprint |
| 2026-10-22 | `03_PREREG.md` pre-registration draft written; no code or data | Pre-sprint |
| 2026-10-22 | Downloaded and read (abstract and introduction) six related papers (Fish; Keppo; Eschenbaum; Shi; Dietrich; Aharon), local only, listed in `papers/README.md`; literature notes and a paper-only harness spec written; no code | Pre-sprint |
| 2026-10-22 | Downloaded and read a seventh paper, Tewolde et al. (CoopEval), local only; analysis written; no code | Pre-sprint |
| 2026-10-22 | Read starter repos' metadata only (LLMCartel, focal-points, LLM-Trust-Breaking): none has a license, nothing cloned, no code used | Pre-sprint |
| 2026-10-23 | Morning, before the begin marker: deeper reading of all seven related papers (including appendices of Fish, Keppo, Shi, CoopEval), an exploratory ablation list (`ABLATIONS.md`, `06_ABLATIONS.md`) and literature-note updates; reading and planning only, no code, data or results | Pre-sprint (planning) |
| 2026-10-23 | `pre-sprint` tag moved to the last commit before the begin marker; sprint begun at 13:15 IST by the author; tag `sprint-start` | Sprint |
