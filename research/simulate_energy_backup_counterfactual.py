import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.state import GameState, parse_game_state
from agent.policy import rank_energy_attachment_options
from agent.card_database import init_card_database

init_card_database()

print("==================================================================")
print("ENERGY ATTACHMENT POLICY COUNTERFACTUAL AUDIT")
print("==================================================================")

# Scenario: Active Crustle has 2 Energies (attack-ready: 120 dmg).
# Bench has Benched Crustle with 0 Energies.
# Hand has Basic Grass Energy.
obs = {
    "select": {
        "type": 0,
        "minCount": 1,
        "maxCount": 1,
        "option": [
            {"type": 8, "inPlayArea": 4, "inPlayIndex": 0, "text": "Attach Energy to Active Crustle (has 2 energies)"}, # Option 0
            {"type": 8, "inPlayArea": 5, "inPlayIndex": 0, "text": "Attach Energy to Benched Crustle (has 0 energies)"}, # Option 1
            {"type": 7, "text": "Attack with Active Crustle"},                                                         # Option 2
            {"type": 14, "text": "Pass Turn"},                                                                         # Option 3
        ]
    },
    "current": {
        "yourIndex": 0,
        "turn": 4,
        "players": [
            {
                "active": [{"id": 345, "hp": 130, "energies": [1, 1]}], # 2 ENERGIES (ATTACK READY)
                "bench": [{"id": 345, "hp": 130, "energies": []}],     # 0 ENERGIES (BACKUP ATTACKER)
                "hand": [{"id": 1}],
                "prize": [1, 2, 3, 4, 5, 6],
                "discard": []
            },
            {
                "active": [{"id": 678, "hp": 260, "energies": [6, 6]}],
                "bench": [{"id": 674, "hp": 140, "energies": [6, 6, 6]}], # HARIYAMA POWERING UP
                "hand": 4,
                "prize": [1, 2, 3, 4, 5, 6],
                "discard": []
            }
        ]
    }
}

state = parse_game_state(obs)
ranks = rank_energy_attachment_options(state)
print("Energy Attachment Ranks for Candidate B:")
for idx, score in ranks:
    print(f"  Option {idx} ({obs['select']['option'][idx]['text']}): Score = {score:.1f}")

best_opt = ranks[0][0]
print(f"\nPreferred Attachment: Option {best_opt} -> '{obs['select']['option'][best_opt]['text']}'")
