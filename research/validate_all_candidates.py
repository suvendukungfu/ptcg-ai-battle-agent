import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANDIDATE_DIR = os.path.join(BASE_DIR, "research/deck_candidates")

decks = {
    "A_bellibolt_baseline.csv": [721]*4 + [722]*4 + [723]*4 + [1092] + [1121]*2 + [1145]*2 + [1163]*2 + [1219]*4 + [1227]*4 + [1262]*2 + [3]*31,
    "B_bellibolt_consistency_4_3_3.csv": [721]*4 + [722]*3 + [723]*3 + [1092] + [1121]*2 + [1145]*2 + [1163]*2 + [1219]*4 + [1227]*4 + [1262]*2 + [3]*33,
    "C_anti_crustle_tech.csv": [721]*4 + [722]*4 + [723]*2 + [1092] + [1121]*2 + [1145]*2 + [1163]*2 + [1219]*4 + [1227]*4 + [1262]*3 + [3]*32,
    "D_crustle_control.csv": [344]*4 + [345]*4 + [1092] + [1121]*2 + [1145]*2 + [1227]*4 + [1262]*2 + [1]*41,
    "E_alakazam_psychic.csv": [741]*4 + [742]*4 + [743]*4 + [1092] + [1121]*2 + [1145]*2 + [1227]*4 + [1262]*2 + [5]*37,
}

for fname, card_list in decks.items():
    assert len(card_list) == 60, f"{fname} has length {len(card_list)}"
    fpath = os.path.join(CANDIDATE_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(",".join(str(c) for c in card_list) + "\n")
    print(f"Verified {fname}: {len(card_list)} cards written.")
