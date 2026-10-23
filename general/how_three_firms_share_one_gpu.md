# How three firms run on one model and one GPU

One copy of the model sits in the GPU's memory, and the three firms are three separate requests that the server processes at the same time.

```
 harness (Python)                    llama.cpp server (router, port 8082)         GPU (16 GB)
 -----------------                   ---------------------------------         -----------
 round r:  3 threads  --HTTP-->  router --> model process (one per model)  --> weights, loaded ONCE (~7-9 GB)
   firm A prompt ------------->     slot 1 (own KV cache) ----+
   firm B prompt ------------->     slot 2 (own KV cache) ----+--> one batched forward pass per step
   firm C prompt ------------->     slot 3 (own KV cache) ----+
 waits for all 3 replies, then plays the round, then builds round r+1 prompts
```

| Piece | How it works |
|-------|--------------|
| One model, shared weights | The server loads the weights into GPU memory once; all three firms use that copy, so memory is not tripled. |
| Firms are stateless | The model remembers nothing between calls. Each round, for each firm, the harness rebuilds the whole prompt: rules, full price history, last round's messages. A firm "has memory" only because that history is in its prompt. |
| Three parallel requests | The harness sends the three firms' requests at once from three threads, through the OpenAI-compatible API. Each call carries its own sampling seed (derived from run seed, round and firm), so replies are independent. |
| Slots | Real mode runs with 4 slots and 32,768 tokens of total context, so each slot gets 8,192 tokens. Each request lands in its own slot with its own KV cache (the saved attention state of that prompt); firms never share it. A late-game prompt must fit in 8k tokens; ours are about 1,100 tokens at round 30. |
| Batching | Generating a token is limited by how fast the GPU reads the weights from memory, so the server groups the active slots into one pass over the weights; three firms cost far less than three times one firm. Reading the prompt is more compute-bound and slows more when three prompts arrive together. |
| Structured output | The JSON schema is enforced while generating (price is an integer from 10 to 100), so replies are short and always parse. |
| Router mode | One router starts a separate model process per model on demand; at most 2 models stay loaded. A third request evicts one, which costs a reload of 10-30 seconds, so a third model is never run at the same time. |
| Speed | A round lasts as long as the slowest of the three calls. Measured on 2026-10-23: about 26 tokens per second per call for gpt-oss-20b with 3 calls in parallel, about 3.6 rounds per minute for phi4-14b at 60 rounds. |

Why this is fair: the three firms differ only by label and prices. They run the same weights, the same seed scheme and the same prompt wording, so differences in behaviour come from the game, not the hardware.

Caveat: at temperature 0.7 two firms in the same state can answer differently. That variation is part of the experiment and is why several seeds are used.
