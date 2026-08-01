"""
Candidate G Architecture Generator (G0 through G9).
100% legal CABT decks generated for adversarial evaluation.
"""

import os

def generate_candidate_g_decks():
    os.makedirs("research/deck_candidates", exist_ok=True)

    # G0: Candidate F baseline unchanged (4 Dwebble, 4 Crustle, 1 Secret Box, 4 Ultra Ball, 4 Poffin, 4 Rare Candy, 4 Boss, 35 Grass)
    g0 = [344]*4 + [345]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*35

    # G1: Higher Basic Density (4 Dwebble 344 + 2 Tapu Bulu 920 [140 HP Basic], 4 Crustle 345, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Rare Candy 1079, 4 Boss 1182, 33 Grass 1)
    g1 = [344]*4 + [345]*4 + [920]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33

    # G2: Alternate Grass Attacker with Better Damage Efficiency (4 Dwebble 344, 4 Crustle 345, 2 Shaymin 343, 2 Tapu Bulu 920, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 35 Grass 1)
    g2 = [344]*4 + [345]*4 + [343]*2 + [920]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*35

    # G3: Grass Attacker with Higher HP (4 Dwebble 344, 4 Crustle 345, 3 Grookey 89, 2 Thwackey 90, 3 Rillaboom 91, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Rare Candy 1079, 4 Boss 1182, 27 Grass 1)
    g3 = [344]*4 + [345]*4 + [89]*3 + [90]*2 + [91]*3 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*27

    # G4: Alternate Attacker (Colorless Snorlax 160 HP Basic) (4 Dwebble 344, 4 Crustle 345, 2 Snorlax 1072, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 37 Grass 1)
    g4 = [344]*4 + [345]*4 + [1072]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*37

    # G5: Minimal Single-Prize Backup Attacker (4 Dwebble 344, 4 Crustle 345, 1 Tapu Bulu 920, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 38 Grass 1)
    g5 = [344]*4 + [345]*4 + [920]*1 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*38

    # G6: Hybrid Attacker Package (3 Tadbulb 721, 3 Bellibolt ex 723, 3 Dwebble 344, 3 Crustle 345, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 17 Lightning 4, 18 Grass 1)
    g6 = [721]*3 + [723]*3 + [344]*3 + [345]*3 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [4]*17 + [1]*18

    # G7: Anti-Resistance Package (4 Dwebble 344, 4 Crustle 345, 2 Crushing Hammer 1120, 2 Night Stretcher 1097, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 35 Grass 1)
    g7 = [344]*4 + [345]*4 + [1120]*2 + [1097]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*35

    # G8: Anti-Weakness Package (4 Dwebble 344, 4 Crustle 345, 2 Super Potion 1112, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 37 Grass 1)
    g8 = [344]*4 + [345]*4 + [1112]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*37

    # G9: Optimized Combination (4 Dwebble 344, 4 Crustle 345, 2 Tapu Bulu 920, 2 Crushing Hammer 1120, 1 Secret Box 1092, 4 Ultra Ball 1121, 4 Poffin 1086, 4 Boss 1182, 35 Grass 1)
    g9 = [344]*4 + [345]*4 + [920]*2 + [1120]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*35

    g_decks = {
        "G0_f_baseline": g0,
        "G1_high_basic_density": g1,
        "G2_alt_grass_attacker": g2,
        "G3_rillaboom_hp": g3,
        "G4_snorlax_colorless": g4,
        "G5_minimal_backup": g5,
        "G6_hybrid_bellibolt": g6,
        "G7_anti_resistance": g7,
        "G8_anti_weakness": g8,
        "G9_optimized_combination": g9,
    }

    for name, deck in g_decks.items():
        assert len(deck) == 60, f"Deck {name} has {len(deck)} cards, expected 60"
        csv_path = f"research/deck_candidates/{name}.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("Card ID\n")
            for cid in deck:
                f.write(f"{cid}\n")
        print(f"Generated {name}: {csv_path} (60 cards, valid)")

if __name__ == "__main__":
    generate_candidate_g_decks()
