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

    # Check if our active is Safeguarded and opponent has a non-ex breaker
    our_active_safeguarded = is_target_immune_to_ex(state.your_active)
    all_opp = ([state.opp_active] if state.opp_active else []) + [b for b in state.opp_bench if b]
    has_nonex_threat = any(not is_ex_attacker(o) and len(o.get("energies", [])) >= 2 for o in all_opp if isinstance(o, dict))

    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict) or opt.get("type") != 8:
            continue

        score = 20.0
        in_play_area = opt.get("inPlayArea")
        in_play_idx = opt.get("inPlayIndex")

        target_pkmn = None
        is_active_target = False
        if in_play_area in (4, 1):
            target_pkmn = state.your_active
            is_active_target = True
            score += 40.0
        elif in_play_area == 5 and isinstance(in_play_idx, int) and 0 <= in_play_idx < len(state.your_bench):
            target_pkmn = state.your_bench[in_play_idx]
            score += 25.0

        if target_pkmn and isinstance(target_pkmn, dict):
            energies = target_pkmn.get("energies", [])
            n_energies = len(energies) if isinstance(energies, list) else 0

            from agent.damage_model import GeneralizedDamageModel
            profile = GeneralizedDamageModel.get_pokemon_profile(target_pkmn)
            nominal_cost = profile["nominal_cost"]
            is_target_ex = profile["is_ex"]
            opp_is_immune = is_target_immune_to_ex(state.opp_active)

            # Power up active/bench attackers based on nominal energy requirement
            if n_energies < nominal_cost:
                if opp_is_immune and is_target_ex:
                    score -= 50.0  # Do not attach to EX if opponent active is immune to EX
                elif opp_is_immune and not is_target_ex:
                    score += 95.0  # Strongly prioritize charging Non-EX counter against Safeguard
                else:
                    score += 80.0  # Standard primary attacker charging
            elif n_energies >= nominal_cost:
                if is_active_target and has_nonex_threat and len(state.your_bench) > 0:
                    score -= 20.0  # Avoid over-attaching to doomed active
                else:
                    score += 15.0  # Surplus attachment
            else:
                score += 10.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def rank_card_play_options(state: GameState) -> List[Tuple[int, float]]:
    """Rank available item, supporter, and evolution plays."""
    ranks: List[Tuple[int, float]] = []
    bench_count = len(state.your_bench)

    for idx, opt in enumerate(state.options):
        if not isinstance(opt, dict):
            continue

        opt_type = opt.get("type", -1)
        card_id = opt.get("id", 0)
        card = get_card(card_id) if card_id else None
        score = 0.0

        # Check if opponent active is immune to ex attacks
        opp_is_immune = is_target_immune_to_ex(state.opp_active)

        from agent.damage_model import GeneralizedDamageModel
        profile = GeneralizedDamageModel.get_pokemon_profile(card) if card else None

        # 1. BENCH_FIRST: Playing Basic Pokemon to Bench
        is_basic_pokemon = (card and card.get("basic", False)) or (profile and profile["is_basic"])
        is_basic_play = is_basic_pokemon and (opt_type in (0, 1, 2) or "bench" in str(opt).lower())
        if is_basic_play:
            if bench_count == 0:
                # RULE 1 — BENCH_FIRST: Prioritize establishing bench security before item searches/discards
                score += 350.0
            else:
                score += 95.0

        # 2. Evolutions (OptionType 3, 4)
        elif opt_type in (3, 4) or (profile and (profile["is_stage1"] or profile["is_stage2"])):
            if profile and profile["is_ex"]:
                score += 80.0 if opp_is_immune else 160.0
            else:
                score += 260.0 if opp_is_immune else 140.0

        # 3. Trainers / Items / Supporters
        elif card_id in (1262, 1182):  # Boss's Orders / Gust
            score += 350.0 if (opp_is_immune and len(state.opp_bench) > 0) else 95.0
        elif card_id == 1219:  # Electric Generator / Ramp
            score += 110.0
        elif card_id in (1145, 1086):  # Basic search items (Nest Ball / Poffin)
            score += 180.0 if bench_count == 0 else 75.0
        elif card_id in (1121, 1227):  # Search items (Ultra Ball / Rare Candy)
            score += 75.0
        elif card_id == 1092:  # Draw Supporters
            if state.your_deck_count <= 7:
                score -= 10000.0  # Anti-deckout rule!
            else:
                score += 85.0 if len(state.your_hand) <= 3 else 35.0
        elif opt_type in (0, 5, 6):
            score += 40.0
        elif opt_type == 14:  # End Turn / Pass
            score -= 50.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def rank_discard_options(options: List[Dict[str, Any]], state: GameState) -> List[Tuple[int, float]]:
    """
    RULE 2 — PROTECT_BASIC_DISCARD:
    Rank card discard options (e.g. Ultra Ball cost payment).
    Higher score = preferred card to discard.
    """
    ranks: List[Tuple[int, float]] = []
    bench_count = len(state.your_bench)

    for idx, opt in enumerate(options):
        if not isinstance(opt, dict):
            ranks.append((idx, 0.0))
            continue

        cid = opt.get("id", 0)
        card = get_card(cid) if cid else None
        card_type = card.get("cardType", 0) if card else 0
        is_basic_pokemon = card.get("basic", False) if card else (cid in (344, 721))

        score = 10.0

        # 1. Basic Energy -> Top discard fodder (+100.0)
        if card_type == 5 or cid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 17, 18):
            score += 90.0

        # 2. Duplicate or situational trainers (+50.0)
        elif card_type in (6, 7, 8, 9, 10) or cid in (1092, 1121, 1145, 1227, 1262):
            score += 50.0

        # 3. Duplicate Stage 1 Evolution cards (+25.0)
        elif (card and card.get("stage1", False)) or cid in (345, 722, 723):
            score += 25.0

        # 4. Basic Pokémon (Dwebble, Tadbulb)
        elif is_basic_pokemon:
            if bench_count == 0:
                # RULE 2: NEVER discard Basic Pokemon if bench is empty and other options exist!
                score = -5000.0
            else:
                score = 5.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def rank_target_options(options: List[Dict[str, Any]], state: GameState) -> List[Tuple[int, float]]:
    """Rank generic selection/target options (e.g. search targets or gust targets)."""
    ranks: List[Tuple[int, float]] = []
    our_safeguarded = is_target_immune_to_ex(state.your_active)

    for idx, opt in enumerate(options):
        if not isinstance(opt, dict):
            ranks.append((idx, 0.0))
            continue

        cid = opt.get("id", 0)
        card = get_card(cid) if cid else None
        score = 0.0

        # Gust selection / Opponent Pokémon target
        if "inPlayArea" in opt or opt.get("type") in (1, 2):
            # If opponent Pokémon on bench
            if card:
                is_ex = card.get("ex", False) or card.get("megaEx", False)
                if our_safeguarded and not is_ex:
                    score += 250.0  # Drag out non-ex breaker to eliminate it!
                elif is_ex:
                    score += 150.0
            else:
                score += 50.0

        # When searching deck: prioritize evolution lines and key pieces
        elif cid in (723, 345):  # Crustle / Bellibolt ex
            score += 100.0
        elif cid in (722, 344):  # Dwebble / Bellibolt
            # If bench is empty, prioritize basic Pokémon to secure the board
            score += 120.0 if len(state.your_bench) == 0 else 80.0
        elif cid == 721:  # Tadbulb
            score += 90.0 if len(state.your_bench) == 0 else 60.0
        elif cid in (1219, 1145, 1086):  # Generator / Nest Ball / Poffin
            score += 70.0
        elif cid in (1092, 1227):  # Research / Lillie
            score += 65.0
        elif cid in (1, 2, 3, 4, 5, 6, 7, 8):  # Energy
            score += 30.0
        else:
            score += 10.0

        ranks.append((idx, score))

    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks
