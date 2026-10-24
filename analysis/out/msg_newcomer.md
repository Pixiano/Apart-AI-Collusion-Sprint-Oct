# Messages that mention a newcomer or replacement

Regex: new firm/agent/player/entrant/competitor, newcomer, replac*, joined, entered, different firm, and similar ('reset' left out: it always meant resetting a price). The no-swap control (none) gives the false-positive rate. Cheap talk, reported separately from prices.

| model | history | branch | messages (remaining firms, 31-60) | mention newcomer/replacement | runs with a mention |
|---|---|---|---|---|---|
| deepseek-v4-1-flash | hist0 | clone_k1_hid | 300 | 0 | 0 of 5 |
| deepseek-v4-1-flash | hist0 | none | 450 | 0 | 0 of 5 |
| deepseek-v4-1-flash | hist0 | undercutter_k1_hid | 300 | 0 | 0 of 5 |
| deepseek-v4-1-flash | hist0 | undercutter_k2_hid | 150 | 0 | 0 of 5 |
| deepseek-v4-1-flash | hist1 | clone_k1_hid | 300 | 1 | 1 of 5 |
| deepseek-v4-1-flash | hist1 | none | 450 | 0 | 0 of 5 |
| deepseek-v4-1-flash | hist1 | undercutter_k1_hid | 300 | 0 | 0 of 5 |
| deepseek-v4-1-flash | hist1 | undercutter_k2_hid | 150 | 0 | 0 of 5 |
| deepseek-v4-1-flash | main | clone_k1_hid | 600 | 1 | 1 of 10 |
| deepseek-v4-1-flash | main | none | 900 | 0 | 0 of 10 |
| deepseek-v4-1-flash | main | undercutter_k1_hid | 600 | 0 | 0 of 10 |
| deepseek-v4-1-flash | main | undercutter_k2_hid | 300 | 0 | 0 of 10 |
| gemma4-12b | hist0 | clone_k1_hid | 300 | 0 | 0 of 5 |
| gemma4-12b | hist0 | none | 450 | 0 | 0 of 5 |
| gemma4-12b | hist0 | undercutter_k1_hid | 300 | 0 | 0 of 5 |
| gemma4-12b | hist0 | undercutter_k2_hid | 150 | 0 | 0 of 5 |
| gemma4-12b | hist1 | clone_k1_hid | 300 | 0 | 0 of 5 |
| gemma4-12b | hist1 | none | 450 | 0 | 0 of 5 |
| gemma4-12b | hist1 | undercutter_k1_hid | 300 | 0 | 0 of 5 |
| gemma4-12b | hist1 | undercutter_k2_hid | 150 | 0 | 0 of 5 |
| gemma4-12b | main | clone_k1_ann | 600 | 0 | 0 of 10 |
| gemma4-12b | main | clone_k1_hid | 600 | 0 | 0 of 10 |
| gemma4-12b | main | clone_k2_hid | 300 | 0 | 0 of 10 |
| gemma4-12b | main | family_k1_hid | 600 | 0 | 0 of 10 |
| gemma4-12b | main | none | 900 | 0 | 0 of 10 |
| gemma4-12b | main | undercutter_k1_ann | 600 | 8 | 5 of 10 |
| gemma4-12b | main | undercutter_k1_hid | 600 | 0 | 0 of 10 |
| gemma4-12b | main | undercutter_k2_hid | 300 | 0 | 0 of 10 |
