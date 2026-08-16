import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

with open("reports/kaggle_replays/episode-93479756-replay.json", "r") as f:
    data = json.load(f)

steps = data.get("steps", [])
info = data.get("info", {})
rewards = data.get("rewards", [])
statuses = data.get("statuses", [])

print("==================================================================")
print(f"ANALYSIS OF KAGGLE EPISODE 93479756 ({len(steps)} Steps)")
print("==================================================================")
print(f"Info: {info}")
print(f"Rewards: {rewards}")
print(f"Statuses: {statuses}")

# Frame 0 / Initial Step Decks
p0_deck = steps[0][0].get("action")
p1_deck = steps[0][1].get("action")

if not p0_deck and len(steps) > 1:
    p0_deck = steps[1][0].get("action")
    p1_deck = steps[1][1].get("action")

print("\n--- Decks Submitted ---")
print(f"Player 0 Deck ({len(p0_deck) if p0_deck else 0} cards):")
counts_p0 = Counter(p0_deck if p0_deck else [])
for cid, cnt in counts_p0.items():
    print(f"  ID {cid:4d} (x{cnt:02d}): {get_card_name(cid)}")

print(f"\nPlayer 1 Deck ({len(p1_deck) if p1_deck else 0} cards):")
counts_p1 = Counter(p1_deck if p1_deck else [])
for cid, cnt in counts_p1.items():
    print(f"  ID {cid:4d} (x{cnt:02d}): {get_card_name(cid)}")

# Determine our player index
is_p0_our = 345 in counts_p0 or 344 in counts_p0
is_p1_our = 345 in counts_p1 or 344 in counts_p1
our_player_idx = 0 if is_p0_our else (1 if is_p1_our else -1)
print(f"\nOur Submission 55540242 Player Index: Player {our_player_idx}")
print(f"Outcome: {'WIN (+1)' if rewards[our_player_idx] == 1 else ('LOSS (-1)' if rewards[our_player_idx] == -1 else 'TIE (0)')}")

vis = steps[0][0].get("visualize")
print(f"Total Visualizer Frames: {len(vis) if vis else 'None'}")

if vis:
    for idx, frame in enumerate(vis):
        action = frame.get("action")
        select = frame.get("select") or {}
        selected = frame.get("selected")
        logs = frame.get("logs") or []
        curr = frame.get("obs", {}).get("current", {})
        
        act_desc = f"P0: {action[0]} | P1: {action[1]}" if action else "None"
        sel_t = select.get("type")
        options = select.get("option") or []
        
        print(f"\n{'='*75}")
        print(f"FRAME {idx:02d} | Action: {act_desc} | Selected: {selected} | Select Type: {sel_t}")
        print(f"{'='*75}")
        
        if options:
            print(f"  Options Available ({len(options)}):")
            for oi, opt in enumerate(options):
                cid = opt.get("cardId")
                cname = get_card_name(cid) if cid else "N/A"
                print(f"    [{oi}] Type={opt.get('type')}, Card={cname} (ID {cid}), Pos={opt.get('pos')}, Area={opt.get('area')}")
                
        if logs:
            print(f"  Game Engine Logs ({len(logs)}):")
            for log in logs:
                print(f"    • {log}")
