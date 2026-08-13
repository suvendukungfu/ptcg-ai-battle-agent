from typing import Dict, Any, Optional

# Card IDs or ability markers known for ex / Special immunity (e.g. Crustle, Mimikyu, etc.)
EX_IMMUNE_CARD_IDS = {
    # Known safeguard / ex-damage immunity card IDs in engine
    542, 600, 750, 999 
}


def is_ex_attacker(pokemon: Optional[Dict[str, Any]]) -> bool:
    """Check if the given Pokémon is an ex or Mega-ex attacker."""
    if not pokemon or not isinstance(pokemon, dict):
        return False
    card_id = pokemon.get("id", 0)
    max_hp = pokemon.get("maxHp", 0)
    # Bellibolt ex ID 723 or high-HP ex indicator (maxHp >= 200)
    return card_id == 723 or max_hp >= 200


def is_target_immune_to_ex(target_pokemon: Optional[Dict[str, Any]]) -> bool:
    """Check if target Pokémon prevents damage from ex / Mega-ex attackers."""
    if not target_pokemon or not isinstance(target_pokemon, dict):
        return False
    
    card_id = target_pokemon.get("id", 0)
    if card_id in EX_IMMUNE_CARD_IDS:
        return True

    # Check for safeguard / immunity flags in card abilities or conditions if present
    abilities = target_pokemon.get("abilities", [])
    if isinstance(abilities, list):
        for ab in abilities:
            if isinstance(ab, dict) and "safeguard" in str(ab.get("name", "")).lower():
                return True

    return False


def calculate_immunity_multiplier(attacker: Optional[Dict[str, Any]], target: Optional[Dict[str, Any]]) -> float:
    """Returns 0.0 if damage is completely blocked by immunity, else 1.0."""
    if is_ex_attacker(attacker) and is_target_immune_to_ex(target):
        return 0.0
    return 1.0
