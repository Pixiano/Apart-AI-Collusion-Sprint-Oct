# Message classes before a price rise, cut or no change

All communication-on runs and rounds pooled (main, hist0, hist1). A move is the sender's own price next round against this round.

| model | own price next round | messages | price | hold | match | warn | trust | other |
|---|---|---|---|---|---|---|---|---|
| deepseek-v4-1-flash | cut | 1671 | 99% | 77% | 42% | 86% | 53% | 0% |
| deepseek-v4-1-flash | rise | 524 | 98% | 60% | 42% | 75% | 48% | 0% |
| deepseek-v4-1-flash | same | 4765 | 100% | 88% | 16% | 57% | 83% | 0% |
| gemma4-12b | cut | 605 | 63% | 82% | 39% | 44% | 68% | 2% |
| gemma4-12b | rise | 75 | 57% | 60% | 27% | 35% | 69% | 1% |
| gemma4-12b | same | 9470 | 98% | 97% | 3% | 21% | 77% | 0% |
