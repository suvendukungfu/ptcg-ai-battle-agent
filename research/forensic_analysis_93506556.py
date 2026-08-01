import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

replay_path = "reports/kaggle_candidate_d/public_93506556/episode-93506556-replay.json"
with open(replay_path, "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])
print(f"Total Steps: {len(steps)}")

# Identify players
last_step = steps[-1]
p0 = last_step[0]
p1 = last_step[1]

vis0 = steps[0][0].get("visualize", [])
p0_deck = vis0[0]["action"][0] if vis0 else []
p1_deck = vis0[0]["action"][1] if vis0 else []

p0_counts = Counter(p0_deck)
p1_counts = Counter(p1_deck)

is_p0_ours = (344 in p0_counts and 345 in p0_counts)
is_p1_ours = (344 in p1_counts and 345 in p1_counts)

our_idx = 0 if is_p0_ours else 1
opp_idx = 1 if is_p0_ours else 0

print(f"Our Player Index: Player {our_idx}")
print(f"Opponent Player Index: Player {opp_idx}")

our_stat = last_step[our_idx].get("status")
our_rew = last_step[our_idx].get("reward")
opp_stat = last_step[opp_idx].get("status")
opp_rew = last_step[opp_idx].get("reward")

print(f"Our Result: Status={our_stat}, Reward={our_rew} -> {'WIN (+1.0)' if our_rew == 1 else 'LOSS (-1.0)' if our_rew == -1 else 'TIE (0.0)'}")
print(f"Opponent Result: Status={opp_stat}, Reward={opp_rew}")

# Opponent Deck
opp_deck = p0_deck if our_idx == 1 else p1_deck
opp_counts = Counter(opp_deck)
print("\nOpponent Deck Composition:")
for cid, cnt in opp_counts.items():
    cname = get_card_name(cid)
    card = get_card(cid)
    is_ex = card and (card.get("ex") or card.get("megaEx"))
    tag = " [EX]" if is_ex else ""
    print(f"  ID {cid:4d} (x{cnt:02d}): {cname}{tag}")

# Step by Step Trace
print("\n=== STEP BY STEP TRACE ===")
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
        
        our_bench_str = [get_card_name((b or {}).get('id', 0)) + f"(HP:{(b or {}).get('hp')},E:{len((b or {}).get('energies', []))})" for b in our_bench]
        opp_bench_str = [get_card_name((b or {}).get('id', 0)) + f"(HP:{(b or {}).get('hp')},E:{len((b or {}).get('energies', []))})" for b in opp_bench]
        
        if act is not None or sel_type is not None or s_idx in (0, 1, len(steps)-1):
            print(f"Step {s_idx:02d} | Turn {turn:02d} | select_type={sel_type} | {chosen_desc}")
            print(f"  OUR (P{our_idx}): Active={get_card_name(our_act.get('id', 0))} (HP: {our_act.get('hp')}/{our_act.get('maxHp', 0)}, E: {len(our_act.get('energies', []))}) | Bench ({len(our_bench)}): {our_bench_str} | Prizes={our_prizes} | Deck={our_deck_cnt}")
            print(f"  OPP (P{opp_idx}): Active={get_card_name(opp_act.get('id', 0))} (HP: {opp_act.get('hp')}/{opp_act.get('maxHp', 0)}, E: {len(opp_act.get('energies', []))}) | Bench ({len(opp_bench)}): {opp_bench_str} | Prizes={opp_prizes} | Deck={opp_deck_cnt}")
            print("-" * 80)
