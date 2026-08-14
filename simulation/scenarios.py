from typing import Dict, Any, List, Tuple
from agent.state import GameState, parse_game_state
from agent.action_selector import select_action, select_heuristic_action
from agent.search import shallow_risk_aware_search


def create_lethal_knockout_scenario() -> Dict[str, Any]:
    """
    Scenario: Our Bellibolt ex (723) has 2 energies (160 dmg) against an opponent's Active Tadbulb (100 HP)
    with 1 Prize remaining. Expected action: Select attack (Type 7) to win the game immediately.
    """
    return {
        "remainingOverageTime": 600.0,
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"type": 14},  # Pass turn
                {"type": 8, "inPlayArea": 4},  # Attach energy
                {"type": 7, "index": 0},  # Attack active
            ]
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {
                    "active": [{"id": 723, "hp": 350, "maxHp": 350, "energies": [3, 3]}],
                    "bench": [],
                    "prize": [1],
                    "deckCount": 30,
                },
                {
                    "active": [{"id": 721, "hp": 100, "maxHp": 150, "energies": [3]}],
                    "bench": [{"id": 721, "hp": 150}],
                    "prize": [1, 2, 3, 4],
                    "deckCount": 30,
                }
            ]
        }
    }


def create_crustle_safeguard_scenario() -> Dict[str, Any]:
    """
    Scenario: Our active Bellibolt ex faces an immune Crustle (542) active, but opponent has a vulnerable
    Tadbulb on bench. Expected action: Do NOT waste 0-dmg attack on Crustle; snipe or setup.
    """
    return {
        "remainingOverageTime": 600.0,
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"type": 7, "area": 4, "index": 0},  # Attack active Crustle (immune: 0 damage)
                {"type": 8, "inPlayArea": 5, "inPlayIndex": 0},  # Attach energy to bench anchor
                {"type": 14},  # Pass
            ]
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {
                    "active": [{"id": 723, "hp": 350, "maxHp": 350, "energies": [3, 3]}],
                    "bench": [{"id": 722, "hp": 180, "energies": []}],
                    "prize": [1, 2, 3],
                    "deckCount": 25,
                },
                {
                    "active": [{"id": 542, "hp": 130, "maxHp": 130, "energies": [1, 1]}],  # Crustle Safeguard
                    "bench": [{"id": 721, "hp": 100}],
                    "prize": [1, 2, 3],
                    "deckCount": 25,
                }
            ]
        }
    }


def create_low_deck_scenario() -> Dict[str, Any]:
    """
    Scenario: Own deck has only 2 cards remaining. Professor's Research (1092) would cause deckout defeat.
    Expected action: Do not play Professor's Research.
    """
    return {
        "remainingOverageTime": 600.0,
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"type": 2, "id": 1092},  # Professor's Research (draw 7 cards -> DECKOUT!)
                {"type": 8, "inPlayArea": 4},  # Attach energy
                {"type": 14},  # Pass turn
            ]
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {
                    "active": [{"id": 723, "hp": 350, "energies": [3]}],
                    "bench": [],
                    "prize": [1, 2],
                    "deckCount": 2,  # Danger!
                    "hand": [{"id": 1092}],
                },
                {
                    "active": [{"id": 723, "hp": 350, "energies": [3, 3]}],
                    "bench": [],
                    "prize": [1, 2],
                    "deckCount": 20,
                }
            ]
        }
    }


def run_scenario_tests() -> Dict[str, bool]:
    """Run verification against all handcrafted scenarios."""
    results = {}

    # 1. Lethal Knockout
    obs_ko = create_lethal_knockout_scenario()
    action_ko = select_action(obs_ko)
    # Option 2 is Attack active
    results["lethal_knockout"] = (action_ko == [2])

    # 2. Crustle Safeguard Immunity Avoidance
    obs_crustle = create_crustle_safeguard_scenario()
    action_crustle = select_action(obs_crustle)
    # Option 0 is attack immune Crustle; agent must avoid option 0
    results["crustle_immunity_avoidance"] = (action_crustle != [0])

    # 3. Anti-Deckout Preservation
    obs_deckout = create_low_deck_scenario()
    action_deckout = select_action(obs_deckout)
    # Option 0 is Professor's Research (Deckout suicide); agent must avoid option 0
    results["anti_deckout_preservation"] = (action_deckout != [0])

    return results
