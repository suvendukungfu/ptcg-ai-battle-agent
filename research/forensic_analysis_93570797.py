"""
Forensic Match Analyzer for Public Episode 93570797 (Candidate F).
"""

import json
import csv

def analyze_match():
    replay_path = "reports/leaderboard_optimization/public_93570797/episode-93570797-replay.json"
    with open(replay_path) as f:
        replay = json.load(f)

    # Load card names
    card_names = {}
    with open("data/EN Card Data.csv") as f:
        reader = csv.DictReader(f)
        for r in reader:
            card_names[int(r["Card ID"])] = r["Card Name"]

    steps = replay.get("steps", [])
    print(f"Total Match Steps: {len(steps)}")

    final_step = steps[-1]
    reward_0 = final_step[0].get("reward")
    reward_1 = final_step[1].get("reward")
    status_0 = final_step[0].get("status")
    status_1 = final_step[1].get("status")

    print(f"Player 0 (Opponent): Reward = {reward_0}, Status = {status_0}")
    print(f"Player 1 (Candidate F): Reward = {reward_1}, Status = {status_1}")

    if reward_1 == 1:
        outcome = "VICTORY (+1)"
    elif reward_1 == -1:
        outcome = "DEFEAT (-1)"
    else:
        outcome = f"DRAW ({reward_1})"
    print(f"\nResult: {outcome}")

    # Inspect Knockouts and Prize Events
    prev_p0_prizes = None
    prev_p1_prizes = None

    for s_idx in range(len(steps)):
        s = steps[s_idx]
        cur = s[1].get("observation", {}).get("current")
        if cur:
            c = json.loads(cur) if isinstance(cur, str) else cur
            players = c.get("players", [])
            if len(players) >= 2:
                our_p = players[c.get("yourIndex", 1)]
                opp_p = players[1 - c.get("yourIndex", 1)]
                
                our_act = our_p.get("active", [{}])[0] if (our_p.get("active") and our_p.get("active")[0]) else {}
                opp_act = opp_p.get("active", [{}])[0] if (opp_p.get("active") and opp_p.get("active")[0]) else {}
                
                our_pz = len(our_p.get("prize", []))
                opp_pz = len(opp_p.get("prize", []))
                act = s[1].get("action")

                if prev_p0_prizes != opp_pz or prev_p1_prizes != our_pz or s_idx in [5, 20, 50, 80, 100, len(steps)-1]:
                    our_act_name = card_names.get(our_act.get('id', -1), 'None')
                    opp_act_name = card_names.get(opp_act.get('id', -1), 'None')
                    print(f"Step {s_idx:3d}: Prizes (Us: {our_pz}, Opp: {opp_pz}) | Us: {our_act_name} (HP {our_act.get('hp')}/{our_act.get('maxHp')}, E: {len(our_act.get('energies', []))}) | Opp: {opp_act_name} (HP {opp_act.get('hp')}/{opp_act.get('maxHp')}, E: {len(opp_act.get('energies', []))}) | Act: {act}")
                    prev_p0_prizes = opp_pz
                    prev_p1_prizes = our_pz

if __name__ == "__main__":
    analyze_match()
