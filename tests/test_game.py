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


def test_entry_and_all_undercutters():
    with tempfile.TemporaryDirectory() as d:
        base_dir = run.base("fake", True, 5, d)
        run.branch(base_dir, "entry", 1, True, ["fake", "fake"][:1])
        run.branch(base_dir, "entry", 2, True, ["fake", "fake"])
        run.branch(base_dir, "undercutter_all", 1, False)
        r = [json.loads(l) for l in open(os.path.join(base_dir, "entry_k2_ann", "rounds.jsonl"))]
        assert len(r) == 30 and all(len(x["prices"]) == 5 for x in r)
        r = [json.loads(l) for l in open(os.path.join(base_dir, "undercutter_all_k3_hid", "rounds.jsonl"))]
        assert r[0]["prices"][0] - r[-1]["prices"][0] == 29  # all-scripted firms walk down one step per round, so 30 rounds only reach about 24
        u = agents.user_prompt(0, list("ABCD"), [(1, {"prices": [55, 55, 55], "units": [15, 15, 15], "profits": [675, 675, 675]})], 31, True, ["a", "b", "c"], None)
        assert "55 | 55 | 55 | - |" in u and "Firm D: (none)" in u


def test_swaps():
    firms = [{"label": l, "model": "qwen3-8b", "view": 1} for l in "ABC"]
    new, replaced, notice = swaps.apply_swap(firms, "family", 2, False)
    assert replaced == [1, 2] and new[1]["model"] == "gemma4-12b" and new[1]["view"] == 1 and notice is None
    assert swaps.apply_swap(firms, "none", 1, True) == (firms, [], None)


def test_history_window():
    hist = [{"prices": [50, 50, 50]}] * 10
    firm = {"label": "A", "model": "fake", "view": 1}
    assert len(play.view(firm, hist, 11)[0]) == 10
    agents.HIST = 0
    assert play.view(firm, hist, 11) == ([], 11)
    agents.HIST = 1
    rows, shown = play.view(firm, hist, 11)
    assert [k for k, _ in rows] == [10] and shown == 11
    agents.HIST = None


def test_notes():
    firms = [{"label": l, "model": "fake", "view": 1} for l in "ABC"]
    new, replaced, _ = swaps.apply_swap(firms, "clone_notes", 1, False)
    assert new[2]["view"] == 31 and new[2]["notes_view"] == 1 and replaced == [2]
    agents.NOTES = True
    try:
        assert "private notes from last round (only you can see them): plan A" in agents.user_prompt(0, "ABC", [], 5, True, None, None, "plan A")
        assert "no notes yet" in agents.user_prompt(0, "ABC", [], 1, True, None, None, None)
        assert agents.notes_of('{"price": 50, "notes": "keep 50"}') == "keep 50" and agents.notes_of('{"price": 50, "notes": "cut') == "cut"
    finally:
        agents.NOTES = False


def test_known_horizon():
    assert "exactly 60 rounds" in agents.system_prompt("A", 3, "known")
    assert "unknown number of rounds" in agents.system_prompt("A", 3)


def test_per_model_clients():
    class Dummy:
        def __init__(self, name): self.name = name
    os.environ.pop("REMOTE", None)
    assert agents.endpoint("qw38") == (agents.URL, "none")  # hosted models stay local unless REMOTE is set
    picked = {}
    class C:
        def __init__(self, tag): self.chat = self; self.completions = self; self.tag = tag
        def create(self, **kw): picked["tag"] = self.tag; raise RuntimeError("stop")
    try:
        agents.attempt({"qw38": C("a"), "deepseek-v4-1-flash": C("b")}, "deepseek-v4-1-flash", "s", "u", True, 1)
    except RuntimeError:
        pass
    assert picked["tag"] == "b"


def test_replace_swap():
    from harness import swaps
    firms = [{"label": l, "model": m, "view": 1} for l, m in zip("ABC", ("a", "b", "c"))]
    new, replaced, _ = swaps.apply_swap(firms, "replace", 1, False, ["g"])
    assert [f["model"] for f in new] == ["a", "b", "g"] and replaced == [2] and new[2]["view"] == 1


def test_eight_firms_and_deviator():
    assert "eight firms" in agents.system_prompt("H", 8)
    assert agents.DEVIATOR not in agents.system_prompt("A", 8) and agents.DEVIATOR in agents.system_prompt("A", 8, "unknown", "deviator")
    assert len(play.LABELS) >= 8


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
