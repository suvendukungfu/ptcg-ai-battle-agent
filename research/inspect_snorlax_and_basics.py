"""
Inspect Snorlax (1072) attack data closely - it's a 160-HP Basic Colorless Non-EX.
Also look at other high-damage Colorless/Grass non-EX options.
"""
import csv
import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_pokemon_data

init_card_database()

# Get attack data for key candidates
for cid in [1072, 345, 344, 924, 304, 66, 65]:
    name = get_card_name(cid)
    card = get_card(cid)
    pdata = get_pokemon_data(cid)
    print(f"\n=== {name} (ID {cid}) ===")
    if card:
        print(f"  HP={card.get('hp')}, Type={card.get('pokemonType')}, Stage={card.get('stage')}, EX={card.get('ex')}")
        print(f"  evolvesFrom={card.get('evolvesFrom')}")
    if pdata:
        for k, v in pdata.items():
            print(f"  {k}: {v}")

# Now search CSV for all Colorless basics with HP >= 130 and no evolution requirement
print("\n\n=== ALL COLORLESS/GRASS BASIC NON-EX WITH HP >= 100 ===")
with open("data/EN Card Data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("Card Type") != "Pokemon":
            continue
        if row.get("ex", "").lower() == "true" or row.get("Mega ex", "").lower() == "true":
            continue
        ptype = row.get("Pokemon Type", "")
        if ptype not in ("Grass", "Colorless"):
            continue
        if row.get("Basic", "").lower() != "true":
            continue
        try:
            hp = int(row.get("HP", "0"))
        except:
            hp = 0
        if hp >= 100:
            cid = row.get("Card ID", "")
            print(f"\n  ID {cid}: {row.get('Card Name')} | Type={ptype} | HP={hp} | Basic=True")
            print(f"    Attacks: {row.get('Attacks', '')[:200]}")
            print(f"    Skills:  {row.get('Skills', '')[:200]}")

# Search for Grass Stage 1 non-EX with high damage
print("\n\n=== GRASS STAGE 1 NON-EX WITH HP >= 120 ===")
with open("data/EN Card Data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("Card Type") != "Pokemon":
            continue
        if row.get("ex", "").lower() == "true" or row.get("Mega ex", "").lower() == "true":
            continue
        ptype = row.get("Pokemon Type", "")
        if ptype != "Grass":
            continue
        if row.get("Stage 1", "").lower() != "true":
            continue
        try:
            hp = int(row.get("HP", "0"))
        except:
            hp = 0
        if hp >= 120:
            cid = row.get("Card ID", "")
            print(f"\n  ID {cid}: {row.get('Card Name')} | Type={ptype} | HP={hp}")
            print(f"    Evolves From: {row.get('Evolves From', '')}")
            print(f"    Attacks: {row.get('Attacks', '')[:200]}")
            print(f"    Skills:  {row.get('Skills', '')[:200]}")
