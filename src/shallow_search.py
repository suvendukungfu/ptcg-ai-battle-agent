import copy
import time
from typing import Dict, Any, List, Tuple, Optional
from src.state_evaluator import GameState
from src.value_function import evaluate_board_value
from src.attack_evaluator import estimate_raw_damage, get_target_hp, get_target_prize_value
from src.immunity_handler import calculate_immunity_multiplier
from src.opponent_model import estimate_next_attack_probability, estimate_gust_probability

# Configurable Search Budget
SEARCH_BUDGET = {
    "max_candidates": 8,
    "time_limit_ms": 50.0,
    "min_overage_time_sec": 30.0,
}


def make_distinct_choice(preferred_indices: List[int], n_opts: int, max_cnt: int) -> List[int]:
    """Ensure distinct option indices are selected up to max_cnt."""
    if n_opts <= 0:
        return []

    chosen: List[int] = []
    for idx in preferred_indices:
        if idx not in chosen and 0 <= idx < n_opts:
            chosen.append(idx)
            if len(chosen) == max_cnt:
                return chosen

    for idx in range(n_opts):
        if idx not in chosen:
            chosen.append(idx)
            if len(chosen) == max_cnt:
                return chosen

    while len(chosen) < max_cnt:
        chosen.append((chosen[-1] + 1) % n_opts if n_opts > 0 else 0)

    return chosen


def should_use_search(state: GameState, remaining_time: float = 600.0) -> bool:
    """Determine whether search lookahead should be invoked for this decision."""
    if len(state.options) <= 1:
        return False

    if remaining_time < SEARCH_BUDGET["min_overage_time_sec"]:
        return False

    return state.select_type in (0, 7, 8, 1, 2, 3, 4, 5, 6)


def project_action(state: GameState, opt_idx: int) -> Tuple[GameState, float]:
    """Fast Python state projection of a candidate legal action, returning (projected_state, action_bonus)."""
    proj = copy.deepcopy(state)
    if opt_idx < 0 or opt_idx >= len(proj.options):
        return proj, 0.0

    opt = proj.options[opt_idx]
    if not isinstance(opt, dict):
        return proj, 0.0

    opt_type = opt.get("type", -1)
    card_id = opt.get("id", 0)
    action_bonus = 0.0

    # 1. OptionType 7: Attack
    if opt_type == 7:
        attacker = proj.your_active
        target = proj.opp_active

        opt_area = opt.get("area")
        opt_idx_target = opt.get("index")
        if opt_area == 5 and isinstance(opt_idx_target, int) and 0 <= opt_idx_target < len(proj.opp_bench):
            target = proj.opp_bench[opt_idx_target]

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
                action_bonus += 200.0 * prize_val
                if target == proj.opp_active:
                    proj.opp_active = proj.opp_bench.pop(0) if proj.opp_bench else None
                elif target in proj.opp_bench:
                    proj.opp_bench.remove(target)
            else:
                action_bonus += 50.0

    # 2. OptionType 8: Energy Attachment
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
                energies.append(3)
                target_pkmn["energies"] = energies
        action_bonus += 60.0

    # 3. Evolution (OptionTypes 3, 4)
    elif opt_type in (3, 4) or card_id in (722, 723):
        if proj.your_active:
            proj.your_active["id"] = card_id if card_id in (722, 723) else 723
            proj.your_active["maxHp"] = 350 if card_id == 723 else 180
            proj.your_active["hp"] = min(proj.your_active.get("hp", 100) + 100, proj.your_active["maxHp"])
        action_bonus += 120.0  # High bonus for evolution

    # 4. Item / Supporter Play (OptionTypes 0, 1, 2, 5, 6)
    elif opt_type in (0, 1, 2, 5, 6) or card_id in (1092, 1121, 1219, 1227, 1262):
        if card_id == 1262:  # Boss's Orders
            action_bonus += 80.0
        elif card_id == 1219:  # Electric Generator
            action_bonus += 75.0
        elif card_id in (1121, 1227):  # Search balls
            action_bonus += 65.0
        else:
            action_bonus += 40.0

    # 5. End Turn / Pass (OptionType 14)
    elif opt_type == 14:
        action_bonus -= 30.0  # Lower priority than playing active cards

    return proj, action_bonus


def estimate_opponent_retaliation(projected: GameState) -> float:
    """Estimate expected opponent counter-attack damage using Bayesian opponent model."""
    opp_active = projected.opp_active
    your_active = projected.your_active

    if not opp_active or not your_active:
        return 0.0

    p_attack = estimate_next_attack_probability(projected)
    p_gust = estimate_gust_probability(projected)

    raw_retaliation_dmg = estimate_raw_damage(opp_active)
    mult = calculate_immunity_multiplier(opp_active, your_active)
    eff_retaliation_dmg = raw_retaliation_dmg * mult

    your_hp = get_target_hp(your_active)
    
    expected_active_dmg = p_attack * eff_retaliation_dmg
    if eff_retaliation_dmg >= your_hp:
        expected_active_dmg += p_attack * 300.0

    expected_bench_threat = 0.0
    for b in projected.your_bench:
        if b and isinstance(b, dict):
            b_hp = get_target_hp(b)
            if eff_retaliation_dmg >= b_hp:
                expected_bench_threat = max(expected_bench_threat, p_gust * p_attack * 200.0)

    return expected_active_dmg + expected_bench_threat


def shallow_risk_aware_search(state: GameState, remaining_time: float = 600.0) -> Optional[List[int]]:
    """Run 1-2 ply shallow risk-aware search with Bayesian opponent modeling."""
    start_time = time.perf_counter()

    if not should_use_search(state, remaining_time):
        return None

    n_opts = len(state.options)
    max_cnt = state.max_count

    candidate_indices = list(range(min(n_opts, SEARCH_BUDGET["max_candidates"])))
    scored_candidates: List[Tuple[int, float]] = []

    for idx in candidate_indices:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if elapsed_ms > SEARCH_BUDGET["time_limit_ms"]:
            break

        projected, action_bonus = project_action(state, idx)
        board_val = evaluate_board_value(projected)
        retaliation_risk = estimate_opponent_retaliation(projected)

        risk_adjusted_score = board_val + action_bonus - (1.5 * retaliation_risk)
        scored_candidates.append((idx, risk_adjusted_score))

    if not scored_candidates:
        return None

    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    preferred_order = [x[0] for x in scored_candidates]

    return make_distinct_choice(preferred_order, n_opts, max_cnt)
