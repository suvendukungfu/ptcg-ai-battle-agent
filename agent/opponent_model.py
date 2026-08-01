import math
from typing import Dict, Any, List, Set, Optional
from dataclasses import dataclass, field
from enum import Enum

from agent.state import GameState
from agent.card_database import get_card, get_pokemon_data


class ThreatCategory(str, Enum):
    ATTACK_THREAT = "ATTACK_THREAT"
    ENERGY_RAMP = "ENERGY_RAMP"
    EVOLUTION_THREAT = "EVOLUTION_THREAT"
    BENCH_ENGINE = "BENCH_ENGINE"
    RESOURCE_ENGINE = "RESOURCE_ENGINE"
    CONTROL_THREAT = "CONTROL_THREAT"
    PRIZE_RACE = "PRIZE_RACE"
    STALL = "STALL"
    UNKNOWN = "UNKNOWN"


class ThreatReadiness(str, Enum):
    T0_READY = "T0_READY"          # Ready to attack now (ΔE == 0)
    T1_NEXT_TURN = "T1_NEXT_TURN"  # Likely ready next turn (ΔE == 1)
    T2_SETUP = "T2_SETUP"          # Requires 2 attachments / turns (ΔE == 2)
    T3_DISTANT = "T3_DISTANT"      # Distant threat (ΔE >= 3 or unpowered basic)


@dataclass
class OpponentThreat:
    card_id: int
    name: str
    is_ex: bool
    hp: float
    max_hp: float
    energy_attached: int
    attack_cost: int
    raw_damage: float
    effective_damage: float
    readiness: ThreatReadiness
    is_lethal: bool
    is_safeguard_blocked: bool
    categories: List[ThreatCategory] = field(default_factory=list)
    threat_score: float = 0.0


@dataclass
class OpponentBoardModel:
    active_threat: Optional[OpponentThreat]
    bench_threats: List[OpponentThreat]
    primary_threat: Optional[OpponentThreat]
    total_known_energies: int
    estimated_hand_energy_prob: float
    estimated_hand_gust_prob: float
    opponent_win_condition: str
    threat_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'


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

    return max(0.0, min(1.0, 1.0 - prob_less_than_k))


def get_observable_opponent_cards(state: GameState) -> Set[int]:
    """Collect all card IDs legitimately revealed in opponent visible zones."""
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


def classify_opponent_archetype(seen_cards: Set[int]) -> str:
    """Classify opponent deck archetype based strictly on observable cards."""
    if any(c in seen_cards for c in (723, 722, 721)):
        return "Bellibolt_Lightning"
    elif any(c in seen_cards for c in (542, 541, 345, 344)):
        return "Crustle_Grass_Control"
    elif any(c in seen_cards for c in (65, 64, 63)):
        return "Alakazam_Psychic"
    elif any(c in seen_cards for c in (678, 677, 674, 673)):
        return "Lucario_Fighting_Aggro"
    return "Generic_Standard"


def estimate_energy_probability(state: GameState) -> float:
    """Estimate probability that opponent holds an attachable energy card in hand."""
    opp_deck_count = max(1, getattr(state, "opp_deck_count", 30))
    opp_hand_count = max(1, getattr(state, "opp_hand_count", 4))
    seen_energies = getattr(state, "total_opp_energies", 0)

    estimated_total_energies = 18
    remaining_energies = max(1, estimated_total_energies - seen_energies)
    return calculate_hypergeometric_prob(opp_deck_count + opp_hand_count, remaining_energies, opp_hand_count, 1)


def estimate_gust_probability(state: GameState) -> float:
    """Estimate probability that opponent holds Boss's Orders / Gust in hand."""
    opp_deck_count = max(1, getattr(state, "opp_deck_count", 30))
    opp_hand_count = max(1, getattr(state, "opp_hand_count", 4))

    seen_boss = 0
    opp_discard = getattr(state, "opp_discard", [])
    for d in opp_discard:
        cid = d.get("id") if isinstance(d, dict) else d
        if cid in (1182, 1262):  # Boss's Orders
            seen_boss += 1

    remaining_boss = max(0, 2 - seen_boss)
    if remaining_boss == 0:
        return 0.0
    return calculate_hypergeometric_prob(opp_deck_count + opp_hand_count, remaining_boss, opp_hand_count, 1)


def estimate_evolution_probability(state: GameState) -> float:
    """Estimate probability that opponent can evolve an active or benched basic."""
    opp_deck_count = max(1, getattr(state, "opp_deck_count", 30))
    opp_hand_count = max(1, getattr(state, "opp_hand_count", 4))

    has_evolvable_basic = False
    if state.opp_active and get_pokemon_data(state.opp_active.get("id", 0)) and get_pokemon_data(state.opp_active.get("id", 0)).get("basic"):
        has_evolvable_basic = True
    for b in state.opp_bench:
        if b and get_pokemon_data(b.get("id", 0)) and get_pokemon_data(b.get("id", 0)).get("basic"):
            has_evolvable_basic = True

    if not has_evolvable_basic:
        return 0.1

    remaining_evos = 6
    return calculate_hypergeometric_prob(opp_deck_count + opp_hand_count, remaining_evos, opp_hand_count, 1)


def estimate_next_attack_probability(state: GameState) -> float:
    """Estimate probability that opponent can launch an attack on their upcoming turn."""
    if not state.opp_active:
        return 0.0

    opp_active = state.opp_active
    energies = opp_active.get("energies", [])
    energy_cnt = len(energies) if isinstance(energies, list) else 0

    cid = opp_active.get("id", 0)
    _, nominal_cost = get_pokemon_damage_profile(cid, energy_cnt)

    if energy_cnt >= nominal_cost:
        return 0.95
    elif energy_cnt == nominal_cost - 1:
        p_energy = estimate_energy_probability(state)
        return 0.85 * p_energy
    return 0.20


def get_pokemon_damage_profile(card_id: int, energy_cnt: int) -> tuple[float, int]:
    """
    Generalized database-backed attack damage and energy cost estimation.
    Returns: (estimated_raw_damage, nominal_attack_cost)
    """
    from agent.damage_model import GeneralizedDamageModel

    card = get_card(card_id)
    pdata = get_pokemon_data(card_id)

    if not card and not pdata:
        return (float(max(10, energy_cnt * 30)), 2)

    profile = GeneralizedDamageModel.get_pokemon_profile({"id": card_id})
    nominal_cost = profile["nominal_cost"]
    base_dmg = profile["base_damage"]

    if energy_cnt >= nominal_cost:
        dmg = base_dmg
    elif energy_cnt >= 1:
        dmg = base_dmg * (energy_cnt / nominal_cost) * 0.6
    else:
        dmg = 0.0

    return (dmg, nominal_cost)


def classify_single_threat(pkmn: Dict[str, Any], state: GameState, is_active: bool) -> OpponentThreat:
    """Classify an individual opponent Pokémon into structured threat representation."""
    cid = pkmn.get("id", 0)
    card = get_card(cid)
    pdata = get_pokemon_data(cid)
    name = card.get("name", f"Card #{cid}") if card else f"Card #{cid}"

    is_ex = bool(card and (card.get("ex") or card.get("megaEx"))) or bool(pdata and pdata.get("ex"))
    energies = pkmn.get("energies", [])
    energy_cnt = len(energies) if isinstance(energies, list) else 0
    hp = float(pkmn.get("hp", 100))
    max_hp = float(card.get("hp", hp)) if card else hp

    raw_dmg, attack_cost = get_pokemon_damage_profile(cid, energy_cnt)

    # Check Safeguard applicability against our Active Pokémon
    our_active = state.your_active
    from agent.evaluator import is_target_immune_to_ex
    our_active_safeguarded = is_target_immune_to_ex(our_active)
    our_active_hp = float(our_active.get("hp", 130)) if our_active and isinstance(our_active, dict) else 130.0

    if our_active_safeguarded and is_ex:
        effective_dmg = 0.0
        is_safeguard_blocked = True
    else:
        effective_dmg = raw_dmg
        is_safeguard_blocked = False

    # Calculate Energy Distance & Readiness
    delta_e = max(0, attack_cost - energy_cnt)
    p_energy = estimate_energy_probability(state)

    if is_active:
        if delta_e == 0:
            readiness = ThreatReadiness.T0_READY
            readiness_multiplier = 1.0
        elif delta_e == 1:
            readiness = ThreatReadiness.T1_NEXT_TURN
            readiness_multiplier = 0.85 * p_energy
        else:
            readiness = ThreatReadiness.T3_DISTANT
            readiness_multiplier = 0.20
    else:
        # Benched Pokémon requires promotion/switch in addition to energy
        if delta_e == 0:
            readiness = ThreatReadiness.T1_NEXT_TURN
            readiness_multiplier = 0.70
        elif delta_e == 1:
            readiness = ThreatReadiness.T2_SETUP
            readiness_multiplier = 0.40 * p_energy
        else:
            readiness = ThreatReadiness.T3_DISTANT
            readiness_multiplier = 0.15

    is_lethal = (effective_dmg >= our_active_hp) and (not is_safeguard_blocked)

    # Determine Threat Categories
    categories: List[ThreatCategory] = []
    if effective_dmg >= 50.0:
        categories.append(ThreatCategory.ATTACK_THREAT)
    if energy_cnt >= 2 and not is_active:
        categories.append(ThreatCategory.ENERGY_RAMP)
    if card and (card.get("basic") or pdata and pdata.get("basic")) and energy_cnt >= 1:
        categories.append(ThreatCategory.EVOLUTION_THREAT)

    # Quantitative Threat Score
    threat_score = 0.0
    if not is_safeguard_blocked:
        threat_score += effective_dmg * readiness_multiplier
        if is_lethal:
            threat_score += 400.0 * readiness_multiplier
    else:
        # Safeguarded EX still has a small residual threat for prize value or future gust
        threat_score += 15.0

    return OpponentThreat(
        card_id=cid,
        name=name,
        is_ex=is_ex,
        hp=hp,
        max_hp=max_hp,
        energy_attached=energy_cnt,
        attack_cost=attack_cost,
        raw_damage=raw_dmg,
        effective_damage=effective_dmg,
        readiness=readiness,
        is_lethal=is_lethal,
        is_safeguard_blocked=is_safeguard_blocked,
        categories=categories,
        threat_score=threat_score,
    )


def evaluate_opponent_threats(state: GameState) -> OpponentBoardModel:
    """Build full OpponentBoardModel evaluating active and all bench threats."""
    active_threat = classify_single_threat(state.opp_active, state, is_active=True) if state.opp_active else None

    bench_threats: List[OpponentThreat] = []
    for b in state.opp_bench:
        if b and isinstance(b, dict):
            bench_threats.append(classify_single_threat(b, state, is_active=False))

    all_threats = ([active_threat] if active_threat else []) + bench_threats
    all_threats.sort(key=lambda t: t.threat_score, reverse=True)

    primary_threat = all_threats[0] if all_threats else None

    # Estimate Opponent Win Condition
    opp_prizes = getattr(state, "opp_prizes", 6)
    has_nonex_breaker = any(not t.is_ex and t.raw_damage >= 120.0 for t in all_threats)
    has_active_ex = active_threat.is_ex if active_threat else False

    if opp_prizes <= 2:
        opp_win_con = "PRIZE_SWEEP"
    elif has_nonex_breaker and active_threat and active_threat.is_safeguard_blocked:
        opp_win_con = "SAFEGUARD_BREAKER_PIVOT"
    elif has_active_ex:
        opp_win_con = "OVERWHELM_ACTIVE_EX"
    else:
        opp_win_con = "STANDARD_ENERGY_RAMP"

    # Overall Threat Level
    max_threat_score = primary_threat.threat_score if primary_threat else 0.0
    if max_threat_score >= 350.0:
        threat_level = "CRITICAL"
    elif max_threat_score >= 120.0:
        threat_level = "HIGH"
    elif max_threat_score >= 40.0:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    return OpponentBoardModel(
        active_threat=active_threat,
        bench_threats=bench_threats,
        primary_threat=primary_threat,
        total_known_energies=getattr(state, "total_opp_energies", 0),
        estimated_hand_energy_prob=estimate_energy_probability(state),
        estimated_hand_gust_prob=estimate_gust_probability(state),
        opponent_win_condition=opp_win_con,
        threat_level=threat_level,
    )


def estimate_opponent_threat(state: GameState) -> Dict[str, Any]:
    """Backward-compatible helper returning dictionary threat assessment."""
    model = evaluate_opponent_threats(state)
    seen_cards = get_observable_opponent_cards(state)
    return {
        "archetype": classify_opponent_archetype(seen_cards),
        "p_attack": estimate_next_attack_probability(state),
        "p_gust": model.estimated_hand_gust_prob,
        "p_evolution": estimate_evolution_probability(state),
        "expected_damage": model.active_threat.effective_damage if model.active_threat else 0.0,
        "threat_level": model.threat_level,
    }
