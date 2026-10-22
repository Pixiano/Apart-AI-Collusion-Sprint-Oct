# Report skeleton (follows the official template; structure only, no results)

Template: https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing (make your own copy, delete all guidance text and the info box before submitting).
Length: the sprint page allows a maximum of 8 pages excluding references and appendices; the template recommends about 4 (Introduction + Related Work 1 page, Methods + Results 2.5, Discussion 0.5). Aim for 4 to 5 and keep it tight. PDF, up to 25 MB. Abstract 150 to 250 words. The template asks that the report is primarily written by the author; use AI help for checking and code, and say so in the LLM usage statement.

Working title: Does the cartel survive turnover? Collusion persistence under agent replacement in a repeated pricing game (stylised model of model updates)

## What judges score (sprint page Guidelines tab, each 1 to 5)
- Impact Potential and Innovation: important or neglected problem, original approach, new rather than a replication of recent work, clear theory of change.
- Execution Quality: sound method, convincing validation, results that support the conclusions, limitations acknowledged.
- Presentation and Clarity: easy to follow, problem, method, findings and limitations all present, no key information buried.
- Rewarded: acknowledged limitations, variance, seeds, baselines, and a positive control. Penalised: made-up results or references, undisclosed prior work.
- Required appendix: "Limitations and Dual-Use / Ethical Considerations": what the result does and does not establish, and any way the setup could make real-world collusion easier to carry out or harder to detect.
- Our controls: the no-swap branch is the baseline; the scripted undercutter is the positive control (it should break collusion by construction); report seeds and bootstrap intervals.

## Front matter
- Author, affiliation (school or independent), event credit: AI Collusion Research Sprint, October 2026.
- Abstract, 150 to 250 words, written last: problem, approach, key result with numbers, takeaway.

## 1. Introduction
- Problem: LLM pricing agents can sustain supra-competitive prices; deployed models get replaced (updates, swaps). Does collusion survive replacement?
- Why it matters (market-manipulation and oversight angle). Threat model: tacit collusion without explicit instruction.
- Contributions (numbered, filled from results only).

## 2. Related Work
- Verified citations only (read before citing). Candidates to read: Eschenbaum et al. 2022; Keppo et al. 2026 (arXiv 2603.20281); Aharon et al. 2026 (arXiv 2601.22184); LLMCartel and focal-points repos (no license, ideas only).
- How this differs; the gap.

## 3. Methods
- Game (from 03_PREREG.md): 3 firms, prices 10 to 100, cost 10, demand 100 - P, 60 rounds; collusion index.
- Agents: local models via llama.cpp (pinned build b11798), sampling settings, prompt (appendix).
- Design: base run to round 30, checkpoint, paired branches (control, clone, different-family, scripted undercutter, ...).
- Gate and exclusions as pre-registered. What did not work (pilot, prompt change).
- Prior work and setup note (from 01_DISCLOSURE_LOG.md, Pre-sprint section).

## 4. Results
- Gate pass rates per model. At least one figure: collusion index over rounds with the swap marked, by swap type.
- Primary outcome table: post-swap CI minus control, 95% bootstrap CI, per swap type and model.
- Secondary: re-convergence time, parse-failure rate. Observations separated from interpretation.
- Exploratory results labelled as such.

## 5. Discussion and Limitations
- Implications, limits (small models, one game, stylised swap, integer-grid ties, few seeds), what would change the conclusion, future work.

## 6. Conclusion (1 to 2 paragraphs)

## 7. Code and Data
- https://github.com/Pixiano/Apart-AI-Collusion-Sprint-Oct, tags `pre-sprint`, `sprint-start`, `submitted`. Info-hazard note (low risk: toy pricing game).

## 8. Author Contributions (optional)

## 9. References (one consistent format)

## 10. Appendix: prompts, full parameters, per-seed plots, and the REQUIRED "Limitations and Dual-Use / Ethical Considerations" appendix

## 11. LLM Usage Statement
- Which tools helped with what (planning debate, coding, checking), confirmation that every claim and citation was verified by the author.

## Fallback version (if the pilot fails the gate and we switch to the plus-factor detector study)
Same sections; Methods describes the scripted-cartel positives and the detector; Results report detection rates and false positives.
