import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_pokemon_data
from agent.state import GameState

init_card_database()

def get_pokemon_max_damage(card_id: int) -> float:
    """Extract maximum damage capability of a Pokémon from card database."""
    pdata = get_pokemon_data(card_id)
    if not pdata:
        card = get_card(card_id)
        if card:
            # Fallback estimation
            return 160.0 if card.get("ex") else 70.0
        return 50.0
        
    attacks = pdata.get("attacks") or []
    max_dmg = 0.0
    for atk in attacks:
        if isinstance(atk, dict):
            dmg_val = atk.get("damage", 0)
            try:
                # Parse numeric damage (e.g. 210, "120+", "50x")
                if isinstance(dmg_val, (int, float)):
                    max_dmg = max(max_dmg, float(dmg_val))
                elif isinstance(dmg_val, str):
                    clean_digits = "".join(c for c in dmg_val if c.isdigit())
                    if clean_digits:
                        max_dmg = max(max_dmg, float(clean_digits))
            except Exception:
                pass
    return max_dmg if max_dmg > 0 else 50.0

print("--- Damage Extraction Verification ---")
test_cards = [
    (674, "Hariyama (Non-ex)"),
    (678, "Mega Lucario ex (ex)"),
    (666, "Cinderace (Non-ex)"),
    (756, "Mega Kangaskhan ex (ex)"),
    (345, "Crustle (Non-ex)"),
    (723, "Bellibolt ex (ex)"),
]

for cid, name in test_cards:
    pdata = get_pokemon_data(cid)
    is_ex = bool(pdata and pdata.get("ex", False))
    dmg = get_pokemon_max_damage(cid)
    print(f"Card ID {cid:4d} | {name:<26} | Is EX: {str(is_ex):<5} | Max Damage: {dmg:.1f}")
