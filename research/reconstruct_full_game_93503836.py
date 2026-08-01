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
print("EPISODE 93503836 COMPLETE TURN-BY-TURN RECONSTRUCTION")
print("==================================================")

for s_idx, step in enumerate(steps):
    p0 = step[0]
    p1 = step[1]
    
    # Check if there are log events in visualize
    v0 = p0.get("visualize", [])
    if v0:
        for item in v0:
            obs = item.get("obs") or {}
            cur = obs.get("current") or {}
            logs = item.get("logs", [])
            turn = cur.get("turn", 0)
            
            players = cur.get("players") or []
            p0_data = players[0] if len(players) > 0 and players[0] else {}
            p1_data = players[1] if len(players) > 1 and players[1] else {}
            
            p0_act = p0_data.get("active", [{}])[0] if p0_data.get("active") else {}
            p0_act = p0_act or {}
            p0_bench = p0_data.get("bench") or []
            p0_prizes = len(p0_data.get("prize", [])) if isinstance(p0_data.get("prize"), list) else p0_data.get("prize", 0)
            
            p1_act = p1_data.get("active", [{}])[0] if p1_data.get("active") else {}
            p1_act = p1_act or {}
            p1_bench = p1_data.get("bench") or []
            p1_prizes = len(p1_data.get("prize", [])) if isinstance(p1_data.get("prize"), list) else p1_data.get("prize", 0)
            
            # Print significant events
            event_strs = []
            for l in logs:
                l_type = l.get("type")
                if l_type == "PlayCard":
                    cid = l.get("cardId")
                    event_strs.append(f"PlayCard({get_card_name(cid)})")
                elif l_type == 15: # Attack
                    event_strs.append(f"Attack(cardId={get_card_name(l.get('cardId'))}, attackId={l.get('attackId')})")
                elif l_type == 16: # Damage
                    event_strs.append(f"Damage(target={get_card_name(l.get('cardId'))}, val={l.get('value')})")
                elif l_type == "MoveCard":
                    event_strs.append(f"MoveCard({get_card_name(l.get('cardId'))} fromArea={l.get('fromArea')} toArea={l.get('toArea')})")
                elif l_type == "Result":
                    event_strs.append(f"GameResult({l.get('result')}, reason={l.get('reason')})")
                    
            if event_strs:
                print(f"\nStep {s_idx:02d} | Turn {turn:02d} | Active Player: P{cur.get('yourIndex')}")
                print(f"  Events: {', '.join(event_strs)}")
                print(f"  Our Board: Active={get_card_name(p0_act.get('id', 0))} (HP: {p0_act.get('hp')}/{p0_act.get('maxHp', 0)}, E: {len(p0_act.get('energies', []))}) | Bench ({len(p0_bench)}): {[get_card_name((b or {}).get('id', 0)) for b in p0_bench]} | Prizes={p0_prizes}")
                print(f"  Opp Board: Active={get_card_name(p1_act.get('id', 0))} (HP: {p1_act.get('hp')}/{p1_act.get('maxHp', 0)}, E: {len(p1_act.get('energies', []))}) | Bench ({len(p1_bench)}): {[get_card_name((b or {}).get('id', 0)) for b in p1_bench]} | Prizes={p1_prizes}")
