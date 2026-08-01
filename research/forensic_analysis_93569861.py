"""
Forensic Match Analyzer for Public Episode 93569861 (Candidate F).
"""

import json
import os
import sys

def analyze_match():
    replay_path = "reports/leaderboard_optimization/public_93569861/episode-93569861-replay.json"
    with open(replay_path) as f:
        replay = json.load(f)

    steps = replay.get("steps", [])
    print(f"Total Match Steps: {len(steps)}")

    final_step = steps[-1]
    reward_0 = final_step[0].get("reward")
    reward_1 = final_step[1].get("reward")
    status_0 = final_step[0].get("status")
    status_1 = final_step[1].get("status")

    print(f"Player 0 (Opponent): Reward = {reward_0}, Status = {status_0}")
    print(f"Player 1 (Candidate F): Reward = {reward_1}, Status = {status_1}")

    # Determine outcome for Candidate F (Player 1)
    if reward_1 == 1:
        outcome = "VICTORY (+1)"
    elif reward_1 == -1:
        outcome = "DEFEAT (-1)"
    else:
        outcome = f"DRAW ({reward_1})"
    print(f"\nResult: {outcome}")

    # Reconstruct cards played by both players
    p0_cards_seen = set()
    p1_cards_seen = set()

    for s_idx, s in enumerate(steps):
        # Player 0
        cur_0 = s[0].get("observation", {}).get("current")
        if cur_0:
            c0 = json.loads(cur_0) if isinstance(cur_0, str) else cur_0
            for p in c0.get("players", []):
                for a in p.get("active", []):
                    if a and a.get("id"): p0_cards_seen.add(a["id"])
                for b in p.get("bench", []):
                    if b and b.get("id"): p0_cards_seen.add(b["id"])

        # Player 1 (Candidate F)
        cur_1 = s[1].get("observation", {}).get("current")
        if cur_1:
            c1 = json.loads(cur_1) if isinstance(cur_1, str) else cur_1
            for p in c1.get("players", []):
                for a in p.get("active", []):
                    if a and a.get("id"): p1_cards_seen.add(a["id"])
                for b in p.get("bench", []):
                    if b and b.get("id"): p1_cards_seen.add(b["id"])

    print("\nOpponent (P0) Cards Observed in Match:", p0_cards_seen)
    print("Candidate F (P1) Cards Observed in Match:", p1_cards_seen)

    # Turn-by-turn breakdown
    print("\n--- Key Match Milestones ---")
    prev_prizes_0 = None
    prev_prizes_1 = None
    
    for s_idx, s in enumerate(steps):
        p1_obs = s[1].get("observation", {})
        cur = p1_obs.get("current")
        if cur:
            cdata = json.loads(cur) if isinstance(cur, str) else cur
            players = cdata.get("players", [])
            if len(players) >= 2:
                our_p = players[cdata.get("yourIndex", 1)]
                opp_p = players[1 - cdata.get("yourIndex", 1)]
                
                our_prizes = len(our_p.get("prize", []))
                opp_prizes = len(opp_p.get("prize", []))
                
                our_active = our_p.get("active", [{}])[0] if our_p.get("active") else {}
                opp_active = opp_p.get("active", [{}])[0] if opp_p.get("active") else {}

                action_taken = s[1].get("action")

                if prev_prizes_0 != our_prizes or prev_prizes_1 != opp_prizes or s_idx % 20 == 0 or s_idx == len(steps) - 1:
                    print(f"Step {s_idx:3d}: Prizes (Us: {our_prizes}, Opp: {opp_prizes}) | Our Active: {our_active.get('id')} (HP {our_active.get('hp')}/{our_active.get('maxHp')}, E: {len(our_active.get('energies', []))}) | Opp Active: {opp_active.get('id')} (HP {opp_active.get('hp')}/{opp_active.get('maxHp')}, E: {len(opp_active.get('energies', []))}) | Act: {action_taken}")
                    prev_prizes_0 = our_prizes
                    prev_prizes_1 = opp_prizes

if __name__ == "__main__":
    analyze_match()
