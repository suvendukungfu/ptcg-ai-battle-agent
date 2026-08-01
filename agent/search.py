import copy
import time
from typing import Dict, Any, List, Tuple, Optional
from agent.state import GameState
from agent.evaluator import (
    evaluate_board_value,
    estimate_raw_damage,
    get_target_hp,
    get_target_prize_value,
    calculate_immunity_multiplier,
    is_ex_attacker,
    is_target_immune_to_ex,
    DEFAULT_WEIGHTS,
)
from agent.opponent_model import (
    estimate_next_attack_probability,
    estimate_gust_probability,
    evaluate_opponent_threats,
)
from agent.risk_model import determine_risk_profile
from agent.fallback import make_distinct_choice


SEARCH_CONFIG = {
    "max_candidates": 8,
    "time_budget_ms": 40.0,
    "min_overage_time_sec": 20.0,
}


def should_invoke_search(state: GameState, remaining_time: float = 600.0) -> bool:
    """Determine whether search lookahead is appropriate for this decision context."""
    if len(state.options) <= 1:
        return False
    if remaining_time < SEARCH_CONFIG["min_overage_time_sec"]:
        return False
    # Search is applied for macro Main Phase turn actions and direct combat/energy actions
    return state.select_type in (0, 7, 8)


def project_action(state: GameState, opt_idx: int) -> Tuple[GameState, float]:
    """
    Project state transition resulting from executing candidate option index.
    Returns (projected_state, immediate_action_bonus).
    """
    proj = copy.deepcopy(state)
    if opt_idx < 0 or opt_idx >= len(proj.options):
        return proj, 0.0

    opt = proj.options[opt_idx]
    if not isinstance(opt, dict):
        return proj, 0.0

    opt_type = opt.get("type", -1)
    card_id = opt.get("id", 0)
    bonus = 0.0

    # 1. Attack (OptionType 7)
    if opt_type == 7:
        attacker = proj.your_active
        target = proj.opp_active

        opt_area = opt.get("area")
        opt_target_idx = opt.get("index")
        if opt_area == 5 and isinstance(opt_target_idx, int) and 0 <= opt_target_idx < len(proj.opp_bench):
            target = proj.opp_bench[opt_target_idx]

        if attacker and target:
            mult = calculate_immunity_multiplier(attacker, target)
            raw_dmg = estimate_raw_damage(attacker)
            eff_dmg = raw_dmg * mult

            curr_hp = get_target_hp(target)
            new_hp = max(0.0, curr_hp - eff_dmg)
            target["hp"] = new_hp

            if new_hp <= 0:  # Knockout achieved!
                prize_val = get_target_prize_value(target)
                proj.your_prizes = max(0, proj.your_prizes - prize_val)
                bonus += 220.0 * prize_val

                # Remove KO'd pokemon
                if target == proj.opp_active:
                    proj.opp_active = proj.opp_bench.pop(0) if proj.opp_bench else None
                elif target in proj.opp_bench:
                    proj.opp_bench.remove(target)
            else:
                bonus += 40.0

    # 2. Energy Attachment (OptionType 8)
    elif opt_type == 8:
        in_play_area = opt.get("inPlayArea")
        in_play_idx = opt.get("inPlayIndex")

        target_pkmn = None
        if in_play_area in (4, 1):
            target_pkmn = proj.your_active
        elif in_play_area == 5 and isinstance(in_play_idx, int) and 0 <= in_play_idx < len(proj.your_bench):
            target_pkmn = proj.your_bench[in_play_idx]

        if target_pkmn and isinstance(target_pkmn, dict):
            energies = target_pkmn.get("energies", [])
            if isinstance(energies, list):
                energies.append(1)  # Grass energy
                target_pkmn["energies"] = energies
        bonus += 55.0

    # 3. Evolution (OptionTypes 3, 4)
    elif opt_type in (3, 4) or card_id in (345, 722, 723):
        if proj.your_active:
            proj.your_active["id"] = card_id if card_id in (345, 722, 723) else 345
            proj.your_active["maxHp"] = 350 if card_id in (723, 756) else 130
            proj.your_active["hp"] = min(proj.your_active.get("hp", 100) + 70, proj.your_active["maxHp"])
        bonus += 130.0

    # 4. BENCH_FIRST: Playing Basic Pokemon to Bench (OptionTypes 1, 2)
    elif opt_type in (1, 2) and card_id in (344, 721):
        # Project establishing a new benched Pokemon
        proj.your_bench.append({"id": card_id or 344, "hp": 60, "maxHp": 60, "energies": []})
        if len(state.your_bench) == 0:
            # Critical board security bonus
            bonus += 180.0
        else:
            bonus += 65.0

    # 5. Key Trainer Items / Supporters
    elif opt_type in (0, 2, 5, 6) or card_id in (1092, 1121, 1145, 1219, 1227, 1262):
        if card_id in (1262, 1182):  # Boss's Orders
            bonus += 85.0
        elif card_id == 1219:  # Electric Generator
            bonus += 80.0
        elif card_id in (1145, 1086):  # Nest Ball / Poffin (Basic search to bench)
            bonus += 100.0 if len(state.your_bench) == 0 else 60.0
        elif card_id in (1121, 1227):  # Search balls
            bonus += 70.0
        elif card_id == 1092:  # Professor's Research
            if proj.your_deck_count <= 7:
                bonus -= 10000.0  # Prevent deckout suicide!
            else:
                bonus += 75.0
        else:
            bonus += 40.0

    # 6. Pass / End Turn (OptionType 14)
    elif opt_type == 14:
        bonus -= 35.0

    return proj, bonus


def estimate_opponent_counterattack(projected: GameState) -> float:
    """Estimate expected opponent counter-attack damage considering active and benched threats."""
    opp_active = projected.opp_active
    your_active = projected.your_active

    if not opp_active or not your_active:
        return 0.0

    p_attack = estimate_next_attack_probability(projected)
    p_gust = estimate_gust_probability(projected)

    # 1. Active Threat
    raw_dmg = estimate_raw_damage(opp_active)
    mult = calculate_immunity_multiplier(opp_active, your_active)
    eff_dmg = raw_dmg * mult

    your_hp = get_target_hp(your_active)
    expected_active_dmg = p_attack * eff_dmg
    if eff_dmg >= your_hp:
        if len(projected.your_bench) == 0:
            # Fatal Bench-Depletion lethal threat!
            expected_active_dmg += p_attack * 2500.0
        else:
            expected_active_dmg += p_attack * 350.0  # Normal knockout penalty

    # 2. Benched Non-EX Breaker Promotion Threat
    expected_bench_breaker_threat = 0.0
    if is_target_immune_to_ex(your_active):
        for b in projected.opp_bench:
            if b and isinstance(b, dict) and not is_ex_attacker(b):
                e_cnt = len(b.get("energies", [])) if isinstance(b.get("energies"), list) else 0
                if e_cnt >= 2:
                    b_dmg = estimate_raw_damage(b)
                    if b_dmg >= your_hp:
                        expected_bench_breaker_threat = max(expected_bench_breaker_threat, 0.40 * b_dmg + 150.0)

    # 3. Bench threat if opponent plays Boss's Orders
    expected_bench_threat = 0.0
    for b in projected.your_bench:
        if b and isinstance(b, dict):
            b_hp = get_target_hp(b)
            if eff_dmg >= b_hp:
                expected_bench_threat = max(expected_bench_threat, p_gust * p_attack * 250.0)

    return expected_active_dmg + expected_bench_breaker_threat + expected_bench_threat


def shallow_risk_aware_search(state: GameState, remaining_time: float = 600.0) -> Optional[List[int]]:
    """
    Execute 1-2 ply shallow risk-aware lookahead search with dynamic risk profiling.
    """
    start_t = time.perf_counter()

    if not should_invoke_search(state, remaining_time):
        return None

    n_opts = len(state.options)
    max_cnt = state.max_count
    min_cnt = state.min_count

    # Determine dynamic risk profile for the current state
    risk_profile = determine_risk_profile(state)

    candidate_limit = min(n_opts, SEARCH_CONFIG["max_candidates"])
    scored_candidates: List[Tuple[int, float]] = []

    for idx in range(candidate_limit):
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        if elapsed_ms > SEARCH_CONFIG["time_budget_ms"]:
            break

        projected, action_bonus = project_action(state, idx)
        board_val = evaluate_board_value(projected)
        retaliation_threat = estimate_opponent_counterattack(projected)

        # Dynamic risk-adjusted score
        risk_adjusted_score = (
            board_val
            + (action_bonus * risk_profile.aggression_bonus)
            - (retaliation_threat * risk_profile.retaliation_weight)
        )
        scored_candidates.append((idx, risk_adjusted_score))

    if not scored_candidates:
        return None

    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    preferred = [x[0] for x in scored_candidates]

    return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)
