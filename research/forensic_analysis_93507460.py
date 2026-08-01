import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

replay_path = "reports/kaggle_candidate_d/public_93507460/episode-93507460-replay.json"
with open(replay_path, "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])
print(f"Total Steps: {len(steps)}")

# Identify players
last_step = steps[-1]
vis0 = steps[0][0].get("visualize", [])
p0_deck = vis0[0]["action"][0] if vis0 else []
p1_deck = vis0[0]["action"][1] if vis0 else []

p0_counts = Counter(p0_deck)
is_p0_ours = (344 in p0_counts and 345 in p0_counts)
our_idx = 0 if is_p0_ours else 1
opp_idx = 1 if is_p0_ours else 0

print(f"Our Player Index: Player {our_idx}")
print(f"Opponent Player Index: Player {opp_idx}")

our_rew = last_step[our_idx].get("reward")
our_stat = last_step[our_idx].get("status")
print(f"Result: {our_stat}, Reward={our_rew}")

opp_deck = p0_deck if our_idx == 1 else p1_deck
opp_counts = Counter(opp_deck)
print("\nOpponent Deck Composition:")
for cid, cnt in opp_counts.items():
    cname = get_card_name(cid)
    card = get_card(cid)
    is_ex = card and (card.get("ex") or card.get("megaEx"))
    tag = " [EX]" if is_ex else ""
    print(f"  ID {cid:4d} (x{cnt:02d}): {cname}{tag}")

# Critical Turns
for s_idx in range(0, len(steps), 5):
    step = steps[s_idx]
    obs = step[our_idx].get("observation") or {}
    cur = obs.get("current") or {}
    turn = cur.get("turn", 0) if isinstance(cur, dict) else 0
    players = cur.get("players") or []
    if len(players) >= 2:
        our_p = players[our_idx] or {}
        opp_p = players[opp_idx] or {}
        our_act = (our_p.get("active") or [{}])[0] or {}
        opp_act = (opp_p.get("active") or [{}])[0] or {}
        print(f"Step {s_idx:02d} | Turn {turn:02d} | Our Active: {get_card_name(our_act.get('id', 0))} (HP:{our_act.get('hp')}, E:{len(our_act.get('energies', []))}) | Opp Active: {get_card_name(opp_act.get('id', 0))} (HP:{opp_act.get('hp')}, E:{len(opp_act.get('energies', []))}) | Prizes: {len(our_p.get('prize', []))} vs {len(opp_p.get('prize', []))}")
