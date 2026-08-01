"""
Search the card database for anti-Non-EX candidates that:
1. Use Grass Energy OR require no special energy type (Colorless cost)
2. Can exceed Crustle's 120 damage ceiling
3. Can hit 140+ HP Non-EX attackers efficiently
4. Can disrupt evolution
5. Can gust an evolving attacker
6. Can improve prize efficiency
7. Can survive 120+ damage Non-EX attacks
"""
import csv
import json
import sys
import os
import re

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_pokemon_data, get_all_cards

init_card_database()

# Read full CSV for complete data
rows = []
with open("data/EN Card Data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"Total cards in database: {len(rows)}")

# ---------------------------------------------------------------
# SECTION 1: Grass / Colorless Pokemon that deal >= 120 damage
# ---------------------------------------------------------------
print("\n" + "="*80)
print("SECTION 1: HIGH-DAMAGE GRASS/COLORLESS POKEMON (>= 120 DMG)")
print("="*80)

for row in rows:
    card_type = row.get("Card Type", "")
    poke_type = row.get("Pokemon Type", "")
    energy_type = row.get("Energy Type", "")
    hp_raw = row.get("HP", "0")
    card_id_raw = row.get("Card ID", "0")
    attacks_raw = row.get("Attacks", "")
    name = row.get("Card Name", "")
    is_ex = row.get("ex", "").lower() == "true"
    is_mega = row.get("Mega ex", "").lower() == "true"
    stage = row.get("Evolution Type", "")
    evolves_from = row.get("Evolves From", "")
    retreat = row.get("Retreat Cost", "")
    skills = row.get("Skills", "")

    if card_type != "Pokemon":
        continue
    if is_ex or is_mega:
        continue  # We want Non-EX pokemon for single-prize trades

    # Only Grass or Colorless type
    if poke_type not in ("Grass", "Colorless", ""):
        continue

    try:
        hp = int(hp_raw)
    except:
        hp = 0
    try:
        card_id = int(card_id_raw)
    except:
        card_id = 0

    # Parse attacks to find max damage
    max_dmg = 0
    attack_details = []
    if attacks_raw:
        # Attacks field format varies; try to parse
        # Look for damage numbers
        dmg_matches = re.findall(r'(\d+)\s*(?:damage|dmg|\+)', attacks_raw, re.IGNORECASE)
        plain_matches = re.findall(r'"damage"\s*:\s*(\d+)', attacks_raw)
        all_dmgs = dmg_matches + plain_matches
        for d in all_dmgs:
            try:
                v = int(d)
                if v > max_dmg:
                    max_dmg = v
            except:
                pass
        attack_details.append(attacks_raw[:200])

    if max_dmg >= 100 or hp >= 140:
        print(f"\n  ID {card_id:4d}: {name}")
        print(f"    Type={poke_type}, Stage={stage}, HP={hp}, EX={is_ex}")
        print(f"    Max DMG={max_dmg}, Retreat={retreat}")
        print(f"    Evolves From={evolves_from}")
        if skills:
            print(f"    Skills/Abilities={skills[:150]}")
        for ad in attack_details:
            print(f"    Attacks={ad}")

# ---------------------------------------------------------------
# SECTION 2: Trainer cards useful for anti-Non-EX
# ---------------------------------------------------------------
print("\n" + "="*80)
print("SECTION 2: GUST / DISRUPTION / CONTROL TRAINER CARDS")
print("="*80)

gust_keywords = ["gust", "switch", "boss", "signal", "counter catcher", "prime catcher",
                  "hammer", "devolution", "remove energy", "discard energy", "evolv",
                  "devolve"]

for row in rows:
    card_type = row.get("Card Type", "")
    if card_type == "Pokemon":
        continue
    
    name = row.get("Card Name", "")
    card_id_raw = row.get("Card ID", "0")
    skills = row.get("Skills", "")
    attacks_raw = row.get("Attacks", "")
    
    combined_text = (name + " " + skills + " " + attacks_raw).lower()
    
    for kw in gust_keywords:
        if kw in combined_text:
            try:
                card_id = int(card_id_raw)
            except:
                card_id = 0
            print(f"\n  ID {card_id:4d}: {name} (Type={card_type})")
            if skills:
                print(f"    Effect={skills[:200]}")
            if attacks_raw:
                print(f"    Extra={attacks_raw[:200]}")
            break

# ---------------------------------------------------------------
# SECTION 3: Specific cards we should inspect closely
# ---------------------------------------------------------------
print("\n" + "="*80)
print("SECTION 3: CRUSTLE (345) REFERENCE STATS")
print("="*80)
for row in rows:
    try:
        cid = int(row.get("Card ID", "0"))
    except:
        continue
    if cid in (344, 345):
        print(f"\n  ID {cid}: {row.get('Card Name')}")
        print(f"    Type={row.get('Pokemon Type')}, HP={row.get('HP')}, Stage={row.get('Evolution Type')}")
        print(f"    Attacks={row.get('Attacks', '')[:300]}")
        print(f"    Skills={row.get('Skills', '')[:300]}")
