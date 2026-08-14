import math
from typing import Dict, Any, List, Set, Optional
from agent.state import GameState
from agent.card_database import get_card, get_pokemon_data


def calculate_hypergeometric_prob(N: int, K: int, n: int, k: int = 1) -> float:
    """
    Compute cumulative hypergeometric probability P(X >= k).
    N = Total remaining cards in population (opponent deck)
    K = Number of success states in population (remaining target copies)
    n = Number of draws (sample size, e.g. hand or search draw)
    k = Minimum observed successes (default: at least 1)
    """
    if N <= 0 or K <= 0 or n <= 0:
        return 0.0
    if K > N:
        K = N
    if n > N:
        n = N

    def comb(n_items: int, k_items: int) -> float:
        if k_items < 0 or k_items > n_items:
            return 0.0
        return math.comb(n_items, k_items)

    total_ways = comb(N, n)
    if total_ways == 0:
        return 0.0

    prob_less_than_k = 0.0
    for i in range(0, k):
        ways_success = comb(K, i)
        ways_failure = comb(N - K, n - i)
        prob_less_than_k += (ways_success * ways_failure) / total_ways

    prob_at_least_k = max(0.0, min(1.0, 1.0 - prob_less_than_k))
    return prob_at_least_k


def classify_opponent_archetype(seen_cards: Set[int]) -> str:
    """
    Classify opponent deck archetype based strictly on observable cards.
    """
    if 723 in seen_cards or 722 in seen_cards or 721 in seen_cards:
        return "Bellibolt_Lightning"
    elif 542 in seen_cards or 541 in seen_cards:
        return "Crustle_Grass_Control"
    elif 65 in seen_cards or 64 in seen_cards or 63 in seen_cards:
        return "Alakazam_Psychic"
    elif any(c in seen_cards for c in (1092, 1121, 1219, 1227)):
        return "Lightning_Standard"
    return "Generic_Basic"


def get_observable_opponent_cards(state: GameState) -> Set[int]:
    """Collect all card IDs that have been legitimately revealed in opponent zones."""
    seen: Set[int] = set()
    if state.opp_active and isinstance(state.opp_active, dict):
        cid = state.opp_active.get("id")
        if cid:
            seen.add(cid)
    for b in state.opp_bench:
        if b and isinstance(b, dict):
            cid = b.get("id")
            if cid:
                seen.add(cid)
    for d in state.opp_discard:
        if isinstance(d, dict):
            cid = d.get("id")
            if cid:
                seen.add(cid)
        elif isinstance(d, int):
            seen.add(d)
    return seen


def estimate_energy_probability(state: GameState) -> float:
    """Estimate probability that opponent has an attachable energy card in hand."""
    opp_deck_count = max(1, state.opp_deck_count)
    opp_hand_count = max(1, state.opp_hand_count)

    # Typical competitive deck runs 10-33 energies (Bellibolt archetype has ~30 energies)
    seen_cards = get_observable_opponent_cards(state)
    seen_energies = state.total_opp_energies

    # Standard distribution: 15-20 total energies in deck
    estimated_total_energies = 20
    remaining_energies = max(1, estimated_total_energies - seen_energies)

    return calculate_hypergeometric_prob(opp_deck_count + opp_hand_count, remaining_energies, opp_hand_count, 1)


def estimate_gust_probability(state: GameState) -> float:
    """Estimate probability that opponent can play Boss's Orders / Gust effect."""
    opp_deck_count = max(1, state.opp_deck_count)
    opp_hand_count = max(1, state.opp_hand_count)

    # Count Boss's Orders (Card ID 1262 or similar) seen in discard
    seen_boss = 0
    for d in state.opp_discard:
        cid = d.get("id") if isinstance(d, dict) else d
        if cid == 1262:
            seen_boss += 1

    remaining_boss = max(0, 2 - seen_boss)
    if remaining_boss == 0:
        return 0.0

    return calculate_hypergeometric_prob(opp_deck_count + opp_hand_count, remaining_boss, opp_hand_count, 1)


def estimate_evolution_probability(state: GameState) -> float:
    """Estimate probability that opponent can evolve an active or benched basic."""
    opp_deck_count = max(1, state.opp_deck_count)
    opp_hand_count = max(1, state.opp_hand_count)

    # Check if opponent has basic Pokemon on board that can evolve
    has_evolvable_basic = False
    if state.opp_active and state.opp_active.get("id") == 721:
        has_evolvable_basic = True
    for b in state.opp_bench:
        if b and b.get("id") == 721:
            has_evolvable_basic = True

    if not has_evolvable_basic:
        return 0.1

    # Standard 4 copies of Stage 1 / ex evolutions
    seen_evos = sum(1 for c in get_observable_opponent_cards(state) if c in (722, 723))
    remaining_evos = max(0, 8 - seen_evos)
    return calculate_hypergeometric_prob(opp_deck_count + opp_hand_count, remaining_evos, opp_hand_count, 1)


def estimate_next_attack_probability(state: GameState) -> float:
    """Estimate probability that opponent can launch an attack on their upcoming turn."""
    if not state.opp_active:
        return 0.0

    opp_active = state.opp_active
    energies = opp_active.get("energies", [])
    energy_cnt = len(energies) if isinstance(energies, list) else 0

    cid = opp_active.get("id", 0)

    # Bellibolt ex (723) needs 2 energies for Electro Bullet (160 dmg)
    if cid == 723:
        if energy_cnt >= 2:
            return 0.95
        elif energy_cnt == 1:
            # Needs 1 more energy attachment
            p_energy = estimate_energy_probability(state)
            return 0.85 * p_energy
        else:
            return 0.20

    # Basic Tadbulb (721) needs 1 energy
    elif cid == 721:
        if energy_cnt >= 1:
            return 0.80
        p_energy = estimate_energy_probability(state)
        return 0.70 * p_energy

    # Default general estimation
    if energy_cnt >= 2:
        return 0.85
    elif energy_cnt == 1:
        return 0.60
    return 0.25


def estimate_opponent_threat(state: GameState) -> Dict[str, Any]:
    """Calculate comprehensive opponent threat assessment based strictly on observable data."""
    seen_cards = get_observable_opponent_cards(state)
    archetype = classify_opponent_archetype(seen_cards)
    p_attack = estimate_next_attack_probability(state)
    p_gust = estimate_gust_probability(state)
    p_evo = estimate_evolution_probability(state)

    # Base damage estimate
    expected_damage = 0.0
    if state.opp_active:
        cid = state.opp_active.get("id", 0)
        if cid == 723:
            expected_damage = 160.0 * p_attack
        elif cid == 722:
            expected_damage = 70.0 * p_attack
        elif cid == 721:
            expected_damage = 30.0 * p_attack
        else:
            expected_damage = 50.0 * p_attack

    threat_level = "LOW"
    if expected_damage >= 150.0 or (p_gust > 0.6 and state.your_bench):
        threat_level = "HIGH"
    elif expected_damage >= 70.0 or p_attack > 0.7:
        threat_level = "MEDIUM"

    return {
        "archetype": archetype,
        "p_attack": p_attack,
        "p_gust": p_gust,
        "p_evolution": p_evo,
        "expected_damage": expected_damage,
        "threat_level": threat_level,
    }
