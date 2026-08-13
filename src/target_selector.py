from typing import Dict, Any, List, Tuple, Optional
from src.state_evaluator import GameState
from src.immunity_handler import is_target_immune_to_ex, is_ex_attacker


def evaluate_target_priority(target: Optional[Dict[str, Any]], state: GameState) -> float:
    """Evaluate target score based on KO potential, prize value, energy threat, and HP."""
    if not target or not isinstance(target, dict):
        return 0.0

    hp = float(target.get("hp", 100))
    max_hp = float(target.get("maxHp", 100))
    energies = target.get("energies", [])
    energy_cnt = len(energies) if isinstance(energies, list) else 0
    card_id = target.get("id", 0)

    prize_val = 2 if (card_id == 723 or max_hp >= 200) else 1

    score = 0.0

    # 1. High prize value (+50)
    score += prize_val * 50.0

    # 2. Low HP / KOable (+40 for low HP)
    if hp <= 50:
        score += 40.0
    elif hp <= 90:
        score += 25.0

    # 3. Threat / Energy buildup (+15 per attached energy)
    score += energy_cnt * 15.0

    # 4. Ex Immunity penalty: if our active is Bellibolt ex and target is immune
    if is_ex_attacker(state.your_active) and is_target_immune_to_ex(target):
        score -= 200.0

    # 5. Prize race adjustment
    if state.prize_race == "match_point" and hp <= 100:
        score += 100.0

    return score


def rank_target_options(options: List[Dict[str, Any]], state: GameState) -> List[Tuple[int, float]]:
    """Rank legal target options by priority score."""
    ranked = []
    for idx, opt in enumerate(options):
        if not isinstance(opt, dict):
            continue
        
        # Resolve target from option index/area if available
        target = state.opp_active
        opt_area = opt.get("area")
        opt_idx = opt.get("index")
        if opt_area == 5 and isinstance(opt_idx, int) and 0 <= opt_idx < len(state.opp_bench):
            target = state.opp_bench[opt_idx]
            
        score = evaluate_target_priority(target, state)
        ranked.append((idx, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
