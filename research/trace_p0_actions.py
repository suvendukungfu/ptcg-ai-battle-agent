import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

with open("reports/kaggle_candidate_b/public_93482398/episode-93482398-replay.json", "r") as f:
    d = json.load(f)

vis = d["steps"][0][0]["visualize"]

print(f"Total Visualizer Frames: {len(vis)}")

for idx, frame in enumerate(vis):
    action = frame.get("action")
    select = frame.get("select") or {}
    selected = frame.get("selected")
    logs = frame.get("logs") or []
    
    p0_act = action[0] if action else []
    p1_act = action[1] if action else []
    
    if p0_act:  # Player 0 (Our Agent) action frame
        print(f"\n===========================================================================")
        print(f"FRAME {idx:02d} | OUR AGENT (P0) ACTION: {p0_act} | Select Type: {select.get('type')} | Context: {select.get('context')}")
        print(f"===========================================================================")
        options = select.get("option") or []
        for oi, opt in enumerate(options):
            cid = opt.get("cardId")
            cname = get_card_name(cid) if cid else "N/A"
            print(f"  Option [{oi}]: Type={opt.get('type')}, Card={cname} (ID {cid}), Pos={opt.get('pos')}, Area={opt.get('area')}")
            
        if logs:
            print("  Logs:")
            for l in logs:
                print(f"    • {l}")
