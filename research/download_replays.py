import os
import subprocess
import json
import time

EPISODES = [
    93511999,
    93511069,
    93510165,
    93509250,
    93508436,
    93507460,
    93506556,
    93505666,
    93504748,
    93503836,
    93503735 # Validation
]

OUTPUT_DIR = "reports/leaderboard_optimization/replays"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_replay(episode_id):
    replay_file = f"{OUTPUT_DIR}/episode_{episode_id}.json"
    if not os.path.exists(replay_file):
        print(f"Downloading replay for {episode_id}...")
        try:
            subprocess.run(["./.venv/bin/kaggle", "competitions", "replay", str(episode_id), "-p", OUTPUT_DIR], check=True, capture_output=True)
            # rename to episode_ID.json if kaggle downloads it differently. Actually kaggle replay saves it as episode_id.json or similar.
            # Usually it saves as `episode_id.json` or `episode_id-replay.json`.
            # We'll just let kaggle save it, then rename properly.
            for f in os.listdir(OUTPUT_DIR):
                if str(episode_id) in f and f != f"episode_{episode_id}.json":
                    os.rename(os.path.join(OUTPUT_DIR, f), replay_file)
        except subprocess.CalledProcessError as e:
            print(f"Failed to download replay {episode_id}: {e.stderr.decode('utf-8', errors='ignore')}")
    else:
        print(f"Replay {episode_id} already exists.")
        
def download_logs(episode_id):
    for agent_id in [0, 1]:
        log_file = f"{OUTPUT_DIR}/episode_{episode_id}_agent_{agent_id}.log"
        if not os.path.exists(log_file):
            print(f"Downloading logs for {episode_id} agent {agent_id}...")
            try:
                res = subprocess.run(["./.venv/bin/kaggle", "competitions", "logs", str(episode_id), str(agent_id)], capture_output=True, text=True)
                if res.returncode == 0:
                    with open(log_file, "w") as f:
                        f.write(res.stdout)
            except Exception as e:
                print(f"Failed to download log {episode_id}-{agent_id}: {e}")
        else:
            print(f"Log {episode_id} agent {agent_id} already exists.")

for ep in EPISODES:
    download_replay(ep)
    download_logs(ep)
    time.sleep(1) # Rate limiting
