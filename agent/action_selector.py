from typing import Dict, Any, List, Optional
from agent.state import GameState, parse_game_state
from agent.policy import (
    classify_game_situation,
    rank_attack_options,
    rank_energy_attachment_options,
    rank_card_play_options,
    rank_target_options,
)
import agent.search
import src.shallow_search
from agent.fallback import deterministic_fallback, make_distinct_choice
from agent.utils import DIAGNOSTICS, track_telemetry


def select_heuristic_action(state: GameState) -> List[int]:
    """Fast tactical heuristic selector for rapid or low-budget decision points."""
    n_opts = len(state.options)
    max_cnt = state.max_count
    min_cnt = state.min_count
    select_type = state.select_type

    if select_type == 0:  # Main turn actions
        # 1. Check for knockout or high value attacks
        attack_ranks = rank_attack_options(state)
        if attack_ranks and attack_ranks[0][1] > -5000.0:
            preferred = [r[0] for r in attack_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 2. Check energy attachment
        energy_ranks = rank_energy_attachment_options(state)
        if energy_ranks:
            preferred = [r[0] for r in energy_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 3. Check card plays (evolutions, trainers, supporters)
        card_ranks = rank_card_play_options(state)
        if card_ranks:
            preferred = [r[0] for r in card_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 4. Pass turn if no actions remain
        for idx, opt in enumerate(state.options):
            if isinstance(opt, dict) and opt.get("type") == 14:
                return make_distinct_choice([idx], n_opts, max_cnt, min_cnt)

    elif select_type in (7, 8):
        ranks = rank_attack_options(state) if select_type == 7 else rank_energy_attachment_options(state)
        if ranks:
            preferred = [r[0] for r in ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

    # General target / selection ranking
    target_ranks = rank_target_options(state.options, state)
    if target_ranks:
        preferred = [r[0] for r in target_ranks]
        return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

    return make_distinct_choice(list(range(n_opts)), n_opts, max_cnt, min_cnt)


def select_action(obs: Dict[str, Any]) -> List[int]:
    """
    Unified AI Action Decision Pipeline:
    1. Parse and normalize GameState.
    2. Try 1-2 ply shallow risk-aware search lookahead.
    3. Fallback to fast tactical heuristic policy.
    4. Validate choice with legal validator.
    """
    state = parse_game_state(obs)
    n_opts = len(state.options)
    if n_opts == 0:
        return []

    remaining_time = float(obs.get("remainingOverageTime", 600.0))

    # 1. 1-2 Ply Shallow Search Lookahead (Check src/agent search)
    search_fn = getattr(src.shallow_search, "shallow_risk_aware_search", agent.search.shallow_risk_aware_search)
    search_choice = search_fn(state, remaining_time)
    if search_choice is not None:
        DIAGNOSTICS["search_decisions"] += 1
        track_telemetry(search_choice, state.options)
        return search_choice

    # 2. Fast Tactical Heuristic Policy
    DIAGNOSTICS["heuristic_decisions"] += 1
    heuristic_choice = select_heuristic_action(state)
    track_telemetry(heuristic_choice, state.options)
    return heuristic_choice
