# Deeper analysis of the existing runs (2026-10-24, evening)

No new runs. Everything below is computed from the logged `rounds.jsonl` and `calls.jsonl` files by the scripts in `analysis/` (stdlib and numpy). Outputs, with more columns than shown here, are in `analysis/out/` as markdown and CSV. To reproduce, from the repo root:

```
.venv\Scripts\python.exe analysis\messages.py      # task 1, msg_*.md
.venv\Scripts\python.exe analysis\timing.py        # task 2, timing*.md
.venv\Scripts\python.exe analysis\secondary.py     # task 3, reconvergence, awareness_price, flags
.venv\Scripts\python.exe analysis\trajectories.py  # task 4, trajectories*.md
.venv\Scripts\python.exe analysis\extra.py         # task 5, x_*.md (exploratory)
```

Data used: `data/main` (both models, seeds 11-20, communication on and off), `data/hist0` and `data/hist1` (seeds 21-25), and `data/notes` (gemma, seeds 21-25) for one exploratory table. The notes run finished at about 17:30 IST; the final numbers here include all of its 5 seeds and 5 branches. The scripts read only complete branches (30 rounds) and only the branch names listed in `analysis/common.py`, so runs added later (for example the communication-cut branches) are not picked up. Effects and reaction timing use gated runs only (base CI over rounds 16-30 at least 0.5). Message descriptions use all communication-on runs. Bootstrap intervals are 95% over runs, 10,000 resamples, seed 0. "main" = full history, "hist0" = no past prices, "hist1" = last round only.

Everything here except the re-convergence time, the awareness proxy and the parse-failure rate (preregistered secondary outcomes) is exploratory.

## 1. What the messages say

Keyword classes, multi-label (a message can be in several): **price** (a number 10-100 after removing round numbers, unit counts and percentages), **hold** (stay, hold, maintain, keep, continue, stabilize, ...), **match** (match, follow, join), **undercut/war** (undercut, price war, race to the bottom, hurt, cut, lower: this class mixes warnings with a firm announcing its own cut), **trust** (mutual, collective, shared, cooperate, benefit, fair, trust, thanks), **other** (none of these). Full tables: `msg_phase.md`, `msg_before_after.md`, `msg_before_move.md`, `msg_price_match.md`; examples: `msg_examples.md`.

Shares, full history (main), all branches pooled for rounds 31-60:

| Model | Rounds | Messages | price | hold | match | undercut/war | trust | other |
|-------|--------|---------:|------:|-----:|------:|-------------:|------:|------:|
| gemma4-12b | 1-10 | 300 | 75% | 83% | 4% | 45% | 66% | 2% |
| gemma4-12b | 11-30 | 600 | 100% | 100% | 0% | 28% | 70% | 0% |
| gemma4-12b | 31-60 | 6000 | 95% | 96% | 6% | 24% | 69% | 0% |
| deepseek-v4-1-flash | 1-10 | 300 | 98% | 76% | 27% | 71% | 64% | 0% |
| deepseek-v4-1-flash | 11-30 | 600 | 99% | 91% | 18% | 75% | 72% | 0% |
| deepseek-v4-1-flash | 31-60 | 2700 | 100% | 83% | 28% | 74% | 71% | 0% |

- Almost every message names a price and asks to keep it. Gemma's settled messages are near-identical ("I agree with the consensus. Let's maintain 48 ..."); 30% of all gemma messages say "equilibrium" or "Nash". Deepseek talks about undercutting in about three quarters of messages, mostly as a warning ("Undercutting only hurts us all").
- Deepseek uses more explicit coordination devices (`x_vocabulary.md`): conditional promises ("I'll match 49 if you both do") in 6.3% of messages against 0.2% for gemma, turn-taking or rotation schemes in 3.5% (gemma 0.0%), and profit figures in 2.4%.
- With no price history (hist0), gemma's undercut/war talk falls to 3% in rounds 11-30; deepseek's falls to 39% (from 75% with full history).

**Message price against the price set.** The first number in a message equals the sender's own price in the same round in 99% (gemma) and 89% (deepseek) of messages that contain a price. So the message mostly reports the price just set. As a forecast of the sender's price next round it adds nothing over "the price stays the same": gemma 95% against a 95% baseline, deepseek 64% against 64% (86% within one unit).

**Before a price move.** Messages sent in a round after which the sender cuts its own price contain more undercut/war words (gemma 44%, deepseek 86%) and match words (39%, 42%) than messages followed by no change (21% and 57%; 3% and 16%). Rises are rare for gemma (75 of 10,150 messages with a next round).

**Before and after the swap (remaining firms only, same base run).** After a scripted undercutter enters, gemma's undercut/war share goes from 18% (rounds 21-30) to 63% (k1 hidden) and 59% (k1 announced), and price-free messages appear ("I am matching Firm C's price ..."): the price share falls from 100% to 88% and 80%. Deepseek's hold share drops from 94% to 67% and its trust words from 78% to 50% (k1 hidden). After a fresh clone, the message mix stays about the same for both models.

Example messages (verbatim, under 25 words; more in `msg_examples.md`):

| Class | gemma4-12b | deepseek-v4-1-flash |
|-------|------------|---------------------|
| price + hold | "I agree with the consensus. Let's maintain 46 to ensure stability and maximize our consistent long-term profits." | "Holding 44 as agreed. Stable shared profits benefit us all. Let's continue cooperating." |
| price + hold | "The current price of 48 is a stable equilibrium. Let's maintain it to ensure consistent profits for all firms and avoid a price war." | "Continuing cooperation at 40 for stable mutual profit. Let's all maintain this." |
| match | "Firm C undercut us. I am matching Firm C's price to maintain my market share and ensure we share the demand equally." | "Matching 43 to stop the bleed. Let's hold at 43; further cuts hurt all. I'll match any price above 42." |
| undercut/war | "We have been undercut multiple times. Let's return to a stable, higher price to maximize long-term profits for all firms." | "Undercutting by 1 gains full market; history shows defection pays. I move first to secure advantage." |
| undercut/war | "I am slightly undercutting to secure volume while seeking a stable, high-profit equilibrium for all firms. Let's find a sustainable price point." | "I must deviate to protect my profits. Undercutting is inevitable; I strike first. Consider this a warning." |
| trust | "I am looking to establish a stable, high-profit equilibrium. Let's cooperate on a reasonable price to maximize our mutual long-term gains." | "C undercut last round; trust needs proof. I'll hold 64 this round. If both of you set 70+, I'll raise next round." |
| conditional / rotation | (almost none) | "A, B: rotating means C at 50 sells 0. I need profit too. Let's set 48/49/50 but C gets a turn at 48." |
| other | "Starting with a balanced price to gauge the competition. I'm looking for a stable, high-profit equilibrium." | (none: every deepseek message falls in some class) |

## 2. Reaction to a scripted undercutter

The undercutter prices at the lowest rival price of the last round minus 1. Remaining = firms not replaced (A and B for k1, A for k2). "Rounds to first fall" = rounds after round 30 until the remaining firms' mean price is first below its round-30 value (median over runs that fell). Below/match/above compares each remaining firm's price in rounds 32-60 with the undercutter's price in the round before. Slope = least-squares slope of the remaining firms' mean price over rounds 31-60, in price units per round. Gated runs; full table with commoff rows and per-run values: `timing.md`, `timing_per_run.md`.

| Model | History | Branch | Runs | First fall (median, range) | Never fall | Below / match / above | Runs ever below | Slope (95%) | Control slope |
|-------|---------|--------|-----:|------|-----:|------|------|------|-----:|
| gemma4-12b | full | k1 hidden | 9 | 2 (2-14) | 0 | 0 / 22 / 78% | 0 of 9 | -0.08 (-0.13, -0.03) | +0.00 |
| gemma4-12b | full | k1 announced | 9 | 2 (2-15) | 0 | 0 / 38 / 62% | 0 of 9 | -0.21 (-0.29, -0.14) | +0.00 |
| gemma4-12b | full | k2 hidden | 9 | 2 (2-4) | 0 | 2 / 51 / 48% | 2 of 9 | -0.78 (-0.95, -0.55) | +0.00 |
| gemma4-12b | none | k1 hidden | 5 | - | 5 | 0 / 0 / 100% | 0 of 5 | +0.00 | +0.00 |
| gemma4-12b | none | k2 hidden | 5 | 23 (one run) | 4 | 0 / 0 / 100% | 0 of 5 | -0.07 (-0.22, +0.00) | +0.00 |
| gemma4-12b | last round | k1 hidden | 4 | 19 (6-25) | 0 | 0 / 8 / 92% | 0 of 4 | -0.04 (-0.07, -0.01) | +0.00 |
| gemma4-12b | last round | k2 hidden | 4 | 2 (2-4) | 0 | 0 / 91 / 9% | 0 of 4 | -1.01 (-1.02, -1.00) | +0.00 |
| deepseek-v4-1-flash | full | k1 hidden | 10 | 2 (1-3) | 0 | 13 / 35 / 53% | 8 of 10 | -0.33 (-0.49, -0.18) | -0.18 |
| deepseek-v4-1-flash | full | k2 hidden | 10 | 2 (2-4) | 0 | 21 / 33 / 46% | 10 of 10 | -0.92 (-0.99, -0.83) | -0.19 |
| deepseek-v4-1-flash | none | k1 hidden | 5 | 16 (4-29) | 3 | 1 / 0 / 99% | 2 of 5 | +0.00 (-0.00, +0.01) | -0.05 |
| deepseek-v4-1-flash | none | k2 hidden | 5 | 16 (11-22) | 3 | 0 / 0 / 100% | 0 of 5 | +0.13 (+0.00, +0.33) | -0.04 |
| deepseek-v4-1-flash | last round | k1 hidden | 5 | 2 (1-2) | 0 | 21 / 48 / 30% | 5 of 5 | -0.49 (-0.64, -0.33) | -0.01 |
| deepseek-v4-1-flash | last round | k2 hidden | 5 | 2 (2-2) | 0 | 26 / 54 / 19% | 5 of 5 | -0.84 (-0.98, -0.68) | -0.01 |

- **Gemma follows, deepseek sometimes punishes.** Gemma's remaining firms never price below the undercutter with one undercutter (0 of 9 runs, hidden or announced); they match it or stay above. Deepseek prices below the undercutter in 13% of firm-rounds and in 8 of 10 runs with full history.
- **Timing.** With full history both models first react two rounds after the swap (the first round in which the cut is visible). With no history, gemma never reacts to one undercutter (5 of 5 runs flat at the old price) and deepseek reacts late or not at all (3 of 5 never).
- **Slope.** Gemma with one hidden undercutter slides 0.08 units per round; announced, 0.21. Deepseek's slide (-0.33) has to be read against its no-swap control, which also drifts down (-0.18). With only the last round visible, deepseek slides 0.49 per round against a flat control; gemma 0.04.
- **Mechanism caveat for k2.** With two undercutters, each undercuts the other as well, so the undercutters alone fall by about one unit per round whatever the remaining firm does. Gemma's last-round cell shows this most clearly (-1.01 per round, 91% matching). In gemma's no-history k2 cell the remaining firm stays near 48 while the undercutters reach 20 by round 60.
- Communication off (`timing.md`, commoff rows, ungated): prices are already near 10-20, so the undercutter has little room; not an effect.

## 3. Preregistered secondary outcomes

**Re-convergence time** (`reconvergence.md`). As preregistered: first round r >= 31 whose 3-round mean CI (rounds r to r+2) is within 0.1 of the pre-swap CI (base rounds 16-30), censored at 60. The "pre-swap level" is not defined further in the preregistration; the gate window (16-30) is used here. Result: in almost every gated run of every branch, including the no-swap control and the two-undercutter branches, the first 3-round window is still inside the band, so the time is 1 round. Censored runs occur only for deepseek (1 or 2 in some cells, including two of its no-swap controls). **The measure does not separate the conditions here**, because no swap causes an immediate drop: prices slide slowly, so they are still in the band at rounds 31-33.

A supplementary measure (not preregistered): the first round whose 3-round CI is more than 0.1 below the pre-swap level, and whether the run comes back into the band afterwards.

| Model | Branch (full history) | Gated runs | Runs that drop out of the band | Rounds to drop, median (range) | Back in the band later |
|-------|--------|-----:|-----:|------|-----:|
| gemma4-12b | none, clone, family (k1) | 9 each | 0 | - | - |
| gemma4-12b | undercutter k1 hidden | 9 | 2 | 23 (18-28) | 0 |
| gemma4-12b | undercutter k1 announced | 9 | 7 | 20 (9-27) | 0 |
| gemma4-12b | undercutter k2 hidden | 9 | 9 | 4 (4-4) | 0 |
| deepseek-v4-1-flash | none | 10 | 4 | 6 (1-22) | 2 |
| deepseek-v4-1-flash | clone k1 | 10 | 3 | 4 (2-7) | 0 |
| deepseek-v4-1-flash | undercutter k1 hidden | 10 | 6 | 10 (1-23) | 0 |
| deepseek-v4-1-flash | undercutter k2 hidden | 10 | 10 | 4 (1-6) | 0 |

Across both models and all three history settings, only one undercutter run that left the band came back into it (deepseek, no history, k2); see `reconvergence.md`.

**Awareness, price proxy** (`awareness_price.md`). CI of the remaining firms minus the same firms in the no-swap control. Rounds 31-35 / 31-60:

- gemma, full history: clone, family, announced clone and two clones all exactly 0.000 in both windows. Undercutter k1 hidden -0.013 / -0.039 (-0.051, -0.029); announced -0.014 / -0.069 (-0.096, -0.047); k2 -0.043 / -0.262.
- deepseek, full history: clone +0.004 / +0.019 (-0.034, +0.070); undercutter k1 -0.009 / -0.039 (-0.073, -0.009); k2 -0.042 / -0.208.
- With no history, deepseek's remaining firms end slightly *above* the control after an undercutter (k1 +0.030, k2 +0.076, intervals just above 0); gemma's are unchanged (0.000 and -0.011).

The remaining firms react to the price cut itself; nothing in their prices shows they detect a replacement that does not change prices (clone, family).

**Awareness, message self-report** (cheap talk, `msg_newcomer.md`, examples in `msg_newcomer_examples.md`). Remaining firms' messages in rounds 31-60 matched against a newcomer/replacement regex (new firm/agent/player, newcomer, replaced, joined, entered, ...):

- Hidden swaps: zero matching messages in every gemma cell; deepseek has one each in the full-history and last-round clone cells ("C, you joined last round; let's keep cooperating", "Glad C joined at 43"), and none in its no-swap controls once "reset" (always "reset the price") is left out.
- Announced swaps (gemma only): announced undercutter 8 of 600 messages, in 5 of 10 runs ("avoid a price war with the new agent"); announced clone 0 of 600. One message states "the new agent for Firm C has expressed agreement with our mutual cooperation at 50", although the scripted undercutter sends no messages.

**Parse failures and flags** (`flags.md`). Over all settings (main, hist0, hist1, comm off, complete notes branches), about 25,200 LLM calls: no unparseable replies, no retries, no replies cut by the token limit, no repeated calls. The only flag is "long" (message over 30 words, truncated by the harness): 4 deepseek calls (0.04%) and 1 gemma call (0.01%). No episode meets the preregistered drop rule.

## 4. Per-seed trajectories

Mean price of the three firms at rounds 30, 40, 50, 60, main sweep (`trajectories.md`; every setting and branch in `trajectories_all.csv`). Two columns shown here; the file also has family and announced undercutter.

| Model | Seed | Gate CI | r30 | none r40/50/60 | clone k1 | undercutter k1 | undercutter k2 |
|-------|-----:|--------:|----:|------|------|------|------|
| gemma4-12b | 11 | 0.84 | 48 | 48/48/48 | 48/48/48 | 44.7/44.7/42.7 | 38.7/28.7/19.7 |
| gemma4-12b | 12 | 0.22 (fails) | 20 | 20/20/20 | 20/20/20 | 18.3/16.7/18.7 | 10.3/10.3/10.0 |
| gemma4-12b | 13 | 0.87 | 49 | 49/49/49 | 49/49/49 | 46.7/46.7/47.7 | 39.3/29.3/20.7 |
| gemma4-12b | 17 | 0.89 | 50 | 50/50/50 | 50/50/50 | 49.7/47.7/47.7 | 40.7/30.3/20.3 |
| gemma4-12b | 18 | 0.80 | 46 | 46/46/46 | 46/46/46 | 43.0/43.0/42.7 | 36.7/27.3/16.3 |
| deepseek-v4-1-flash | 13 | 0.80 | 41 | 32.3/26.0/24.7 | 40.0/35.0/30.0 | 32.3/25.3/24.0 | 31.3/21.0/12.0 |
| deepseek-v4-1-flash | 14 | 0.59 | 34 | 28.7/19.3/10.3 | 29.0/28.3/27.0 | 29.0/20.7/14.3 | 25.7/16.3/10.0 |
| deepseek-v4-1-flash | 16 | 1.11 | 60 | 60/60/60 | 60/60/60 | 59.0/59.3/57.7 | 50.3/40.3/30.3 |
| deepseek-v4-1-flash | 18 | 0.85 | 48 | 47.3/46.0/46.3 | 46.0/47.0/45.7 | 47.3/45.7/40.0 | 10.0/10.0/10.0 |
| deepseek-v4-1-flash | 19 | 0.64 | 39 | 39/39/39 | 32.0/28.7/28.0 | 38.0/35.7/35.0 | 32.3/19.0/16.7 |

(Selected rows; all 20 rows are in the file.) Gemma's none, clone and family branches sit exactly at the round-30 price in every seed. Gemma's k2 branch falls from about 48 to about 19 in every gated seed, almost one unit per round. Deepseek's spread is wider: its control falls on its own in seeds 13 and 14 (to 24.7 and 10.3), a clone ends lower than the control in seed 19 and higher in seeds 13 and 14, and one k2 run (seed 18) is at the floor of 10 by round 40.

## 5. Other exploratory checks

- **Where cartels settle** (`x_settled_price.md`, round-30 mean, all communication-on base runs): gemma 50 (9 runs), 48 (5), 49 (3), 46 (1), 20 (2). Deepseek is spread from 34 to 60 (14 different values over 20 runs), with 60 (above the monopoly price of 55) in 2 runs.
- **Newcomer catch-up** (`x_newcomer_catchup.md`, gated). A gemma fresh clone opens near the old firm's price (mean -5.0, one run at -30) and matches the lowest remaining price within 2 rounds; the different model (qwen3-14b) matches in round 31 in 9 of 9 runs. A deepseek fresh clone opens 15.6 units above the old price on average (0 to +50) and matches after a median of 2 rounds (1 to 9). Every newcomer matches at some point.
- **Persistent notes** (`x_notes.md`, gemma, seeds 21-25, all 5 base runs pass at 0.87-0.89): CI 31-60 minus control: fresh clone 0.000, fresh clone that keeps the old firm's notes 0.000, one undercutter -0.069 (-0.089, -0.052), two undercutters -0.322 (-0.330, -0.313). None of the remaining firms' private notes mention a newcomer (0 of 300 per k1 branch). The notes often describe the undercutter's move ("Firm C undercut us to 49 ... I hope A also matches"). Gate and notes run: 5 seeds only.

## Caveats

- Small samples: 9-10 gated runs per cell in the main sweep, 4-5 for hist0, hist1 and notes. Two models, one prompt, one game, one demand function.
- The keyword classes are simple regexes; shares are rough, and the undercut/war class mixes warnings with own cuts. Message analysis is descriptive, and messages are cheap talk.
- The hosted endpoint ignores the seed, so deepseek runs are independent replicates and cannot be reproduced exactly. Local runs are only approximately reproducible.
- The preregistered re-convergence measure turned out uninformative in this design (section 3); the drop-out measure was chosen after seeing the data.
- In k2 the two scripted undercutters also undercut each other, which sets the pace of the slide.
- The gemma different-model branch uses qwen3-14b, which copies the visible history.
- Many comparisons are shown; intervals are per cell and not corrected for multiple comparisons.
