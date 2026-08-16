import json
import os

def analyze_replay(file_path):
    print(f"\n=======================================================")
    print(f"ANALYZING KAGGLE REPLAY: {os.path.basename(file_path)}")
    print(f"=======================================================")
    
    with open(file_path, "r") as f:
        data = json.load(f)
    
    print("Keys:", list(data.keys()) if isinstance(data, dict) else f"List length: {len(data)}")
    
    steps = data.get("steps", data if isinstance(data, list) else [])
    print(f"Total Steps in Episode: {len(steps)}")
    
    if not steps:
        return
        
    initial_step = steps[0]
    final_step = steps[-1]
    
    print("\nInitial State (Turn 0):")
    for idx, player_state in enumerate(initial_step):
        action = player_state.get("action")
        status = player_state.get("status")
        deck_len = len(action) if isinstance(action, list) else (action if action is not None else "None")
        print(f"  Player {idx}: Status={status}, Deck Submitted={deck_len} cards")
        
    print("\nFinal State (Game Outcome):")
    for idx, player_state in enumerate(final_step):
        status = player_state.get("status")
        reward = player_state.get("reward")
        print(f"  Player {idx}: Status={status}, Reward={reward}")
        
    # Check agents / specification
    if "agents" in data:
        print("\nAgents:")
        for idx, agent in enumerate(data.get("agents", [])):
            print(f"  Player {idx}: {agent}")

    print("\nAction Timeline (First 12 Steps):")
    for i, step in enumerate(steps[:12]):
        act_0 = step[0].get("action")
        stat_0 = step[0].get("status")
        act_1 = step[1].get("action")
        stat_1 = step[1].get("status")
        print(f"  Step {i:02d}: P0[{stat_0}] Action={act_0} | P1[{stat_1}] Action={act_1}")

if __name__ == "__main__":
    p_val = "reports/kaggle_replays/episode-93477872-replay.json"
    p_pub = "reports/kaggle_replays/episode-93478840-replay.json"
    
    if os.path.exists(p_val):
        analyze_replay(p_val)
    if os.path.exists(p_pub):
        analyze_replay(p_pub)
