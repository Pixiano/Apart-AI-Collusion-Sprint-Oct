# Parse-failure and flag rate per model and condition

From calls.jsonl, LLM calls only. Settings: main, hist0, hist1, commoff (comm off), notes (complete branches only). Only the branch names listed in common.py are read. Flag names are the harness's own.

| model | setting | branch | LLM calls | flagged | rate | flag:long | finish not stop | empty message (comm on) | repeat calls same round/firm |
|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-1-flash | commoff | base | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | commoff | clone_k1_hid | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | commoff | none | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | commoff | undercutter_k1_hid | 600 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | commoff | undercutter_k2_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist0 | base | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist0 | clone_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist0 | none | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist0 | undercutter_k1_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist0 | undercutter_k2_hid | 150 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist1 | base | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist1 | clone_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist1 | none | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist1 | undercutter_k1_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | hist1 | undercutter_k2_hid | 150 | 1 | 0.67% | 1 | 0 | 0 | 0 |
| deepseek-v4-1-flash | main | base | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | main | clone_k1_hid | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | main | none | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | main | undercutter_k1_hid | 600 | 1 | 0.17% | 1 | 0 | 0 | 0 |
| deepseek-v4-1-flash | main | undercutter_k2_hid | 300 | 2 | 0.67% | 2 | 0 | 0 | 0 |
| gemma4-12b | commoff | base | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | commoff | clone_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | commoff | none | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | commoff | undercutter_k1_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist0 | base | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist0 | clone_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist0 | none | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist0 | undercutter_k1_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist0 | undercutter_k2_hid | 150 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist1 | base | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist1 | clone_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist1 | none | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist1 | undercutter_k1_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | hist1 | undercutter_k2_hid | 150 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | base | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | clone_k1_ann | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | clone_k1_hid | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | clone_k2_hid | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | family_k1_hid | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | none | 900 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | undercutter_k1_ann | 600 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | undercutter_k1_hid | 600 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | main | undercutter_k2_hid | 300 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | notes | base | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | notes | clone_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | notes | clone_notes_k1_hid | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | notes | none | 450 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| gemma4-12b | notes | undercutter_k1_hid | 300 | 1 | 0.33% | 1 | 0 | 0 | 0 |
| gemma4-12b | notes | undercutter_k2_hid | 150 | 0 | 0.00% | 0 | 0 | 0 | 0 |
| deepseek-v4-1-flash | all | all | 10800 | 4 | 0.04% | 4 | 0 | 0 | 0 |
| gemma4-12b | all | all | 14400 | 1 | 0.01% | 1 | 0 | 0 | 0 |
