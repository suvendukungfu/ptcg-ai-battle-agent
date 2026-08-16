import sys
import os

sys.path.insert(0, os.path.abspath("."))
import main
from agent.state import parse_game_state
from agent.action_selector import select_action, select_heuristic_action
from agent.policy import rank_card_play_options, rank_discard_options

print("==================================================================")
print("REPRODUCING EXACT KAGGLE EPISODE 93478840 FAILURE SCENARIO")
print("==================================================================")

# Scenario: Player 0 Turn 1
# Active Dwebble (60 HP), 0 Bench
# Hand: Dwebble (344), Ultra Ball (1121), Ultra Ball (1121), Lillie (1227), Grass Energy (1)
options_main = [
    {"type": 1, "id": 344, "text": "Play Dwebble to Bench"},       # Option 0
    {"type": 0, "id": 1121, "text": "Play Ultra Ball #1"},          # Option 1
    {"type": 0, "id": 1121, "text": "Play Ultra Ball #2"},          # Option 2
    {"type": 0, "id": 1227, "text": "Play Lillie's Determination"}, # Option 3
    {"type": 14, "text": "Pass Turn"},                             # Option 4
]

obs_main = {
    "select": {
        "type": 0,
        "minCount": 1,
        "maxCount": 1,
        "option": options_main
    },
    "current": {
        "yourIndex": 0,
        "turn": 1,
        "players": [
            {
                "active": [{"id": 344, "hp": 60, "energies": []}],
                "bench": [],  # ZERO BENCH
                "hand": [{"id": 344}, {"id": 1121}, {"id": 1121}, {"id": 1227}, {"id": 1}],
                "prize": [1, 2, 3, 4, 5, 6],
                "discard": []
            },
            {
                "active": [{"id": 666, "hp": 120, "energies": []}],
                "bench": [{"id": 1030, "hp": 60, "energies": []}],
                "hand": 5,
                "prize": [1, 2, 3, 4, 5, 6],
                "discard": []
            }
        ]
    }
}

state = parse_game_state(obs_main)
ranks = rank_card_play_options(state)
print("1. Main Phase Ranked Options:")
for idx, score in ranks:
    print(f"   Option {idx} ({options_main[idx]['text']}): Score = {score:.1f}")

chosen_action = select_action(obs_main)
print(f"\n2. Agent Chosen Action: {chosen_action} -> '{options_main[chosen_action[0]]['text']}'")
assert chosen_action == [0], f"Expected [0] (Play Dwebble to Bench), got {chosen_action}"
print("   -> VERIFIED: Candidate B prioritizes BENCHING Dwebble before playing Ultra Ball!")

# Scenario 2: Discard payment with Dwebble, Energy, Lillie in hand when Bench = 0
options_discard = [
    {"id": 344, "text": "Dwebble (Basic)"},           # Option 0
    {"id": 1, "text": "Grass Energy"},                 # Option 1
    {"id": 1, "text": "Grass Energy"},                 # Option 2
    {"id": 1227, "text": "Lillie's Determination"},    # Option 3
]

obs_discard = {
    "select": {
        "type": 1,
        "context": "Discard",
        "minCount": 2,
        "maxCount": 2,
        "option": options_discard
    },
    "current": {
        "yourIndex": 0,
        "turn": 1,
        "players": [
            {
                "active": [{"id": 344, "hp": 60, "energies": []}],
                "bench": [],  # ZERO BENCH
                "hand": options_discard,
                "prize": [1, 2, 3, 4, 5, 6],
                "discard": []
            },
            {
                "active": [{"id": 666, "hp": 120, "energies": []}],
                "bench": [],
                "hand": 5,
                "prize": [1, 2, 3, 4, 5, 6],
                "discard": []
            }
        ]
    }
}

state_discard = parse_game_state(obs_discard)
discard_ranks = rank_discard_options(options_discard, state_discard)
print("\n3. Discard Phase Ranked Options:")
for idx, score in discard_ranks:
    print(f"   Option {idx} ({options_discard[idx]['text']}): Score = {score:.1f}")

chosen_discard = select_action(obs_discard)
print(f"\n4. Agent Chosen Discard: {chosen_discard} -> {[options_discard[i]['text'] for i in chosen_discard]}")
assert 0 not in chosen_discard, f"Dwebble (Option 0) was erroneously chosen for discard: {chosen_discard}"
print("   -> VERIFIED: Candidate B PROTECTS the Basic Pokemon from being discarded!")

print("\n==================================================================")
print("REPRODUCTION SCENARIO PASSED 100% PERFECTLY!")
print("==================================================================")
