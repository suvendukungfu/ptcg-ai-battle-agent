import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

with open("reports/kaggle_candidate_d/public_93503836/episode-93503836-replay.json", "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])

print("=== DETAILED ACTION TRACE BY TURN ===")
for s_idx, step in enumerate(steps):
    for p_idx in (0, 1):
        p_state = step[p_idx]
        obs = p_state.get("observation") or {}
        act = p_state.get("action")
        cur = obs.get("current") or {}
        turn = cur.get("turn", 0) if isinstance(cur, dict) else 0
        sel = obs.get("select") or {}
        sel_type = sel.get("type") if isinstance(sel, dict) else None
        opts = sel.get("option", []) if isinstance(sel, dict) else []
        
        if act is not None and len(opts) > 0 and isinstance(act, list) and act:
            opt_idx = act[0]
            if opt_idx < len(opts):
                opt = opts[opt_idx]
                p_label = "OURS (P0)" if p_idx == 0 else "OPP (P1)"
                print(f"Step {s_idx:02d} | Turn {turn:02d} | {p_label} | Type={opt.get('type')}, Card={get_card_name(opt.get('id', 0)) if opt.get('id') else 'N/A'}, Target={opt.get('target')}, InPlayArea={opt.get('inPlayArea')}, Text='{opt.get('text')}'")
