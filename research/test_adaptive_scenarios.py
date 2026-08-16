import sys
import os
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_pokemon_data
from agent.state import GameState, parse_game_state

init_card_database()

def create_scenario_A_ex_only() -> Dict[str, Any]:
    """Scenario A: EX-only attacker (Mega Kangaskhan ex active + Mega Lucario ex bench). Safeguard should wall 100%."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 4, "text": "Attach to Active"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 4,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": [1]}], "hand": [{"id": 1}], "prize": [1, 2, 3], "discard": []},
                {"active": [{"id": 756, "hp": 300, "energies": [1, 1]}], "bench": [{"id": 678, "hp": 260, "energies": [6]}], "hand": 4, "prize": [1, 2, 3], "discard": []}
            ]
        }
    }

def create_scenario_B_nonex_attacker() -> Dict[str, Any]:
    """Scenario B: Non-EX attacker active (Hariyama 150 HP with 3 energies dealing 210 dmg). Real threat!"""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Hariyama"}, {"type": 8, "inPlayArea": 5, "inPlayIndex": 0, "text": "Attach to Bench Backup"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 5,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": [1]}], "hand": [{"id": 1}], "prize": [1, 2], "discard": []},
                {"active": [{"id": 674, "hp": 150, "energies": [6, 6, 6]}], "bench": [], "hand": 3, "prize": [1, 2], "discard": []}
            ]
        }
    }

def create_scenario_C_energy_ramp() -> Dict[str, Any]:
    """Scenario C: Opponent benched attacker with 1/3 energies (T2 threat). Low immediate threat."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 4, "text": "Attach to Active"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 3,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 344, "hp": 60, "energies": []}], "hand": [{"id": 1}], "prize": [1, 2, 3, 4], "discard": []},
                {"active": [{"id": 677, "hp": 70, "energies": [6]}], "bench": [{"id": 674, "hp": 150, "energies": [6]}], "hand": 5, "prize": [1, 2, 3, 4], "discard": []}
            ]
        }
    }

def create_scenario_D_evolution_threat() -> Dict[str, Any]:
    """Scenario D: Opponent has un-evolved Makuhita on bench with 2 energies (T1 threat upon evolution)."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 4, "text": "Attach to Active"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 3,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": []}], "hand": [{"id": 1}], "prize": [1, 2, 3, 4], "discard": []},
                {"active": [{"id": 677, "hp": 70, "energies": []}], "bench": [{"id": 673, "hp": 70, "energies": [6, 6]}], "hand": 5, "prize": [1, 2, 3, 4], "discard": []}
            ]
        }
    }

def create_scenario_E_bench_engine() -> Dict[str, Any]:
    """Scenario E: Opponent has Solrock energy accelerator engine on bench."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 4, "text": "Attach to Active"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 3,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": []}], "hand": [{"id": 1}], "prize": [1, 2, 3, 4], "discard": []},
                {"active": [{"id": 678, "hp": 260, "energies": []}], "bench": [{"id": 676, "hp": 90, "energies": [6]}], "hand": 4, "prize": [1, 2, 3, 4], "discard": []}
            ]
        }
    }

def create_scenario_F_mixed_ex_nonex() -> Dict[str, Any]:
    """Scenario F: Mixed Active Mega Lucario ex (blocked) + Benched Hariyama (3 energies, ready)."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 5, "inPlayIndex": 0, "text": "Attach to Backup Bench"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 5,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": [1]}], "hand": [{"id": 1}], "prize": [1, 2, 3], "discard": []},
                {"active": [{"id": 678, "hp": 260, "energies": [6, 6]}], "bench": [{"id": 674, "hp": 150, "energies": [6, 6, 6]}], "hand": 4, "prize": [1, 2, 3], "discard": []}
            ]
        }
    }

def create_scenario_G_safeguard_wall() -> Dict[str, Any]:
    """Scenario G: Full Safeguard lock (Opponent has only EX Pokémon). Total immunity."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active EX"}, {"type": 8, "inPlayArea": 4, "text": "Attach to Active"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 4,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": []}], "hand": [{"id": 1}], "prize": [1, 2], "discard": []},
                {"active": [{"id": 756, "hp": 300, "energies": [1, 1]}], "bench": [{"id": 756, "hp": 300, "energies": []}], "hand": 3, "prize": [1, 2, 3, 4], "discard": []}
            ]
        }
    }

def create_scenario_H_hidden_info() -> Dict[str, Any]:
    """Scenario H: Opponent has large 7-card hand, unknown attachments."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 4, "text": "Attach to Active"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 3,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": []}], "hand": [{"id": 1}], "prize": [1, 2, 3, 4], "discard": []},
                {"active": [{"id": 677, "hp": 70, "energies": [6]}], "bench": [{"id": 673, "hp": 70, "energies": []}], "hand": 7, "prize": [1, 2, 3, 4], "discard": []}
            ]
        }
    }

def create_scenario_I_prize_race() -> Dict[str, Any]:
    """Scenario I: Match Point prize race (Your prizes: 1, Opponent prizes: 1)."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack for Game KO"}, {"type": 8, "inPlayArea": 4, "text": "Attach Energy"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 7,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": [1, 1]}], "hand": [{"id": 1}], "prize": [1], "discard": []},
                {"active": [{"id": 677, "hp": 70, "energies": [6, 6]}], "bench": [{"id": 674, "hp": 150, "energies": [6, 6, 6]}], "hand": 2, "prize": [1], "discard": []}
            ]
        }
    }

def create_scenario_J_low_resource() -> Dict[str, Any]:
    """Scenario J: Low-resource endgame (Deck count = 3, Active has 2 energies)."""
    return {
        "select": {"type": 0, "minCount": 1, "maxCount": 1, "option": [{"type": 7, "text": "Attack Active"}, {"type": 8, "inPlayArea": 4, "text": "Attach Energy"}, {"type": 14, "text": "Pass"}]},
        "current": {
            "yourIndex": 0, "turn": 10,
            "players": [
                {"active": [{"id": 345, "hp": 130, "energies": [1, 1]}], "bench": [{"id": 345, "hp": 130, "energies": []}], "hand": [{"id": 1}], "prize": [1, 2], "deckCount": 3, "discard": []},
                {"active": [{"id": 756, "hp": 100, "energies": [1, 1]}], "bench": [], "hand": 2, "prize": [1, 2, 3], "discard": []}
            ]
        }
    }

ALL_SCENARIOS = {
    "A_ex_only": create_scenario_A_ex_only,
    "B_nonex_attacker": create_scenario_B_nonex_attacker,
    "C_energy_ramp": create_scenario_C_energy_ramp,
    "D_evolution_threat": create_scenario_D_evolution_threat,
    "E_bench_engine": create_scenario_E_bench_engine,
    "F_mixed_ex_nonex": create_scenario_F_mixed_ex_nonex,
    "G_safeguard_wall": create_scenario_G_safeguard_wall,
    "H_hidden_info": create_scenario_H_hidden_info,
    "I_prize_race": create_scenario_I_prize_race,
    "J_low_resource": create_scenario_J_low_resource,
}

print(f"Constructed {len(ALL_SCENARIOS)} Deterministic Research Scenarios (A to J) successfully.")
