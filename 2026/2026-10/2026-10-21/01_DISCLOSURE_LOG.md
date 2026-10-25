# Prior-work disclosure and log

Purpose: show what existed before the sprint (2026-10-23) versus what was built during it. Copy the "Pre-sprint" section into the report's "Prior work and setup" note.

## Pre-sprint (before 2026-10-23)
- Planning and question selection only (see 02_PLAN.md).
- Hardware and tooling inventory: local GGUF models already on disk (LM Studio), API keys for hosted endpoints (unnamed).
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
| 2026-10-24 | Hosted models used through a hosted endpoint (deepseek-v4-1-flash, Qwen3.8, GLM-5.3-Flash; Kimi K3 gate only), address and key in untracked `.env` files; swap studies, factor cells and more seeds | Sprint |
| 2026-10-24 | Mixed-family markets (three models in one market), eight-firm runs (two copies of each of four models), external-agent firm (a small hosted chat model, 2 seeds) | Sprint |
| 2026-10-24 | Ablations and probes: temperature, entry of new firms, known end date, notes, history none and last round, communication cut; results in `06_MORE_CELLS.md`, each logged in `03_PREREG.md` as an exploratory addition | Sprint |
| 2026-10-25 | Overnight gap-fill runs, awareness probes, LLM newcomer variants, 120-round horizon, number of firms (2, 4, 5) | Sprint |
| 2026-10-25 | Parity runs (deepseek temperature, number of firms and horizon; glm53f entry and probe; gemma newcomers) | Sprint |
| 2026-10-25 | Preliminary report folder `Submission/preliminary_report/` (findings, structure, rough report, audit), figures and pooled results table made from `data/`; README, plan and tools cleanup | Sprint |
| 2026-10-25 | Afternoon, fun research direction (case studies, not estimates): human games 1 to 5, the author as one firm against gemma4-12b firms through the external-agent file hook (3 firms three times, 5 firms, 10 firms); gemma firms debriefed after games 4 and 5 (`tools/debrief.py`); game 5 stopped by mistake at round 13 and resumed with two firms on an agree-with-the-human prompt (`RESUME_AGREE`, exploratory, game 5 only) | Sprint |
| 2026-10-25 | Harness extended to up to ten firms (labels and number words); terminal player `tools/play_human.py` | Sprint |
| 2026-10-25 | Round-1 spread test on gemma4-12b, 50 seeds (147 of 150 opening replies are 50) | Sprint |
| 2026-10-25 | Gemma entry variants: a qwen3-14b entrant and a scripted-undercutter entrant (seeds 11, 13-16), reported for rounds 31-60 and 46-60 | Sprint |
| 2026-10-25 | glm53f newcomer variants: 21 of 25 branches finished, the hosted credit ran out in seed 25 and the unfinished branches were deleted | Sprint |
| 2026-10-25 | Gemma main-study seeds 31-40 attempted and paused after seed 31 (base, none, clone); nothing from it is reported | Sprint |
| 2026-10-25 | Evening, human suite (fun research direction, case studies): the author as firm C in four information conditions, one game each (normal, no history, no messages, neither) | Sprint |
| 2026-10-25 | Evening, audit by four read-only reviewers (leaks, numbers, documents, report readiness) and the fixes that followed: official template PDF untracked, provider names unnamed in tracked text, a home path removed, `tools/models.ini` untracked (an example file kept), the external-agent data folders renamed, this log, README, plan and results note refreshed; the report drafts are rebuilt as `Submission/preliminary_report/V2` (V1 kept as the record of the first draft) | Sprint |
