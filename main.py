import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure project root directory is in sys.path safely without relying unconditionally on __file__
def _resolve_base_dir() -> str:
    """Resolve base directory across normal imports and Kaggle exec() environments."""
    # 1. Kaggle remote evaluation container
    if os.path.isdir("/kaggle_simulations/agent"):
        return "/kaggle_simulations/agent"

    # 2. Check __file__ if defined in this execution scope
    try:
        if "__file__" in globals() and globals()["__file__"]:
            return os.path.dirname(os.path.abspath(globals()["__file__"]))
    except Exception:
        pass

    # 3. Current working directory check for signature files
    cwd = os.path.abspath(".")
    if os.path.isfile(os.path.join(cwd, "deck.csv")) or os.path.isdir(os.path.join(cwd, "agent")):
        return cwd

    # 4. Check sys.path entries
    for p in sys.path:
        if p and (os.path.isfile(os.path.join(p, "deck.csv")) or os.path.isdir(os.path.join(p, "agent"))):
            return os.path.abspath(p)

    return cwd

BASE_DIR = _resolve_base_dir()
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agent.state import parse_game_state, GameState
from agent.deck_policy import (
    resolve_deck_path,
    DEFAULT_BELLIBOLT_DECK,
)
from agent.action_selector import select_action, select_heuristic_action
from agent.fallback import deterministic_fallback
from agent.utils import (
    DIAGNOSTICS,
    reset_diagnostics,
    get_diagnostics,
    track_telemetry,
    get_runtime_root,
    resolve_runtime_path,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

_CACHED_DECK: Optional[List[int]] = None


def get_deck_path() -> str:
    """Resolve deck.csv path relative to main.py or Kaggle environment."""
    return resolve_deck_path()


def load_and_validate_deck(deck_path: Optional[str] = None) -> List[int]:
    """Load and validate 60-card list for Turn 0 deck submission."""
    global _CACHED_DECK
    if deck_path is None and _CACHED_DECK is not None and len(_CACHED_DECK) == 60:
        return _CACHED_DECK

    path = deck_path or get_deck_path()
    if not os.path.exists(path):
        _CACHED_DECK = list(DEFAULT_BELLIBOLT_DECK)
        return _CACHED_DECK

    card_ids: List[int] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                parts = line_str.split(",")
                for p in parts:
                    p_clean = p.strip()
                    if p_clean.lstrip("-").isdigit():
                        card_ids.append(int(p_clean))

    if len(card_ids) != 60:
        raise ValueError(f"Deck at {path} must contain exactly 60 cards, found {len(card_ids)}")

    _CACHED_DECK = card_ids
    return card_ids


def agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """
    Official Kaggle competition entrypoint.
    - Turn 0 (obs["select"] is None): Returns 60-card deck list.
    - Turns 1..N: Returns chosen legal option indices from obs["select"]["option"].
    """
    start_t = time.perf_counter()
    DIAGNOSTICS["decisions"] += 1

    try:
        if not isinstance(obs, dict):
            return deterministic_fallback(None)

        select = obs.get("select")

        # Turn 0: Deck Submission
        if select is None:
            return load_and_validate_deck()

        # Turns 1..N: AI Decision Pipeline
        action = select_action(obs)

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
