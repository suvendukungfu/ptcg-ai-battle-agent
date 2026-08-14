import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

from analytics.metrics import wilson_score_interval


@dataclass
class DeckEvaluation:
    deck_name: str
    expected_win_rate: float
    robustness_score: float
    min_matchup_win_rate: float
    max_matchup_win_rate: float
    variance: float
    confidence_interval_95: List[float]
    recommended_tier: str
    rationale: str


class MetaPredictor:
    """
    Dynamic Meta-Game Environment Forecaster & Robustness Optimizer.
    Evaluates expected deck performance across shifting ladder meta distributions,
    and computes worst-case robustness metrics.
    """

    # Baseline meta distribution across ladder archetypes
    DEFAULT_META_DISTRIBUTION: Dict[str, float] = {
        "Bellibolt_Lightning": 0.40,
        "Crustle_Control": 0.25,
        "Alakazam_Psychic": 0.20,
        "Generic_Basic": 0.15,
    }

    # Head-to-head empirical matchup win rates (Row deck vs Column deck)
    EMPIRICAL_MATCHUP_MATRIX: Dict[str, Dict[str, float]] = {
        "Bellibolt_Lightning": {
            "Bellibolt_Lightning": 50.0,
            "Crustle_Control": 62.5,
            "Alakazam_Psychic": 68.0,
            "Generic_Basic": 92.0,
        },
        "Crustle_Control": {
            "Bellibolt_Lightning": 37.5,
            "Crustle_Control": 50.0,
            "Alakazam_Psychic": 54.0,
            "Generic_Basic": 75.0,
        },
        "Alakazam_Psychic": {
            "Bellibolt_Lightning": 32.0,
            "Crustle_Control": 46.0,
            "Alakazam_Psychic": 50.0,
            "Generic_Basic": 64.0,
        },
        "Anti_Crustle_Tech": {
            "Bellibolt_Lightning": 48.0,
            "Crustle_Control": 78.0,
            "Alakazam_Psychic": 60.0,
            "Generic_Basic": 88.0,
        },
    }

    @classmethod
    def evaluate_deck(
        cls,
        deck_name: str,
        meta_distribution: Optional[Dict[str, float]] = None,
        sample_size: int = 150
    ) -> DeckEvaluation:
        meta = meta_distribution or cls.DEFAULT_META_DISTRIBUTION
        matchups = cls.EMPIRICAL_MATCHUP_MATRIX.get(deck_name, {})

        if not matchups:
            return DeckEvaluation(
                deck_name=deck_name,
                expected_win_rate=50.0,
                robustness_score=50.0,
                min_matchup_win_rate=50.0,
                max_matchup_win_rate=50.0,
                variance=0.0,
                confidence_interval_95=[45.0, 55.0],
                recommended_tier="Tier 2",
                rationale="Unindexed custom deck profile.",
            )

        # Compute Expected Win Rate E[WR] = sum( P(Archetype_i) * WR(Deck, Archetype_i) )
        expected_wr = 0.0
        wr_list = []
        for arch, prob in meta.items():
            wr = matchups.get(arch, 50.0)
            expected_wr += prob * wr
            wr_list.append(wr)

        min_wr = min(wr_list)
        max_wr = max(wr_list)
        mean_wr = sum(wr_list) / len(wr_list)
        variance = sum((x - mean_wr) ** 2 for x in wr_list) / len(wr_list)
        std_dev = math.sqrt(variance)

        # Robustness Score: R = min_i(WR_i) - 0.5 * std_dev + 0.5 * mean_wr
        robustness = round(min_wr - (0.5 * std_dev) + (0.5 * mean_wr), 1)

        # 95% Wilson Confidence Bounds
        wins = int(expected_wr * sample_size / 100.0)
        ci_low, ci_high = wilson_score_interval(wins, sample_size, confidence=0.95)

        tier = "Tier 1 (Optimal)" if expected_wr >= 65.0 else ("Tier 1.5" if expected_wr >= 55.0 else "Tier 2")

        rationale = (
            f"Expected Win Rate of {expected_wr:.1f}% across active ladder meta. "
            f"Lowest matchup floor is {min_wr:.1f}%. Robustness index: {robustness:.1f}."
        )

        return DeckEvaluation(
            deck_name=deck_name,
            expected_win_rate=round(expected_wr, 1),
            robustness_score=robustness,
            min_matchup_win_rate=round(min_wr, 1),
            max_matchup_win_rate=round(max_wr, 1),
            variance=round(variance, 1),
            confidence_interval_95=[round(ci_low, 1), round(ci_high, 1)],
            recommended_tier=tier,
            rationale=rationale,
        )

    @classmethod
    def get_all_deck_rankings(
        cls,
        meta_distribution: Optional[Dict[str, float]] = None
    ) -> List[DeckEvaluation]:
        rankings = []
        for deck in cls.EMPIRICAL_MATCHUP_MATRIX.keys():
            rankings.append(cls.evaluate_deck(deck, meta_distribution))

        # Sort by combination of Expected Win Rate and Robustness
        rankings.sort(key=lambda d: (d.expected_win_rate + d.robustness_score), reverse=True)
        return rankings
