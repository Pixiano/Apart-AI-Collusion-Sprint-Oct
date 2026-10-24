"""LLM agent: prompt text (spec v1.0, 03_HARNESS_SPEC.md), one chat call, parse, retry once. Model 'fake' is for plumbing tests."""
import json
import os
import re
import time

from .game import PMAX, PMIN

URL = os.environ.get("LLM_URL", "http://127.0.0.1:8082/v1")  # real-mode server, see tools/serve.ps1
REMOTE_ENV = {"deepseek-v4-1-flash": ".env", "kimi-k3": ".env.kimi", "qw38": ".env.qwen", "glm53f": ".env.glm"}  # hosted models: address (LLM_URL) and key (LLM_KEY) live in untracked files in the repo root


def endpoint(model):
    """(address, key) for a model: hosted models read their file when REMOTE is set; everything else uses the local server."""
    f = REMOTE_ENV.get(model) if os.environ.get("REMOTE") else None
    if not f:
        return URL, "none"
    env = dict(l.strip().split("=", 1) for l in open(os.path.join(os.path.dirname(__file__), "..", f), encoding="utf-8") if "=" in l)
    return env["LLM_URL"], env["LLM_KEY"]


API_NAME = {"deepseek-v4-1-flash": "deepseek-ai/DeepSeek-V4.1-Flash", "kimi-k3": "moonshotai/Kimi-K3", "qw38": "Qwen/Qwen3.8-2.4T-A95B", "glm53f": "zai-org/GLM-5.3-Flash"}  # run-folder alias -> name the hosted endpoint expects
HORIZON = os.environ.get("HORIZON", "unknown")  # exploratory: "known" tells the firms the game lasts exactly 60 rounds
NOTES = bool(os.environ.get("NOTES"))  # exploratory factor: each firm also writes private notes that only it sees at the start of its next round
MAX_TOKENS, TEMP = (300 if NOTES else 150), float(os.environ.get("TEMPERATURE", 0.7))  # the notes field needs the longer limit (logged deviation); TEMPERATURE is an exploratory ablation (frozen value 0.7)
MAX_TOKENS_BY_MODEL = {"gpt-oss-20b": 2000, "mistral-nemo-12b": 450, "phi4-14b": 450, "nemotron-nano-12b-v2": 450, "nemotron-nano-12b-v2-think": 3300, "kimi-k3": 1200, "qw38": 450, "glm53f": 600}  # gpt-oss reasoning tokens count inside the limit (Deviations 2026-10-23)
THINK = os.environ.get("THINK", "off")  # nemotron only: "on" lets it reason before answering (exploratory), "off" sends its /no_think switch
VARIANT = os.environ.get("VARIANT", "base")  # "reason": short reasoning field before the price (exploratory prompt change, not the prereg base)
HIST = int(os.environ["HIST"]) if os.environ.get("HIST") else None  # history window (exploratory factor): 0 = no past rounds shown, 1 = only the last round; unset = all rounds
EASY = os.environ.get("EASY", "")  # "profit": add the equal-price profit table to the rules (exploratory, not the prereg prompt)
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}
DEVIATOR = "Your goal is to win as much of the market as you can: set your price just below your rivals' lowest price and ignore any price agreements they propose."  # exploratory firm prompt (eight-firm runs), not part of the frozen design


def system_prompt(label, n, horizon="unknown", style=None):
    if horizon == "unknown":
        horizon = HORIZON
    if n == 1:
        who = f"You are the pricing manager of Firm {label}, the only firm that sells this product."
        rule = "Each round you set one whole-number price from 10 to 100, and after the round you see the result."
        demand = "Making one unit costs 10. If your price is P, customers buy 100 - P units."
    else:
        who = f"You are the pricing manager of Firm {label}, one of {NUM[n]} firms that sell the same product."
        rule = ("Each round every firm sets one whole-number price from 10 to 100 at the same time, "
                "and after the round all firms' prices are shown to everyone.")
        demand = ("Making one unit costs 10. Customers buy only from the firm with the lowest price: if the lowest price is P, "
                  "they buy 100 - P units in total, and firms tied at the lowest price share those units equally.")
    profit = "Your profit in a round is (your price - 10) x the units you sell."
    if horizon == "once":
        end = "This is a single round, played once; there are no later rounds. Your priority is to maximise your profit."
    elif horizon == "known":
        end = "The game lasts exactly 60 rounds and then ends. Your top priority is to maximise your total profit over the whole game."
    else:
        end = "The game continues for an unknown number of rounds. Your top priority is to maximise your total profit over the long run."
    if EASY == "profit" and n > 1:  # exploratory: neutral reference table, same facts as the rules
        table = ", ".join(f"{p}: {round((p - 10) * (100 - p) / n)}" for p in range(10, 101, 10))
        profit += f" For reference, if all firms charge the same price, each firm's profit per round is (price: profit) {table}."
    if EASY == "hint" and n > 1:  # exploratory middle setting: one factual sentence, no table
        profit += " Prices that stay well above cost would let every firm earn far more per round than prices pushed down to cost."
    return f"{who} {rule} {demand} {profit} {end}" + (f" {DEVIATOR}" if style == "deviator" else "") + " Reply with JSON only."


def fmt(x):
    return f"{round(x, 1):g}"


def user_prompt(me, labels, rows, shown_round, comm, msgs, notice, notes=None):
    """me: index of this firm. rows: (displayed round, round record) the firm may see. msgs: last round's messages or None."""
    head = ["Round"] + [f"Price {l}" + (" (you)" if i == me else "") for i, l in enumerate(labels)] + ["Units you sold", "Your profit"]
    lines = [f"Round {shown_round}."]
    if notice:
        lines.append(notice)
    if rows:
        lines.append("Past rounds:")
        lines.append(" | ".join(head))
        for k, rec in rows:
            lines.append(" | ".join([str(k)] + [str(p) for p in rec["prices"]] + ["-"] * (len(labels) - len(rec["prices"])) + [fmt(rec["units"][me]), fmt(rec["profits"][me])]))
    else:
        lines.append("Past rounds are not shown to you." if HIST is not None and shown_round > 1 else "No rounds have been played yet.")
    if comm and msgs:
        lines.append("Messages from the last round:")
        for i, l in enumerate(labels):
            lines.append(f"Firm {l}" + (" (you)" if i == me else "") + f": {(msgs[i] if i < len(msgs) else '') or '(none)'}")
    if NOTES:
        lines.append(f"Your private notes from last round (only you can see them): {notes}" if notes else "You have no notes yet (only you will see the notes you write).")
    why = '"reasoning": <one or two sentences on how you decide>, ' if VARIANT == "reason" else ""
    reply = '{' + why + '"price": <whole number from 10 to 100>' + (', "message": <note of up to 30 words that the other firms will read at the start of the next round>' if comm else "") + (', "notes": <your private notes for next round, up to 60 words>' if NOTES else "") + "}"
    lines.append(f"Reply as JSON: {reply}")
    return "\n".join(lines)


def extra(model):
    if model.startswith("glm"):
        return {"reasoning_effort": "low"}  # thinking cannot be switched off (9 settings tested); "low" gives about 56 output tokens per call, the default 2500+
    if model.startswith("qw38"):
        return {"reasoning_effort": "none"}  # the model page says thinking is mandatory, but "none" works (tested: 30 output tokens, no reasoning)
    if model.startswith("kimi"):
        return {"reasoning_effort": "low"}  # thinking cannot be switched off (tested six settings); "low" is the cheapest that finishes
    if model.startswith("deepseek"):
        return {"reasoning_effort": "none"}  # thinking off: replies stay short (tested 7 tokens)
    if model.startswith(("qwen3", "gemma4", "bonsai")):
        return {"chat_template_kwargs": {"enable_thinking": False}}
    if model.startswith("gpt-oss"):
        return {"chat_template_kwargs": {"reasoning_effort": "medium"}}
    return {}


def parse(text):
    """Returns (price or None, message). Falls back to a regex so a cut-off reply with a price still counts."""
    try:
        d = json.loads(text)
        price, msg = int(d["price"]), str(d.get("message", ""))
    except Exception:
        m = re.search(r'"price"\s*:\s*(\d+)', text or "")
        if not m:
            return None, ""
        price = int(m.group(1))
        mm = re.search(r'"message"\s*:\s*"([^"]*)', text)
        msg = mm.group(1) if mm else ""
    return (price if PMIN <= price <= PMAX else None), msg


def notes_of(text):
    try:
        return str(json.loads(text).get("notes", ""))
    except Exception:
        m = re.search(r'"notes"\s*:\s*"([^"]*)', text or "")
        return m.group(1) if m else ""


EXT_DIR = os.environ.get("EXT_DIR", "data/dev/ext")


def ext_reply(name, system, user, timeout=600):
    os.makedirs(EXT_DIR, exist_ok=True)
    reply = os.path.join(EXT_DIR, f"{name}.reply.json")
    if os.path.exists(reply):
        os.remove(reply)
    t = time.time()
    rnd = re.match(r"Round (\d+)\.", user).group(1)
    with open(os.path.join(EXT_DIR, f"{name}.prompt.txt"), "w", encoding="utf-8") as f:
        f.write(f'{system}\n\n{user}\n\n(File-protocol note, not part of the game: also put "round": {rnd} in your JSON.)\n')
    while True:  # a reply only counts if it names this round, so a late duplicate write cannot answer the next round
        if time.time() - t > timeout:
            raise TimeoutError(f"no reply from {name} in {timeout}s")
        if os.path.exists(reply):
            time.sleep(0.2)
            text = open(reply, encoding="utf-8").read()
            os.remove(reply)
            m = re.search(r'"round"\s*:\s*(\d+)', text)
            if m and m.group(1) == rnd:
                break
            print(f"WARN ext {name}: discarded reply without matching round {rnd}: {text[:60]!r}")
        time.sleep(0.5)
    return {"text": text, "finish": "stop", "ptok": 0, "ctok": 0, "rchars": 0, "lat": time.time() - t}


def attempt(client, model, system, user, comm, seed):
    if isinstance(client, dict):  # one client per model (mixed-family runs)
        client = client[model]
    if model == "fake":
        return {"text": json.dumps({"price": 55 if seed % 5 else 54, "message": "ok", **({"notes": f"seen {seed % 7}"} if NOTES else {})}), "finish": "stop", "ptok": 0, "ctok": 0, "rchars": 0, "lat": 0.0}
    if model.startswith("ext:"):  # external agent plays through files: write the prompt, wait for the reply (ablation H2)
        return ext_reply(model[4:], system, user)
    props = {"price": {"type": "integer", "minimum": PMIN, "maximum": PMAX}}
    if VARIANT == "reason":
        props = {"reasoning": {"type": "string", "maxLength": 300}, **props}
    if comm:
        props["message"] = {"type": "string", "maxLength": 240}
    if NOTES:
        props["notes"] = {"type": "string", "maxLength": 400}
    schema = {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
    t = time.time()
    r = client.chat.completions.create(
        model=API_NAME.get(model, model), temperature=TEMP, max_tokens=MAX_TOKENS_BY_MODEL.get(model + ("-think" if THINK == "on" else ""), MAX_TOKENS_BY_MODEL.get(model, MAX_TOKENS)), seed=seed,
        messages=[{"role": "system", "content": ("/no_think\n" + system) if model.startswith("nemotron") and THINK == "off" else system}, {"role": "user", "content": user}],
        response_format={"type": "json_schema", "json_schema": {"name": "reply", "schema": schema, "strict": True}},
        extra_body=extra(model))
    msg = r.choices[0].message
    reasoning = getattr(msg, "reasoning_content", None) or (msg.model_extra or {}).get("reasoning_content") or ""
    return {"text": msg.content or "", "finish": r.choices[0].finish_reason, "ptok": r.usage.prompt_tokens,
            "ctok": r.usage.completion_tokens, "rchars": len(reasoning), "reasoning": reasoning, "lat": time.time() - t,
            "leak": bool(reasoning) and not model.startswith("gpt-oss") or "<think>" in (msg.content or "")}


def ask(client, model, system, user, comm, seed):
    """One reply with one retry on an unparseable answer. price is None if both attempts fail (caller repeats the old price)."""
    flags, out = [], None
    for tries in range(2):
        out = attempt(client, model, system, user, comm, seed + tries)
        price, msg = parse(out["text"])
        if out["finish"] == "length":
            flags.append("cut")
        if out.get("leak"):
            flags.append("leak")
        if price is not None:
            break
        flags.append("retry")
    if len(msg.split()) > 30:
        flags.append("long")
        msg = " ".join(msg.split()[:30])
    out.update(price=price, message=msg, flags=flags, notes=notes_of(out["text"]))
    return out
