"""
Candidate H Architecture Generator & Automated Deck Search (H0 through H10).
"""

import os

def generate_h_decks():
    os.makedirs("research/deck_candidates", exist_ok=True)

    h0 = [344]*4 + [345]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*35
    h1 = [344]*4 + [345]*4 + [920]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33
    h2 = [344]*4 + [345]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1120]*4 + [1]*31
    h3 = [344]*4 + [345]*4 + [1097]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33
    h4 = [344]*4 + [345]*4 + [1072]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33
    h5 = [344]*4 + [345]*4 + [1120]*2 + [1097]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*31
    h6 = [344]*4 + [345]*4 + [1112]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33
    h7 = [344]*4 + [345]*4 + [1182]*4 + [1120]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1]*31
    h8 = [344]*4 + [345]*4 + [343]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1]*33
    # H9: 12 Pokemon + 17 Trainers + 15 Lightning + 16 Grass = 60
    h9 = [721]*3 + [723]*3 + [344]*3 + [345]*3 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [4]*15 + [1]*16
    # H10: 8 Pokemon + 22 Trainers + 30 Grass = 60
    h10 = [344]*4 + [345]*4 + [1120]*2 + [1097]*2 + [1092]*1 + [1121]*4 + [1086]*4 + [1079]*4 + [1182]*4 + [1112]*1 + [1]*30

    h_decks = {
        "H0_f_baseline": h0,
        "H1_basic_density": h1,
        "H2_trainer_density": h2,
        "H3_minimal_recovery": h3,
        "H4_neutral_snorlax": h4,
        "H5_anti_resistance": h5,
        "H6_anti_weakness": h6,
        "H7_gust_control": h7,
        "H8_prize_race_shield": h8,
        "H9_adaptive_hybrid": h9,
        "H10_pareto_disruption": h10,
    }

    for name, deck in h_decks.items():
        assert len(deck) == 60, f"Deck {name} has {len(deck)} cards, expected 60"
        csv_path = f"research/deck_candidates/{name}.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("Card ID\n")
            for cid in deck:
                f.write(f"{cid}\n")
        print(f"Generated {name}: {csv_path} (60 cards, valid)")

if __name__ == "__main__":
    generate_h_decks()
