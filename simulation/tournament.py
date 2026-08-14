import os
import sys
import time
import math
from typing import Dict, Any, List, Tuple, Callable
from kaggle_environments import make

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def update_elo(r_a: float, r_b: float, score_a: float, k: float = 32.0) -> Tuple[float, float]:
    """Calculate new FIDE-style Elo ratings for player A and player B given match result."""
    e_a = 1.0 / (1.0 + 10.0 ** ((r_b - r_a) / 400.0))
    e_b = 1.0 - e_a

    new_r_a = r_a + k * (score_a - e_a)
    new_r_b = r_b + k * ((1.0 - score_a) - e_b)

    return new_r_a, new_r_b


def run_tournament(
    contestants: Dict[str, Callable],
    games_per_pairing: int = 10,
    initial_elo: float = 1500.0,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Run round-robin tournament among all contestant agents with alternating seat assignments.
    """
    names = list(contestants.keys())
    elos = {name: initial_elo for name in names}
    records = {name: {"wins": 0, "losses": 0, "draws": 0, "games": 0, "steps": 0} for name in names}
    matchup_matrix: Dict[str, Dict[str, Dict[str, int]]] = {
        n1: {n2: {"wins": 0, "losses": 0, "draws": 0} for n2 in names if n1 != n2}
        for n1 in names
    }

    start_time = time.perf_counter()

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name_a = names[i]
            name_b = names[j]
            agent_a = contestants[name_a]
            agent_b = contestants[name_b]

            if verbose:
                print(f"\n--- Matchup: {name_a} vs {name_b} ({games_per_pairing} games) ---")

            for g in range(games_per_pairing):
                env = make("cabt", debug=False)
                # Alternate seats
                a_is_seat_0 = (g % 2 == 0)
                agents_pair = [agent_a, agent_b] if a_is_seat_0 else [agent_b, agent_a]

                env.run(agents_pair)

                final = env.steps[-1]
                steps = len(env.steps)
                reward_0 = final[0].reward
                reward_1 = final[1].reward

                reward_a = reward_0 if a_is_seat_0 else reward_1
                reward_b = reward_1 if a_is_seat_0 else reward_0

                score_a = 0.5
                if reward_a == 1:
                    score_a = 1.0
                    records[name_a]["wins"] += 1
                    records[name_b]["losses"] += 1
                    matchup_matrix[name_a][name_b]["wins"] += 1
                    matchup_matrix[name_b][name_a]["losses"] += 1
                elif reward_b == 1:
                    score_a = 0.0
                    records[name_a]["losses"] += 1
                    records[name_b]["wins"] += 1
                    matchup_matrix[name_a][name_b]["losses"] += 1
                    matchup_matrix[name_b][name_a]["wins"] += 1
                else:
                    records[name_a]["draws"] += 1
                    records[name_b]["draws"] += 1
                    matchup_matrix[name_a][name_b]["draws"] += 1
                    matchup_matrix[name_b][name_a]["draws"] += 1

                records[name_a]["games"] += 1
                records[name_b]["games"] += 1
                records[name_a]["steps"] += steps
                records[name_b]["steps"] += steps

                # Update Elo
                new_a, new_b = update_elo(elos[name_a], elos[name_b], score_a)
                elos[name_a] = new_a
                elos[name_b] = new_b

    elapsed = time.perf_counter() - start_time

    # Sort leaderboard by Elo
    leaderboard = []
    for name in names:
        rec = records[name]
        g = max(1, rec["games"])
        wr = (rec["wins"] / g) * 100.0
        avg_s = rec["steps"] / g
        leaderboard.append({
            "agent": name,
            "elo": round(elos[name], 1),
            "win_rate": round(wr, 1),
            "wins": rec["wins"],
            "losses": rec["losses"],
            "draws": rec["draws"],
            "total_games": rec["games"],
            "avg_steps": round(avg_s, 1),
        })

    leaderboard.sort(key=lambda x: x["elo"], reverse=True)

    if verbose:
        print("\n" + "=" * 70)
        print("                 TOURNAMENT FINAL LEADERBOARD")
        print("=" * 70)
        print(f"{'Rank':<5} {'Agent Name':<25} {'Elo':<8} {'Win Rate':<10} {'W-L-D':<12} {'Avg Steps':<10}")
        print("-" * 70)
        for rank, row in enumerate(leaderboard, 1):
            wld = f"{row['wins']}-{row['losses']}-{row['draws']}"
            print(f"{rank:<5} {row['agent']:<25} {row['elo']:<8.1f} {row['win_rate']:<9.1f}% {wld:<12} {row['avg_steps']:<10.1f}")
        print("=" * 70)

    return {
        "leaderboard": leaderboard,
        "elos": elos,
        "records": records,
        "matchup_matrix": matchup_matrix,
        "duration_sec": elapsed,
    }
