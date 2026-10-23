# Does the Cartel Survive Turnover?

Entry to the [Apart Research AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25) (2026-10-23 to 2026-10-25), solo.

**Status:** sprint in progress (begun 2026-10-23). The harness is being written; no experiment runs or results exist yet. This file is updated as the sprint progresses. See [PLAN.md](PLAN.md) for the plan.

## Research question

Once a group of LLM pricing agents has settled into tacit or explicit collusion, what happens when members are replaced mid-episode? Does collusion persist, and do the remaining agents notice?

The claim is deliberately narrow: *collusion persistence under agent replacement, as a stylised model of model updates.* It is not a claim about real markets. Addresses sprint questions 1.2 and 3.3.

## Planned design

- Repeated Bertrand pricing game, 3 LLM agents, 60 rounds, swap at round 30.
- Swap types: none (control), fresh clone with no memory, different-family model, scripted undercutter.
- Other factors: 1 vs 2 of 3 agents replaced, hidden vs announced swap, communication on or off.
- Metric: collusion index `(mean price - Nash) / (monopoly - Nash)` before and after the swap, plus re-convergence time. Awareness is measured by price shift against the no-swap control.
- Gating: only (model, framing) cells that collude before the swap enter the swap analysis; the per-model pass rate is reported as a result.
- 10+ seeds per cell, bootstrap confidence intervals, no-swap control.
- Models: local open models only (llama.cpp / local OpenAI-compatible server on one 16 GB GPU).

**Fallback:** if no model colludes in the pilot, switch to a plus-factor collusion detection study using a scripted cartel for positives.

## Prior work and disclosure

The sprint requires disclosing prior work. Everything before 2026-10-23 is planning and tooling inventory only, recorded with timestamps in [`2026/2026-10/2026-10-21/01_DISCLOSURE_LOG.md`](2026/2026-10/2026-10-21/01_DISCLOSURE_LOG.md). The git tag `pre-sprint` marks the last commit before the sprint began. Third-party starter code, once used, will be listed in that log and in the report.

## Repository layout

```
harness/                      the game and the agents: game, agents, play, swaps, run, analyze
tests/                        checks (python tests/test_game.py)
tools/                        local server launcher, model presets, pilot launcher
data/                         run output (pilot and main; data/dev is scratch and ignored)
general/                      READMEs and notes not tied to one day
YYYY/YYYY-MM/YYYY-MM-DD/      daily work log; each day has 00_SUMMARY.md
PLAN.md, ABLATIONS.md         plan and the exploratory ablation sheet
```

## Ethics and dual-use

The work documents how agent collusion persists or breaks. Only the experiment harness and aggregate results will be released. The collusion-eliciting prompts used in the literature are already public; this project frames its findings defensively, for auditors and market designers. A full limitations and dual-use appendix will accompany the report.

## Credits and references

This project builds on the work of others and credits it: [`references.bib`](references.bib) lists every paper, repository, tool and model used or consulted, with links. Third-party code is not copied into this repository (the starter repositories named on the sprint page have no license, so none of their code is used), and downloaded papers are kept locally and not redistributed (see [`papers/README.md`](papers/README.md)). Model and tool licenses are those of their own pages.

## License

MIT, see [LICENSE](LICENSE).
