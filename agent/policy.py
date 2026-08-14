from typing import List, Dict, Any, Tuple, Optional
from agent.state import GameState
from agent.evaluator import (
    estimate_raw_damage,
    get_target_hp,
    get_target_prize_value,
    calculate_immunity_multiplier,
    is_target_immune_to_ex,
    is_ex_attacker,
)
from agent.card_database import get_card, get_pokemon_data


def classify_game_situation(state: GameState) -> str:
    """Classify the current strategic game situation."""
    if state.turn <= 2:
        return "EARLY_SETUP"
    elif state.your_prizes <= 1:
        return "MATCH_POINT"
    elif state.opp_prizes <= 1:
        return "DEFENSIVE_URGENT"
    elif state.opp_prizes - state.your_prizes >= 2:
        return "ADVANTAGE"
    elif state.your_prizes - state.opp_prizes >= 2:
        return "COMEBACK"
    return "MIDGAME_PRESSURE"


def rank_attack_options(state: GameState) -> List[Tuple[int, float]]:
    """Rank all available attack options in state.options."""
    ranks: List[Tuple[int, float]] = []
    attacker = state.your_active
    target = state.opp_active

    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict) or opt.get("type") != 7:
            continue

        score = 50.0  # Base attack score
        opt_area = opt.get("area")
        opt_idx = opt.get("index")

        # Bench snipe target
        curr_target = target
        if opt_area == 5 and isinstance(opt_idx, int) and 0 <= opt_idx < len(state.opp_bench):
            curr_target = state.opp_bench[opt_idx]

        if attacker and curr_target:
            mult = calculate_immunity_multiplier(attacker, curr_target)
            if mult == 0.0:
                score -= 10000.0  # Zero damage to immune target
            else:
                raw_dmg = estimate_raw_damage(attacker)
                eff_dmg = raw_dmg * mult
                target_hp = get_target_hp(curr_target)
                prize_val = get_target_prize_value(curr_target)

                if eff_dmg >= target_hp:
                    score += 500.0 * prize_val  # Guaranteed Knockout
                    if state.your_prizes <= prize_val:
                        score += 3000.0  # Game winning attack!
                else:
                    score += (eff_dmg / max(1.0, target_hp)) * 120.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def rank_energy_attachment_options(state: GameState) -> List[Tuple[int, float]]:
    """Rank available energy attachment options in state.options."""
    ranks: List[Tuple[int, float]] = []

    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict) or opt.get("type") != 8:
            continue

        score = 20.0
        in_play_area = opt.get("inPlayArea")
        in_play_idx = opt.get("inPlayIndex")

        target_pkmn = None
        if in_play_area in (4, 1):
            target_pkmn = state.your_active
            score += 40.0
        elif in_play_area == 5 and isinstance(in_play_idx, int) and 0 <= in_play_idx < len(state.your_bench):
            target_pkmn = state.your_bench[in_play_idx]
            score += 25.0

        if target_pkmn and isinstance(target_pkmn, dict):
            cid = target_pkmn.get("id", 0)
            energies = target_pkmn.get("energies", [])
            n_energies = len(energies) if isinstance(energies, list) else 0

            # Prioritize powering up Bellibolt ex (723) to 2 energies
            if cid == 723:
                if n_energies < 2:
                    score += 80.0
                elif n_energies == 2:
                    score += 15.0
            elif cid == 722 and n_energies < 2:
                score += 50.0
            elif cid == 721 and n_energies < 1:
                score += 35.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def rank_card_play_options(state: GameState) -> List[Tuple[int, float]]:
    """Rank available item, supporter, and evolution plays."""
    ranks: List[Tuple[int, float]] = []

    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict):
            continue

        opt_type = opt.get("type", -1)
        card_id = opt.get("id", 0)
        score = 0.0

        # Evolutions (OptionType 3, 4)
        if opt_type in (3, 4) or card_id in (722, 723):
            score += 150.0 if card_id == 723 else 110.0

        # Trainers / Items / Supporters
        elif card_id == 1262:  # Boss's Orders
            # High score if opponent bench has a low-HP or high-prize target
            score += 90.0
        elif card_id == 1219:  # Electric Generator
            score += 85.0
        elif card_id in (1121, 1227):  # Ultra Ball / Nest Ball
            score += 75.0
        elif card_id == 1092:  # Professor's Research
            score += 70.0 if len(state.your_hand) <= 3 else 30.0
        elif card_id == 1145:  # Switch
            # Prioritize switch if active is low HP or trapped
            if state.your_active and float(state.your_active.get("hp", 100)) < 60:
                score += 80.0
            else:
                score += 15.0
        elif opt_type in (0, 1, 2, 5, 6):
            score += 40.0
        elif opt_type == 14:  # End Turn / Pass
            score -= 50.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def rank_target_options(options: List[Dict[str, Any]], state: GameState) -> List[Tuple[int, float]]:
    """Rank generic selection/target options (e.g. discard selections, search targets)."""
    ranks: List[Tuple[int, float]] = []

    for idx, opt in enumerate(options):
        if not isinstance(opt, dict):
            ranks.append((idx, 0.0))
            continue

        cid = opt.get("id", 0)
        score = 0.0

        # When searching: prioritize Bellibolt ex (723) -> Bellibolt (722) -> Tadbulb (721)
        if cid == 723:
            score += 100.0
        elif cid == 722:
            score += 80.0
        elif cid == 721:
            score += 60.0
        elif cid == 1219:
            score += 70.0
        elif cid == 1092:
            score += 65.0
        elif cid == 3:  # Energy
            score += 30.0
        else:
            score += 10.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks
