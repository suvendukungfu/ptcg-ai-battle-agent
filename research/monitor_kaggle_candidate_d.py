import json
import time
import subprocess
import sys
import os
from collections import Counter
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card

init_card_database()

SUBMISSION_ID = 55542011

def extract_json_array(text: str) -> List[Dict[str, Any]]:
    text = text.strip()
    s = text.find("[")
    e = text.rfind("]")
    if s != -1 and e != -1 and e > s:
        try:
            return json.loads(text[s:e+1])
        except Exception as ex:
            print(f"Slice parse error: {ex}")
    return []

def get_episodes() -> List[Dict[str, Any]]:
    cmd = [".venv/bin/kaggle", "competitions", "episodes", str(SUBMISSION_ID), "--format", "json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching episodes: {res.stderr}")
        return []
    return extract_json_array(res.stdout)

def get_submission_info() -> Dict[str, Any]:
    cmd = [".venv/bin/kaggle", "competitions", "submissions", "pokemon-tcg-ai-battle", "--format", "json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {}
    subs = extract_json_array(res.stdout)
    for s in subs:
        if s.get("ref") == SUBMISSION_ID:
            return s
    return {}

def download_and_process_episode(ep_id: int):
    out_dir = f"reports/kaggle_candidate_d/public_{ep_id}"
    os.makedirs(out_dir, exist_ok=True)
    
    replay_file = os.path.join(out_dir, f"episode-{ep_id}-replay.json")
    if not os.path.exists(replay_file):
        print(f"Downloading replay for Episode {ep_id}...")
        subprocess.run([".venv/bin/kaggle", "competitions", "replay", str(ep_id), "-p", out_dir])
        
    for p in (0, 1):
        log_file = os.path.join(out_dir, f"agent-{p}-logs.json")
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                subprocess.run([".venv/bin/kaggle", "competitions", "logs", str(ep_id), str(p)], stdout=f, stderr=subprocess.DEVNULL)
                
    # Run analysis
    if os.path.exists(replay_file):
        with open(replay_file, "r") as f:
            replay = json.load(f)
        steps = replay.get("steps", [])
        last_step = steps[-1]
        
        vis0 = steps[0][0].get("visualize", [])
        p0_deck = vis0[0]["action"][0] if vis0 else []
        p1_deck = vis0[0]["action"][1] if vis0 else []
        
        is_p0_ours = (344 in p0_deck and 345 in p0_deck)
        our_idx = 0 if is_p0_ours else 1
        opp_idx = 1 if is_p0_ours else 0
        
        our_rew = last_step[our_idx].get("reward")
        our_stat = last_step[our_idx].get("status")
        
        opp_deck = p0_deck if our_idx == 1 else p1_deck
        opp_counts = Counter(opp_deck)
        
        has_ex = any(get_card(cid) and (get_card(cid).get("ex") or get_card(cid).get("megaEx")) for cid in opp_counts)
        opp_pkmn = [get_card_name(cid) for cid in opp_counts if get_card(cid) and get_card(cid).get("cardType") == 0]
        
        print(f"\nEpisode {ep_id}: Result={'WIN (+1.0)' if our_rew == 1 else 'LOSS (-1.0)' if our_rew == -1 else 'TIE (0.0)'} | Steps={len(steps)} | EX={has_ex} | Opponent={', '.join(opp_pkmn[:4])}")

if __name__ == "__main__":
    print(f"Checking episodes for Submission {SUBMISSION_ID}...")
    episodes = get_episodes()
    sub_info = get_submission_info()
    print(f"Current Public Score: {sub_info.get('publicScore', 'Unknown')}")
    print(f"Found {len(episodes)} total episodes:")
    for ep in episodes:
        print(f"  ID {ep.get('id')} | Type: {ep.get('type')} | Created: {ep.get('createTime')}")
        if ep.get("type") == "EpisodeType.EPISODE_TYPE_PUBLIC":
            download_and_process_episode(ep.get("id"))
