import os
import sys
import argparse
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from simulation.tournament import run_tournament
from research.baselines import random_agent, first_legal_agent, heuristic_v1_agent
from analytics.matchup_analysis import generate_matchup_matrix
from analytics.meta_analysis import generate_meta_reports


def main_cli():
    parser = argparse.ArgumentParser(description="PTCG Round-Robin Tournament Engine")
    parser.add_argument("--games", type=int, default=6, help="Number of games per pairing")
    args = parser.parse_args()

    contestants = {
        "Production_Agent_V2": main.agent,
        "Heuristic_V1_Agent": heuristic_v1_agent,
        "Random_Baseline": random_agent,
        "First_Legal_Baseline": first_legal_agent,
    }

    print(f"=== Launching Tournament with {len(contestants)} Contestants ({args.games} games/pairing) ===")
    results = run_tournament(contestants, games_per_pairing=args.games, verbose=True)

    matrix_file = generate_matchup_matrix(results)
    meta_files = generate_meta_reports()
    print(f"\nGenerated Matchup Matrix: {matrix_file}")
    for k, v in meta_files.items():
        print(f"Generated {k}: {v}")


if __name__ == "__main__":
    main_cli()
