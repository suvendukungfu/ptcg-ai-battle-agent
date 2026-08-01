import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

with open("reports/kaggle_candidate_d/public_93504748/episode-93504748-replay.json", "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])
print(f"=== EPISODE 93504748 STEP TRACE ({len(steps)} STEPS) ===")

our_idx = 1
opp_idx = 0

for s_idx, step in enumerate(steps):
    our_state = step[our_idx]
    opp_state = step[opp_idx]
    
    obs = our_state.get("observation") or {}
    act = our_state.get("action")
    cur = obs.get("current") or {}
    turn = cur.get("turn", 0) if isinstance(cur, dict) else 0
    sel = obs.get("select") or {}
    sel_type = sel.get("type") if isinstance(sel, dict) else None
    opts = sel.get("option", []) if isinstance(sel, dict) else []
    
    chosen_desc = ""
    if act is not None:
        if isinstance(act, list) and act and act[0] < len(opts):
            o = opts[act[0]]
            chosen_desc = f"Action {act} -> Type {o.get('type')}: {o.get('text', '')}"
        else:
            chosen_desc = f"Action {act}"
            
    players = cur.get("players") or []
    if len(players) >= 2:
        our_p = players[our_idx] or {}
        opp_p = players[opp_idx] or {}
        
        our_act = our_p.get("active", [{}])[0] if our_p.get("active") else {}
        our_act = our_act or {}
        our_bench = our_p.get("bench") or []
        our_prizes = len(our_p.get("prize", [])) if isinstance(our_p.get("prize"), list) else our_p.get("prize", 0)
        our_deck_cnt = our_p.get("deckCount", 0)
        
        opp_act = opp_p.get("active", [{}])[0] if opp_p.get("active") else {}
        opp_act = opp_act or {}
        opp_bench = opp_p.get("bench") or []
        opp_prizes = len(opp_p.get("prize", [])) if isinstance(opp_p.get("prize"), list) else opp_p.get("prize", 0)
        opp_deck_cnt = opp_p.get("deckCount", 0)
        
        our_bench_str = [get_card_name((b or {}).get('id', 0)) for b in our_bench]
        opp_bench_str = [get_card_name((b or {}).get('id', 0)) for b in opp_bench]
        
        print(f"Step {s_idx:02d} | Turn {turn:02d} | select_type={sel_type} | {chosen_desc}")
        print(f"  OUR (P1): Active={get_card_name(our_act.get('id', 0))} (HP: {our_act.get('hp')}/{our_act.get('maxHp', 0)}, E: {len(our_act.get('energies', []))}) | Bench ({len(our_bench)}): {our_bench_str} | Prizes={our_prizes} | Deck={our_deck_cnt}")
        print(f"  OPP (P0): Active={get_card_name(opp_act.get('id', 0))} (HP: {opp_act.get('hp')}/{opp_act.get('maxHp', 0)}, E: {len(opp_act.get('energies', []))}) | Bench ({len(opp_bench)}): {opp_bench_str} | Prizes={opp_prizes} | Deck={opp_deck_cnt}")
        print("-" * 80)
