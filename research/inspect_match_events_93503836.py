import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

with open("reports/kaggle_candidate_d/public_93503836/episode-93503836-replay.json", "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])

print("=== GAME PLAY EVENT LOG (EPISODE 93503836) ===")

for s_idx, step in enumerate(steps):
    for p_idx in (0, 1):
        p_state = step[p_idx]
        vis_list = p_state.get("visualize") or []
        for v in vis_list:
            v_type = v.get("type")
            v_data = v.get("data")
            p_label = "OURS (P0)" if p_idx == 0 else "OPP (P1)"
            
            # Format event description
            if v_type == "playCard":
                cid = v_data.get("card", {}).get("id") if isinstance(v_data.get("card"), dict) else v_data.get("card")
                print(f"Step {s_idx:02d} | {p_label} | PLAY CARD: {get_card_name(cid)} (ID: {cid})")
            elif v_type == "attack":
                atk_name = v_data.get("name")
                dmg = v_data.get("damage")
                print(f"Step {s_idx:02d} | {p_label} | ATTACK: '{atk_name}' -> Dealt {dmg} damage")
            elif v_type == "knockout":
                tgt = v_data.get("target")
                print(f"Step {s_idx:02d} | {p_label} | KNOCKOUT on {tgt}")
            elif v_type == "drawPrize":
                print(f"Step {s_idx:02d} | {p_label} | TOOK PRIZE")
            elif v_type == "ability":
                ab_name = v_data.get("name")
                print(f"Step {s_idx:02d} | {p_label} | ABILITY: '{ab_name}'")
            elif v_type == "energyAttach":
                print(f"Step {s_idx:02d} | {p_label} | ATTACH ENERGY to {v_data.get('target')}")
