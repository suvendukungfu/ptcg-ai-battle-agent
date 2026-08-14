import os
import sys
import argparse
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.self_play import run_self_play
from research.experiments.experiment_tracker import ExperimentTracker
from tools.benchmark import run_benchmark


def main_cli():
    parser = argparse.ArgumentParser(description="PTCG Experiment Runner & Registry Logger")
    parser.add_argument("--id", type=str, default=f"exp_{int(time.time())}", help="Unique Experiment ID")
    parser.add_argument("--games", type=int, default=20, help="Number of evaluation games")
    parser.add_argument("--notes", type=str, default="Standard evaluation run", help="Experiment notes")
    args = parser.parse_args()

    print(f"Running Experiment: {args.id} ({args.games} games)")
    perf = run_benchmark(num_games=args.games, verbose=True)

    tracker = ExperimentTracker()
    record = tracker.log_experiment(
        experiment_id=args.id,
        agent_version="v2.0-search-integrated",
        deck="bellibolt_standard.csv",
        policy_version="risk_aware_v2",
        search_depth=2,
        search_budget={"max_candidates": 8, "time_budget_ms": 40.0},
        seed=42,
        games=perf["games_evaluated"],
        wins=int(perf["win_rate_pct"] * perf["games_evaluated"] / 100.0),
        losses=perf["games_evaluated"] - int(perf["win_rate_pct"] * perf["games_evaluated"] / 100.0),
        draws=0,
        win_rate=perf["win_rate_pct"],
        average_game_length=perf["total_steps"] / max(1, perf["games_evaluated"]),
        average_decision_time_ms=perf["latency_avg_ms"],
        p95_latency_ms=perf["latency_p95_ms"],
        fallback_rate=perf["fallback_rate_pct"],
        notes=args.notes,
    )
    print(f"Experiment successfully recorded to registry: {tracker.registry_file}")


if __name__ == "__main__":
    main_cli()
