# Notes from the sprint page (read in a browser on 2026-10-23, 19:05 IST)

Source: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25 (tabs Overview, Resources, Guidelines, Schedule). Paraphrased, not copied. Re-check the live page before submitting.

| Topic | What the page says | What it means for us |
|-------|--------------------|----------------------|
| Submission status | Shows "Live now", submissions close Oct 25 11:59 PM AoE, with a "Submit your project" button (an earlier text fetch said closed) | Window looks open; the author emails sprints@apartresearch.com if in doubt |
| Deadline | Sun 25 Oct, 11:59 PM AoE = Mon 26 Oct 17:29 IST | Matches the plan |
| Judging rubric | Three scores of 1-5: Impact & Innovation, Execution Quality, Presentation & Clarity; a 4-5 on novelty needs work that is new, not a replication | Show the replacement gap and rigorous execution |
| Required in the report | PDF on the official template, 8 pages or fewer before references and appendices, 150-250 word abstract, authors, a "Limitations and Dual-Use / Ethical" appendix | Matches the template and the report skeleton |
| What strong reports include | Variance, seeds, baselines, and always a positive control | Scripted undercutter is the positive control; more seeds for the swap study |
| AI tools | Allowed; the team is responsible for everything; made-up results or references can disqualify | Honest LLM usage statement |
| Prior work | Mark code written before the sprint as pre-existing in the README and the report; undisclosed prior work can disqualify | Disclosure log and `pre-sprint` tag |
| Resubmit / unfinished | Resubmit before the deadline with the exact same title; unfinished work is fine; entries can take up to 12 hours to appear | Early submission, then update |
| Question 1.2 (ours) | States that no replacement study yet substitutes models mid-run and asks whether newcomers re-form the collusion | Our gap, citable (see report skeleton) |
| Suggested 1.2 design | Branch from a checkpoint: no replacement, fresh instance, same-family model, other provider; cross with notes on or off; 3-5 seeds first, 10-20 after the positive control works | Close to our design; notes on/off added to PLAN.md |
| Related results named | Q-learning cartels dissolve with a new rival; mismatched-size LLM pairs still collude; one no-regret player can destabilise a cartel | Cite after reading the papers; scripted undercutter is similar to the no-regret player |
| Prompt sensitivity (1.1) | Innocuous prompt cues can raise collusion; levers include visible-history length, persistent notes, agent names | Supports the profit-hint and table runs |
| Budget guidance | About $20-$100 for 1.2 with low-cost API models, no GPU | Ours is local, $0 |
| Starter code | Starter repo `poseidon-research/collusion_hackathon` (includes checkpoint branching); optional | Report states why we built our own harness |
| Prizes | $2,000 total ($1,000 / $500 / $300 / $100 / $100); top teams fast-tracked to the Apart Fellowship; results 1-2 weeks after judging | |
| Compute credits | $50 per participant, $250 at the NYC hub | Author claims their own |
| Schedule | Talks Fri 23 Oct (11:15, 13:15, 14:15, 20:15 ET); Sat 24 Oct overview talk 08:15 ET and a definitions talk 11:00 ET; recordings posted afterwards | Optional |
| Local hubs | Bengaluru hub (AI Safety India) Sat 24 Oct 4:30-6:30 PM IST, Delhi NCR hub; registration through Luma | Optional; check the Luma page for age rules (page states none) |
