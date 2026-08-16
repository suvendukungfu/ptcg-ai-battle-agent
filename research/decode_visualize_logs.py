import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

with open("reports/kaggle_replays/episode-93478840-replay.json", "r") as f:
    data = json.load(f)

steps = data.get("steps", [])

# Check if visualize data is embedded in step 0
vis = steps[0][0].get("visualize")
print("Visualize data in step 0:", type(vis), len(vis) if isinstance(vis, list) else "None")

if isinstance(vis, list):
    for idx, frame in enumerate(vis):
        print(f"\n--- Frame {idx} ---")
        print("Keys:", list(frame.keys()) if isinstance(frame, dict) else type(frame))
        if isinstance(frame, dict):
            obs = frame.get("obs", {})
            act = frame.get("action")
            print(f"Action: {act}")
            curr = obs.get("current", {})
            if curr:
                print(f"Turn: {curr.get('turn')}, Player: {curr.get('currentPlayer')}, YourIndex: {curr.get('yourIndex')}")
                print(f"Hand: {[get_card_name(c) for c in curr.get('yourHandCards', [])]}")
                print(f"Active: {get_card_name(curr.get('yourActiveCardId'))} (HP={curr.get('yourActiveHp')})")
                print(f"Bench: {[get_card_name(c) for c in curr.get('yourBenchCardIds', [])]}")
                print(f"Opp Active: {get_card_name(curr.get('oppActiveCardId'))} (HP={curr.get('oppActiveHp')})")
                print(f"Opp Bench: {[get_card_name(c) for c in curr.get('oppBenchCardIds', [])]}")
else:
    # Print the exact observation structures across steps
    for s_idx, s in enumerate(steps):
        p0_obs = s[0].get("observation", {})
        p1_obs = s[1].get("observation", {})
        print(f"Step {s_idx:02d}: P0 obs keys={list(p0_obs.keys())} | P1 obs keys={list(p1_obs.keys())}")
