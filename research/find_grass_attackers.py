import os
import sys
sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_pokemon_data, get_attack_data

init_card_database()

for card_id in range(1, 1500):
    card = get_card(card_id)
    if not card or card.get("cardType") != 0: continue
    pdata = get_pokemon_data(card_id)
    if not pdata: continue
    types = pdata.get("types", [])
    if 1 in types or 7 in types:
        name = get_card_name(card_id)
        if "ex" not in name and "Ex" not in name and card.get("hp", 0) >= 120:
            attacks = []
            for atk_id in pdata.get("attacks", []):
                atk = get_attack_data(atk_id)
                if atk: 
                    dmg = atk.get("damage", "")
                    n = atk.get("name", "")
                    attacks.append(f"{n}({dmg})")
            print(f"ID {card_id}: {name} (HP {card.get('hp')}) - Basic: {pdata.get('basic')} | Attacks: {attacks}")
