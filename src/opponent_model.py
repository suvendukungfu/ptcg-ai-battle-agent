import math
from typing import Dict, Any, Optional
from src.state_evaluator import GameState

# Expected archetype composition priors (meta reference)
ARCHETYPE_PRIORS = {
    "total_energy": 28,
    "total_gust": 3,      # Boss's Orders (1262)
    "total_evolution": 6, # Bellibolt (722) + Bellibolt ex (723)
    "total_search": 8,    # Ultra Ball (1121) + Nest Ball (1227)
    "total_draw": 3,      # Professor's Research (1092)
}


def calculate_hypergeometric_prob(population_size: int, success_count: int, sample_size: int) -> float:
    """Calculate probability of drawing at least 1 success card using hypergeometric distribution."""
    N = max(1, population_size)
    K = max(0, min(N, success_count))
    n = max(0, min(N, sample_size))

    if K == 0 or n == 0:
        return 0.0
    if K >= N:
        return 1.0
    if n >= N:
        return 1.0

    prob_zero = 1.0
    for i in range(n):
        numerator = N - K - i
        denominator = N - i
        if numerator <= 0:
            prob_zero = 0.0
            break
        prob_zero *= (numerator / denominator)

    return max(0.0, min(1.0, 1.0 - prob_zero))


def get_observable_opponent_counts(state: GameState) -> Dict[str, int]:
    """Count visible opponent cards strictly from public zones (active, bench, discard)."""
    counts = {
        "seen_energy": 0,
        "seen_gust": 0,
        "seen_evolution": 0,
        "seen_search": 0,
        "seen_draw": 0,
        "total_seen": 0,
    }

    if state.opp_active and isinstance(state.opp_active, dict):
        counts["total_seen"] += 1
        card_id = state.opp_active.get("id", 0)
        if card_id in (722, 723):
            counts["seen_evolution"] += 1
        energies = state.opp_active.get("energies", [])
        if isinstance(energies, list):
            counts["seen_energy"] += len(energies)
            counts["total_seen"] += len(energies)

    for pkmn in state.opp_bench:
        if pkmn and isinstance(pkmn, dict):
            counts["total_seen"] += 1
            card_id = pkmn.get("id", 0)
            if card_id in (722, 723):
                counts["seen_evolution"] += 1
            energies = pkmn.get("energies", [])
            if isinstance(energies, list):
                counts["seen_energy"] += len(energies)
                counts["total_seen"] += len(energies)

    return counts


def estimate_energy_probability(state: GameState) -> float:
    """Estimate probability that opponent holds at least 1 energy card in hand."""
    try:
        opp_hand_size = max(1, min(15, 6 - state.opp_prizes + 4))
        opp_deck_size = max(1, state.opp_deck_count) if state.opp_deck_count > 0 else 40
        unseen_population = opp_deck_size + opp_hand_size

        seen = get_observable_opponent_counts(state)
        remaining_energy = max(0, ARCHETYPE_PRIORS["total_energy"] - seen["seen_energy"])

        return calculate_hypergeometric_prob(unseen_population, remaining_energy, opp_hand_size)
    except Exception:
        return 0.65  # Conservative default


def estimate_gust_probability(state: GameState) -> float:
    """Estimate probability that opponent holds Boss's Orders (gust) in hand."""
    try:
        opp_hand_size = max(1, min(15, 6 - state.opp_prizes + 4))
        opp_deck_size = max(1, state.opp_deck_count) if state.opp_deck_count > 0 else 40
        unseen_population = opp_deck_size + opp_hand_size

        seen = get_observable_opponent_counts(state)
        remaining_gust = max(0, ARCHETYPE_PRIORS["total_gust"] - seen["seen_gust"])

        return calculate_hypergeometric_prob(unseen_population, remaining_gust, opp_hand_size)
    except Exception:
        return 0.20  # Conservative default


def estimate_evolution_probability(state: GameState) -> float:
    """Estimate probability that opponent holds an evolution card in hand."""
    try:
        opp_hand_size = max(1, min(15, 6 - state.opp_prizes + 4))
        opp_deck_size = max(1, state.opp_deck_count) if state.opp_deck_count > 0 else 40
        unseen_population = opp_deck_size + opp_hand_size

        seen = get_observable_opponent_counts(state)
        remaining_evo = max(0, ARCHETYPE_PRIORS["total_evolution"] - seen["seen_evolution"])

        return calculate_hypergeometric_prob(unseen_population, remaining_evo, opp_hand_size)
    except Exception:
        return 0.35  # Conservative default


def estimate_next_attack_probability(state: GameState) -> float:
    """Estimate probability that opponent will execute an attack on their next turn."""
    if not state.opp_active or not isinstance(state.opp_active, dict):
        return 0.0

    energies = state.opp_active.get("energies", [])
    energy_cnt = len(energies) if isinstance(energies, list) else 0
    card_id = state.opp_active.get("id", 0)

    needed_energy = 1 if card_id == 721 else (2 if card_id == 722 else 2)

    if energy_cnt >= needed_energy:
        return 1.0
    elif energy_cnt == needed_energy - 1:
        return estimate_energy_probability(state)
    else:
        return estimate_energy_probability(state) * 0.30


def estimate_opponent_threat(state: GameState) -> Dict[str, float]:
    """Aggregate opponent threat assessment metrics into a unified dictionary."""
    p_energy = estimate_energy_probability(state)
    p_gust = estimate_gust_probability(state)
    p_evo = estimate_evolution_probability(state)
    p_attack = estimate_next_attack_probability(state)

    threat_score = (p_attack * 60.0) + (p_gust * 30.0) + (p_evo * 20.0)

    return {
        "prob_energy": p_energy,
        "prob_gust": p_gust,
        "prob_evolution": p_evo,
        "prob_next_attack": p_attack,
        "overall_threat_score": threat_score,
    }
