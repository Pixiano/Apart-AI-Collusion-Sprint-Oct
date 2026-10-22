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
