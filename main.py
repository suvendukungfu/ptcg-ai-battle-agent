import os
import sys
import time
import logging
from typing import List, Dict, Any, Optional

# Ensure project root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.state_evaluator import parse_game_state, GameState
from src.attack_evaluator import rank_attack_options
from src.target_selector import rank_target_options
from src.energy_policy import rank_energy_attachment_options
from src.bench_trainer_policy import rank_card_play_options
from src.shallow_search import shallow_risk_aware_search, make_distinct_choice, SEARCH_BUDGET

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Diagnostic telemetry counters for V2
DIAGNOSTICS: Dict[str, Any] = {
    "decisions": 0,
    "search_decisions": 0,
    "heuristic_decisions": 0,
    "fallback_decisions": 0,
    "exceptions": 0,
    "total_decision_time_ms": 0.0,
    "max_decision_time_ms": 0.0,
    "option_types_selected": {},
    "attacks_selected": 0,
    "kos_achieved": 0,
    "games_completed": 0,
}

_CACHED_DECK: Optional[List[int]] = None


def get_deck_path() -> str:
    """Resolve deck.csv relative to main.py directory, with fallback to Kaggle submission path."""
    primary_path = os.path.join(BASE_DIR, "deck.csv")
    if os.path.isfile(primary_path):
        return primary_path

    kaggle_path = "/kaggle_simulations/agent/deck.csv"
    if os.path.isfile(kaggle_path):
        return kaggle_path

    return primary_path


def load_and_validate_deck() -> List[int]:
    """Load deck.csv and validate that it contains exactly 60 valid card IDs."""
    global _CACHED_DECK
    if _CACHED_DECK is not None and len(_CACHED_DECK) == 60:
        return _CACHED_DECK

    deck_path = get_deck_path()
    if not os.path.exists(deck_path):
        # Default Bellibolt ex starter deck
        default_deck = [
            721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
            1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219, 1219, 1219,
            1219, 1227, 1227, 1227, 1227, 1262, 1262
        ] + [3] * 33
        _CACHED_DECK = default_deck
        return _CACHED_DECK

    deck_ids: List[int] = []
    with open(deck_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                parts = line_str.split(",")
                for p in parts:
                    p_clean = p.strip()
                    if p_clean.lstrip("-").isdigit():
                        deck_ids.append(int(p_clean))

    if len(deck_ids) != 60:
        raise ValueError(f"Deck at {deck_path} must contain exactly 60 card IDs, found {len(deck_ids)}")

    _CACHED_DECK = deck_ids
    return _CACHED_DECK


def deterministic_fallback(select: Optional[Dict[str, Any]]) -> List[int]:
    """Deterministic, crash-proof fallback for action selection."""
    DIAGNOSTICS["fallback_decisions"] += 1
    if not select or not isinstance(select, dict):
        return []

    options = select.get("option", [])
    if not isinstance(options, list) or len(options) == 0:
        return []

    max_count = select.get("maxCount", 1)
    if not isinstance(max_count, int) or max_count < 1:
        max_count = 1

    n_opts = len(options)
    selected_indices = make_distinct_choice(list(range(n_opts)), n_opts, max_count)

    # Telemetry tracking
    for idx in selected_indices:
        if 0 <= idx < n_opts:
            opt = options[idx]
            if isinstance(opt, dict) and "type" in opt:
                opt_t = opt["type"]
                DIAGNOSTICS["option_types_selected"][opt_t] = DIAGNOSTICS["option_types_selected"].get(opt_t, 0) + 1
                if opt_t == 7:  # Attack
                    DIAGNOSTICS["attacks_selected"] += 1

    return selected_indices


def select_v1_heuristic_action(state: GameState) -> List[int]:
    """Fast V1 heuristic rule engine fallback for simple/trivial decisions."""
    n_opts = len(state.options)
    max_cnt = state.max_count
    select_type = state.select_type

    if select_type == 0:
        attack_ranks = rank_attack_options(state)
        if attack_ranks and attack_ranks[0][1] > -10000.0:
            preferred = [r[0] for r in attack_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt)

        energy_ranks = rank_energy_attachment_options(state)
        if energy_ranks:
            preferred = [r[0] for r in energy_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt)

        card_ranks = rank_card_play_options(state)
        if card_ranks:
            preferred = [r[0] for r in card_ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt)

        for idx, opt in enumerate(state.options):
            if isinstance(opt, dict) and opt.get("type") == 14:
                return make_distinct_choice([idx], n_opts, max_cnt)

    elif select_type in (7, 8):
        ranks = rank_attack_options(state) if select_type == 7 else rank_energy_attachment_options(state)
        if ranks:
            preferred = [r[0] for r in ranks]
            return make_distinct_choice(preferred, n_opts, max_cnt)

    target_ranks = rank_target_options(state.options, state)
    if target_ranks:
        preferred = [r[0] for r in target_ranks]
        return make_distinct_choice(preferred, n_opts, max_cnt)

    return make_distinct_choice(list(range(n_opts)), n_opts, max_cnt)


def select_policy_action(obs: Dict[str, Any]) -> List[int]:
    """V2 Search-Integrated Policy Decision Engine."""
    state = parse_game_state(obs)
    n_opts = len(state.options)
    if n_opts == 0:
        return []

    remaining_time = float(obs.get("remainingOverageTime", 600.0))

    # 1. Try 1-2 ply shallow risk-aware search
    search_choice = shallow_risk_aware_search(state, remaining_time)
    if search_choice is not None:
        DIAGNOSTICS["search_decisions"] += 1
        _track_telemetry(search_choice, state.options)
        return search_choice

    # 2. Fallback to V1 fast heuristic policy
    DIAGNOSTICS["heuristic_decisions"] += 1
    heuristic_choice = select_v1_heuristic_action(state)
    _track_telemetry(heuristic_choice, state.options)
    return heuristic_choice


def _track_telemetry(chosen_indices: List[int], options: List[Dict[str, Any]]) -> None:
    """Helper to update telemetry counters for selected options."""
    n_opts = len(options)
    for idx in chosen_indices:
        if 0 <= idx < n_opts:
            opt = options[idx]
            if isinstance(opt, dict) and "type" in opt:
                opt_t = opt["type"]
                DIAGNOSTICS["option_types_selected"][opt_t] = DIAGNOSTICS["option_types_selected"].get(opt_t, 0) + 1
                if opt_t == 7:
                    DIAGNOSTICS["attacks_selected"] += 1


def agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """Kaggle competition runner entrypoint function."""
    start_t = time.perf_counter()
    DIAGNOSTICS["decisions"] += 1

    try:
        if not isinstance(obs, dict):
            return deterministic_fallback(None)

        select = obs.get("select")

        # Turn 0: Return 60-card deck
        if select is None:
            return load_and_validate_deck()

        action = select_policy_action(obs)
        
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        DIAGNOSTICS["total_decision_time_ms"] += elapsed_ms
        if elapsed_ms > DIAGNOSTICS["max_decision_time_ms"]:
            DIAGNOSTICS["max_decision_time_ms"] = elapsed_ms

        return action

    except Exception as e:
        DIAGNOSTICS["exceptions"] += 1
        logging.error(f"Exception in agent decision loop: {e}", exc_info=True)
        select_dict = obs.get("select") if isinstance(obs, dict) else None
        return deterministic_fallback(select_dict)


def get_diagnostics() -> Dict[str, Any]:
    """Return diagnostic telemetry snapshot."""
    diag = dict(DIAGNOSTICS)
    total_decs = max(1, diag["decisions"])
    diag["avg_decision_time_ms"] = diag["total_decision_time_ms"] / total_decs
    return diag


def reset_diagnostics() -> None:
    """Reset diagnostic telemetry counters."""
    global DIAGNOSTICS
    DIAGNOSTICS["decisions"] = 0
    DIAGNOSTICS["search_decisions"] = 0
    DIAGNOSTICS["heuristic_decisions"] = 0
    DIAGNOSTICS["fallback_decisions"] = 0
    DIAGNOSTICS["exceptions"] = 0
    DIAGNOSTICS["total_decision_time_ms"] = 0.0
    DIAGNOSTICS["max_decision_time_ms"] = 0.0
    DIAGNOSTICS["option_types_selected"] = {}
    DIAGNOSTICS["attacks_selected"] = 0
    DIAGNOSTICS["kos_achieved"] = 0
    DIAGNOSTICS["games_completed"] = 0
