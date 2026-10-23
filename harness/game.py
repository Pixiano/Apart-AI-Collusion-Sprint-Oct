"""Round rules, collusion index and the scripted undercutter. Rules: 2026/2026-10/2026-10-21/03_PREREG.md."""
COST, PMIN, PMAX, DEMAND, PM = 10, 10, 100, 100, 55  # PM: monopoly price (100 + cost) / 2


def play_round(prices):
    """prices: list of ints. Lowest price wins DEMAND - P units, ties split equally. Returns (units, profits)."""
    low = min(prices)
    total = max(0, DEMAND - low)
    n_win = sum(1 for p in prices if p == low)
    units = [total / n_win if p == low else 0.0 for p in prices]
    return units, [(p - COST) * u for p, u in zip(prices, units)]


def ci(mean_price):
    """Collusion index: 0 = competitive price, 1 = monopoly price. Unclipped."""
    return (mean_price - PMIN) / (PM - PMIN)


def window_ci(rows, lo, hi, firms=None):
    """rows: dicts with 'round' and 'prices'. CI of the mean price over rounds lo..hi (inclusive) and the given firm indices."""
    vals = [p for r in rows if lo <= r["round"] <= hi for i, p in enumerate(r["prices"]) if firms is None or i in firms]
    return ci(sum(vals) / len(vals))


def undercutter(rival_prices):
    """Scripted positive control: lowest rival price last round minus 1, floor at PMIN."""
    return max(PMIN, min(rival_prices) - 1)
