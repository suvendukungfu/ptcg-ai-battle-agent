import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

with open("reports/kaggle_replays/episode-93478840-replay.json", "r") as f:
    data = json.load(f)

vis = data["steps"][0][0]["visualize"]

AREA_NAMES = {
    0: "Deck",
    1: "Hand",
    2: "Active",
    3: "Discard/Trash",
    4: "Bench",
    5: "Side/Prizes",
    6: "LostZone",
    7: "Stadium",
    8: "AttachedEnergy",
}

LOG_TYPE_NAMES = {
    0: "Turn/Phase/Action Marker",
    1: "Draw Card",
    2: "Play Card",
    3: "Attach Energy",
    4: "Attack",
    5: "Ability/Skill",
    6: "Move Card",
    7: "Shuffle",
    8: "Coin Flip",
    9: "Damage Dealt",
    10: "Heal",
    11: "Special Effect",
    12: "Retreat",
    13: "Knockout",
}

print(f"Total Visualizer Frames: {len(vis)}")

for idx, frame in enumerate(vis):
    action = frame.get("action")
    select = frame.get("select") or {}
    selected = frame.get("selected")
    logs = frame.get("logs") or []
    
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
            lt = log.get("type")
            pid = log.get("playerIndex")
            cid = log.get("cardId")
            cname = get_card_name(cid) if cid else ""
            from_a = AREA_NAMES.get(log.get("fromArea"), log.get("fromArea"))
            to_a = AREA_NAMES.get(log.get("toArea"), log.get("toArea"))
            dmg = log.get("damage")
            
            detail = f"P{pid} | Type {lt} ({LOG_TYPE_NAMES.get(lt, 'Unknown')})"
            if cid:
                detail += f" | Card: {cname} (ID {cid})"
            if from_a is not None or to_a is not None:
                detail += f" | From: {from_a} -> To: {to_a}"
            if dmg is not None:
                detail += f" | Damage: {dmg}"
            print(f"    • {detail} -> raw: {log}")
