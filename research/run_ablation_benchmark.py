import os
import sys
import time
import csv
from typing import Dict, Any, List, Callable

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from kaggle_environments import make
from agent.action_selector import select_action, select_heuristic_action
from agent.state import parse_game_state
from analytics.metrics import wilson_score_interval
from research.run_deck_tournament import load_deck_from_file, create_agent_with_deck


def create_ablated_agent(deck_cards: List[int], variant: str) -> Callable:
    """Create agent closure with specific ablated component configurations."""
    deck_copy = list(deck_cards)

    def ablated_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
        if not isinstance(obs, dict):
            return []
        select = obs.get("select")
        if select is None:
            return list(deck_copy)

        state = parse_game_state(obs)
        n_opts = len(state.options)
        if n_opts == 0:
            return []

        if variant == "A_Pure_Heuristic":
            return select_heuristic_action(state, goal_state=None)

        elif variant == "B_Heuristic_Plus_Goals":
            from agent.goals import GoalPlanner
            goal = GoalPlanner.identify_goal(state)
            return select_heuristic_action(state, goal_state=goal)

        elif variant == "C_Heuristic_Plus_Search_1Ply":
            from agent.search import shallow_risk_aware_search
            choice = shallow_risk_aware_search(state, remaining_time=600.0)
            if choice is not None:
                return choice
            return select_heuristic_action(state)

        elif variant == "D_Full_System":
            return select_action(obs)

        return select_action(obs)

    return ablated_agent


def run_ablation_study():
    """Run systematic ablation study across 4 variants against benchmark opponents."""
    print("=========================================================")
    print("PTCG AI BATTLE CHALLENGE — COMPONENT ABLATION BENCHMARK")
    print("=========================================================")

    # Use the best deck: Candidate D (Crustle Control) and Candidate A (Bellibolt)
    crustle_deck = load_deck_from_file(os.path.join(BASE_DIR, "research/deck_candidates/D_crustle_control.csv"))
    bellibolt_deck = load_deck_from_file(os.path.join(BASE_DIR, "research/deck_candidates/A_bellibolt_baseline.csv"))

    from kaggle_environments.envs.cabt import cabt

    opponents = [
        ("Random_Bot", cabt.random_agent),
        ("Heuristic_Bot", create_agent_with_deck(bellibolt_deck, use_full_pipeline=False)),
    ]

    variants = [
        "A_Pure_Heuristic",
        "B_Heuristic_Plus_Goals",
        "C_Heuristic_Plus_Search_1Ply",
        "D_Full_System",
    ]

    results: List[Dict[str, Any]] = []

    for var in variants:
        agent_fn = create_ablated_agent(crustle_deck, var)
        print(f"\nTesting Ablation Variant: {var}...")

        total_wins = 0
        total_losses = 0
        total_draws = 0
        latencies: List[float] = []

        for opp_name, opp_fn in opponents:
            for g in range(10):
                env = make("cabt", debug=False)
                a_is_seat_0 = (g % 2 == 0)

                times_in_game: List[float] = []
                def timed_agent(obs, cfg=None):
                    t0 = time.perf_counter()
                    act = agent_fn(obs, cfg)
                    times_in_game.append((time.perf_counter() - t0) * 1000.0)
                    return act

                agents = [timed_agent, opp_fn] if a_is_seat_0 else [opp_fn, timed_agent]
                env.run(agents)
                latencies.extend(times_in_game)

                final_step = env.steps[-1]
                reward_a = final_step[0].reward if a_is_seat_0 else final_step[1].reward
                reward_b = final_step[1].reward if a_is_seat_0 else final_step[0].reward

                if reward_a == 1 and reward_b != 1:
                    total_wins += 1
                elif reward_b == 1 and reward_a != 1:
                    total_losses += 1
                else:
                    total_draws += 1

        total_games = total_wins + total_losses + total_draws
        wr = (total_wins / total_games) * 100.0
        ci_low, ci_high = wilson_score_interval(total_wins, total_games, 0.95)

        latencies.sort()
        p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0.0

        print(f"--> {var:30s}: WR = {wr:5.1f}% ({total_wins}/{total_games}) | 95% CI: [{ci_low:.1f}%, {ci_high:.1f}%] | P95: {p95:.3f}ms")

        results.append({
            "variant": var,
            "games": total_games,
            "wins": total_wins,
            "losses": total_losses,
            "draws": total_draws,
            "win_rate": round(wr, 1),
            "ci_low": round(ci_low, 1),
            "ci_high": round(ci_high, 1),
            "p95_latency_ms": round(p95, 3),
        })

    # Save to reports/final_ablation.csv
    csv_path = os.path.join(BASE_DIR, "reports/final_ablation.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["variant", "games", "wins", "losses", "draws", "win_rate", "ci_low", "ci_high", "p95_latency_ms"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nWrote final ablation report to {csv_path}")


if __name__ == "__main__":
    run_ablation_study()
