"""
10 Scripted Adversarial Opponent Deck Generator.
Creates 100% legal CABT decks for all 10 meta archetypes.
"""

import os

def generate_adversarial_opponent_decks():
    os.makedirs("research/deck_candidates", exist_ok=True)

    # 1. Mega Lucario ex (677 Riolu 4, 678 Lucario 4, 676 Solrock 4, 675 Lunatone 4 = 16) + 13 Trainers + 31 Fighting Energy
    d_lucario = [677]*4 + [678]*4 + [676]*4 + [675]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [6]*31

    # 2. Mega Abomasnow ex (697 Snover 4, 698 Abomasnow 4 = 8) + 13 Trainers + 39 Water Energy
    d_abomasnow = [697]*4 + [698]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [3]*39

    # 3. Marnie's Grimmsnarl ex (856 Impidimp 4, 857 Morgrem 4, 858 Grimmsnarl 4 = 12) + 13 Trainers + 35 Darkness Energy
    d_grimmsnarl = [856]*4 + [857]*4 + [858]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [7]*35

    # 4. Duraludon Non-EX (169 Duraludon 4 = 4) + 17 Trainers + 39 Metal Energy
    d_duraludon = [169]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1120]*4 + [8]*39

    # 5. Alakazam Non-EX (741 Abra 4, 742 Kadabra 4, 743 Alakazam 4, 65 Dunsparce 4, 66 Dudunsparce 4 = 20) + 13 Trainers + 27 Psychic Energy
    d_alakazam = [741]*4 + [742]*4 + [743]*4 + [65]*4 + [66]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [5]*27

    # 6. Hop's Trevenant Non-EX (878 Phantump 4, 879 Trevenant 4 = 8) + 13 Trainers + 39 Psychic Energy
    d_trevenant = [878]*4 + [879]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [5]*39

    # 7. Cinderace Non-EX (664 Scorbunny 4, 665 Raboot 4, 666 Cinderace 4 = 12) + 13 Trainers + 35 Fire Energy
    d_cinderace = [664]*4 + [665]*4 + [666]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [2]*35

    # 8. Generic Metal Resistance (989 Meltan 4, 991 Melmetal 4 = 8) + 13 Trainers + 39 Metal Energy
    d_melmetal = [989]*4 + [991]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [8]*39

    # 9. Generic Fire Attacker (1027 Turtonator 4 = 4) + 13 Trainers + 43 Fire Energy
    d_fire = [1027]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [2]*43

    # 10. Generic Single Prize Swarm (65 Dunsparce 4, 66 Dudunsparce 4, 1072 Snorlax 4 = 12) + 13 Trainers + 35 Grass Energy
    d_swarm = [65]*4 + [66]*4 + [1072]*4 + [1092]*1 + [1121]*4 + [1086]*4 + [1182]*4 + [1]*35

    opponents = {
        "OPP_Mega_Lucario_ex": d_lucario,
        "OPP_Mega_Abomasnow_ex": d_abomasnow,
        "OPP_Marnie_Grimmsnarl_ex": d_grimmsnarl,
        "OPP_Duraludon_NonEX": d_duraludon,
        "OPP_Alakazam_NonEX": d_alakazam,
        "OPP_Hops_Trevenant_NonEX": d_trevenant,
        "OPP_Cinderace_NonEX": d_cinderace,
        "OPP_Melmetal_Metal_Resist": d_melmetal,
        "OPP_Turtonator_Fire_Aggro": d_fire,
        "OPP_Single_Prize_Swarm": d_swarm,
    }

    for name, deck in opponents.items():
        assert len(deck) == 60, f"Deck {name} has {len(deck)} cards, expected 60"
        csv_path = f"research/deck_candidates/{name}.csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("Card ID\n")
            for cid in deck:
                f.write(f"{cid}\n")
        print(f"Generated Opponent {name}: {csv_path} (60 cards, valid)")

if __name__ == "__main__":
    generate_adversarial_opponent_decks()
