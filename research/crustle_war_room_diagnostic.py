import os
import sys
import time
from typing import Dict, Any, List

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from kaggle_environments import make
from research.run_deck_tournament import load_deck_from_file, create_agent_with_deck
from analytics.metrics import wilson_score_interval


def run_crustle_forensics(candidate_path: str, candidate_name: str, num_games: int = 15):
    """Run detailed forensic diagnostic against Crustle Safeguard Wall."""
    print(f"\n=======================================================")
    print(f"CRUSTLE WAR ROOM DIAGNOSTIC: {candidate_name} ({num_games} games)")
    print(f"=======================================================")

    candidate_deck = load_deck_from_file(candidate_path)
    crustle_deck = load_deck_from_file(os.path.join(BASE_DIR, "research/decks/crustle_control.csv"))

    agent_a = create_agent_with_deck(candidate_deck, use_full_pipeline=True)
    agent_b = create_agent_with_deck(crustle_deck, use_full_pipeline=False)

    wins = 0
    losses = 0
    draws = 0
    blocked_attacks = 0
    non_ex_attacks = 0
    boss_gusts = 0
    non_ex_evolutions = 0

    for g in range(num_games):
        env = make("cabt", debug=False)
        a_is_seat_0 = (g % 2 == 0)
        agents = [agent_a, agent_b] if a_is_seat_0 else [agent_b, agent_a]

        env.run(agents)
        final_step = env.steps[-1]
        reward_a = final_step[0].reward if a_is_seat_0 else final_step[1].reward
        reward_b = final_step[1].reward if a_is_seat_0 else final_step[0].reward

        if reward_a == 1 and reward_b != 1:
            wins += 1
        elif reward_b == 1 and reward_a != 1:
            losses += 1
        else:
            draws += 1

        # Audit step events for seat a
        seat_idx = 0 if a_is_seat_0 else 1
        for step in env.steps:
            obs = step[seat_idx].observation
            action = step[seat_idx].action

    total = wins + losses + draws
    wr = (wins / total) * 100.0 if total > 0 else 0.0
    ci_low, ci_high = wilson_score_interval(wins, total, 0.95)

    print(f"Result for {candidate_name}:")
    print(f"  Record  : {wins}W - {losses}L - {draws}D (Win Rate: {wr:.1f}%)")
    print(f"  95% CI  : [{ci_low:.1f}%, {ci_high:.1f}%]")

    return {
        "candidate": candidate_name,
        "games": total,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": round(wr, 1),
        "ci_low": round(ci_low, 1),
        "ci_high": round(ci_high, 1),
    }


if __name__ == "__main__":
    candidates = [
        ("research/deck_candidates/A_bellibolt_baseline.csv", "Candidate_A_Baseline"),
        ("research/deck_candidates/B_bellibolt_consistency_4_3_3.csv", "Candidate_B_Consistency_4_3_3"),
        ("research/deck_candidates/C_anti_crustle_tech.csv", "Candidate_C_Anti_Crustle_Tech"),
    ]
    for c_path, c_name in candidates:
        run_crustle_forensics(os.path.join(BASE_DIR, c_path), c_name, num_games=10)
