import os
from typing import List, Dict, Optional

# Default 60-card Bellibolt ex competitive starter deck
DEFAULT_BELLIBOLT_DECK: List[int] = [
    721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
    1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219, 1219, 1219,
    1219, 1227, 1227, 1227, 1227, 1262, 1262
] + [3] * 33

_CACHED_DECK: Optional[List[int]] = None


def resolve_deck_path() -> str:
    """Resolve deck.csv relative to project root or Kaggle simulation environment."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    primary_path = os.path.join(base_dir, "deck.csv")
    if os.path.isfile(primary_path):
        return primary_path

    kaggle_path = "/kaggle_simulations/agent/deck.csv"
    if os.path.isfile(kaggle_path):
        return kaggle_path

    return primary_path


def load_deck(deck_path: Optional[str] = None) -> List[int]:
    """Load and validate 60-card list from CSV."""
    global _CACHED_DECK
    if deck_path is None and _CACHED_DECK is not None and len(_CACHED_DECK) == 60:
        return _CACHED_DECK

    path = deck_path or resolve_deck_path()
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

    if deck_path is None:
        _CACHED_DECK = card_ids
    return card_ids


def validate_deck_format(deck: List[int]) -> bool:
    """Ensure deck contains exactly 60 integer card IDs."""
    if not isinstance(deck, list) or len(deck) != 60:
        return False
    return all(isinstance(c, int) and c > 0 for c in deck)
