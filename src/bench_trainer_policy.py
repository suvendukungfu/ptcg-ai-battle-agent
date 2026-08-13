from typing import Dict, Any, List, Tuple
from src.state_evaluator import GameState


def rank_card_play_options(state: GameState) -> List[Tuple[int, float]]:
    """Rank legal card play/bench/trainer/evolution options by strategic priority."""
    ranked = []

    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict):
            continue

        opt_type = opt.get("type", -1)
        # Skip Attack (7), Energy Attach (8), End Turn (14)
        if opt_type in (7, 8, 14):
            continue

        score = 20.0
        
        # Determine card ID or area context
        card_id = opt.get("id", 0)

        # 1. Evolution (High Priority)
        if opt_type in (3, 4):  # Evolution / Stage1 / Stage2 play
            score += 150.0
        elif card_id in (722, 723):  # Bellibolt / Bellibolt ex card
            score += 140.0

        # 2. Key Trainer Items & Supporters
        elif card_id == 1262:  # Boss's Orders / Gust
            # Higher priority if opp bench has KOable / high-prize target or in match point
            score += 120.0 if state.prize_race == "match_point" else 80.0
        elif card_id == 1219:  # Electric Generator (Energy acceleration)
            score += 110.0 if not state.energy_attached else 60.0
        elif card_id == 1121:  # Ultra Ball
            score += 95.0
        elif card_id == 1227:  # Nest Ball
            score += 90.0 if len(state.your_bench) < 3 else 40.0
        elif card_id == 1092:  # Professor's Research
            score += 85.0 if len(state.your_hand) <= 3 else 30.0
        elif card_id == 1163:  # Heavy Baton / Tool
            score += 75.0

        # 3. Benching Basic Pokémon (Tadbulb 721)
        elif card_id == 721 or opt_type in (0, 1):  # Basic Bench
            if len(state.your_bench) < 3:
                score += 70.0
            else:
                score += 20.0

        ranked.append((idx, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
