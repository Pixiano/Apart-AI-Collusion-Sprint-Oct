# Plan

## Goal
Solo entry to the Apart AI Collusion Sprint (2026-10-23 to 10-25). Priorities: exposure first, prize money second.

## Chosen question
Does a colluding group of LLM pricing agents keep colluding when members are replaced mid-episode? (sprint questions 1.2 + 3.3)
Claim wording: "collusion persistence under agent replacement, as a stylised model of model updates". Not a claim about real markets.

## Design
- Repeated Bertrand pricing game, 3 agents, 60 rounds, swap at round 30.
- Swap types: none (control), fresh clone (memory wiped), different-family model, scripted undercutter.
- Other factors: 1 vs 2 of 3 replaced, hidden vs announced, communication on/off.
- Metrics: collusion index (mean price - Nash) / (monopoly - Nash) before and after swap; re-convergence time; awareness as price shift vs control (self-report only as cheap talk).
- Gating: only (model, framing) cells with pre-swap collusion above a threshold enter the swap analysis; report per-model pass rate.
- 10+ seeds per cell, bootstrap CIs, no-swap control.

## Resources
Local-only: GGUF models on one 16 GB GPU (Qwen3-8B/14B, Gemma-4-12B, gpt-oss-20b on disk). No paid or hosted APIs ($0 budget). Keep the setup simple (one game, one manipulation), with short structured model outputs and a smaller grid to fit local throughput.

## Weekend (sprint days only)
- Fri 10-23: harness, pilot gate (does any model collude with no swap?). If none, switch to fallback.
- Sat 10-24: main sweep in background; write intro/method.
- Sun 10-25: analysis, figures, paper, ethics appendix, README; submit early afternoon, deadline 11:59 PM AoE.

## Phases
- **Phase 0 (Wed 10-21 to Thu 10-22), planning and setup only, no experiment code:** confirm submission form and template; locate llama.cpp or use a local server; read rate limits and test keys; write 03_PREREG.md; draft report skeleton (verified citations only); create a Python venv; commit and refresh tags; ask before pushing.
- **Phase 1 (Fri 10-23):** tag `sprint-start`; write harness; pilot of about 24 episodes; go/no-go gate around 3pm.
- **Phase 2 (Sat 10-24):** main sweep in the background; write intro, related work, methods. If quotas bite, drop conditions from the bottom: 2-of-3 replaced, announced swap, comm off.
- **Phase 3 (Sun 10-25):** analysis, figures, report, ethics appendix; submit early afternoon (deadline 11:59 PM AoE).

## Gate and fallback rule
GO if at least one (model, framing) cell has pre-swap collusion index >= 0.5 in at least 2 of 3 pilot seeds. If none passes after one logged prompt change, switch to the fallback by 4pm Friday. Pilot data is not pooled with main results.

## Fallback
Plus-factor collusion detector (messages-only vs actions-only vs plus-factor report) using a scripted cartel for positives.

## Rules to respect
- Disclose all prior work in the report (see 01_DISCLOSURE_LOG.md).
- Report needs: PDF on official template, abstract 150 to 250 words, maximum 8 pages excluding references and appendices (the template suggests about 4); judged on Impact and Innovation, Execution Quality, Presentation and Clarity (see 2026-10-22/01_REPORT_SKELETON.md), Limitations and Dual-Use/Ethics appendix.
- Never fabricate results or references.
