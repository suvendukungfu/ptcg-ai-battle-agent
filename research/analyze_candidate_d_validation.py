import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

with open("reports/kaggle_candidate_d/episode-93503735-replay.json", "r") as f:
    replay = json.load(f)

steps = replay.get("steps", [])
print(f"Total Steps: {len(steps)}")

last_step = steps[-1]
p0 = last_step[0]
p1 = last_step[1]

print(f"Player 0: Status={p0.get('status')}, Reward={p0.get('reward')}")
print(f"Player 1: Status={p1.get('status')}, Reward={p1.get('reward')}")

vis = steps[0][0].get("visualize", [])
p0_deck = vis[0]["action"][0] if vis else []
p1_deck = vis[0]["action"][1] if vis else []

print("\nPlayer 0 (Our Agent) Deck Sample:")
for cid, cnt in Counter(p0_deck).items():
    print(f"  ID {cid:4d} (x{cnt:02d}): {get_card_name(cid)}")

print("\nPlayer 1 (Opponent) Deck Sample:")
for cid, cnt in Counter(p1_deck).items():
    print(f"  ID {cid:4d} (x{cnt:02d}): {get_card_name(cid)}")

# Check agent logs
with open("reports/kaggle_candidate_d/episode-93503735-agent-0-logs.json", "r") as f:
    agent_logs = json.load(f)

print(f"\nAgent Logs Size: {len(agent_logs)} lines")
err_lines = [l for l in agent_logs if "error" in l.lower() or "exception" in l.lower() or "traceback" in l.lower()]
print(f"Error / Exception Lines in Log: {len(err_lines)}")
if err_lines:
    print("Sample error:", err_lines[:3])

print("\n=== VALIDATION OUTCOME ===")
if p0.get("reward") == 1 and p0.get("status") == "DONE":
    print("RESULT: VALIDATION VICTORY (Reward: 1.0, Status: DONE)")
else:
    print(f"RESULT: Status={p0.get('status')}, Reward={p0.get('reward')}")
