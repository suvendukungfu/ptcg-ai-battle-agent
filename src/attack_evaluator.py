from typing import Dict, Any, List, Tuple, Optional
from src.state_evaluator import GameState
from src.immunity_handler import calculate_immunity_multiplier, is_ex_attacker


def estimate_raw_damage(attacker: Optional[Dict[str, Any]]) -> float:
    """Estimate base attack damage based on active Pokémon ID and HP/energy state."""
    if not attacker or not isinstance(attacker, dict):
        return 30.0

    card_id = attacker.get("id", 0)
    max_hp = attacker.get("maxHp", 0)
    energies = attacker.get("energies", [])
    energy_count = len(energies) if isinstance(energies, list) else 0

    if card_id == 723 or max_hp >= 200:  # Bellibolt ex
        base_dmg = 160.0
        return base_dmg + (energy_count * 20.0)
    elif card_id == 722 or (100 <= max_hp < 200):  # Bellibolt
        base_dmg = 90.0
        return base_dmg + (energy_count * 15.0)
    elif card_id == 721:  # Tadbulb
        base_dmg = 30.0
        return base_dmg + (energy_count * 10.0)

    return 40.0 + (energy_count * 10.0)


def get_target_hp(target: Optional[Dict[str, Any]]) -> float:
    if not target or not isinstance(target, dict):
        return 100.0
    hp = target.get("hp", 100)
    return float(hp) if isinstance(hp, (int, float)) and hp > 0 else 1.0


def get_target_prize_value(target: Optional[Dict[str, Any]]) -> int:
    if not target or not isinstance(target, dict):
        return 1
    card_id = target.get("id", 0)
    max_hp = target.get("maxHp", 0)
    if card_id == 723 or max_hp >= 200:
        return 2
    return 1


def score_attack_option(opt_idx: int, opt: Dict[str, Any], state: GameState) -> float:
    """Score a single attack option (OptionType 7)."""
    attacker = state.your_active
    target = state.opp_active

    # Check target specifier in option dict if option targets bench
    target_area = opt.get("area")
    target_idx = opt.get("index")
    if target_area == 5 and isinstance(target_idx, int) and 0 <= target_idx < len(state.opp_bench):
        target = state.opp_bench[target_idx]

    immunity_mult = calculate_immunity_multiplier(attacker, target)
    raw_dmg = estimate_raw_damage(attacker)
    effective_dmg = raw_dmg * immunity_mult

    target_hp = get_target_hp(target)
    prize_val = get_target_prize_value(target)
    is_ko = (effective_dmg >= target_hp)

    score = 0.0

    # 1. Immunity check: if blocked by Crustle/Safeguard, penalize ex attacks severely
    if immunity_mult == 0.0:
        return -50000.0

    # 2. Immediate Game Winning KO (Priority 1)
    if is_ko and prize_val >= state.your_prizes:
        score += 100000.0

    # 3. Guaranteed KO (Priority 2)
    elif is_ko:
        score += 10000.0 + (prize_val * 5000.0)

    # 4. High-Prize Target / Heavy Damage (Priority 3)
    else:
        score += (effective_dmg * 10.0) + (prize_val * 2000.0)

    # Prize race adjustments
    if state.prize_race == "match_point":
        if is_ko:
            score += 50000.0
    elif state.prize_race == "behind":
        # Prefer high prize KO lines when behind
        score += (prize_val * 1000.0)
    elif state.prize_race == "ahead":
        # Prefer safest KO line when ahead
        if is_ko:
            score += 2000.0

    return score


def rank_attack_options(state: GameState) -> List[Tuple[int, float]]:
    """Find and rank all OptionType 7 attack options in legal options."""
    attack_scores = []
    for idx, opt in enumerate(state.options):
        if isinstance(opt, dict) and opt.get("type") == 7:
            s = score_attack_option(idx, opt, state)
            attack_scores.append((idx, s))

    # Sort descending by score
    attack_scores.sort(key=lambda x: x[1], reverse=True)
    return attack_scores
