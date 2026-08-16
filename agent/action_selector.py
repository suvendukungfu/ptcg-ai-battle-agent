from typing import Dict, Any, List, Optional
from agent.state import GameState, parse_game_state
from agent.policy import (
    classify_game_situation,
    rank_attack_options,
    rank_energy_attachment_options,
    rank_card_play_options,
    rank_discard_options,
    rank_target_options,
)
from agent.search import shallow_risk_aware_search
from agent.belief_state import BeliefStateTracker, BeliefDistribution

from agent.goals import GoalPlanner, StrategicGoal, GoalState
from agent.decomposition import ScoreDecomposer, ValueDecomposition
from agent.fallback import deterministic_fallback, make_distinct_choice
from agent.utils import DIAGNOSTICS, track_telemetry

_BELIEF_TRACKER = BeliefStateTracker()


def select_heuristic_action(state: GameState, goal_state: Optional[GoalState] = None) -> List[int]:
    """Fast tactical heuristic selector guided by strategic goal state."""
    n_opts = len(state.options)
    max_cnt = state.max_count
    min_cnt = state.min_count
    select_type = state.select_type

    if goal_state is None:
        goal_state = GoalPlanner.identify_goal(state)

    if select_type == 0:  # Main turn actions
        # 1. Check for decisive game-winning knockout attack (Score >= 3000)
        attack_ranks = rank_attack_options(state)
        if attack_ranks and attack_ranks[0][1] >= 3000.0:
            preferred = [r[0] for r in attack_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 2. Pre-Attack Development: Card plays (BENCH_FIRST basic placement, Evolutions, Nest Ball, Ultra Ball)
        card_ranks = rank_card_play_options(state)
        if card_ranks and card_ranks[0][1] > 0.0:
            preferred = [r[0] for r in card_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 3. Pre-Attack Development: Energy attachment (to Active or Bench)
        energy_ranks = rank_energy_attachment_options(state)
        if energy_ranks and energy_ranks[0][1] > 0.0:
            preferred = [r[0] for r in energy_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 4. Execute Attack with Active Pokémon (concludes the turn)
        if attack_ranks and attack_ranks[0][1] > -5000.0:
            preferred = [r[0] for r in attack_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

        # 5. Pass turn if no actions remain
        for idx, opt in enumerate(state.options):
            if isinstance(opt, dict) and opt.get("type") == 14:
                return make_distinct_choice([idx], n_opts, max_cnt, min_cnt)

    elif select_type in (7, 8):
        ranks = rank_attack_options(state) if select_type == 7 else rank_energy_attachment_options(state)
        if ranks:
            preferred = [r[0] for r in ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

    # Check for Discard dialogs (e.g. Ultra Ball cost payment)
    is_discard_context = False
    if isinstance(state.select_context, str) and state.select_context.lower() == "discard":
        is_discard_context = True
    elif state.select_type == 1 and state.max_count == 2 and state.min_count == 2:
        # Standard Ultra Ball 2-card discard dialog
        is_discard_context = True

    if is_discard_context:
        discard_ranks = rank_discard_options(state.options, state)
        if discard_ranks:
            preferred = [r[0] for r in discard_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

    # General target / search selection ranking
    target_ranks = rank_target_options(state.options, state)
    if target_ranks:
        preferred = [r[0] for r in target_ranks]
        return make_distinct_choice(preferred, n_opts, max_cnt, min_cnt)

    return make_distinct_choice(list(range(n_opts)), n_opts, max_cnt, min_cnt)


def select_action(obs: Dict[str, Any]) -> List[int]:
    """
    Unified AI Action Decision Pipeline:
    1. Parse and normalize GameState.
    2. Update Bayesian Belief State (opponent hidden hand probabilities).
    3. Identify strategic GoalState.
    4. Execute 1-2 ply shallow risk-aware search lookahead.
    5. Fallback to goal-guided tactical heuristic policy.
    6. Validate choice with legal validator.
    """
    state = parse_game_state(obs)
    n_opts = len(state.options)
    if n_opts == 0:
        return []

    # 1. Update Belief State & Goal
    beliefs = _BELIEF_TRACKER.update_beliefs(state)
    goal_state = GoalPlanner.identify_goal(state)

    remaining_time = float(obs.get("remainingOverageTime", 600.0))

    # 2. 1-2 Ply Shallow Search Lookahead
    search_choice = shallow_risk_aware_search(state, remaining_time)
    if search_choice is not None:
        DIAGNOSTICS["search_decisions"] += 1
        track_telemetry(search_choice, state.options)
        return search_choice

    # 3. Fast Heuristic Selector
    DIAGNOSTICS["heuristic_decisions"] += 1
    action = select_heuristic_action(state, goal_state)
    track_telemetry(action, state.options)
    return action
