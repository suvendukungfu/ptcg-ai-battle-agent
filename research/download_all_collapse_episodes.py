"""
Bulk Downloader for all Candidate F Collapse Public Episodes (Episodes 11 through 19).
"""

import os
import subprocess

episodes = [
    93569861,
    93570797,
    93571687,
    93572601,
    93573491,
    93574392,
    93575313,
    93576224,
    93577146,
    93578041,
    93578958,
    93579869,
    93580784,
    93581692,
    93582613,
    93583569,
    93584447,
    93585347,
    93586267,
]

os.makedirs("reports/leaderboard_optimization/candidate_f_collapse", exist_ok=True)

for ep_id in episodes:
    ep_dir = f"reports/leaderboard_optimization/candidate_f_collapse/public_{ep_id}"
    os.makedirs(ep_dir, exist_ok=True)
    replay_file = f"{ep_dir}/episode-{ep_id}-replay.json"
    
    if not os.path.exists(replay_file):
        print(f"Downloading Replay {ep_id}...")
        subprocess.run([
            ".venv/bin/kaggle", "competitions", "replay", str(ep_id), "-p", ep_dir
        ], capture_output=True)

    for agent_idx in [0, 1]:
        log_file = f"{ep_dir}/agent-{agent_idx}-logs.json"
        if not os.path.exists(log_file):
            res = subprocess.run([
                ".venv/bin/kaggle", "competitions", "logs", str(ep_id), str(agent_idx)
            ], capture_output=True, text=True)
            if res.returncode == 0 and "403" not in res.stderr and "403" not in res.stdout:
                with open(log_file, "w") as f:
                    f.write(res.stdout)

print("All 19 episodes downloaded to candidate_f_collapse!")
