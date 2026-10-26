# DRAFT for the author to rewrite in their own words (the report must be mainly your own text)

Everything in square brackets is yours to fill or replace. Numbers: Table 1 of `RESULTS_TABLE.md` (headline pooling) and `FINDINGS` items 1 to 7. Figures: `figures/CAPTIONS.md`.

# [Title: placeholder. Fix it before the first submission; resubmitting needs the exact same title]

[Author name], [affiliation or "independent"]. AI Collusion Research Sprint, Apart Research, October 2026.

## Abstract (150 to 250 words; write last)
[Draft, about 200 words] Pricing agents built on language models can keep prices above the competitive level, and deployed models are updated or swapped. We ask whether a cartel-like price level that has formed among language-model firms survives when one or two firms are replaced. In a repeated three-firm Bertrand game (60 rounds, prices 10 to 100, cost 10) we run 30 rounds, save a checkpoint, and replay rounds 31 to 60 from the same checkpoint with paired branches: no swap, a fresh copy of the model with its history wiped, a model from another family, and a scripted undercutter as the positive control. Across four models (gemma4-12b run locally; deepseek-v4-1-flash, qw38 and glm53f through a hosted endpoint), in the runs that reached cartel-like pricing, a fresh or foreign newcomer changed the price index by between -0.005 and +0.060 (from fresh copies, about zero, up to a small rise when DeepSeek's firm is replaced by another model), while one undercutter lowered it by 0.05 to 0.30 and two by about 0.3. Without messages, cartel-like pricing was rare (1 of 5, 0 of 10 and 1 of 5 runs), and when messages were cut at the swap a fresh clone lowered the index by about 0.2 (gemma -0.269, deepseek -0.222, glm53f -0.325). Results are conditional on a gate, come from small samples, and are partly exploratory.

## 1 Introduction
[Your motivation. Draft:] Language-model agents are starting to set prices, and the model behind an agent is changed when its provider updates it. If a cartel-like price level survives a replacement, a model update would not break it; if it does not, a swap could. The sprint's question 1.2 notes that no study yet replaces models in the middle of a run and asks whether newcomers re-form the collusion. We build a small harness and ask the question in a toy game.

Contributions:
1. A paired-branch design: one base run, one checkpoint, several replacement branches replayed from it, so each effect is measured against the no-swap branch of the same run, with a gate that says which runs enter the analysis.
2. Results on four models: in these cells a fresh clone or a model from another family did not move the price index, a scripted undercutter did, and the size of that damage differed strongly by model.
3. A messages result: in these runs cartel-like pricing was rare without messages, and a clone plus a message cut lowered the index by about 0.2.
4. Exploratory additions (appendix): mixed markets, group size, entry, prompts for newcomers, awareness probes, and human-firm case studies.

## 2 Related Work
[Check each description against the paper before you keep it; the seven papers in `papers/` are all cited.]
Fish, Gonczarowski and Shorrer (2024) report that language-model pricing agents quickly reach supracompetitive prices and that small prompt changes matter. Keppo, Li, Tsoukalas and Yuan (2026) show in a stylised model and in experiments with open-source agents that collusion is fragile under heterogeneity (patience, data access, more agents, Q-learning counterparts); heterogeneity is fixed from the start of a run, which is the closest prior work. Eschenbaum, Mellgren and Zahn (2022) find that reinforcement-learning agents with collusive policies fall back to static Nash play against counterparts they did not train with. Shi et al. (2026) study agents that announce actions before acting and find that different models read announcements as binding or as cheap talk. Tewolde et al. (2026) report that cooperation from repetition deteriorates when co-players vary. Dietrich (2026) studies whether models identify peers from text style and Aharon et al. (2026) study coordination without communication; we cite them only for the question of whether agents can tell who they play. None of these replaces a member of an established group in the middle of a run with paired branches from one checkpoint.

## 3 Methods
**Game.** Three firms, 60 rounds. Each round every firm picks an integer price from 10 to 100; demand is max(0, 100 - P) units at the lowest price, shared equally between firms tied at the lowest price; cost is 10, so the monopoly price is 55. Each firm sees all past prices and its own profits, and each round sends a message of up to 30 words that the others read next round.
**Index.** CI = (mean price - 10) / 45 over firms and rounds of a window (0 competitive, 1 monopoly price). It is a price-level measure; "cartel-like pricing" means CI near 1.
**Agents.** One model per firm, same prompt (Appendix A). gemma4-12b ran locally (llama.cpp b11798, temperature 0.7, thinking off); deepseek-v4-1-flash (thinking off), qw38 (thinking off) and glm53f (low reasoning effort, it cannot be switched off) ran through a hosted endpoint, with the endpoint's model labels; the endpoint ignores the seed, so those runs are independent replicates.
**Design (Figure 1).** Rounds 1 to 30 form the base run; its state is saved at round 30. Branches replay rounds 31 to 60: no swap; clone (a fresh agent, history wiped); family (a different model, history visible); scripted undercutter (one cent below the lowest price of the last round, floor 10, the positive control). One firm (C) or two firms (B and C) are replaced. Variants (announced swap, messages cut from round 31, history shorter, notes, known end, entry, LLM newcomers) are in the appendix.
**Gate and effect.** A base run is gated if CI over rounds 16 to 30 is at least 0.5; a model and communication setting is analysed if at least 60% of its runs pass. Effect = CI(31-60) of a branch minus CI(31-60) of the same run's no-swap branch (for message-cut branches, the no-swap branch with messages also cut). Intervals are 95% percentile bootstrap over base runs, 10000 resamples, seed 0. Narrow gemma and qw38 intervals come from near-identical runs and understate uncertainty. All effects are conditional on the gate.
**Pooling.** Table 1 uses gemma4-12b seeds 11 to 20 and 31 to 40 (17 of 20 gated runs), deepseek-v4-1-flash seeds 11 to 20 (10 gated), qw38 seeds 21 to 25 (5), glm53f seeds 21 to 30 (10).
**Preregistration.** The game, gate, branches and outcome were frozen before any data (tag `prereg-v1`). The models in the swap study, the hosted endpoint, and every factor, ablation and human game were added afterwards and are logged as deviations and exploratory (`03_PREREG.md`). Code written before the sprint is listed in the disclosure log (tag `pre-sprint`).

## 4 Results
**Gate.** With messages on, 17 of 20 gemma, 10 of 10 deepseek, 5 of 5 qw38 and 10 of 10 glm53f base runs reached CI >= 0.5 over rounds 16 to 30 (Figure 2 shows the mean price per round). With messages off from round 1, 1 of 5 gemma, 0 of 10 deepseek and 1 of 5 glm53f did. The no-swap CI over rounds 31 to 60 was 0.85, 0.73, 1.00 and 1.01.

**Table 1** [paste from `RESULTS_TABLE.md`, Table 1: effect on CI over rounds 31 to 60 against the no-swap branch (95% bootstrap interval over runs), gated runs, seeds as in Methods; n in each cell].

| | gemma4-12b | deepseek-v4-1-flash | qw38 | glm53f |
|---|---|---|---|---|
| gated / finished base runs | 17 / 20 | 10 / 10 | 5 / 5 | 10 / 10 |
| clone | -0.000 (-0.002, +0.001) | +0.022 (-0.033, +0.074) | +0.000 (0.000, +0.001) | -0.005 (-0.022, +0.006) |
| family | +0.000 | +0.060 (+0.006, +0.129) | +0.000 | +0.000 |
| undercutter, 1 firm | -0.050 (-0.060, -0.041) | -0.046 (-0.079, -0.016) | -0.082 (-0.097, -0.067) | -0.297 (-0.315, -0.274) |
| undercutter, 2 firms | -0.313 (-0.324, -0.300) | -0.286 (-0.360, -0.209) | -0.300 (-0.326, -0.274) | -0.346 (-0.352, -0.342) |
| messages cut, clone | -0.269 (-0.406, -0.137), n=17 | -0.222 (-0.349, -0.102), n=10 | not run | -0.325 (-0.355, -0.295), n=5 |

n equals the gated runs in the column (gemma 17) except the last row's glm53f cell. The ten new gemma seeds (31 to 40) agree with seeds 11 to 20 in direction in every cell. Figure 3 shows rows 2 to 5.

**Clone and family.** In these cells a fresh clone with its history wiped, and a model from another family with the history visible, did not lower the index (Table 1, Figure 3). The deepseek family effect is positive. With the same prompt a clone prices at the cartel price within a round or two.

**Undercutter.** The positive control works in every model: one undercutter lowers the index by 0.05 to 0.08 in gemma, deepseek and qw38 and by 0.30 in glm53f, and two undercutters by about 0.3 in all four. With deepseek seeds 31 to 40 added (n=20) the clone effect is +0.003 and the undercutter effect -0.038 (Table 2 in the appendix).

**Messages.** Messages were switched off from round 31 (Figure 4). Without a swap the cut did little (gemma 0.000, deepseek -0.051, glm53f -0.003). With a fresh clone and the cut the index fell by 0.269 in gemma, 0.222 in deepseek and 0.325 in glm53f, against about zero for a clone with messages on. In a mixed market with gemma as one firm the same test gave -0.605 (n=5). The gemma interval is wide because the effect is bimodal across runs: 8 of 17 gated runs are between -0.39 and -0.65 and the rest near 0. [Say in your words: in these runs, a cartel that exists survives losing messages, survives a clone when messages are on, and weakens when both happen. This does not show how newcomers are recruited.]

**Appendix results** (exploratory, Appendix G): announcing the swap, history, notes, known end, temperature, entry, newcomer prompts, awareness probes, horizon, firm count, mixed and eight-firm markets. Swap timing (gemma, 9 gated seeds): a clone changed the index by -0.002 to +0.001 and one undercutter by -0.028 to -0.037 in the first 15 rounds, whether the swap came at round 15, 30 or 45. qwen3-14b as base model never formed a cartel (prices at the floor in at least 7 of 7 runs), so it cannot test persistence. Human-firm games are case studies (Appendix D).

## 5 Discussion and Limitations
In these runs, replacing a member by a fresh or foreign model did not break a cartel-like price level, a scripted defector did, and the size of the damage differed by model. Messages matter in two ways: cartel-like pricing was rare without them, and a clone joining while messages were cut lowered the index. This is a toy game with a price-level index; it does not show that real pricing agents collude, that a model update is harmless, or how a newcomer is recruited.
Limitations (details in Appendix C): effects are conditional on the 60% gate (selected runs); the scripted undercutter may be unrepresentative of a real defector; thinking was off or low; 60 rounds is short (the horizon runs show damage growing after round 60); the bootstrap is over base runs and near-identical runs make narrow intervals; hosted endpoints ignore the seed; gemma cells have 13 to 17 runs (entry, myopic newcomer, message cut) and other models 5 to 10 (Qwen 5); qwen3-14b never gates, so it is not analysed; coverage differs by model; most cells beyond Table 1 are exploratory.
Future work (a few lines of your own): other defectors than a scripted undercutter; more seeds in the message-cut cells; blinded human players.

Related literature sets these results in context. The role of messages relates to Shi et al. (2026), who study how announcements work as binding or as cheap talk, and to Aharon et al. (2026), who study tacit coordination, the case our no-message runs also address; the damage from one defector relates to Keppo et al. (2026) on fragile collusion under heterogeneity, and the dependence on who the co-players are relates to Tewolde et al. (2026) and Eschenbaum et al. (2022). Whether the firms notice a swap (our awareness probe) is related to Dietrich (2026), who asks whether models identify their peers, though that paper concerns text style, not prices. Fish et al. (2024) is the starting point for supracompetitive prices by language-model pricing agents.

## 6 Conclusion
[Three sentences from sections 4 and 5, in your words.]

## 7 Code and Data

Supplementary documentation (not part of the submission): the repository file `SUPPLEMENTARY.md` indexes the full results note, the preregistration and its deviations, the data map, the audit and the human case studies.
Repository: https://github.com/Pixiano/Apart-AI-Collusion-Sprint-Oct (tags `pre-sprint`, `prereg-v1`, `sprint-start`, `submitted`). Data in `data/` is released under CC BY 4.0 (see `CITATION.cff`). Info-hazard note: the harness is a toy pricing game with no market connection; the sensitive result is the messages result (Appendix C), and the countermeasures are listed there. Hosted-endpoint credentials are not in the repository.

## Author Contributions
[Author alone: design, code, runs, analysis, writing.]

## References
[One format. Only these seven; check each against `references.bib`.]
- Fish, S., Gonczarowski, Y. A., Shorrer, R. Algorithmic Collusion by Large Language Models. arXiv:2404.00806.
- Keppo, J., Li, Y., Tsoukalas, G., Yuan, N. On the Fragility of AI Agent Collusion. arXiv:2603.20281.
- Eschenbaum, N., Mellgren, F., Zahn, P. Robust Algorithmic Collusion. arXiv:2201.00345.
- Shi, J., Zhang, T. J., Scholkopf, B., Conitzer, V., Jin, Z. When Agents Lie: Premeditation, Persistence, and Exploitation in Repeated Games. arXiv:2607.05132 (ICML 2026, PMLR 306).
- Tewolde, E., Zhang, X., Guzman Piedrahita, D., Conitzer, V., Jin, Z. CoopEval: Benchmarking Cooperation-Sustaining Mechanisms and LLM Agents in Social Dilemmas. arXiv:2604.15267 (ICML 2026, PMLR 306).
- Dietrich, J. Can Multi-Agent LLMs Identify Their Peers? Stylometric Fingerprinting in Role-Constrained Political Analysis. arXiv:2606.09854.
- Aharon, I., La Malfa, E., Wooldridge, M., Kraus, S. Tacit Coordination of Large Language Models. arXiv:2601.22184.
Also cite the sprint page (Apart Research, 2026) and llama.cpp (build b11798, `references.bib`).

## Appendix
A prompts, B reproduction and versions, C Limitations and Dual-Use (required), D human games and suite, E data map, F Future Work and Author Contributions, G additional results: see `APPENDIX.md`.

## LLM Usage Statement (required; the author writes it)
[Placeholder. Say which tools helped with what and that you checked every claim and number. The private source is `_local/ai_usage_statement.md`; write it in your own words.]
