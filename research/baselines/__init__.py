import random
from typing import Dict, Any, List
from agent.fallback import deterministic_fallback


def random_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Pure random agent selecting random legal options."""
    if not isinstance(obs, dict):
        return []

    select = obs.get("select")
    if select is None:
        # Default 60-card Bellibolt starter
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    options = select.get("option", [])
    if not options:
        return []

    min_count = select.get("minCount", 1)
    max_count = select.get("maxCount", 1)
    n_opts = len(options)

    k = min(max_count, n_opts)
    if k <= 0:
        return []

    indices = list(range(n_opts))
    random.shuffle(indices)
    return sorted(indices[:k])


def first_legal_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Deterministic agent always picking the first legal option(s)."""
    if not isinstance(obs, dict):
        return []

    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    return deterministic_fallback(select)


def heuristic_v1_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Pure heuristic V1 rule-based agent without search lookahead or opponent modeling."""
    if not isinstance(obs, dict):
        return []

    select = obs.get("select")
    if select is None:
        from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
        return list(DEFAULT_BELLIBOLT_DECK)

    from agent.state import parse_game_state
    from agent.action_selector import select_heuristic_action
    state = parse_game_state(obs)
    if not state.options:
        return []
    return select_heuristic_action(state)
