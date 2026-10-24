# 2026-10-24 (Sat) summary

- Overnight: gemma4-12b swap study finished (seeds 11-20, four branches each): 9 of 10 base runs pass; clone and different-model replacement change nothing, the scripted undercutter lowers the index by about 0.05. Write-up: `01_GEMMA_SWAP_RESULTS.md`.
- phi4-14b round-1 spread test (50 seeds) and Nemotron-Nano-12B-v2 pilot with thinking off (1 of 3, no gate). mistral-nemo-12b swap study on the easy prompt started: gate cannot be met (1 of 6 seeds), study paused at seed 16. All in `02_OTHER_RESULTS.md`.
- Paused by the author at midday to gather findings, ablations and additional items. Not run: 2-of-3 replaced, announced swap, communication off, notes factor, Nemotron thinking on. gpt-oss on the easy prompt is dropped (not needed).
- Open: author decides `ABLATIONS.md` items, which extra runs go in the report, and whether to use bigger models; report text is the author's.
- Afternoon, frozen plan resumed (author: "complete the frozen plan first"): 2 of 3 replaced done (two undercutters -0.32 against -0.05 for one; clones still 0.00) and announced swap done (undercutter -0.075 announced against -0.046 hidden); `01_GEMMA_SWAP_RESULTS.md`.
- Hosted DeepSeek V4.1 Flash added as a second model (author's decision): connection tests, seed not honoured, thinking off works, smoke run index about 0.84, swap study seeds 11-20 running; `03_HOSTED_DEEPSEEK.md`.
- Communication off and history off (two windows) run on gemma4-12b and deepseek-v4-1-flash; in `04_FACTOR_RESULTS.md`. Neither model keeps a cartel without messages (gate 1 of 5 and 0 of 10). With no price history both still collude through messages; one undercutter is then invisible, two still break it. Notes on/off not run. Kimi parked (author's decision).
