# Analysis of Tewolde et al., CoopEval (ICML 2026, arXiv 2604.15267), 2026-10-22

Why this paper: Shi et al. cite it as finding that "repetition-induced cooperation deteriorates when co-players vary", which sounds close to our swap question. Read for this note: abstract, introduction, contributions, experimental setup and metrics, research questions 1 to 5 (results), future work and impact statement. Not read: appendices (66 pages in total), mediation and contract details.

## What they did
- Benchmark of four social dilemmas (Prisoner's Dilemma, Traveler's Dilemma, Trust game, 3-player Public Goods) with six LLMs from several developers (Gemini with and without reasoning, GPT-5.2, GPT-4o, Qwen-30B and one more; see their paper for the exact list), every model pairing in cross-play, each combination repeated three times (over 50,000 decisions).
- Five conditions: no mechanism (single-shot), Repetition (same co-player each round), Reputation (a new co-player each round, with their history shown; two versions, first-order and higher-order), Mediation (delegate to a third-party mediator), Contract (agree on outcome-conditional payments).
- Metrics: payoff rescaled so 0 = everyone defects and 1 = everyone fully cooperates (mean over match-ups), "fitness" after replicator dynamics (a society that shifts toward better-performing models), and deviation ratings.

## Results we can use (their Table 2, all games pooled, scale 0 to 1)
| Condition | Mean cooperation score |
|---|---|
| No mechanism | 0.07 |
| Repetition (same co-player) | 0.59 |
| Reputation, first-order (new co-player each round) | 0.32 |
| Reputation, higher-order | 0.23 |
| Mediation | 0.70 |
| Contract | 0.80 |

- Modern LLMs defect almost always in single-shot dilemmas (often 100% of the time), reasoning or not; only the older GPT-4o cooperates about half the time.
- Cooperation under Repetition is insensitive to the history window and the continuation probability they varied; Reputation is not (shorter windows did better, which they link to LLMs handling long histories poorly).
- Under Repetition, LLMs often defect in round one in some games, contrary to "never be the first to defect".
- Under evolutionary pressure (replicator dynamics), the more cooperative models are outcompeted and payoffs fall in the no-mechanism case; with mechanisms cooperation rises.
- Their impact statement warns that "cooperation" between agents that ignore others' utilities can be collusion that harms the collective.

## How it relates to our question (honest comparison)
- Their "co-players vary" result is Reputation: each round a fresh opponent. That is a market of strangers, not a stable group in which one member is replaced once, which is our design. So it does NOT answer our question. It does motivate it: cooperation among LLMs that rests on repeated interaction with the same partner is weaker when partners keep changing.
- Different games: social dilemmas with discrete actions versus our pricing game with 91 prices. Their baseline is one-shot defection; ours is the competitive price.
- Our novelty claim should therefore be worded: "to our knowledge, existing LLM studies either fix the agents for the whole run (Keppo et al.; Fish et al.) or re-match strangers every round (Tewolde et al.); we replace one member of an established group once and compare with the unchanged continuation."

## What it gives us
1. **Evidence that history length matters.** They suggest LLMs manage long histories badly, and cooperation under Reputation did better with short windows. Our full 60-round table might not be ideal; as a possible prompt change, consider a rolling window (last 20 rounds plus summary statistics). Prefer the notes field first (Fish et al., Keppo et al.). Only one prompt change is allowed by the pre-registration.
2. **A selection-pressure framing** for model updates: if firms switch to whichever model earns more, the less cooperative models take over (their replicator-dynamics result). A natural paragraph for the Discussion, not something we test.
3. **A baseline expectation:** independent play drives LLMs toward the non-cooperative outcome. In our game the analogue is the competitive price, so a fresh clone that sees only the rules may start low. Already written as expectation 2 in `04_PAPER_INSIGHTS.md`.
4. **Reporting practice:** they ran three repeats per cell and speak only of aggregated signals, warning that single cells may not be significant. Our 10 seeds and bootstrap intervals are stronger; keep per-cell results exploratory when intervals are wide.
5. **Dual-use wording:** their impact statement names collusion as a harm that cooperation research can enable. Use similar care in our ethics appendix.

## Citation rule
Cite as: Tewolde, Zhang, Guzman Piedrahita, Conitzer, Jin (ICML 2026). Say exactly what they tested ("cooperation under repetition compared with re-matching a new co-player each round"); do not say they studied replacement of an agent in a group.

## Update 2026-10-23: appendices read (C, H, J, N.1 to N.2; not read: proofs D, tables E, evolutionary dynamics F, judge prompts G, mechanism prompts N.3)
- **What "history window" means.** The window k is how many past rounds are shown, and they tried only k = 2, 3, 4 (appendix H, Prisoner's Dilemma only), with continuation probability 0.7, 0.8, 0.9 told in the prompt. That is far shorter than our 60 rounds. Under Repetition the average score barely moved with k or the continuation probability (about 1.77 to 1.86 on their scale); under Reputation (a new stranger each round) shorter windows scored higher (for example 1.54 at k = 2 against 1.32 at k = 3 with probability 0.9, first-order version). So the "long histories hurt" evidence is for the stranger setting, and in a stable pair the window did not matter. Correction to point 1 above: for our stable group the paper predicts little effect of a rolling window; ablation 3 is a weak candidate. The earlier note that history handling is the reason is their own hypothesis (they cite another paper), not something they tested.
- **They tell the agents the continuation probability and run a fixed 15 rounds**, weighting payoffs by probability (appendix C, T = 15, error under 4.2 percent of the payoff range). We hide the end. Their insensitivity to the continuation probability under Repetition is mild evidence that telling the horizon (ablation 1) may not change much either, though their games and horizon are different.
- **Settings.** Temperature 1 throughout. Agents return a probability distribution over actions and the harness samples from it, to avoid a known gap between what a model says and what it samples; reasoning is on low or medium for some models. Action names are anonymised tags to avoid memorised game names. Our prompts should likewise avoid words such as cartel, collusion and Bertrand, as the spec already intends.
- **Round-one behaviour.** In Public Goods and Traveller's Dilemma, several models defected in round one at 50 to 100 percent even under Repetition, and in Reputation they cooperated less towards a partner who had just cooperated than towards one with no history. A fresh clone, which has no history, may behave like those no-history players: low first, then adapt. Keeps expectation 2 in `04_PAPER_INSIGHTS.md` as a guess.
- **Judging justifications.** They label the reasoning text with an LLM judge (appendix G, not read). For our short messages, reading a sample by hand is enough; a judge model would need validation we do not have time for.
- **Settings table** (temperature): Fish et al. and CoopEval both use temperature 1; Keppo et al. report none. Our base is 0.7, so ablation 8 includes 1.0 as the value the other two papers used.
