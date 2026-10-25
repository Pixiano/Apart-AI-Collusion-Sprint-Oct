# Report structure (maps the official template and the judging rubric)

Limit: 8 pages before references and appendices (aim 4 to 5), PDF up to 25 MB, abstract 150 to 250 words. Title: fix it before first submission (resubmitting needs the exact same title).

| Section | Pages | Content | Rubric item | Source files |
|---|---:|---|---|---|
| Abstract | 0.25 | Problem, approach, 2 numbers, takeaway (write last) | Presentation | FINDINGS.md |
| 1 Introduction | 0.5 | LLM pricing agents sustain high prices; models get swapped; question; contributions | Impact | skeleton, literature notes |
| 2 Related work | 0.5 | Fish et al.; Keppo et al. (closest); Eschenbaum et al.; Shi et al.; CoopEval; Dietrich; Aharon et al.; organiser question 1.2 | Impact, no fabricated citations | 02_LITERATURE_NOTES.md |
| 3 Methods | 1 | Game, models, base-run-to-checkpoint-to-branches design, swaps, gate, switches, prompt in appendix | Execution | 03_PREREG.md, 03_HARNESS_SPEC.md |
| 4 Results | 2 | Gate table; main figure (price vs round, swap at 30); effect table by model; factor cells; mixed markets; eight firms; probes; ablations | Execution | 06_MORE_CELLS.md, README tables |
| 5 Discussion and limitations | 0.5 | What it means for model updates, what does not follow, limits | Execution, Presentation | FINDINGS.md caveats |
| 6 Conclusion | 0.25 | Three sentences | Presentation | |
| 7 Code and data | 0.1 | Repo, tags pre-sprint, sprint-start, prereg-v1, submitted | Rewarded: undisclosed prior work penalised | 01_DISCLOSURE_LOG.md |
| References | - | Only the papers read (see literature notes) | no made-up references | |
| Appendix A | - | Prompts and parameters | Execution | agents.py, 03_HARNESS_SPEC.md |
| Appendix B | - | Per-seed plots, all condition tables | Execution | README, 06_MORE_CELLS.md |
| Appendix C (required) | 0.5 | Limitations and dual-use: what it does and does not establish; can the setup make collusion easier or harder to detect | required | below |
| LLM usage statement | 0.25 | Which tools helped with what; author verified every claim | required by template | `_local/ai_usage_statement.md` (private, paste in) |

## Figures to make (from existing data, no new runs)
1. Mean price per round, one panel per model, lines for no swap / clone / family / undercutter k=1 / k=2, vertical line at round 30 (data/main, data/glm, data/qwen).
2. Bar chart: effect with interval, by model and swap type (the effect table).
3. Communication cut: clone effect by market (gemma -0.207, deepseek -0.222, mixed with gemma -0.605).
4. Optional: gate pass rate by model and communication on/off.

## What only the author can write
Abstract, introduction motivation, discussion of meaning, conclusion, author contributions, the choice of title, and every sentence you rewrite in your own words. The rough draft is a scaffold. Read the prize terms and the privacy policy first (you are a minor: age, consent and payout rules).
