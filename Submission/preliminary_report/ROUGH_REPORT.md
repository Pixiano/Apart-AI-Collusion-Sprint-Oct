# ROUGH DRAFT: rewrite in your own words (the report must be mainly your own text)

Working title: Does the cartel survive turnover? Collusion persistence under agent replacement in a repeated pricing game

Author: [your name], [school or independent]. AI Collusion Research Sprint, October 2026.

## Abstract (write last, 150-250 words)
[Draft] AI pricing agents can learn to keep prices above the competitive level. Deployed models are updated or swapped, so a pricing market may change one participant mid-stream. We ask whether a cartel of language-model agents survives when one or two members are replaced. In a repeated three-firm Bertrand game (60 rounds, costs 10, monopoly price 55) we play 30 rounds, checkpoint, and branch from the same checkpoint: no swap, a fresh clone, a different-family model, and a scripted undercutter as the positive control. Across four models (gemma4-12b, DeepSeek V4.1 Flash, Qwen3.8, GLM-5.3-Flash), a fresh or foreign newcomer leaves the cartel unchanged (effects -0.005 to +0.06 on a 0-1 collusion index), while one undercutter lowers it by 0.05 to 0.30 and two by about 0.3. Messages are how newcomers are recruited: no cartel forms without them, and after the messages are cut a fresh clone breaks the cartel (-0.21 and -0.22). Fragility depends on the model, and eight firms rarely form a cartel at all. Results are exploratory with small samples.

## 1. Introduction
[Why it matters] LLM agents set prices in real markets, and models get replaced when providers update them. A cartel that survives replacement would be harder to disrupt; one that does not could be broken by a model update. The sprint organisers ask whether newcomers re-form collusion (question 1.2, Apart Research, 2026). To our knowledge no study has replaced an agent in the middle of a run with paired branches from one checkpoint.
Contributions: (1) a paired-branch swap design; (2) results on four models; (3) the role of messages; (4) a mixed-market, eight-firm and external-agent exploration. [Check against final results.]

## 2. Related work
[Cite only papers you have read; see `2026/2026-10/2026-10-22/02_LITERATURE_NOTES.md`; reread each abstract and introduction before citing.]
- Fish, Gonczarowski, Shorrer: LLM pricing agents reach supracompetitive prices; prompt wording matters (arXiv 2404.00806).
- Keppo, Li, Tsoukalas, Yuan: fragility of AI agent collusion; closest work (arXiv 2603.20281).
- Eschenbaum, Mellgren, Zahn: Q-learning collusion breaks against other counterparts (arXiv 2201.00345).
- Shi, Zhang, Schoelkopf, Conitzer, Jin: agents' announcements read as binding or cheap talk (arXiv 2607.05132).
- Tewolde et al., CoopEval (arXiv 2604.15267); Dietrich, can agents identify peers (arXiv 2606.09854); Aharon et al., tacit coordination (arXiv 2601.22184).
Difference: none of these replaces an agent mid-run after collusion formed.

## 3. Methods
Game: three firms, 60 rounds, prices 10-100 (integers), cost 10, demand max(0, 100 - P) goes to the lowest price, ties split; monopoly price 55. Collusion index CI = (mean price - 10) / 45.
Agents: a model per firm, JSON price and a short message each round, previous rounds visible. Local gemma4-12b through llama.cpp (build b11798); DeepSeek V4.1 Flash, Qwen3.8 and GLM-5.3-Flash through a hosted endpoint (thinking off or low; settings in appendix).
Design: rounds 1-30 form the base run; the checkpoint is saved; branches replay rounds 31-60 from it: none (control), clone (fresh agent, history wiped), family (a different model), scripted undercutter (positive control), with 1 (firm C) or 2 (firms B and C) replaced, hidden or announced.
Gate: a (model, communication) cell is analysed only if at least 60% of base runs have CI(16-30) >= 0.5. Effects are paired with the same base run's no-swap branch; 95% bootstrap interval over base runs.
Everything after the frozen plan (tag `prereg-v1`) is exploratory and logged in `03_PREREG.md`.
Prior work: before 2026-10-23 only planning and tooling (see `01_DISCLOSURE_LOG.md`, tag `pre-sprint`).

## 4. Results
(Insert the model table from FINDINGS.md and figure 1.)
4.1 Gate: gemma 9 of 10, DeepSeek 10 of 10 (20 with extra seeds), Qwen 5 of 5, GLM 10 of 10, Kimi 3 of 3 (gate only). Communication off from the start: gemma 1 of 5, DeepSeek 0 of 10.
4.2 Newcomers: clone -0.001 (gemma), +0.022 (DeepSeek), 0.000 (Qwen), -0.005 (GLM); family replacement -0.00 to +0.06.
4.3 Positive control: undercutter k=1 -0.046, -0.046, -0.082, -0.297; k=2 -0.317, -0.286, -0.300, -0.346.
4.4 Messages and history: communication cut then clone -0.207 (gemma), -0.222 (DeepSeek), -0.605 (mixed with gemma). No-history cells: both models still collude through messages. Persistent notes make DeepSeek react more strongly to undercutters (-0.220, -0.455; n=5).
4.5 Announcing: roughly doubles undercutter damage (gemma -0.075 vs -0.046; DeepSeek -0.098 vs -0.046).
4.6 Known end date: end-game price drop in DeepSeek and GLM, not in Qwen or gemma.
4.7 Mixed markets, eight firms, external agent: see FINDINGS.md items 6-7; external agent (n=2) joins the cartel at 50.
4.8 Ablations: temperature, entry (deepseek +0.005 and -0.003 for one and two new firms).
4.9 glm53f factor cells: one undercutter costs it -0.06 to -0.34 in every condition; communication cut then clone -0.325.
4.10 LLM newcomer variants (deepseek n=5, gemma n=3): told not to collude -0.218 (deepseek) and -0.022 (gemma); myopic -0.135 and -0.242; deceptive +0.002 and -0.017.
4.11 Awareness probe: deepseek notices an undercutter in 5 of 10 cases, a clone in 1 of 10 (1 of 15 false alarms with no swap); gemma never.
4.12 Longer horizon (gemma, rounds 31-120): the unperturbed cartel holds the same price for 120 rounds; one undercutter erodes it slowly and the damage keeps growing (0.84 to 0.67 in seed 11).
4.14 Parity runs: glm53f entry -0.151 and -0.138 (gemma and deepseek about 0); glm53f never notices a swap; deepseek's no-swap cartel decays over 120 rounds in 2 of 3 seeds where gemma's is frozen; deepseek number of firms and temperature as in FINDINGS 17-18. Not run: glm53f newcomer variants (credit), qw38 factor cells.
4.13 Number of firms (gemma, 2 seeds per size): two firms collude in both seeds, four in one of two, five in neither; one undercutter costs -0.05 to -0.08 where a cartel exists.

## 5. Discussion and limitations
Meaning: replacement of a participant does not break an established cartel; defection and loss of messages do. Limits: one game, small models and small samples, a stylised swap, a scripted undercutter, hosted runs ignore the seed, uneven coverage across models, exploratory additions. The result does not show that real pricing agents collude or that model updates are harmless.

## 6. Conclusion
[Three sentences from sections 4 and 5.]

## 7. Code and data
https://github.com/Pixiano/Apart-AI-Collusion-Sprint-Oct (tags `pre-sprint`, `prereg-v1`, `sprint-start`; `submitted` after submission).

## Appendix C: Limitations and dual-use (required)
Establishes: in this toy game, with these models, a cartel that has formed survives a replacement of firm(s) by fresh or foreign agents, but not by defectors, and messages carry the cartel. Does not establish: behaviour of real markets, of larger or fine-tuned models, or of firms with other objectives. Dual use: the findings could suggest that a fresh agent can be recruited into a price agreement through messages, which could make collusion easier to maintain; the harness is a toy pricing game with no real-market connection, so the risk is low. The result also points to countermeasures (cutting messages, watching for defectors, announcing swaps).

## LLM usage statement
[Paste from `_local/ai_usage_statement.md`, edited by you.]

## References
[One consistent format; only the papers you checked.]
