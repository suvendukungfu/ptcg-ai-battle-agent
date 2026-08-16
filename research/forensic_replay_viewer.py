import json
import os
from agent.card_database import init_card_database, get_card_name

init_card_database()

with open("reports/kaggle_replays/episode-93478840-replay.json", "r") as f:
    data = json.load(f)

steps = data.get("steps", [])

print("==================================================================")
print(f"KAGGLE PUBLIC MATCH FORENSIC AUDIT: Episode 93478840 ({len(steps)} steps)")
print("==================================================================")

for i, step in enumerate(steps):
    p0 = step[0]
    p1 = step[1]
    
    p0_obs = p0.get("observation", {})
    p1_obs = p1.get("observation", {})
    
    active_idx = 0 if p0.get("status") == "ACTIVE" else 1
    active_player = f"P{active_idx}"
    
    curr = (p0_obs if active_idx == 0 else p1_obs).get("current") or {}
    select = (p0_obs if active_idx == 0 else p1_obs).get("select") or {}
    
    sel_type = select.get("type")
    options = select.get("option", [])
    action = p0.get("action") if active_idx == 0 else p1.get("action")
    
    p0_hp = curr.get("yourHp") if active_idx == 0 else curr.get("oppHp")
    p1_hp = curr.get("oppHp") if active_idx == 0 else curr.get("yourHp")
    
    chosen_desc = []
    if action is not None and isinstance(action, list):
        for idx in action:
            if 0 <= idx < len(options):
                opt = options[idx]
                opt_t = opt.get("type")
                card_id = opt.get("cardId")
                name = get_card_name(card_id) if card_id else f"type_{opt_t}"
                chosen_desc.append(f"[{idx}:{name}(t={opt_t})]")
            else:
                chosen_desc.append(f"[{idx}:out_of_range]")
                
    print(f"Step {i:02d} | {active_player} | SelType={sel_type} | P0(Crustle) HP={p0_hp} vs P1(Starmie) HP={p1_hp} | Action={action} -> {' '.join(chosen_desc)}")
