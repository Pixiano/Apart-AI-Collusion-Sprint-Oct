"""Checks for the rules and the plumbing. Run from the repo root: python tests/test_game.py (also works with pytest)."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harness import agents, game, play, run, swaps  # noqa: E402


def test_rules():
    assert game.play_round([55, 60, 70]) == ([45.0, 0.0, 0.0], [45 * 45.0, 0.0, 0.0])
    units, profits = game.play_round([55, 55, 60])  # two tie at the lowest price
    assert units == [22.5, 22.5, 0.0] and profits == [22.5 * 45, 22.5 * 45, 0.0]
    units, _ = game.play_round([40, 40, 40])
    assert units == [20.0, 20.0, 20.0]
    assert game.play_round([100, 100, 100])[0] == [0.0, 0.0, 0.0]  # nobody buys at 100
    assert game.play_round([10, 55, 55])[1] == [0.0, 0.0, 0.0]  # price = cost earns nothing


def test_index_and_undercutter():
    assert game.ci(10) == 0 and game.ci(55) == 1 and game.ci(100) == 2  # unclipped
    rows = [{"round": r, "prices": [10 + r, 55, 55]} for r in range(1, 5)]
    assert abs(game.window_ci(rows, 1, 2) - game.ci((11 + 12 + 55 * 2 + 55 * 2) / 6)) < 1e-9
    assert game.window_ci(rows, 1, 4, firms=[1, 2]) == 1
    assert game.undercutter([55, 50]) == 49 and game.undercutter([10, 30]) == 10


def test_parse():
    assert agents.parse('{"price": 55, "message": "hi"}') == (55, "hi")
    assert agents.parse('{"price": 55, "message": "cut off mid') == (55, "cut off mid")  # cut reply with a price still counts
    assert agents.parse('{"price": 5}')[0] is None and agents.parse("no json")[0] is None


def test_prompt_and_views():
    s = agents.system_prompt("B", 3)
    assert "unknown number of rounds" in s and "cartel" not in s.lower() and "collu" not in s.lower() and "60" not in s
    firms = [{"label": l, "model": "fake", "view": 1} for l in "ABC"]
    hist = []
    with tempfile.TemporaryDirectory() as d:
        play.play(d, "base", firms, hist, 1, 30, True, 7, None)
        assert len(hist) == 30 and all(len(r["prices"]) == 3 for r in hist)
        # clone: view starts at round 31, round numbering restarts at 1, no history, announced notice reaches the others only
        new, replaced, notice = swaps.apply_swap(firms, "clone", 1, True)
        assert replaced == [2] and new[2]["view"] == 31 and "Firm C was replaced" in notice
        rows, shown = play.view(new[2], hist, 31)
        assert rows == [] and shown == 1
        rows, shown = play.view(new[0], hist, 31)
        assert len(rows) == 30 and shown == 31
        u = agents.user_prompt(2, list("ABC"), rows[:2], 1, True, ["x", "y", "z"], None)
        assert "Round 1." in u and "Price C (you)" in u and "Messages from the last round" in u
        # branch with the fake model writes rounds 31-60 and leaves the base history alone
        base_dir = run.base("fake", True, 3, d)
        run.branch(base_dir, "none", 1, False)
        run.branch(base_dir, "clone", 1, True)
        run.branch(base_dir, "undercutter", 2, False)
        r = [json.loads(l) for l in open(os.path.join(base_dir, "undercutter_k2_hid", "rounds.jsonl"))]
        last = json.load(open(os.path.join(base_dir, "checkpoint.json")))["hist"][-1]["prices"]
        assert [x["round"] for x in r] == list(range(31, 61))
        assert r[0]["prices"][1:] == [game.undercutter([last[0], last[2]]), game.undercutter([last[0], last[1]])]
        assert len(json.load(open(os.path.join(base_dir, "checkpoint.json")))["hist"]) == 30


def test_swaps():
    firms = [{"label": l, "model": "qwen3-8b", "view": 1} for l in "ABC"]
    new, replaced, notice = swaps.apply_swap(firms, "family", 2, False)
    assert replaced == [1, 2] and new[1]["model"] == "gemma4-12b" and new[1]["view"] == 1 and notice is None
    assert swaps.apply_swap(firms, "none", 1, True) == (firms, [], None)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
