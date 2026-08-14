from typing import Dict, Any, Optional
from src.state_evaluator import GameState
from src.immunity_handler import is_target_immune_to_ex, is_ex_attacker


def evaluate_board_value(state: GameState) -> float:
    """Comprehensive value function evaluating a projected or current board state."""
    value = 0.0

    # 1. Prize Advantage & Win Conditions
    your_prizes_taken = max(0, 6 - state.your_prizes)
    opp_prizes_taken = max(0, 6 - state.opp_prizes)

    value += your_prizes_taken * 150.0
    value -= opp_prizes_taken * 120.0

    if state.your_prizes == 0:
        value += 2000.0  # Game victory
    elif state.your_prizes == 1:
        value += 300.0   # Match point

    if state.opp_prizes == 0:
        value -= 2000.0  # Game loss

    # 2. Active Pokémon HP & Opponent Active HP
    if state.your_active and isinstance(state.your_active, dict):
        hp = float(state.your_active.get("hp", 0))
        max_hp = float(state.your_active.get("maxHp") or state.your_active.get("hp") or 100)
        if max_hp > 0:
            value += min(1.0, hp / max_hp) * 100.0
            
        energies = state.your_active.get("energies", [])
        energy_cnt = len(energies) if isinstance(energies, list) else 0
        value += energy_cnt * 25.0

    if state.opp_active and isinstance(state.opp_active, dict):
        opp_hp = float(state.opp_active.get("hp", 0))
        opp_max_hp = float(state.opp_active.get("maxHp") or state.opp_active.get("hp") or 100)
        if opp_max_hp > 0:
            value -= min(1.0, opp_hp / opp_max_hp) * 80.0

        opp_energies = state.opp_active.get("energies", [])
        opp_energy_cnt = len(opp_energies) if isinstance(opp_energies, list) else 0
        value -= opp_energy_cnt * 20.0

    # 3. Viable Attackers & Bench Quality
    viable_attackers = 0
    for pkmn in [state.your_active] + state.your_bench:
        if pkmn and isinstance(pkmn, dict):
            card_id = pkmn.get("id", 0)
            energies = pkmn.get("energies", [])
            energy_cnt = len(energies) if isinstance(energies, list) else 0
            if card_id in (722, 723) and energy_cnt >= 2:
                viable_attackers += 1

    value += viable_attackers * 60.0
    value += len(state.your_bench) * 15.0

    # 4. Resources
    value += len(state.your_hand) * 4.0
    value += min(30, state.your_deck_count) * 0.5

    # 5. Immunity / Counter Matchup
    if is_ex_attacker(state.your_active) and is_target_immune_to_ex(state.opp_active):
        value -= 150.0

    return value
