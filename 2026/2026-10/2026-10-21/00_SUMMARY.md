# 2026-10-21 (Wed) - Daily summary

Sprint: Apart Research AI Collusion Sprint, starts 2026-10-23. Today is pre-sprint, planning only.

## Done today
- Read the sprint page. Rules found: building on existing work is allowed but must be disclosed; undisclosed prior work can lead to disqualification; AI tools allowed; page says nothing about starting early.
- Checked hardware: RTX 5060 Ti 16 GB, 31 GB RAM, Ryzen 5 7600X. hosted-endpoint API keys set.
- Found local GGUF models in LM Studio (Qwen3-8B, Qwen3-14B, Gemma-4-12B, gpt-oss-20b). llama-server/llama-cli not on PATH (location unconfirmed).
- Two AI agents each proposed and debated a research question. Chosen: cartel turnover (see 02_PLAN.md). Fallback: plus-factor detector.
- Set up this folder structure, README, MIT license, .gitignore, local git repo on main, GitHub remote, tag `pre-sprint`.
- README history log (general/readme_history/) with an automatic pre-commit snapshot hook (local only).
- Drafted the phased schedule, go/no-go gate and fallback rule (see 02_PLAN.md). Pre-registration file still to be written (03_PREREG.md, planned before Oct 23).

- Signed up for the sprint.
- Decided compute is local-only (no paid or hosted APIs).
- Installed a pinned llama.cpp build (b11798, CUDA 13.4 prebuilt, third-party tool) in one shared location outside the repo, and wrote `tools/serve.ps1` + `tools/models.ini`, a launcher for a local model server in router mode: a playground (port 8081, web UI with a picker for 7 local models, renamed "Collusion Playground") and a real-run server (port 8080, locked until 2026-10-23). Tooling only.

## NOT done today (important for the prior-work disclosure)
- No experiment code written (the launcher script only starts a model server; no game, agents, episodes or metrics).
- No simulations or model runs.
- No results, data, or paper text produced.
- No starter repos cloned or run.

## Open items
- Page shows "Starts Oct 23" but also "submission window has closed": confirm with Apart (Discord/email) that submission is open.
- Confirm llama.cpp CUDA build location (or use a local OpenAI-compatible server instead).
- Check rate limits and test keys for the free-tier APIs; collect exact starter-repo links and licenses from the sprint page (read only).
- Find the official report template link.

## Files in this folder
- 00_SUMMARY.md - this file
- 01_DISCLOSURE_LOG.md - prior-work disclosure and timestamped log
- 02_PLAN.md - chosen question and weekend plan
