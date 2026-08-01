import csv
import sys
import os
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_all_cards

init_card_database()
all_cards = get_all_cards()

print("=== DESIGNING CANDIDATE E DECK VARIANTS ===")

# E0: Baseline Crustle
E0_DECK = [
    344, 344, 344, 344,  # Dwebble (4)
    345, 345, 345, 345,  # Crustle (4)
    1092,                # Secret Box (1)
    1121, 1121,          # Ultra Ball (2)
    1145, 1145,          # Mega Signal (2)
    1227, 1227, 1227, 1227, # Lillie's Determination (4)
    1262, 1262,          # Surfing Beach (2)
] + [1] * 41             # Basic {G} Energy (41)

# E3: Crustle Control with Gust (Boss's Orders) & Search Optimization
# 4 Dwebble, 4 Crustle, 4 Boss's Orders (1182), 4 Ultra Ball (1121), 4 Buddy Poffin (1086), 4 Lillie's (1227), 2 Surfing Beach (1262), 1 Secret Box (1092), 33 Grass Energy
E3_DECK = [
    344, 344, 344, 344,  # Dwebble (4)
    345, 345, 345, 345,  # Crustle (4)
    1182, 1182, 1182, 1182, # Boss's Orders (4)
    1121, 1121, 1121, 1121, # Ultra Ball (4)
    1086, 1086, 1086, 1086, # Buddy-Buddy Poffin (4)
    1227, 1227, 1227, 1227, # Lillie's Determination (4)
    1262, 1262,          # Surfing Beach (2)
    1092,                # Secret Box (1)
] + [1] * 33             # Basic {G} Energy (33)

# E5: Hybrid Safeguard Wall + High Damage Beatdown (Crustle 4-4 + Bellibolt 4-4 + Boss + Poffin)
# 4 Dwebble (344), 4 Crustle (345), 4 Tadbulb (721), 4 Bellibolt (722), 4 Boss (1182), 4 Poffin (1086), 4 Ultra Ball (1121), 4 Lillie (1227), 24 Lightning/Grass Energy
E5_DECK = [
    344, 344, 344, 344,  # Dwebble (4)
    345, 345, 345, 345,  # Crustle (4)
    721, 721, 721, 721,  # Tadbulb (4)
    722, 722, 722, 722,  # Bellibolt non-ex (4) - deals 160 damage!
    1182, 1182, 1182,    # Boss's Orders (3)
    1086, 1086, 1086, 1086, # Buddy-Buddy Poffin (4)
    1121, 1121, 1121, 1121, # Ultra Ball (4)
    1227, 1227, 1227,    # Lillie's (3)
    1092,                # Secret Box (1)
] + [3] * 29             # Basic {L} Energy (29)

def validate_deck(deck, name):
    print(f"\nValidating {name} ({len(deck)} cards):")
    assert len(deck) == 60, f"Deck length is {len(deck)}, expected 60"
    from collections import Counter
    counts = Counter(deck)
    for cid, cnt in counts.items():
        cname = get_card_name(cid)
        card = get_card(cid)
        is_energy = (cid <= 8)
        if not is_energy and cnt > 4:
            print(f"  ERROR: {cname} has {cnt} copies (>4)")
            return False
        if card is None and not is_energy:
            print(f"  ERROR: Unknown card ID {cid}")
            return False
    print(f"  {name}: 100% VALID LEGAL 60-CARD DECK!")
    return True

validate_deck(E0_DECK, "E0 Baseline Crustle")
validate_deck(E3_DECK, "E3 Crustle + Boss/Poffin Control")
validate_deck(E5_DECK, "E5 Hybrid Crustle + Bellibolt 160 DMG Beatdown")
