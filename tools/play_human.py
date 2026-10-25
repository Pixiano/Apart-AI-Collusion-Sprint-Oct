"""Terminal player for the human-firm games: answers the harness's file hook (EXT_DIR, name 'human') from the keyboard.
usage (second terminal, repo root): .venv\\Scripts\\python.exe tools\\play_human.py [data\\human_ext1] [human]
Shows each round's prompt, asks for a price (10-100) and an optional message (30 words), writes <name>.reply.json. Ctrl-C quits."""
import json
import os
import re
import sys
import time

d = sys.argv[1] if len(sys.argv) > 1 else "data/human_ext1"
name = sys.argv[2] if len(sys.argv) > 2 else "human"
prompt, reply = os.path.join(d, f"{name}.prompt.txt"), os.path.join(d, f"{name}.reply.json")
done = 0
first = True
print(f"Waiting for the game in {d} ... (Ctrl-C to quit)")
while True:
    try:
        text = open(prompt, encoding="utf-8").read()
    except OSError:
        time.sleep(0.5)
        continue
    m = re.search(r"^Round (\d+)\.", text, re.M)
    if not m or int(m.group(1)) <= done:
        time.sleep(0.5)
        continue
    rnd = int(m.group(1))
    body = text.split("\n\n", 1)[1] if "\n\n" in text and not first else text  # the rules are shown once; later rounds show the round part only
    body = body.rsplit("\n\n(File-protocol note", 1)[0]
    print("\n" + "=" * 70 + "\n" + (body if first else body[body.index("Round "):]))
    first = False
    while True:
        s = input("price (10-100)> ").strip()
        if s.isdigit() and 10 <= int(s) <= 100:
            break
        print("whole number from 10 to 100")
    msg = " ".join(input("message (max 30 words, Enter for none)> ").split()[:30])
    tmp = reply + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"round": rnd, "price": int(s), "message": msg}, f)
    os.replace(tmp, reply)
    done = rnd
    print(f"sent round {rnd}: price {s}")
