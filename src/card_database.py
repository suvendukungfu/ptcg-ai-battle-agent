import csv
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

# Cache dictionary to prevent repeated I/O
_CARD_CACHE: Dict[int, Dict[str, Any]] = {}
_INITIALIZED: bool = False


def _find_card_csv() -> Optional[Path]:
    """Search for EN Card Data.csv across standard locations."""
    # Check config.py if available
    try:
        from config import get_competition_data_path
        comp_path = get_competition_data_path()
        if comp_path:
            for cand in comp_path.rglob("*.csv"):
                if "en card data" in cand.name.lower() or "card_data_en" in cand.name.lower():
                    return cand
    except Exception:
        pass

    # Check local data directories relative to file
    project_root = Path(__file__).parent.parent.resolve()
    candidates = [
        project_root / "data" / "EN Card Data.csv",
        project_root / "kaggle_data" / "EN Card Data.csv",
        project_root / "data" / "en_card_data.csv",
    ]
    for c in candidates:
        if c.exists():
            return c
            
    return None


def init_card_database(force_reload: bool = False) -> None:
    """Load and index all card records from EN Card Data.csv into memory."""
    global _CARD_CACHE, _INITIALIZED
    if _INITIALIZED and not force_reload:
        return

    _CARD_CACHE.clear()
    csv_path = _find_card_csv()

    if csv_path and csv_path.exists():
        with open(csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Normalize keys (handle both 'Card ID' and 'cardId' etc.)
                    card_id_str = row.get("Card ID") or row.get("cardId") or row.get("id") or row.get("card_id")
                    if not card_id_str:
                        continue
                    card_id = int(card_id_str)

                    # Parse JSON attacks / skills if serialized
                    attacks_raw = row.get("Attacks") or row.get("attacks") or "[]"
                    try:
                        attacks = json.loads(attacks_raw) if isinstance(attacks_raw, str) and attacks_raw.startswith("[") else []
                    except Exception:
                        attacks = []

                    skills_raw = row.get("Skills") or row.get("skills") or "[]"
                    try:
                        skills = json.loads(skills_raw) if isinstance(skills_raw, str) and skills_raw.startswith("[") else []
                    except Exception:
                        skills = []

                    card_obj = {
                        "cardId": card_id,
                        "name": row.get("Card Name") or row.get("name", f"Card #{card_id}"),
                        "cardType": int(row.get("Card Type") or row.get("cardType", 0)),
                        "pokemonType": int(row.get("Pokemon Type") or row.get("pokemonType", 0)),
                        "evolutionType": int(row.get("Evolution Type") or row.get("evolutionType", 0)),
                        "retreatCost": int(row.get("Retreat Cost") or row.get("retreatCost", 0)),
                        "hp": int(row.get("HP") or row.get("hp", 0)),
                        "weakness": row.get("Weakness") or row.get("weakness"),
                        "resistance": row.get("Resistance") or row.get("resistance"),
                        "energyType": int(row.get("Energy Type") or row.get("energyType", 0)),
                        "basic": str(row.get("Basic") or row.get("basic", "false")).lower() in ("true", "1"),
                        "stage1": str(row.get("Stage 1") or row.get("stage1", "false")).lower() in ("true", "1"),
                        "stage2": str(row.get("Stage 2") or row.get("stage2", "false")).lower() in ("true", "1"),
                        "ex": str(row.get("ex") or row.get("is_ex", "false")).lower() in ("true", "1"),
                        "megaEx": str(row.get("Mega ex") or row.get("megaEx", "false")).lower() in ("true", "1"),
                        "tera": str(row.get("Tera") or row.get("tera", "false")).lower() in ("true", "1"),
                        "aceSpec": str(row.get("ACE SPEC") or row.get("aceSpec", "false")).lower() in ("true", "1"),
                        "evolvesFrom": row.get("Evolves From") or row.get("evolvesFrom"),
                        "attacks": attacks,
                        "skills": skills,
                    }
                    _CARD_CACHE[card_id] = card_obj
                except Exception:
                    continue

    # Fallback to lib.AllCard() if available and cache is empty
    if not _CARD_CACHE:
        try:
            import ctypes
            from cg.sim import lib
            lib.AllCard.restype = ctypes.c_char_p
            raw = lib.AllCard()
            if raw:
                cards = json.loads(raw.decode("utf-8"))
                for c in cards:
                    cid = c.get("cardId")
                    if cid is not None:
                        _CARD_CACHE[int(cid)] = c
        except Exception:
            pass

    _INITIALIZED = True


def get_card(card_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve full card metadata dictionary by Card ID."""
    if not _INITIALIZED:
        init_card_database()
    return _CARD_CACHE.get(card_id)


def get_card_name(card_id: int) -> str:
    """Retrieve localized card name."""
    card = get_card(card_id)
    return card.get("name", f"Card #{card_id}") if card else f"Unknown (#{card_id})"


def get_card_type(card_id: int) -> int:
    """Retrieve card type integer code."""
    card = get_card(card_id)
    return card.get("cardType", 0) if card else 0


def get_card_category(card_id: int) -> str:
    """Retrieve high-level card category (Pokemon, Trainer, Energy)."""
    card = get_card(card_id)
    if not card:
        return "Unknown"
    ctype = card.get("cardType", 0)
    if ctype in (1, 2, 3, 4):  # Pokemon types
        return "Pokemon"
    elif ctype == 5:
        return "Energy"
    elif ctype in (6, 7, 8, 9, 10):
        return "Trainer"
    return "Unknown"


def get_pokemon_data(card_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve Pokémon-specific stats (HP, Retreat, Stage, EvolvesFrom, Weakness)."""
    card = get_card(card_id)
    if not card:
        return None
    return {
        "hp": card.get("hp", 0),
        "retreatCost": card.get("retreatCost", 0),
        "pokemonType": card.get("pokemonType", 0),
        "evolutionType": card.get("evolutionType", 0),
        "basic": card.get("basic", False),
        "stage1": card.get("stage1", False),
        "stage2": card.get("stage2", False),
        "ex": card.get("ex", False),
        "evolvesFrom": card.get("evolvesFrom"),
        "weakness": card.get("weakness"),
        "resistance": card.get("resistance"),
    }


def get_attack_data(card_id: int) -> List[Dict[str, Any]]:
    """Retrieve list of attacks for the specified card ID."""
    card = get_card(card_id)
    if not card:
        return []
    return card.get("attacks", [])


def get_all_cards() -> Dict[int, Dict[str, Any]]:
    """Retrieve dictionary of all cached cards."""
    if not _INITIALIZED:
        init_card_database()
    return _CARD_CACHE
