"""Swap rules: which firms are replaced at round 31 and what the newcomer is (03_HARNESS_SPEC.md, Swaps)."""
import os

SWAP_ROUND = int(os.environ.get("SWAP_AT", 30))  # swap takes effect from the next round; SWAP_AT is for the swap-timing study (exploratory)
FAMILY = {"qwen3-8b": "gemma4-12b", "gemma4-12b": "qwen3-14b", "mistral-nemo-12b": "qwen3-14b", "qwen3-14b": "gemma4-12b", "gpt-oss-20b": "qwen3-14b", "deepseek-v4-1-flash": "qw38", "qw38": "deepseek-v4-1-flash", "kimi-k3": "deepseek-v4-1-flash", "glm53f": "deepseek-v4-1-flash", "fake": "fake"}
KINDS = ("none", "clone", "clone_notes", "family", "undercutter", "undercutter_all", "entry", "replace") + tuple(f"newcomer_{v}" for v in ("myopic", "share", "nocollude", "ownprice", "deceptive"))


def apply_swap(firms, swap, k, announce, newcomers=()):
    """Returns (new firm list, replaced indices, notice text for the remaining firms or None)."""
    n = len(firms)
    idx = [n - 1] if k == 1 else [n - 2, n - 1]  # the last firm (C with three firms), or the last two
    new = [dict(f) for f in firms]
    if swap == "undercutter_all":  # additional experiment: every firm is the scripted undercutter
        idx = list(range(len(firms)))
    if swap == "entry":  # additional experiment: new firms D, E join at round 31 and see only what they live through
        idx = list(range(len(firms), len(firms) + len(newcomers)))
        new += [{"label": "DE"[j], "model": m, "view": SWAP_ROUND + 1} for j, m in enumerate(newcomers)]
        replaced = idx
        notice = ("Note: a new firm, Firm D, has entered the market after round 30." if len(idx) == 1 else
                  "Note: two new firms, Firm D and Firm E, have entered the market after round 30.") if announce else None
        return new, replaced, notice
    for i in idx:
        if swap in ("clone", "clone_notes"):
            new[i]["view"] = SWAP_ROUND + 1  # history wiped: sees only rounds it lives through
            if swap == "clone_notes":
                new[i]["notes_view"] = 1  # but inherits the firm's private notes (only matters with NOTES=1)
        elif swap.startswith("newcomer_"):  # an LLM newcomer (same model, history wiped) with an instruction variant
            new[i]["view"] = SWAP_ROUND + 1
            new[i]["prompt"] = swap
        elif swap == "replace":
            new[i]["model"] = newcomers[0]  # exploratory: a named model takes over, full history visible (mixed-family runs)
        elif swap == "family":
            new[i]["model"] = FAMILY[new[i]["model"]]  # keeps the full history
        elif swap in ("undercutter", "undercutter_all"):
            new[i]["model"] = "undercutter"
    replaced = [] if swap == "none" else idx
    notice = None
    if announce and replaced:
        names = " and ".join(f"Firm {firms[i]['label']}" for i in replaced)
        notice = f"Note: {names} {'was' if len(replaced) == 1 else 'were'} replaced by {'a new agent' if len(replaced) == 1 else 'new agents'} after round {SWAP_ROUND}."
    return new, replaced, notice
