# Report structure V2 (fits the official template and the 8-page limit)

V1 to V2: V2 uses one pooling per table (headline seeds 11-20 for the main cells (gemma seeds 11-20 and 31-40 since 2026-10-26); all seeds only in Table 2), the 06 numbers recomputed from data/, same n across figures a, b and c, error-aware wording ("in these runs"), the human games, round-1 spread test, glm53f newcomers and gemma entry variants added, and the figure scripts moved to V2/figures (V1 scripts still write to the old path).

Limit: 8 pages before references and appendices (the template recommends about 4; aim 5 to 6), PDF up to 25 MB, abstract 150 to 250 words. Fix the title before the first submission (resubmitting needs the exact same title). Draft main text (Introduction to Code and Data) is about 1,650 words plus Table 1 and four figures, roughly 4.5 to 5.5 pages on the template (estimate; check after typesetting).

| Template section | Pages | Content | Source |
|---|---:|---|---|
| Title, authors | 0.1 | placeholders: title, name, affiliation | author |
| Abstract | 0.25 | 150 to 250 words: problem, design, two numbers, caveat | FINDINGS 2 to 6 |
| 1 Introduction | 0.6 | why model replacement matters; question; numbered contributions | ROUGH_REPORT |
| 2 Related Work | 0.5 | Fish; Keppo (closest); Eschenbaum; Shi; Tewolde; Dietrich and Aharon only as their abstracts say | references.bib, papers/ |
| 3 Methods | 1.0 | game, agents, design (Figure 1), gate, effect, bootstrap, what was preregistered | 03_PREREG.md |
| 4 Results | 2.0 | gate; Figure 2 (price per round); Table 1 and Figure 3 (effects); clone and family; undercutter positive control; communication cut (Figure 4) | FINDINGS 1 to 7 |
| 5 Discussion and Limitations (with Future Work) | 0.6 | what the runs show and do not; assumptions; future work in two lines | APPENDIX C |
| 6 Conclusion | 0.15 | three sentences | |
| 7 Code and Data (with info-hazard note) | 0.15 | repo, tags, data license, what is withheld | README, CITATION.cff |
| Author Contributions (optional) | 0.05 | author alone | |
| References | not counted | the seven checked papers only | references.bib |
| Appendix A to G | not counted | A prompts; B reproduction and versions; C Limitations and Dual-Use (required); D human games and suite as case studies; E data map; F Future Work and Author Contributions; G additional results (factor cells, newcomers, entry, probes, temperature, horizon, firms, mixed, eight firms) | APPENDIX.md |
| LLM Usage Statement | not counted | placeholder, the author writes it (private source `_local/ai_usage_statement.md`) | author |

## Figures
Main text (four): Figure 1 design (fig_f), Figure 2 price per round (fig_a), Figure 3 effects (fig_b), Figure 4 messages cut (fig_c). Appendix (thirteen, A13 swap timing = fig_q): A1 gate on and off (g), A2 heatmap of all effects (h), A3 LLM newcomers (i), A4 entry (k), A5 awareness (j), A6 temperature (l), A7 mixed and eight firms (m), A8 known end (n), A9 number of firms (d), A10 horizon (e), A11 per seed (o), A12 message length (p). Captions: `figures/CAPTIONS.md`.

## Tables
Main text: Table 1 (headline pooling, `RESULTS_TABLE.md`). Appendix: Table 2 all seeds, Table 3 factor cells, Table D1 human games, Table D2 human suite.

## Main text keeps / appendix gets
Keeps: design, gate, clone and family null, undercutter positive control, communication cut, one table of effects. Appendix: factor cells, probes, temperature, entry, horizon, number of firms, newcomer prompts, mixed and eight-firm markets, external agent, round-1 spread test, human games.

## Wording rules
"In these runs / cells", never causal absolutes. The index is a price-level measure ("cartel-like pricing"). Messages are explicit communication, not tacit. Effects are conditional on the 60% gate. Human games and the suite are case studies (one game per cell, author not blinded), a fun research direction, never estimates. State pooling and n in every table and caption. State: bootstrap over base runs, 10000 resamples, seed 0; narrow gemma intervals understate uncertainty; hosted endpoints ignore the seed. Hosted models are the endpoint's labels.

## What only the author can write
Abstract, introduction motivation, discussion, conclusion, author contributions, the title, the LLM Usage Statement, and every sentence rewritten in own words. The draft is a scaffold. Read the prize terms and privacy policy first (the author is a minor).
