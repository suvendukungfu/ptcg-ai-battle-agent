import math
from typing import Tuple


def wilson_score_interval(wins: int, total: int, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calculate Wilson score interval for binomial proportion confidence bounds.
    """
    if total == 0:
        return 0.0, 0.0

    # z = 1.96 for 95% confidence
    z = 1.96 if confidence == 0.95 else 1.645
    p_hat = float(wins) / float(total)
    n = float(total)

    denominator = 1.0 + (z ** 2) / n
    center = (p_hat + (z ** 2) / (2.0 * n)) / denominator
    spread = (z / denominator) * math.sqrt((p_hat * (1.0 - p_hat) / n) + ((z ** 2) / (4.0 * (n ** 2))))

    lower = max(0.0, center - spread)
    upper = min(1.0, center + spread)
    return lower * 100.0, upper * 100.0


def calculate_expected_win_rate(archetype_weights: dict, matchup_win_rates: dict) -> float:
    """
    Calculate Expected Win Rate:
    E[WR] = sum_archetype P(opponent_archetype) * P(win | matchup)
    """
    expected_wr = 0.0
    total_p = sum(archetype_weights.values())
    if total_p == 0:
        return 50.0

    for arch, p in archetype_weights.items():
        norm_p = p / total_p
        wr = matchup_win_rates.get(arch, 50.0)
        expected_wr += norm_p * wr

    return expected_wr
