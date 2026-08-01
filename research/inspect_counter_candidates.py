"""
Inspect specific promising anti-Non-EX cards closely.
Focus on cards that:
  - Use Grass or Colorless energy
  - Deal high damage (140+)
  - Have high HP (150+)
  - Disrupt evolution / gust
  - Remain single-energy compatible
"""
import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_pokemon_data

init_card_database()

# Candidates to inspect closely
CANDIDATE_IDS = [
    # High-damage Grass Pokemon
    345,  # Crustle (reference)
    344,  # Dwebble (reference)
    # Colorless non-EX with high HP/damage
    1072, # Snorlax  
    924,  # Meowscarada
    # Trainers
    1182, # Boss's Orders
    1088, # Prime Catcher (ACE SPEC)
    1083, # Counter Catcher
    1120, # Crushing Hammer
    1081, # Enhanced Hammer
    1124, # Pokemon Catcher
    1204, # Lisia's Appeal (switch basic + confuse)
    1191, # Kieran (+30 damage supporter)
    1261, # Forest of Vitality (Grass evolution acceleration)
    604,  # Archeops (devolve ability)
    428,  # Team Rocket's Ampharos (evolve damage counter)
    # Colorless high-HP basics
    304,  # Hop's Snorlax
    66,   # Dudunsparce
]

for cid in CANDIDATE_IDS:
    card = get_card(cid)
    pdata = get_pokemon_data(cid)
    name = get_card_name(cid)
    
    print(f"\n{'='*60}")
    print(f"Card ID {cid}: {name}")
    print(f"{'='*60}")
    
    if card:
        print(f"  cardType:  {card.get('cardType')}")
        print(f"  pokemonType: {card.get('pokemonType')}")
        print(f"  stage:     {card.get('stage')}")
        print(f"  hp:        {card.get('hp')}")
        print(f"  ex:        {card.get('ex')}")
        print(f"  megaEx:    {card.get('megaEx')}")
        print(f"  retreat:   {card.get('retreat')}")
        print(f"  weakness:  {card.get('weakness')}")
        print(f"  resistance:{card.get('resistance')}")
        print(f"  evolvesFrom: {card.get('evolvesFrom')}")
        
        abilities = card.get('abilities') or card.get('skills') or []
        if abilities:
            for a in abilities:
                if isinstance(a, dict):
                    print(f"  Ability: {a.get('name', '')} - {a.get('text', '')[:200]}")
    
    if pdata:
        attacks = pdata.get("attacks") or []
        for a in attacks:
            if isinstance(a, dict):
                cost = a.get("cost", [])
                dmg = a.get("damage", 0)
                eff = a.get("effect", "")
                name_a = a.get("name", "")
                print(f"  Attack: {name_a} | Cost: {cost} | Base Damage: {dmg} | Effect: {eff[:200]}")
    
    if not card and not pdata:
        print(f"  (No data found for card ID {cid})")
