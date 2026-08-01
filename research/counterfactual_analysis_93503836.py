import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

with open("reports/kaggle_candidate_d/public_93503836/episode-93503836-replay.json", "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])

print("==================================================")
print("COUNTERFACTUAL STATE INSPECTION FOR EPISODE 93503836")
print("==================================================")

for s_idx in [44, 45, 63, 64, 79, 80]:
    step = steps[s_idx]
    p0 = step[0]
    obs = p0.get("observation") or {}
    cur = obs.get("current") or {}
    turn = cur.get("turn", 0)
    sel = obs.get("select") or {}
    opts = sel.get("option", [])
    
    players = cur.get("players") or []
    if len(players) >= 2:
        our_p = players[0] or {}
        opp_p = players[1] or {}
        
        hand = our_p.get("hand") or []
        deck_cnt = our_p.get("deckCount", 0)
        discard = our_p.get("discard") or []
        our_act = our_p.get("active", [{}])[0] if our_p.get("active") else {}
        our_bench = our_p.get("bench") or []
        
        print(f"\n--- STEP {s_idx:02d} (Turn {turn:02d}) ---")
        print(f"Hand ({len(hand)} cards): {[get_card_name(c.get('id', 0)) for c in hand]}")
        print(f"Deck Count: {deck_cnt}, Discard Count: {len(discard)}")
        print(f"Our Active: {get_card_name(our_act.get('id', 0))} (HP: {our_act.get('hp')}, E: {len(our_act.get('energies', []))})")
        print(f"Our Bench ({len(our_bench)}): {[get_card_name(b.get('id', 0)) + f'(HP:{b.get('hp')},E:{len(b.get('energies', []))})' for b in our_bench]}")
        print(f"Legal Options ({len(opts)}):")
        for oi, opt in enumerate(opts):
            print(f"  Option {oi}: type={opt.get('type')}, id={opt.get('id')} ({get_card_name(opt.get('id', 0)) if opt.get('id') else ''}), text='{opt.get('text')}'")
