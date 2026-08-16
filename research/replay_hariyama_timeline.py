import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

with open("reports/kaggle_candidate_b/public_93482398/episode-93482398-replay.json", "r") as f:
    d = json.load(f)

vis = d["steps"][0][0]["visualize"]

print("==================================================================")
print("HARIYAMA LOSS TIMELINE & COUNTERPLAY AUDIT (Episode 93482398)")
print("==================================================================")

for i, fr in enumerate(vis):
    logs = fr.get("logs") or []
    act = fr.get("action")
    sel = fr.get("select") or {}
    
    # Check for Makuhita (673), Hariyama (674), Mega Lucario ex (678)
    for l in logs:
        lt = l.get("type")
        cid = l.get("cardId")
        p = l.get("playerIndex")
        
        if cid in (673, 674, 678, 1262, 1145, 1121) or lt in ("Evolve", "Attack", "HpChange", "Result"):
            cname = get_card_name(cid) if cid else ""
            if p == 1 or lt in ("HpChange", "Result") or (p == 0 and cid in (1262, 1145, 1121)):
                print(f"Frame {i:02d} | P{p} {lt}: {cname} (ID {cid}) -> {l}")
