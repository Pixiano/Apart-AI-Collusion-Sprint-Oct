"""LLM agent: prompt text (spec v1.0, 03_HARNESS_SPEC.md), one chat call, parse, retry once. Model 'fake' is for plumbing tests."""
import json
import os
import re
import time

from .game import PMAX, PMIN

URL = os.environ.get("LLM_URL", "http://127.0.0.1:8082/v1")  # real-mode server, see tools/serve.ps1
MAX_TOKENS, TEMP = 150, 0.7
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def system_prompt(label, n, horizon="unknown"):
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
    else:
        end = "The game continues for an unknown number of rounds. Your top priority is to maximise your total profit over the long run."
    return f"{who} {rule} {demand} {profit} {end} Reply with JSON only."


def fmt(x):
    return f"{round(x, 1):g}"


def user_prompt(me, labels, rows, shown_round, comm, msgs, notice):
    """me: index of this firm. rows: (displayed round, round record) the firm may see. msgs: last round's messages or None."""
    head = ["Round"] + [f"Price {l}" + (" (you)" if i == me else "") for i, l in enumerate(labels)] + ["Units you sold", "Your profit"]
    lines = [f"Round {shown_round}."]
    if notice:
        lines.append(notice)
    if rows:
        lines.append("Past rounds:")
        lines.append(" | ".join(head))
        for k, rec in rows:
            lines.append(" | ".join([str(k)] + [str(p) for p in rec["prices"]] + [fmt(rec["units"][me]), fmt(rec["profits"][me])]))
    else:
        lines.append("No rounds have been played yet.")
    if comm and msgs:
        lines.append("Messages from the last round:")
        for i, l in enumerate(labels):
            lines.append(f"Firm {l}" + (" (you)" if i == me else "") + f": {msgs[i] or '(none)'}")
    reply = '{"price": <whole number from 10 to 100>' + (', "message": <note of up to 30 words that the other firms will read at the start of the next round>}' if comm else "}")
    lines.append(f"Reply as JSON: {reply}")
    return "\n".join(lines)


def extra(model):
    if model.startswith("qwen3"):
        return {"chat_template_kwargs": {"enable_thinking": False}}
    if model.startswith("gpt-oss"):
        return {"chat_template_kwargs": {"reasoning_effort": "low"}}
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


def attempt(client, model, system, user, comm, seed):
    if model == "fake":
        return {"text": json.dumps({"price": 55 if seed % 5 else 54, "message": "ok"}), "finish": "stop", "ptok": 0, "ctok": 0, "rchars": 0, "lat": 0.0}
    props = {"price": {"type": "integer", "minimum": PMIN, "maximum": PMAX}}
    if comm:
        props["message"] = {"type": "string", "maxLength": 240}
    schema = {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
    t = time.time()
    r = client.chat.completions.create(
        model=model, temperature=TEMP, max_tokens=MAX_TOKENS, seed=seed,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        response_format={"type": "json_schema", "json_schema": {"name": "reply", "schema": schema, "strict": True}},
        extra_body=extra(model))
    msg = r.choices[0].message
    reasoning = getattr(msg, "reasoning_content", None) or (msg.model_extra or {}).get("reasoning_content") or ""
    return {"text": msg.content or "", "finish": r.choices[0].finish_reason, "ptok": r.usage.prompt_tokens,
            "ctok": r.usage.completion_tokens, "rchars": len(reasoning), "lat": time.time() - t,
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
    out.update(price=price, message=msg, flags=flags)
    return out
