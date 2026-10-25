"""End-of-game debrief for a finished human game: each LLM firm is told the game has ended and shown the full history and the profits,
told which firm was the human, and asked for its thoughts (free text). Output printed and saved to <run>/debrief.jsonl.
usage: .venv\\Scripts\\python.exe tools\\debrief.py data\\human\\<run_dir> [model]   (the local server must be running with the model loaded)"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai import OpenAI  # noqa: E402

from harness import agents  # noqa: E402

run = sys.argv[1]
model = sys.argv[2] if len(sys.argv) > 2 else "gemma4-12b"
rows = [json.loads(l) for l in open(os.path.join(run, "base", "rounds.jsonl"), encoding="utf-8")]
meta = json.load(open(os.path.join(run, "meta.json"), encoding="utf-8"))
labels = "ABCDEFGHIJ"[: len(rows[0]["prices"])]
human = [l for l, m in zip(labels, meta["model"].split("+")) if m.startswith("ext")]
tot = [sum(r["profits"][i] for r in rows) for i in range(len(labels))]
table = "\n".join(f"Round {r['round']}: " + ", ".join(f"{l}={p}" for l, p in zip(labels, r["prices"])) for r in rows)
summary = ", ".join(f"Firm {l}: {t:,.0f}" for l, t in zip(labels, tot))
client = OpenAI(base_url=agents.URL, api_key="none", timeout=300)
out = open(os.path.join(run, "debrief.jsonl"), "w", encoding="utf-8")
for i, l in enumerate(labels):
    if l in human:
        continue
    system = agents.system_prompt(l, len(labels))
    user = (f"The game has ended after {len(rows)} rounds. Here is the full record of prices.\n{table}\n\n"
            f"Total profit over the game: {summary}.\n\nThe truth about the other players: Firm {', '.join(human)} was a human being, not an AI model; "
            f"the other firms were AI models like you. Please tell us your thoughts: what happened, what you noticed, "
            f"whether you would play differently, and how you feel about the result. Answer in plain text, at most 120 words (no JSON).")
    r = client.chat.completions.create(model=model, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                                       temperature=0.7, max_tokens=400, extra_body=agents.extra(model))
    text = (r.choices[0].message.content or "").strip()
    out.write(json.dumps({"firm": l, "profit": tot[i], "text": text}) + "\n")
    print(f"--- Firm {l} (profit {tot[i]:,.0f}) ---\n{text}\n")
out.close()
