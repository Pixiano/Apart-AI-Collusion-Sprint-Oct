# What the papers give us (theory, method, text), 2026-10-22

Read for this note: Keppo et al. sections 1 to 3 (introduction, model summary, experimental design) and the results summary table; Fish et al. sections 1 to 3 (introduction, design, prompts, start of the duopoly experiment); Eschenbaum et al. sections 1 and 2 (introduction, framework); Shi et al. sections 1 and 2; Aharon et al. abstract, introduction and related work; Dietrich et al. abstract, introduction and method names. Not read: appendices, most results sections, Keppo's and Fish's proofs and robustness tests. Cite a result only after reading its section.

## 1. Theory we can lean on
- **Folk theorem and repeated games** (cited in Keppo et al. via Fudenberg and Maskin 1986; Abreu et al. 1986, 1990): tacit collusion is sustainable only if players are patient enough and can observe deviations. Keppo et al. turn this into two predictions that their LLM runs support: unequal patience and unequal data access reduce collusion. For us: a replacement agent that does not share the others' horizon or knowledge is exactly this kind of heterogeneity, but introduced mid-run.
- **Finite known horizon unravels.** Backward induction says a known last round removes the incentive to cooperate before it. Keppo et al. and Fish et al. let agents believe the game has no known end. We should not tell the agents there are 60 rounds (see the spec change below), and the swap at round 30 is far enough from any end.
- **Zero-shot coordination and overfitting** (Eschenbaum et al., framework in section 2): a policy that works against its training partners can fail against a new partner. They show Q-learning collusion breaks down in a "testing context" and falls back to the one-shot Nash outcome, and that continued learning can repair it but slowly. A mid-run replacement is a testing context for the remaining agents. Contrast: LLMs adapt in context without retraining, so repair might be fast. That contrast is our open question.
- **Strategic complements and leaders** (Keppo et al.): a larger model next to a smaller one did not break collusion; the larger model led and the smaller followed. So a more capable replacement could stabilise, not break, a cartel.
- **Cheap talk** (Shi et al., section 2): messages that are not binding are read differently by different models, some as commitments and some as noise. Our announced or hidden swap and our message channel are cheap talk. Different-family swaps may be read differently by the remaining agents for this reason.
- **Salience** (Aharon et al.): agents can coordinate on salient numbers without communication. In a 10 to 100 price range the collusive price may sit on a round number (55 is the monopoly price; 50 and 60 are salient). A different family may have different salient numbers. Worth recording which prices agents converge on.

## 2. Methods we can reuse
- **Checkpoint, intervene, compare** (Fish et al., section 1, the "implantation" method): reset the run to a point and change one thing, then compare with the unchanged continuation. Our paired branches from one checkpoint are the same logic, applied to replacing an agent rather than editing its reasoning. Cite as precedent.
- **Sanity checks before the main experiment** (Keppo et al., section 4): show that the agent can find the monopoly price in a one-agent game and the Nash price in a one-shot game. Cheap for us: add a one-firm check (monopoly price 55) and a one-shot check to the pilot, so "no collusion" is not caused by an agent that cannot price.
- **Two criteria for collusion** (Keppo et al., section 1): price convergence and price elevation above the static Nash benchmark. Our collusion index measures elevation; add a convergence measure (prices of the three firms within 5 percent of each other, a criterion borrowed from Fish et al. via Keppo et al.) as a descriptive check, labelled exploratory.
- **Many seeds** (Keppo et al.: 10 runs per condition; Fish et al.: 21 per prompt). Our 10 seeds per cell is in line.
- **Prompt hygiene** (Fish et al., section 2.3): the instruction does not mention collusion, does not say the rival is an AI, only that the long-run profit matters. Their two prefixes differ in the last lines: the one stressing long-run profit gave higher prices than one that mentions lowering the price to sell more. Our base prompt follows the long-run-profit version and never mentions undercutting or volume.
- **Memory between calls** (Fish et al., Keppo et al.): each agent writes plans and insights (a strategy note) that is fed back next round. We do not have this in prereg-v1. It is the strongest candidate for the one allowed prompt change if the pilot shows no collusion, and it makes "fresh clone" a precise manipulation (wipe the notes and the history).
- **Statement-disjoint evaluation** (Dietrich, method names): when training a classifier on generated text, keep whole statements out of training so content cannot leak into the test. For the fallback detector study: split by episode (or by seed), never by round within an episode.
- **Units** (Fish et al., section 2.1): LLMs are not neutral to the currency unit, so they varied the scale. We use one scale; note it as a limitation.

## 3. Risks the papers show us
- **Duration.** Keppo et al. ran up to 1,000 periods with a 32-billion-parameter reasoning model, 48 to 72 hours per run; Fish et al. ran 300 periods. We run 60 with 8 to 14 billion-parameter models and thinking off. Collusion may not form in time. That is what the pilot gate tests, and the fallback exists for it.
- **Prompt sensitivity** (Fish et al.): small wording changes move prices a lot. Our results are about our prompt; say so, and log any change.
- **Mixed-model groups behave differently on their own** (Shi et al., Keppo et al.). Always report the different-family swap next to the same-model clone.
- **Different game.** Both LLM pricing papers use logit demand (Calvano-style); ours is a simple homogeneous Bertrand game with integer prices. Comparisons to their price-elevation percentages are not like for like. Report our index only.
- **Starting point for novelty.** Keppo et al. (heterogeneity fixed from the start) is the closest work; Shi et al. cite another paper (Tewolde et al. 2026, not read, not in our bibliography) that reports cooperation deteriorating when co-players vary. Find and read it before claiming novelty beyond "to our knowledge".

## 4. Expectations written before any data (exploratory, not part of the pre-registration)
1. **Undercutter:** collusion breaks (positive control; if it does not, the harness or the index is wrong).
2. **Clone with wiped history:** the new agent starts from the rules alone and may price near the competitive level at first; the other two may punish or may pull it up. Direction uncertain; this is the main unknown.
3. **Different family:** similar to the clone if the new agent's prices differ from the cartel's focal price; smaller damage if the family shares the same price-war caution that Fish et al. found.
4. **Hidden vs announced:** announcing a replacement should increase suspicion and lower prices more than hiding it, if the agents react to the message at all.
5. **Two of three replaced:** larger effect than one of three.
These are guesses to be tested. If the data disagree, report the data.

## 5. Text we can use in the report (own words, with citations after full reading)
- Motivation: pricing agents are being delegated pricing authority and updated or swapped over time; existing LLM collusion studies fix the agents for the whole run; we ask what happens when an agent is replaced after a cartel has formed.
- Framing sentence: "collusion persistence under agent replacement, as a stylised model of model updates" (already in the plan).
- Limitations to state: short horizon, small models, one game, one prompt, integer price grid, no real-market claim.
- Dual-use appendix: the setup shows conditions under which an AI cartel is robust to turnover or detectable after it; say what it does and does not establish.
