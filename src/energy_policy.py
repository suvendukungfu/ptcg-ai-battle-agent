from typing import Dict, Any, List, Tuple
from src.state_evaluator import GameState


def rank_energy_attachment_options(state: GameState) -> List[Tuple[int, float]]:
    """Rank OptionType 8 energy attachment options by strategic priority."""
    ranked = []
    
    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict) or opt.get("type") != 8:
            continue

        score = 10.0
        
        # Check target Pokémon area/index in play area
        in_play_area = opt.get("inPlayArea")
        in_play_idx = opt.get("inPlayIndex")

        target_pkmn = None
        is_active_target = False

        if in_play_area == 4 or in_play_area == 1:  # Active area
            target_pkmn = state.your_active
            is_active_target = True
        elif in_play_area == 5 and isinstance(in_play_idx, int) and 0 <= in_play_idx < len(state.your_bench):
            target_pkmn = state.your_bench[in_play_idx]

        if target_pkmn and isinstance(target_pkmn, dict):
            card_id = target_pkmn.get("id", 0)
            hp = target_pkmn.get("hp", 100)
            energies = target_pkmn.get("energies", [])
            energy_cnt = len(energies) if isinstance(energies, list) else 0

            # Active attacker gets highest priority if energy needed
            if is_active_target:
                if card_id == 723:  # Bellibolt ex
                    score += 100.0 if energy_cnt < 3 else 30.0
                elif card_id == 722:  # Bellibolt
                    score += 80.0 if energy_cnt < 2 else 20.0
                else:  # Tadbulb
                    score += 50.0 if energy_cnt < 1 else 10.0
            else:
                # Bench attacker setup
                if card_id == 723:  # Bellibolt ex on bench
                    score += 90.0 if energy_cnt < 3 else 25.0
                elif card_id == 722:
                    score += 70.0 if energy_cnt < 2 else 15.0
                elif card_id == 721:
                    score += 40.0

            # Penalty for dying units
            if hp <= 30 and not is_active_target:
                score -= 60.0

        ranked.append((idx, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
