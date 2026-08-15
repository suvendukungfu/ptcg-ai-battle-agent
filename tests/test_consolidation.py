import os
import sys
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from agent.state import parse_game_state, GameState
from agent.search import shallow_risk_aware_search, project_action, estimate_opponent_counterattack
from agent.action_selector import select_action, select_heuristic_action
from agent.fallback import deterministic_fallback, make_distinct_choice
from agent.evaluator import evaluate_board_value
from agent.opponent_model import estimate_opponent_threat
from agent.goals import GoalPlanner
from agent.belief_state import BeliefStateTracker


def test_consolidated_search_direct_invocation():
    """Verify agent.search works directly on valid game state without src dependencies."""
    obs = {
        "remainingOverageTime": 600.0,
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"index": 0, "type": 7, "name": "Electro Bullet", "damage": 160},
                {"index": 1, "type": 8, "inPlayArea": 4, "name": "Attach Energy"},
                {"index": 2, "type": 14, "name": "Pass"}
            ]
        },
        "current": {
            "yourIndex": 0,
            "turn": 2,
            "players": [
                {"active": [{"id": 723, "hp": 350, "maxHp": 350, "energies": [3, 3]}], "bench": [], "prize": [1, 2, 3, 4, 5, 6], "hand": [{"id": 3}], "deck": 40, "discard": []},
                {"active": [{"id": 721, "hp": 150, "maxHp": 150, "energies": []}], "bench": [], "prize": [1, 2, 3, 4, 5, 6], "hand": 5, "deck": 40, "discard": []}
            ]
        }
    }
    state = parse_game_state(obs)
    choice = shallow_risk_aware_search(state, 600.0)
    assert choice is not None
    assert choice in ([0], [1], [2])


def test_action_selector_end_to_end_pure_agent():
    """Verify select_action works purely through agent/ without any src imports."""
    obs = {
        "remainingOverageTime": 500.0,
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"index": 0, "type": 0, "id": 1219, "name": "Electric Generator"},
                {"index": 1, "type": 14, "name": "Pass"}
            ]
        },
        "current": {
            "yourIndex": 0,
            "turn": 1,
            "players": [
                {"active": [{"id": 723, "hp": 350, "energies": []}], "bench": [], "prize": [1, 2, 3, 4, 5, 6], "hand": [{"id": 1219}], "deck": 45, "discard": []},
                {"active": [{"id": 721, "hp": 150, "energies": []}], "bench": [], "prize": [1, 2, 3, 4, 5, 6], "hand": 5, "deck": 45, "discard": []}
            ]
        }
    }
    action = main.agent(obs)
    assert isinstance(action, list)
    assert len(action) == 1
    assert action in ([0], [1])


def test_zero_src_modules_in_sys_modules():
    """Confirm that executing main.agent does not dynamically import src modules."""
    # Clear any cached src modules
    for mod_name in list(sys.modules.keys()):
        if mod_name.startswith("src.") or mod_name == "src":
            del sys.modules[mod_name]

    obs = {"select": None, "current": None}
    deck = main.agent(obs)
    assert len(deck) == 60

    mock_obs = {
        "remainingOverageTime": 600.0,
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]},
        "current": {"yourIndex": 0, "turn": 1, "players": [{"active": [{"id": 723}], "prize": [1, 2]}, {"active": [{"id": 721}], "prize": [1, 2]}]}
    }
    action = main.agent(mock_obs)
    assert action == [0]

    # Verify no src module was imported
    imported_src = [m for m in sys.modules if m == "src" or m.startswith("src.")]
    assert len(imported_src) == 0, f"Found unexpected src modules imported: {imported_src}"
