import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

with open("reports/kaggle_replays/episode-93478840-replay.json", "r") as f:
    data = json.load(f)

steps = data.get("steps", [])

print(f"Total Steps: {len(steps)}")
print("Header Info:", data.get("info", {}))
print("Rewards:", data.get("rewards", []))
print("Statuses:", data.get("statuses", []))

for step_idx, step in enumerate(steps):
    p0 = step[0]
    p1 = step[1]
    
    print(f"\n================================================================================")
    print(f"STEP {step_idx:02d} | P0 Status={p0.get('status')} | P1 Status={p1.get('status')}")
    print(f"================================================================================")
    
    active_p = 0 if p0.get("status") == "ACTIVE" else 1
    
    for p_idx, p_data in enumerate([p0, p1]):
        obs = p_data.get("observation", {})
        action = p_data.get("action")
        reward = p_data.get("reward")
        
        select = obs.get("select")
        curr = obs.get("current")
        logs = obs.get("logs", [])
        
        print(f"--- Player {p_idx} (Reward: {reward}) ---")
        if action is not None:
            print(f"  Action taken: {action}")
        if select is not None:
            sel_type = select.get("type")
            min_c = select.get("minCount")
            max_c = select.get("maxCount")
            options = select.get("option", [])
            print(f"  Select Dialog: Type={sel_type}, Range=[{min_c}, {max_c}], Options count={len(options)}")
            for o_idx, opt in enumerate(options):
                cid = opt.get("cardId")
                name = get_card_name(cid) if cid else "N/A"
                print(f"    [{o_idx}] Type={opt.get('type')}, Card={name} (ID {cid}), Pos={opt.get('pos')}, Area={opt.get('area')}")
                
        if curr is not None:
            print(f"  Current Game State (Player {p_idx} perspective):")
            print(f"    Turn={curr.get('turn')}, Current Player={curr.get('currentPlayer')}, Your Index={curr.get('yourIndex')}")
            print(f"    Your HP={curr.get('yourHp')}, Opp HP={curr.get('oppHp')}")
            print(f"    Your Prizes Remaining={curr.get('yourPrizes')}, Opp Prizes Remaining={curr.get('oppPrizes')}")
            print(f"    Your Hand Cards: {[f'{cid}:{get_card_name(cid)}' for cid in curr.get('yourHandCards', [])]}")
            print(f"    Your Active: ID={curr.get('yourActiveCardId')} ({get_card_name(curr.get('yourActiveCardId'))}), HP={curr.get('yourActiveHp')}, Energy={curr.get('yourActiveEnergies')}")
            print(f"    Your Bench: {[(cid, get_card_name(cid)) for cid in curr.get('yourBenchCardIds', [])]}")
            print(f"    Opp Active: ID={curr.get('oppActiveCardId')} ({get_card_name(curr.get('oppActiveCardId'))}), HP={curr.get('oppActiveHp')}, Energy={curr.get('oppActiveEnergies')}")
            print(f"    Opp Bench: {[(cid, get_card_name(cid)) for cid in curr.get('oppBenchCardIds', [])]}")
            print(f"    Your Discard Count={curr.get('yourTrashCount')}, Opp Discard Count={curr.get('oppTrashCount')}")
            print(f"    Your Deck Count={curr.get('yourDeckCount')}, Opp Deck Count={curr.get('oppDeckCount')}")
            
        if logs:
            print(f"  Logs ({len(logs)} events):")
            for log_ev in logs[-5:]:
                print(f"    {log_ev}")
