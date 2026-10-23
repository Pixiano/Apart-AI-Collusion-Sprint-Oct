# Ablation candidates (review sheet)

The ten exploratory configurations to run after the base configuration and the core swaps. Not part of the pre-registration (`prereg-v1`). Full reasoning, costs and rules: [`2026/2026-10/2026-10-22/06_ABLATIONS.md`](2026/2026-10/2026-10-22/06_ABLATIONS.md). Papers: [`papers/README.md`](papers/README.md), citations in [`references.bib`](references.bib).

How to use this sheet: read the section named in "Where to read", check that the paper really says what we use it for, then fill "Review notes" and "Decision" (keep, change, drop). Section numbers are from the versions in `papers/` and may shift between versions.

| # | Change versus base | Where to read | What to check | Review notes | Decision |
|---|---|---|---|---|---|
| 1 | Tell the agents the horizon ("60 rounds") instead of hiding it | Keppo et al. section 3 (setup: unknown end, discount factor) and 4.1; Fish et al. section 2 | Do they really hide the end? Is there any result on end-game behaviour we can compare with? | | |
| 2 | Notes field: each agent writes plans carried to the next round | Fish et al. section 2.2 item 4 ("plans and insights"); Keppo et al. section 3.3.1 item 3 (previous strategy) | How much does the memory matter in their setups? Is there an ablation without it? | | |
| 3 | History window: last 20 rounds plus summary instead of the full table | Tewolde et al. RQ5 (Repetition and Reputation) and Appendix H | Is the window result about re-matched strangers only? Does it transfer to a stable group? | | |
| 4 | Prompt wording: add a line about selling more by lowering the price | Fish et al. section 2.3 (prefixes P1 and P2) and section 3 (duopoly results) | Size of the price gap between P1 and P2; same model and game as ours? | | |
| 5 | Swap timing: round 15 and round 45 instead of 30 | Eschenbaum et al. section 2 (training versus testing context); no paper tests timing directly | Anything on when the testing context starts? Else this one is ours alone, so say so | | |
| 6 | gpt-oss reasoning effort: low versus high | Fish et al. Appendix A (newer model at high reasoning effort); gpt-oss model card | Does higher reasoning change collusion in their newer-model check? | | |
| 7 | Replacement strength: a larger model replaces a smaller one, and the reverse | Keppo et al. section 5.3 (model size, leader and follower) | Which model led? Were both patient agents? Does it hold in groups of 3? | | |
| 8 | Temperature: 0.3 and 1.0 | Fish et al. Appendix B (technical settings) | What temperature they used and whether they varied it | | |
| 9 | Number of firms: 2, 4 and 5 instead of 3 (range 2 to 5 as in Keppo et al.; 6 only if cheap; edited 2026-10-23) | Keppo et al. section 5.2 (number of sellers) and the results table (3 patient +36%, 4 +11%, 5 +3% price elevation) | Their exact collusion measure, run length for 4 and 5 sellers, and whether 5 sellers failed to collude only within their horizon | | |
| 10 | Anchor price in the prompt: a round reference price (e.g. 55) in all prompts, in one prompt only, or a non-monopoly anchor (e.g. 30), versus none (added 2026-10-23) | Aharon et al. (focal points; read so far: abstract, introduction, related work only, so read their method for how they pose numeric tasks); Fish et al. section 2.2 item 2 (their prompt gives a price-ceiling hint) | How they build salience and whether numbers behave differently from other cues; whether the ceiling hint in Fish et al. acts as an anchor | | |

Status: none run yet. Update the Decision column after your review, then I fold the decisions into `06_ABLATIONS.md`.
