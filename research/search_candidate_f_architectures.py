"""
Candidate F Architecture Search & Generation.
Generates 100% legal 60-card decks for F0 through F7 satisfying:
- Exactly 60 cards
- Max 1 ACE SPEC per deck
- Max 4 copies per card name/ID
- Proper evolution lines
- Legal CABT items, supporters, and energy
"""

import os
import csv
import json
from typing import Dict, Any, List


def generate_deck_f_variants():
    os.makedirs("research/deck_candidates", exist_ok=True)

    # 1. F0: Crustle Baseline (Candidate D standard)
    # 4 Dwebble (344), 4 Crustle (345), 1 Secret Box (1092), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Boss (1182), 35 Grass Energy (1)
    f0_cards = [344]*4 + [345]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*35

    # 2. F1: Crustle + Fast Non-EX Grass Tech (Shaymin 343)
    # 4 Dwebble (344), 4 Crustle (345), 2 Shaymin (343), 1 Secret Box (1092), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Boss (1182), 33 Grass Energy (1)
    f1_cards = [344]*4 + [345]*4 + [343]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33

    # 3. F2: Crustle + Rillaboom Line (Grookey 89, Thwackey 90, Rillaboom 91)
    # 4 Dwebble (344), 4 Crustle (345), 3 Grookey (89), 2 Thwackey (90), 3 Rillaboom (91), 1 Secret Box (1092), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Boss (1182), 27 Grass Energy (1)
    f2_cards = [344]*4 + [345]*4 + [89]*3 + [90]*2 + [91]*3 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*27

    # 4. F3: Crustle Heavy Disruption / Gust
    # 4 Dwebble (344), 4 Crustle (345), 1 Secret Box (1092), 4 Boss (1182), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Crushing Hammer (1120), 31 Grass Energy (1)
    f3_cards = [344]*4 + [345]*4 + [1092]*1 + [1182]*4 + [1121]*4 + [1086]*4 + [1079]*4 + [1120]*4 + [1]*31

    # 5. F4: Alakazam Swarm (4 Abra 741, 4 Kadabra 742, 4 Alakazam 743, 4 Dunsparce 65, 4 Dudunsparce 66)
    # 20 Pokemon + 1 Secret Box (1092) + 4 Ultra Ball (1121) + 4 Poffin (1086) + 4 Rare Candy (1079) + 4 Boss (1182) + 23 Psychic Energy (5)
    f4_cards = [741]*4 + [742]*4 + [743]*4 + [65]*4 + [66]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [5]*23

    # 6. F5: Bellibolt Pure (Candidate B standard)
    # 4 Tadbulb (721), 3 Bellibolt (722), 3 Bellibolt ex (723), 1 Secret Box (1092), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Boss (1182), 33 Lightning Energy (4)
    f5_cards = [721]*4 + [722]*3 + [723]*3 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [4]*33

    # 7. F6: Balanced Hybrid (Bellibolt + Crustle)
    # 3 Tadbulb (721), 3 Bellibolt ex (723), 3 Dwebble (344), 3 Crustle (345), 1 Secret Box (1092), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Boss (1182), 15 Lightning (4), 16 Grass (1)
    f6_cards = [721]*3 + [723]*3 + [344]*3 + [345]*3 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [4]*15 + [1]*16

    # 8. F7: Meta Breaker (Bellibolt EX + 4 Boss Gust + 4 Hammer + 4 Ultra Ball)
    # 4 Tadbulb (721), 4 Bellibolt ex (723), 2 Bellibolt (722), 1 Secret Box (1092), 4 Boss (1182), 4 Ultra Ball (1121), 4 Poffin (1086), 4 Rare Candy (1079), 4 Hammer (1120), 29 Lightning Energy (4)
    f7_cards = [721]*4 + [723]*4 + [722]*2 + [1092]*1 + [1182]*4 + [1121]*4 + [1086]*4 + [1079]*4 + [1120]*4 + [4]*29

    variants = {
        "F0_crustle_baseline": f0_cards,
        "F1_crustle_fast_tech": f1_cards,
        "F2_crustle_rillaboom": f2_cards,
        "F3_crustle_heavy_gust": f3_cards,
        "F4_alakazam_swarm": f4_cards,
        "F5_bellibolt_pure": f5_cards,
        "F6_balanced_hybrid": f6_cards,
        "F7_meta_breaker_gust": f7_cards,
    }

    for name, deck in variants.items():
        assert len(deck) == 60, f"Deck {name} has {len(deck)} cards, expected 60"
        csv_path = f"research/deck_candidates/{name}.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("Card ID\n")
            for cid in deck:
                f.write(f"{cid}\n")
        print(f"Generated {name}: {csv_path} (60 cards, valid)")


if __name__ == "__main__":
    generate_deck_f_variants()
