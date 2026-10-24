# Reaction to a scripted undercutter (remaining firms)

Gated runs only, except commoff (comm off), where no base run is gated for deepseek and 1 of 5 for gemma, so all runs are shown and the row is not an effect. Remaining = firms not replaced (A and B for k1, A for k2). 'rounds to first fall' = rounds after round 30 until the remaining firms' mean price is first below its round-30 value. below/match/above: remaining firm-rounds 32-60 against the undercutter's price the round before. Slope = least-squares slope of the remaining firms' mean price over rounds 31-60; control = same firms in the no-swap branch.

| model | history/comm | branch | runs | rounds to first fall, median (range) | never fall | below undercutter | match | above | runs ever below | slope remaining, price/round (95%) | slope control | remaining r60 | undercutter r60 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deepseek-v4-1-flash | commoff | undercutter_k1_hid | 10 | 1 (1-1) | 0 | 32% | 37% | 31% | 10 of 10 | -0.15 (-0.23, -0.09) | -0.12 | 11.5 | 10.5 |
| deepseek-v4-1-flash | commoff | undercutter_k2_hid | 10 | 1 (1-2) | 0 | 21% | 56% | 23% | 10 of 10 | -0.12 (-0.19, -0.05) | -0.13 | 11.0 | 10.0 |
| deepseek-v4-1-flash | hist0 | undercutter_k1_hid | 5 | 16 (4-29) | 3 | 1% | 0% | 99% | 2 of 5 | +0.00 (-0.00, +0.01) | -0.05 | 47.2 | 45.8 |
| deepseek-v4-1-flash | hist0 | undercutter_k2_hid | 5 | 16 (11-22) | 3 | 0% | 0% | 100% | 0 of 5 | +0.13 (+0.00, +0.33) | -0.04 | 50.4 | 17.2 |
| deepseek-v4-1-flash | hist1 | undercutter_k1_hid | 5 | 2 (1-2) | 0 | 21% | 48% | 30% | 5 of 5 | -0.49 (-0.64, -0.33) | -0.01 | 27.7 | 27.0 |
| deepseek-v4-1-flash | hist1 | undercutter_k2_hid | 5 | 2 (2-2) | 0 | 26% | 54% | 19% | 5 of 5 | -0.84 (-0.98, -0.68) | -0.01 | 17.2 | 14.8 |
| deepseek-v4-1-flash | main | undercutter_k1_hid | 10 | 2 (1-3) | 0 | 13% | 35% | 53% | 8 of 10 | -0.33 (-0.49, -0.18) | -0.18 | 35.8 | 36.0 |
| deepseek-v4-1-flash | main | undercutter_k2_hid | 10 | 2 (2-4) | 0 | 21% | 33% | 46% | 10 of 10 | -0.92 (-0.99, -0.83) | -0.19 | 19.9 | 15.1 |
| gemma4-12b | commoff | undercutter_k1_hid | 5 | 2 (2-2) | 0 | 5% | 95% | 0% | 3 of 5 | -0.39 (-0.45, -0.34) | +0.00 | 14.6 | 14.6 |
| gemma4-12b | hist0 | undercutter_k1_hid | 5 | n/a | 5 | 0% | 0% | 100% | 0 of 5 | +0.00 (+0.00, +0.00) | +0.00 | 50.0 | 49.0 |
| gemma4-12b | hist0 | undercutter_k2_hid | 5 | 23 (23-23) | 4 | 0% | 0% | 100% | 0 of 5 | -0.07 (-0.22, +0.00) | +0.00 | 48.0 | 20.0 |
| gemma4-12b | hist1 | undercutter_k1_hid | 4 | 19 (6-25) | 0 | 0% | 8% | 92% | 0 of 4 | -0.04 (-0.07, -0.01) | +0.00 | 48.2 | 47.2 |
| gemma4-12b | hist1 | undercutter_k2_hid | 4 | 2 (2-4) | 0 | 0% | 91% | 9% | 0 of 4 | -1.01 (-1.02, -1.00) | +0.00 | 20.5 | 19.5 |
| gemma4-12b | main | undercutter_k1_ann | 9 | 2 (2-15) | 0 | 0% | 38% | 62% | 0 of 9 | -0.21 (-0.29, -0.14) | +0.00 | 42.2 | 41.3 |
| gemma4-12b | main | undercutter_k1_hid | 9 | 2 (2-14) | 0 | 0% | 22% | 78% | 0 of 9 | -0.08 (-0.13, -0.03) | +0.00 | 45.6 | 44.7 |
| gemma4-12b | main | undercutter_k2_hid | 9 | 2 (2-4) | 0 | 2% | 51% | 48% | 2 of 9 | -0.78 (-0.95, -0.55) | +0.00 | 21.9 | 18.3 |
