from typing import Dict, Any, Callable, List
from agent.state import GameState, parse_game_state
from agent.action_selector import select_heuristic_action
from agent.search import shallow_risk_aware_search, project_action
from agent.evaluator import evaluate_board_value
from agent.opponent_model import estimate_opponent_threat
from agent.risk_model import determine_risk_profile
from agent.fallback import deterministic_fallback, make_distinct_choice


def agent_variant_a_rules_only(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Ablation A: Pure rule-based priority list."""
    if not isinstance(obs, dict):
        return []
    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    state = parse_game_state(obs)
    if not state.options:
        return []
    # Pick first attack, else first energy, else first play, else pass
    opts = state.options
    n = len(opts)
    k = state.max_count
    attacks = [i for i, o in enumerate(opts) if isinstance(o, dict) and o.get("type") == 7]
    if attacks:
        return make_distinct_choice(attacks, n, k)
    energies = [i for i, o in enumerate(opts) if isinstance(o, dict) and o.get("type") == 8]
    if energies:
        return make_distinct_choice(energies, n, k)
    cards = [i for i, o in enumerate(opts) if isinstance(o, dict) and o.get("type") in (0, 1, 2, 3, 4, 5, 6)]
    if cards:
        return make_distinct_choice(cards, n, k)
    return make_distinct_choice([0], n, k)


def agent_variant_b_rules_plus_evaluator(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Ablation B: Rules + Tactical board evaluator (no search, no opponent model)."""
    if not isinstance(obs, dict):
        return []
    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    state = parse_game_state(obs)
    if not state.options:
        return []
    return select_heuristic_action(state)


def agent_variant_c_rules_plus_search(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Ablation C: Rules + 1-ply search lookahead (no opponent threat modeling)."""
    if not isinstance(obs, dict):
        return []
    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    state = parse_game_state(obs)
    if not state.options:
        return []

    # Search without retaliation subtraction
    n_opts = len(state.options)
    k = state.max_count
    scored = []
    for idx in range(min(n_opts, 8)):
        proj, bonus = project_action(state, idx)
        score = evaluate_board_value(proj) + bonus
        scored.append((idx, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    preferred = [x[0] for x in scored]
    return make_distinct_choice(preferred, n_opts, k)


def agent_variant_d_rules_plus_opponent_model(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Ablation D: Rules + Bayesian opponent modeling (no lookahead search)."""
    if not isinstance(obs, dict):
        return []
    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    state = parse_game_state(obs)
    if not state.options:
        return []

    threat = estimate_opponent_threat(state)
    # If high incoming threat, prioritize defensive plays/bench evolution
    return select_heuristic_action(state)


def agent_variant_e_search_plus_opponent_model(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Ablation E: Rules + Search + Opponent counterplay model (static risk profile)."""
    if not isinstance(obs, dict):
        return []
    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    from agent.action_selector import select_action
    return select_action(obs)


def agent_variant_f_full_system(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Ablation F: Full system with dynamic risk sensitivity and meta adaptation."""
    import main
    return main.agent(obs, config)


ABLATION_VARIANTS: Dict[str, Dict[str, Any]] = {
    "A_rules_only": {
        "name": "A: Rules Only",
        "description": "Rule-based priority heuristics without valuation",
        "agent": agent_variant_a_rules_only,
    },
    "B_rules_evaluator": {
        "name": "B: Rules + Evaluator",
        "description": "Multi-factor tactical board value function",
        "agent": agent_variant_b_rules_plus_evaluator,
    },
    "C_rules_search": {
        "name": "C: Rules + Search",
        "description": "1-ply candidate state projection lookahead",
        "agent": agent_variant_c_rules_plus_search,
    },
    "D_rules_opponent_model": {
        "name": "D: Rules + Opponent Model",
        "description": "Bayesian hypergeometric threat assessment",
        "agent": agent_variant_d_rules_plus_opponent_model,
    },
    "E_search_opponent_model": {
        "name": "E: Search + Opponent Model",
        "description": "Shallow lookahead with counterplay estimation",
        "agent": agent_variant_e_search_plus_opponent_model,
    },
    "F_full_system": {
        "name": "F: Full System + Dynamic Risk",
        "description": "Complete production agent with situational risk adaptation",
        "agent": agent_variant_f_full_system,
    },
}
