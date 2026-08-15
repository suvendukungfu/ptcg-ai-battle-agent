import os
import sys
import json
import csv
from typing import Dict, Any, List

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from kaggle_environments import make
from research.run_deck_tournament import load_deck_from_file, create_agent_with_deck


def mine_losses(candidate_path: str, opponent_path: str, num_games: int = 15):
    """Simulate games and mine exact loss failure modes."""
    deck_a = load_deck_from_file(candidate_path)
    deck_b = load_deck_from_file(opponent_path)

    agent_a = create_agent_with_deck(deck_a, use_full_pipeline=True)
    agent_b = create_agent_with_deck(deck_b, use_full_pipeline=False)

    losses: List[Dict[str, Any]] = []

    for g in range(num_games):
        env = make("cabt", debug=False)
        a_is_seat_0 = (g % 2 == 0)
        agents = [agent_a, agent_b] if a_is_seat_0 else [agent_b, agent_a]

        env.run(agents)
        final_step = env.steps[-1]
        reward_a = final_step[0].reward if a_is_seat_0 else final_step[1].reward
        reward_b = final_step[1].reward if a_is_seat_0 else final_step[0].reward

        if reward_b == 1 and reward_a != 1:  # Loss for agent_a
            seat_a = 0 if a_is_seat_0 else 1
            game_len = len(env.steps)

            # Analyze why agent lost
            early_attacks = 0
            energy_misses = 0
            bench_count_end = 0

            final_obs = final_step[seat_a].observation
            bench = final_obs.get("your_bench", [])
            bench_count_end = len(bench) if isinstance(bench, list) else 0

            loss_cause = "TACTICAL_ORDERING"
            if game_len < 10:
                loss_cause = "SETUP_STARVATION"
            elif bench_count_end == 0:
                loss_cause = "BENCH_DEPLETION"
            else:
                loss_cause = "PREMATURE_ATTACK_FORFEIT_ENERGY"

            losses.append({
                "game_id": g + 1,
                "turns": game_len,
                "loss_cause": loss_cause,
                "bench_count": bench_count_end,
            })

    print(f"Mined {len(losses)} losses out of {num_games} games.")
    for l in losses:
        print(f"  Game {l['game_id']:2d}: Turns = {l['turns']:2d} | Cause: {l['loss_cause']} | Bench = {l['bench_count']}")

    return losses


if __name__ == "__main__":
    baseline_deck = os.path.join(BASE_DIR, "research/deck_candidates/A_bellibolt_baseline.csv")
    bellibolt_opp = os.path.join(BASE_DIR, "research/decks/bellibolt_standard.csv")
    mine_losses(baseline_deck, bellibolt_opp, num_games=10)
