import argparse
import os
import sys
import json
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaggle_environments import make
from kaggle_environments.envs.cabt import cabt
import main


def run_self_play(num_games: int = 10, opponent_type: str = "self") -> dict:
    """Run multi-game self-play evaluation series."""
    main.reset_diagnostics()
    
    wins = 0
    losses = 0
    draws = 0
    invalids = 0
    total_steps = 0
    
    opponent_func = main.agent
    if opponent_type == "random":
        opponent_func = cabt.random_agent
    elif opponent_type == "first":
        opponent_func = cabt.first_agent

    print(f"=== Starting Self-Play Evaluation: {num_games} games vs {opponent_type} ===")
    
    start_bench_t = time.perf_counter()

    for game_idx in range(num_games):
        env = make("cabt", debug=False)
        
        # Swap seats every alternate game
        p0_is_agent = (game_idx % 2 == 0)
        agents_list = [main.agent, opponent_func] if p0_is_agent else [opponent_func, main.agent]
        
        env.run(agents_list)
        
        steps = len(env.steps)
        total_steps += steps
        final_step = env.steps[-1]
        
        p0_status = final_step[0].status
        p1_status = final_step[1].status
        p0_reward = final_step[0].reward
        p1_reward = final_step[1].reward
        
        agent_seat = 0 if p0_is_agent else 1
        agent_reward = p0_reward if p0_is_agent else p1_reward
        agent_status = p0_status if p0_is_agent else p1_status
        
        if agent_status == "INVALID" or p0_status == "INVALID" or p1_status == "INVALID":
            invalids += 1
            print(f"Game {game_idx+1}/{num_games}: INVALID! Statuses: P0={p0_status}, P1={p1_status}")
            if "error" in env.steps[0][0]:
                print(f"  Error details: {env.steps[0][0]['error']}")
        elif agent_reward == 1:
            wins += 1
            print(f"Game {game_idx+1}/{num_games}: WIN (Seat {agent_seat}, {steps} steps)")
        elif agent_reward == -1:
            losses += 1
            print(f"Game {game_idx+1}/{num_games}: LOSS (Seat {agent_seat}, {steps} steps)")
        else:
            draws += 1
            print(f"Game {game_idx+1}/{num_games}: DRAW (Seat {agent_seat}, {steps} steps)")

    elapsed_bench_sec = time.perf_counter() - start_bench_t
    diag = main.get_diagnostics()
    diag["games_completed"] = num_games - invalids
    
    avg_steps = total_steps / max(1, num_games)
    win_rate = (wins / max(1, num_games)) * 100.0
    fallback_rate = (diag["fallback_decisions"] / max(1, diag["decisions"])) * 100.0

    print("\n" + "=" * 50)
    print("      SELF-PLAY EVALUATION SUMMARY REPORT      ")
    print("=" * 50)
    print(f"Total Games Played  : {num_games}")
    print(f"Wins                : {wins} ({win_rate:.1f}%)")
    print(f"Losses              : {losses}")
    print(f"Draws               : {draws}")
    print(f"Invalid / Crashes   : {invalids}")
    print(f"Avg Steps / Game    : {avg_steps:.1f}")
    print(f"Total Benchmark Time: {elapsed_bench_sec:.2f}s")
    print("-" * 50)
    print("AGENT DIAGNOSTICS & RUNTIME TELEMETRY:")
    print(f"  Total Decisions       : {diag['decisions']}")
    print(f"  Search Decisions      : {diag['search_decisions']}")
    print(f"  Heuristic Decisions   : {diag['heuristic_decisions']}")
    print(f"  Fallback Decisions    : {diag['fallback_decisions']} (Rate: {fallback_rate:.2f}%)")
    print(f"  Exceptions Caught     : {diag['exceptions']}")
    print(f"  Avg Decision Time     : {diag.get('avg_decision_time_ms', 0.0):.3f} ms")
    print(f"  Max Decision Time     : {diag.get('max_decision_time_ms', 0.0):.3f} ms")
    print(f"  Attacks Selected      : {diag['attacks_selected']}")
    print(f"  Option Types Selected : {json.dumps(diag['option_types_selected'])}")
    print("=" * 50 + "\n")

    return {
        "games": num_games,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "invalids": invalids,
        "win_rate": win_rate,
        "avg_steps": avg_steps,
        "fallback_rate": fallback_rate,
        "diagnostics": diag,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PTCG Agent Self-Play Evaluator")
    parser.add_argument("--games", type=int, default=10, help="Number of games to run")
    parser.add_argument("--opponent", type=str, default="self", choices=["self", "random", "first"], help="Opponent type")
    args = parser.parse_args()

    results = run_self_play(num_games=args.games, opponent_type=args.opponent)
    if results["invalids"] > 0:
        print("FAIL: Encountered invalid or crash games!")
        sys.exit(1)
    else:
        print("SUCCESS: All games completed cleanly without crashes or invalid moves.")
        sys.exit(0)
