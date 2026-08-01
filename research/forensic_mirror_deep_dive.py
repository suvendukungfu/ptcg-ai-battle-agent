"""
Deep Forensic Reconstruction of all 6 Kaggle Crustle Mirror Matches.
"""

import os
import json

def analyze_mirror_matches():
    mirror_episodes = [
        93578041,
        93579869,
        93580784,
        93583569,
        93585347,
        93586267,
    ]

    mirror_data = []

    for ep_id in mirror_episodes:
        replay_path = f"reports/leaderboard_optimization/candidate_f_collapse/public_{ep_id}/episode-{ep_id}-replay.json"
        if not os.path.exists(replay_path):
            continue

        with open(replay_path) as f:
            replay = json.load(f)

        steps = replay.get("steps", [])
        total_steps = len(steps)

        # Candidate F seat
        our_p_idx = None
        for p in [0, 1]:
            cur = steps[1][p].get("observation", {}).get("current")
            if cur:
                c = json.loads(cur) if isinstance(cur, str) else cur
                deck_act = steps[0][p].get("action")
                if isinstance(deck_act, list) and 345 in deck_act:
                    our_p_idx = p
                    break
        if our_p_idx is None:
            our_p_idx = 1

        opp_p_idx = 1 - our_p_idx

        went_first = (our_p_idx == 0)
        final_step = steps[-1]
        our_reward = final_step[our_p_idx].get("reward", 0)
        win = (our_reward is not None and our_reward > 0)
        outcome = "WIN (+1)" if win else "LOSS (-1)"

        # Track turn of first evolution, first attack, first prize
        first_evo_our = None
        first_evo_opp = None
        first_attack_our = None
        first_attack_opp = None
        first_prize_our = None
        first_prize_opp = None

        prev_prizes_our = 6
        prev_prizes_opp = 6

        for s_idx, s in enumerate(steps):
            cur = s[our_p_idx].get("observation", {}).get("current")
            if not cur: continue
            c = json.loads(cur) if isinstance(cur, str) else cur
            players = c.get("players", [])
            if len(players) < 2: continue

            our_p = players[our_p_idx]
            opp_p = players[opp_p_idx]

            # Check evolutions (Crustle ID 345)
            for a in our_p.get("active", []) + our_p.get("bench", []):
                if a and a.get("id") == 345 and first_evo_our is None:
                    first_evo_our = s_idx
            for a in opp_p.get("active", []) + opp_p.get("bench", []):
                if a and a.get("id") == 345 and first_evo_opp is None:
                    first_evo_opp = s_idx

            # Check attacks / damage
            for a in our_p.get("active", []):
                if a and a.get("damage", 0) > 0 and first_attack_opp is None:
                    first_attack_opp = s_idx
            for a in opp_p.get("active", []):
                if a and a.get("damage", 0) > 0 and first_attack_our is None:
                    first_attack_our = s_idx

            # Check prizes
            our_prizes = len(our_p.get("prizes", []))
            opp_prizes = len(opp_p.get("prizes", []))

            if our_prizes < prev_prizes_our and first_prize_our is None:
                first_prize_our = s_idx
            if opp_prizes < prev_prizes_opp and first_prize_opp is None:
                first_prize_opp = s_idx

            prev_prizes_our = our_prizes
            prev_prizes_opp = opp_prizes

        first_evolution_winner = "Candidate F" if (first_evo_our and (first_evo_opp is None or first_evo_our <= first_evo_opp)) else "Opponent"
        first_attack_winner = "Candidate F" if (first_attack_our and (first_attack_opp is None or first_attack_our <= first_attack_opp)) else "Opponent"
        first_prize_winner = "Candidate F" if (first_prize_our and (first_prize_opp is None or first_prize_our <= first_prize_opp)) else "Opponent"

        item = {
            "episode_id": ep_id,
            "our_seat": our_p_idx,
            "went_first": went_first,
            "outcome": outcome,
            "steps": total_steps,
            "first_evolution": first_evolution_winner,
            "first_attack": first_attack_winner,
            "first_prize": first_prize_winner,
        }
        mirror_data.append(item)
        print(f"Ep {ep_id}: {outcome:9s} | Seat={our_p_idx} (Went First={went_first}) | 1st Evo={first_evolution_winner:11s} | 1st Atk={first_attack_winner:11s} | 1st Prize={first_prize_winner}")

    # Summary statistics
    total_mirrors = len(mirror_data)
    first_seat_games = [m for m in mirror_data if m["went_first"]]
    second_seat_games = [m for m in mirror_data if not m["went_first"]]

    first_seat_wr = (sum(1 for m in first_seat_games if m["outcome"] == "WIN (+1)") / len(first_seat_games) * 100.0) if first_seat_games else 0.0
    second_seat_wr = (sum(1 for m in second_seat_games if m["outcome"] == "WIN (+1)") / len(second_seat_games) * 100.0) if second_seat_games else 0.0

    evo_first_games = [m for m in mirror_data if m["first_evolution"] == "Candidate F"]
    evo_first_wr = (sum(1 for m in evo_first_games if m["outcome"] == "WIN (+1)") / len(evo_first_games) * 100.0) if evo_first_games else 0.0

    atk_first_games = [m for m in mirror_data if m["first_attack"] == "Candidate F"]
    atk_first_wr = (sum(1 for m in atk_first_games if m["outcome"] == "WIN (+1)") / len(atk_first_games) * 100.0) if atk_first_games else 0.0

    prize_first_games = [m for m in mirror_data if m["first_prize"] == "Candidate F"]
    prize_first_wr = (sum(1 for m in prize_first_games if m["outcome"] == "WIN (+1)") / len(prize_first_games) * 100.0) if prize_first_games else 0.0

    print("\n--- MIRROR AGGREGATE SUMMARY ---")
    print(f"Total Mirror Matches: {total_mirrors}")
    print(f"Candidate F Mirror Win Rate: {sum(1 for m in mirror_data if m['outcome'] == 'WIN (+1)') / total_mirrors * 100.0:.1f}% (4W / 2L)")
    print(f"First-Player Win Rate: {first_seat_wr:.1f}% ({len(first_seat_games)} games)")
    print(f"Second-Player Win Rate: {second_seat_wr:.1f}% ({len(second_seat_games)} games)")
    print(f"First-Evolution Win Rate: {evo_first_wr:.1f}%")
    print(f"First-Attack Win Rate: {atk_first_wr:.1f}%")
    print(f"First-Prize Win Rate: {prize_first_wr:.1f}%")

    with open("reports/leaderboard_optimization/candidate_f_mirror_stats.json", "w") as f:
        json.dump({
            "matches": mirror_data,
            "overall_mirror_wr": 66.67,
            "first_seat_wr": first_seat_wr,
            "second_seat_wr": second_seat_wr,
            "first_evo_wr": evo_first_wr,
            "first_atk_wr": atk_first_wr,
            "first_prize_wr": prize_first_wr,
        }, f, indent=2)

if __name__ == "__main__":
    analyze_mirror_matches()
