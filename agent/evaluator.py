from typing import Dict, Any, Optional
from dataclasses import dataclass
from agent.state import GameState
from agent.card_database import get_card, get_pokemon_data


@dataclass
class EvaluatorWeights:
    """Configurable weights for tactical board value evaluation."""
    w_win: float = 2500.0
    w_loss: float = -2500.0
    w_match_point: float = 400.0
    w_prize_taken: float = 160.0
    w_opp_prize_taken: float = 130.0
    w_active_hp_pct: float = 100.0
    w_active_energy: float = 30.0
    w_opp_active_hp_pct: float = 85.0
    w_opp_active_energy: float = 25.0
    w_viable_attacker: float = 65.0
    w_bench_presence: float = 18.0
    w_hand_resource: float = 4.0
    w_deck_resource: float = 0.5
    w_immunity_penalty: float = 180.0


DEFAULT_WEIGHTS = EvaluatorWeights()


def is_target_immune_to_ex(target: Optional[Dict[str, Any]]) -> bool:
    """Determine if target Pokémon possesses immunity to Pokémon ex attacks (e.g. Crustle Safeguard)."""
    if not target or not isinstance(target, dict):
        return False
    card_id = target.get("id", 0)
    # Recognized Safeguard IDs: Crustle (345, 533, 542)
    if card_id in (345, 533, 542):
        return True
    pdata = get_pokemon_data(card_id)
    if pdata:
        skills = pdata.get("skills", [])
        if isinstance(skills, list):
            for sk in skills:
                if isinstance(sk, dict):
                    sk_text = (sk.get("text") or "").lower()
                    sk_name = (sk.get("name") or "").lower()
                    if "prevent all damage" in sk_text and ("{ex}" in sk_text or "pokemon ex" in sk_text):
                        return True
                    if "mysterious rock inn" in sk_name or "safeguard" in sk_name:
                        return True
    return False



def is_ex_attacker(attacker: Optional[Dict[str, Any]]) -> bool:
    """Determine if attacker is a Pokémon ex."""
    if not attacker or not isinstance(attacker, dict):
        return False
    card_id = attacker.get("id", 0)
    if card_id == 723:  # Bellibolt ex
        return True
    pdata = get_pokemon_data(card_id)
    return bool(pdata and pdata.get("ex", False))


def calculate_immunity_multiplier(attacker: Optional[Dict[str, Any]], target: Optional[Dict[str, Any]]) -> float:
    """Return damage multiplier considering Safeguard / ex immunity."""
    if is_ex_attacker(attacker) and is_target_immune_to_ex(target):
        return 0.0
    return 1.0


def estimate_raw_damage(attacker: Optional[Dict[str, Any]]) -> float:
    """Estimate base damage output based on attacker card ID and attached energy."""
    if not attacker or not isinstance(attacker, dict):
        return 0.0

    card_id = attacker.get("id", 0)
    energies = attacker.get("energies", [])
    n_energies = len(energies) if isinstance(energies, list) else 0

    if card_id == 723:  # Bellibolt ex
        return 160.0 if n_energies >= 2 else (30.0 if n_energies >= 1 else 0.0)
    elif card_id == 722:  # Bellibolt
        return 70.0 if n_energies >= 2 else (20.0 if n_energies >= 1 else 0.0)
    elif card_id == 721:  # Tadbulb
        return 30.0 if n_energies >= 1 else 10.0

    return float(max(10, n_energies * 30))


def get_target_hp(target: Optional[Dict[str, Any]]) -> float:
    """Retrieve current HP of target."""
    if not target or not isinstance(target, dict):
        return 0.0
    return float(target.get("hp", 0))


def get_target_prize_value(target: Optional[Dict[str, Any]]) -> int:
    """Return number of prize cards taken for knocking out the target Pokémon."""
    if not target or not isinstance(target, dict):
        return 1
    card_id = target.get("id", 0)
    if card_id == 723 or is_ex_attacker(target):
        return 2
    return 1


def evaluate_board_value(state: GameState, weights: EvaluatorWeights = DEFAULT_WEIGHTS) -> float:
    """Comprehensive tactical value function evaluating a projected or current board state."""
    value = 0.0

    # 1. Prize Advantage & Terminal Win Conditions
    your_prizes_taken = max(0, 6 - state.your_prizes)
    opp_prizes_taken = max(0, 6 - state.opp_prizes)

    value += your_prizes_taken * weights.w_prize_taken
    value -= opp_prizes_taken * weights.w_opp_prize_taken

    if state.your_prizes == 0:
        value += weights.w_win
    elif state.your_prizes == 1:
        value += weights.w_match_point

    if state.opp_prizes == 0:
        value += weights.w_loss

    # 2. Active Pokémon HP & Energy Comparison
    if state.your_active and isinstance(state.your_active, dict):
        hp = float(state.your_active.get("hp", 0))
        max_hp = float(state.your_active.get("maxHp") or state.your_active.get("hp") or 100)
        if max_hp > 0:
            value += min(1.0, hp / max_hp) * weights.w_active_hp_pct

        energies = state.your_active.get("energies", [])
        energy_cnt = len(energies) if isinstance(energies, list) else 0
        value += energy_cnt * weights.w_active_energy

    if state.opp_active and isinstance(state.opp_active, dict):
        opp_hp = float(state.opp_active.get("hp", 0))
        opp_max_hp = float(state.opp_active.get("maxHp") or state.opp_active.get("hp") or 100)
        if opp_max_hp > 0:
            value -= min(1.0, opp_hp / opp_max_hp) * weights.w_opp_active_hp_pct

        opp_energies = state.opp_active.get("energies", [])
        opp_energy_cnt = len(opp_energies) if isinstance(opp_energies, list) else 0
        value -= opp_energy_cnt * weights.w_opp_active_energy

    # 3. Viable Attackers & Bench Readiness
    viable_attackers = 0
    all_own = [state.your_active] + state.your_bench
    for pkmn in all_own:
        if pkmn and isinstance(pkmn, dict):
            card_id = pkmn.get("id", 0)
            energies = pkmn.get("energies", [])
            energy_cnt = len(energies) if isinstance(energies, list) else 0
            if card_id in (722, 723) and energy_cnt >= 2:
                viable_attackers += 1

    value += viable_attackers * weights.w_viable_attacker
    value += len(state.your_bench) * weights.w_bench_presence

    # 4. Resources
    value += len(state.your_hand) * weights.w_hand_resource
    value += min(30, state.your_deck_count) * weights.w_deck_resource

    # 5. Immunity / Safeguard Counter Matchup
    if is_ex_attacker(state.your_active) and is_target_immune_to_ex(state.opp_active):
        value -= weights.w_immunity_penalty

    return value
