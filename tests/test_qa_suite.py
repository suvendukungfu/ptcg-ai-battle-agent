import os
import sys
import time
import pytest
from unittest.mock import patch

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from src.state_evaluator import parse_game_state, GameState
from src.shallow_search import shallow_risk_aware_search, make_distinct_choice
from src.value_function import evaluate_board_value
from agent.opponent_model import estimate_opponent_threat
from kaggle_environments import make


def test_01_agent_initialization():
    """1. Agent initialization and clean startup."""
    obs = {"select": None, "current": None}
    res = main.agent(obs)
    assert isinstance(res, list)
    assert len(res) == 60
    assert all(isinstance(c, int) for c in res)


def test_02_missing_deck_csv(tmp_path):
    """2. Missing deck.csv falls back gracefully to default 60-card starter deck."""
    with patch("main.get_deck_path", return_value=str(tmp_path / "nonexistent_deck.csv")):
        main._CACHED_DECK = None
        deck = main.load_and_validate_deck()
        assert isinstance(deck, list)
        assert len(deck) == 60


def test_03_invalid_deck_csv(tmp_path):
    """3. Invalid deck.csv with bad format is caught or recovered."""
    bad_deck_file = tmp_path / "bad_deck.csv"
    bad_deck_file.write_text("not_a_number\n123\n")
    with patch("main.get_deck_path", return_value=str(bad_deck_file)):
        main._CACHED_DECK = None
        with pytest.raises(ValueError):
            main.load_and_validate_deck()
    main._CACHED_DECK = None  # Reset


def test_04_60_card_validation():
    """4. 60-card validation strictly requires exactly 60 cards."""
    deck = main.load_and_validate_deck()
    assert len(deck) == 60


def test_05_empty_options():
    """5. Empty options list returns []."""
    obs = {"select": {"type": 0, "minCount": 1, "maxCount": 1, "option": []}}
    action = main.agent(obs)
    assert action == []


def test_06_single_option():
    """6. Single option returns [0]."""
    obs = {"select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]}}
    action = main.agent(obs)
    assert action == [0]


def test_07_multiple_options():
    """7. Multiple options returns valid selection."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 14}, {"type": 7, "index": 0}, {"type": 8, "inPlayArea": 4}]
        }
    }
    action = main.agent(obs)
    assert isinstance(action, list)
    assert len(action) == 1
    assert 0 <= action[0] < 3


def test_08_min_max_count_bounds():
    """8. Adheres strictly to minCount / maxCount bounds."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 2,
            "maxCount": 2,
            "option": [{"type": 0}, {"type": 1}, {"type": 2}, {"type": 3}]
        }
    }
    action = main.agent(obs)
    assert len(action) == 2
    assert action[0] != action[1]


def test_09_multi_select_distinct_indices():
    """9. Multi-select produces strictly distinct indices."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 3,
            "maxCount": 3,
            "option": [{"type": i} for i in range(10)]
        }
    }
    action = main.agent(obs)
    assert len(action) == 3
    assert len(set(action)) == 3


def test_10_attack_selection():
    """10. Attack selection prioritizes damage and KO."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 14}, {"type": 7, "index": 0}]
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {"active": [{"id": 723, "hp": 350, "energies": [3, 3]}]},
                {"active": [{"id": 721, "hp": 50}]}
            ]
        }
    }
    action = main.agent(obs)
    assert action == [1]  # Selects attack option at index 1


def test_11_retreat_selection():
    """11. Retreat options handled without crash."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 14}, {"type": 9, "index": 0}]  # Retreat option
        }
    }
    action = main.agent(obs)
    assert isinstance(action, list)
    assert len(action) == 1


def test_12_evolution_selection():
    """12. Evolution options prioritized for board building."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 14}, {"type": 3, "id": 723}]  # Evolution to Bellibolt ex
        }
    }
    action = main.agent(obs)
    assert action == [1]


def test_13_energy_selection():
    """13. Energy selection attaches to active/bench."""
    obs = {
        "select": {
            "type": 8,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 8, "inPlayArea": 4, "inPlayIndex": 0}]
        }
    }
    action = main.agent(obs)
    assert action == [0]


def test_14_trainer_selection():
    """14. Trainer items (Electric Generator, Boss's Orders) recognized."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 14}, {"type": 2, "id": 1219}]  # Electric Generator
        }
    }
    action = main.agent(obs)
    assert action == [1]


def test_15_search_selection():
    """15. Search selection (Ultra Ball / Nest Ball) handled."""
    obs = {
        "select": {
            "type": 1,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 1, "id": 723}, {"type": 1, "id": 721}]
        }
    }
    action = main.agent(obs)
    assert isinstance(action, list)
    assert len(action) == 1


def test_16_prize_selection():
    """16. Prize card choice context handled."""
    obs = {
        "select": {
            "type": 9,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 10, "index": 0}, {"type": 10, "index": 1}]
        }
    }
    action = main.agent(obs)
    assert len(action) == 1


def test_17_opponent_board_edge_cases():
    """17. Opponent board edge cases (missing/None fields)."""
    obs = {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]},
        "current": {"yourIndex": 0, "players": [None, None]}
    }
    action = main.agent(obs)
    assert action == [0]


def test_18_empty_bench():
    """18. Empty bench handled cleanly."""
    obs = {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]},
        "current": {
            "yourIndex": 0,
            "players": [{"active": [], "bench": []}, {"active": [], "bench": []}]
        }
    }
    action = main.agent(obs)
    assert action == [0]


def test_19_empty_hand():
    """19. Empty hand handled cleanly."""
    obs = {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]},
        "current": {
            "yourIndex": 0,
            "players": [{"hand": []}, {"hand": []}]
        }
    }
    action = main.agent(obs)
    assert action == [0]


def test_20_empty_discard():
    """20. Empty discard handled cleanly."""
    obs = {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]},
        "current": {
            "yourIndex": 0,
            "players": [{"discard": []}, {"discard": []}]
        }
    }
    action = main.agent(obs)
    assert action == [0]


def test_21_nearly_empty_deck():
    """21. Nearly empty deck (deckCount = 0 or 1)."""
    obs = {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 14}]},
        "current": {
            "yourIndex": 0,
            "players": [{"deckCount": 0}, {"deckCount": 1}]
        }
    }
    action = main.agent(obs)
    assert action == [0]


def test_22_game_ending_action():
    """22. Game-ending lethal attack chosen immediately."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 14}, {"type": 7, "index": 0}]
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {"active": [{"id": 723, "hp": 350, "energies": [3, 3, 3]}], "prize": [1]},
                {"active": [{"id": 721, "hp": 50}], "prize": [1, 2, 3]}
            ]
        }
    }
    action = main.agent(obs)
    assert action == [1]  # Lethal winning attack


def test_23_unexpected_card_id():
    """23. Unexpected/unknown card ID (99999) handled safely."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 1, "id": 99999}]
        }
    }
    action = main.agent(obs)
    assert action == [0]


def test_24_unexpected_observation_values():
    """24. Unexpected observation types/values handled without crash."""
    obs = {
        "select": "corrupted_string",
        "current": {"turn": "invalid_int", "players": "not_a_list"}
    }
    action = main.agent(obs)
    assert isinstance(action, list)


def test_25_exceptions_inside_policy():
    """25. Exceptions inside policy caught by defensive outer boundary."""
    with patch("src.shallow_search.shallow_risk_aware_search", side_effect=RuntimeError("Simulated search error")):
        obs = {
            "select": {
                "type": 0,
                "minCount": 1,
                "maxCount": 1,
                "option": [{"type": 14}]
            }
        }
        action = main.agent(obs)
        assert action == [0]
        diag = main.get_diagnostics()
        assert diag["exceptions"] > 0


def test_26_fallback_legality():
    """26. Fallback legality guarantees valid option indices."""
    select = {"maxCount": 2, "option": [{"type": 0}, {"type": 1}, {"type": 2}]}
    action = main.deterministic_fallback(select)
    assert len(action) == 2
    assert action == [0, 1]


def test_27_runtime_performance():
    """27. Runtime performance: average decision time < 20 ms."""
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": 7, "index": 0}, {"type": 8, "inPlayArea": 4}, {"type": 14}]
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {"active": [{"id": 723, "hp": 350, "energies": [3, 3]}], "prize": [1, 2]},
                {"active": [{"id": 721, "hp": 150}], "prize": [1, 2, 3]}
            ]
        }
    }
    start = time.perf_counter()
    for _ in range(50):
        main.agent(obs)
    total_time_ms = (time.perf_counter() - start) * 1000.0
    avg_ms = total_time_ms / 50.0
    assert avg_ms < 20.0  # Must be well under 20ms per decision
