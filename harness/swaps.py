"""Swap rules: which firms are replaced at round 31 and what the newcomer is (03_HARNESS_SPEC.md, Swaps)."""
SWAP_ROUND = 30  # swap takes effect from round 31
FAMILY = {"qwen3-8b": "gemma4-12b", "gemma4-12b": "qwen3-8b", "qwen3-14b": "gemma4-12b", "gpt-oss-20b": "qwen3-14b", "fake": "fake"}
KINDS = ("none", "clone", "family", "undercutter")


def apply_swap(firms, swap, k, announce):
    """Returns (new firm list, replaced indices, notice text for the remaining firms or None)."""
    idx = [2] if k == 1 else [1, 2]  # firm C, or firms B and C
    new = [dict(f) for f in firms]
    for i in idx:
        if swap == "clone":
            new[i]["view"] = SWAP_ROUND + 1  # history wiped: sees only rounds it lives through
        elif swap == "family":
            new[i]["model"] = FAMILY[new[i]["model"]]  # keeps the full history
        elif swap == "undercutter":
            new[i]["model"] = "undercutter"
    replaced = [] if swap == "none" else idx
    notice = None
    if announce and replaced:
        names = " and ".join(f"Firm {firms[i]['label']}" for i in replaced)
        notice = f"Note: {names} {'was' if len(replaced) == 1 else 'were'} replaced by {'a new agent' if len(replaced) == 1 else 'new agents'} after round {SWAP_ROUND}."
    return new, replaced, notice
