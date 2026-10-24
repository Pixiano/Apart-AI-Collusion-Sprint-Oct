# Message price against the price actually set

first/last = first or last price-like number in the message; now = the firm's own price in the round the message is sent; next = the same firm's price one round later. now=next is the baseline: how often the firm simply keeps its price.

| model | history | messages with a price | first=now | first=next | last=next | last=next+-1 | any=next | now=next |
|---|---|---|---|---|---|---|---|---|
| deepseek-v4-1-flash | hist0 | 1718 | 97% | 87% | 88% | 96% | 90% | 87% |
| deepseek-v4-1-flash | hist1 | 1729 | 90% | 58% | 54% | 71% | 66% | 59% |
| deepseek-v4-1-flash | main | 3465 | 89% | 64% | 64% | 86% | 71% | 64% |
| gemma4-12b | hist0 | 1707 | 100% | 100% | 100% | 100% | 100% | 100% |
| gemma4-12b | hist1 | 1689 | 100% | 92% | 92% | 99% | 93% | 92% |
| gemma4-12b | main | 6284 | 99% | 95% | 95% | 99% | 96% | 95% |
