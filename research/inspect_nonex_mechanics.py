import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_pokemon_data

init_card_database()

print("=== INSPECTING NON-EX THREAT MECHANICS ===")

# Alakazam line
for cid in [741, 742, 743, 65, 66]:
    c = get_card(cid)
    p = get_pokemon_data(cid)
    print(f"\nCard ID {cid}: {get_card_name(cid)}")
    print(f"  Type: {c.get('cardType')}, Stage: {c.get('stage')}, HP: {c.get('hp')}, EX: {c.get('ex')}")
    if p:
        for a in p.get("attacks", []):
            print(f"  Attack: {a.get('name')} | Cost: {a.get('cost')} | Damage: {a.get('damage')} | Effect: {a.get('effect')}")

# Trevenant line
# Let's find Hop's Trevenant and Hop's Phantump
print("\n--- TREVENANT LINE ---")
with open("reports/kaggle_candidate_d/public_93506556/episode-93506556-replay.json", "r") as f:
    replay = json.load(f)
p0_deck = replay["steps"][0][0]["visualize"][0]["action"][0]
for cid in set(p0_deck):
    c = get_card(cid)
    if c and c.get("cardType") == 0:
        p = get_pokemon_data(cid)
        print(f"\nCard ID {cid}: {get_card_name(cid)}")
        print(f"  Stage: {c.get('stage')}, HP: {c.get('hp')}, EX: {c.get('ex')}")
        if p:
            for a in p.get("attacks", []):
                print(f"  Attack: {a.get('name')} | Cost: {a.get('cost')} | Damage: {a.get('damage')} | Effect: {a.get('effect')}")
