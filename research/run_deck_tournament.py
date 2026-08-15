import os
import sys
import time
import json
import csv
import math
from typing import Dict, Any, List, Tuple, Callable, Optional

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from kaggle_environments import make
from agent.action_selector import select_action, select_heuristic_action
from agent.state import parse_game_state
from agent.fallback import deterministic_fallback
from agent.utils import reset_diagnostics, get_diagnostics
from analytics.metrics import wilson_score_interval


def load_deck_from_file(csv_path: str) -> List[int]:
    """Load exactly 60 card IDs from a CSV file."""
    cards: List[int] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str:
                parts = line_str.split(",")
                for p in parts:
                    p_clean = p.strip()
                    if p_clean.lstrip("-").isdigit():
                        cards.append(int(p_clean))
    if len(cards) != 60:
        raise ValueError(f"Deck at {csv_path} has {len(cards)} cards instead of 60")
    return cards


def create_agent_with_deck(deck_cards: List[int], use_full_pipeline: bool = True) -> Callable:
    """Create a standalone Kaggle CABT agent closure with a specific 60-card deck."""
    deck_copy = list(deck_cards)

    def custom_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
        if not isinstance(obs, dict):
            return []
        select = obs.get("select")
        if select is None:
            return list(deck_copy)

        if use_full_pipeline:
            return select_action(obs)
        else:
            state = parse_game_state(obs)
            return select_heuristic_action(state)

    return custom_agent


def evaluate_pairing(
    agent_a: Callable,
    agent_b: Callable,
    num_games: int = 20,
    seed_offset: int = 42,
) -> Dict[str, Any]:
    """
    Simulate num_games between agent_a and agent_b, alternating seat 0 and seat 1.
    """
    wins_a = 0
    losses_a = 0
    draws = 0
    turns_list: List[int] = []
    latencies_a: List[float] = []
    illegal_actions_a = 0
    fallbacks_a = 0

    for g in range(num_games):
        env = make("cabt", debug=False)
        a_is_seat_0 = (g % 2 == 0)

        # Wrap agent_a to measure latency and track validity
        latencies_in_game: List[float] = []

        def timed_agent_a(obs: Dict[str, Any], config: Any = None) -> List[int]:
            t0 = time.perf_counter()
            act = agent_a(obs, config)
            dt_ms = (time.perf_counter() - t0) * 1000.0
            latencies_in_game.append(dt_ms)
            return act

        agents = [timed_agent_a, agent_b] if a_is_seat_0 else [agent_b, timed_agent_a]

        try:
            env.run(agents)
            latencies_a.extend(latencies_in_game)

            final_step = env.steps[-1]
            turns_list.append(len(env.steps))

            reward_0 = final_step[0].reward
            reward_1 = final_step[1].reward
            reward_a = reward_0 if a_is_seat_0 else reward_1
            reward_b = reward_1 if a_is_seat_0 else reward_0

            # Check status of seat a
            status_a = final_step[0 if a_is_seat_0 else 1].status
            if status_a == "ERROR" or status_a == "INVALID":
                illegal_actions_a += 1

            if reward_a == 1 and reward_b != 1:
                wins_a += 1
            elif reward_b == 1 and reward_a != 1:
                losses_a += 1
            else:
                draws += 1

        except Exception as e:
            losses_a += 1
            illegal_actions_a += 1

    total_games = wins_a + losses_a + draws
    win_rate = (wins_a / total_games) * 100.0 if total_games > 0 else 0.0
    ci_low, ci_high = wilson_score_interval(wins_a, total_games, confidence=0.95)

    latencies_a.sort()
    p50 = latencies_a[int(len(latencies_a) * 0.50)] if latencies_a else 0.0
    p95 = latencies_a[int(len(latencies_a) * 0.95)] if latencies_a else 0.0
    p99 = latencies_a[int(len(latencies_a) * 0.99)] if latencies_a else 0.0

    avg_turns = sum(turns_list) / len(turns_list) if turns_list else 0.0

    return {
        "games": total_games,
        "wins": wins_a,
        "losses": losses_a,
        "draws": draws,
        "win_rate": round(win_rate, 2),
        "ci_low": round(ci_low, 2),
        "ci_high": round(ci_high, 2),
        "avg_turns": round(avg_turns, 1),
        "p50_latency_ms": round(p50, 3),
        "p95_latency_ms": round(p95, 3),
        "p99_latency_ms": round(p99, 3),
        "illegal_actions": illegal_actions_a,
        "fallback_rate": round((fallbacks_a / max(1, len(latencies_a))) * 100.0, 2),
    }


def run_full_deck_tournament():
    """Run all deck candidates through the competitive tournament benchmark."""
    print("=================================================================")
    print("PTCG AI BATTLE CHALLENGE — FULL DECK CANDIDATE TOURNAMENT ENGINE")
    print("=================================================================")

    candidates = {
        "Candidate_A_Baseline_4_4_4": os.path.join(BASE_DIR, "research/deck_candidates/A_bellibolt_baseline.csv"),
        "Candidate_B_Consistency_4_3_3": os.path.join(BASE_DIR, "research/deck_candidates/B_bellibolt_consistency_4_3_3.csv"),
        "Candidate_C_Anti_Crustle_Tech": os.path.join(BASE_DIR, "research/deck_candidates/C_anti_crustle_tech.csv"),
        "Candidate_D_Crustle_Control": os.path.join(BASE_DIR, "research/deck_candidates/D_crustle_control.csv"),
        "Candidate_E_Alakazam_Psychic": os.path.join(BASE_DIR, "research/deck_candidates/E_alakazam_psychic.csv"),
    }

    # Standard opponent reference decks
    crustle_deck = load_deck_from_file(os.path.join(BASE_DIR, "research/decks/crustle_control.csv"))
    alakazam_deck = load_deck_from_file(os.path.join(BASE_DIR, "research/decks/alakazam_psychic.csv"))
    bellibolt_deck = load_deck_from_file(os.path.join(BASE_DIR, "research/decks/bellibolt_standard.csv"))

    from kaggle_environments.envs.cabt import cabt

    opponents = {
        "Random_Bot": cabt.random_agent,
        "Heuristic_Bellibolt": create_agent_with_deck(bellibolt_deck, use_full_pipeline=False),
        "Crustle_Safeguard_Wall": create_agent_with_deck(crustle_deck, use_full_pipeline=False),
        "Alakazam_Spread": create_agent_with_deck(alakazam_deck, use_full_pipeline=False),
    }

    results: List[Dict[str, Any]] = []

    for c_name, c_path in candidates.items():
        deck_cards = load_deck_from_file(c_path)
        agent_fn = create_agent_with_deck(deck_cards, use_full_pipeline=True)

        print(f"\nEvaluating Candidate: {c_name}...")
        total_wins = 0
        total_losses = 0
        total_draws = 0
        total_games = 0
        total_latencies: List[float] = []

        for opp_name, opp_fn in opponents.items():
            # 10 games per pairing = 40 games per candidate
            eval_res = evaluate_pairing(agent_fn, opp_fn, num_games=10)
            print(f"  vs {opp_name:24s}: WR = {eval_res['win_rate']:5.1f}% ({eval_res['wins']}/{eval_res['games']}) | CI: [{eval_res['ci_low']}, {eval_res['ci_high']}] | P95: {eval_res['p95_latency_ms']}ms")

            results.append({
                "candidate": c_name,
                "opponent": opp_name,
                "games": eval_res["games"],
                "wins": eval_res["wins"],
                "losses": eval_res["losses"],
                "draws": eval_res["draws"],
                "win_rate": eval_res["win_rate"],
                "ci_low": eval_res["ci_low"],
                "ci_high": eval_res["ci_high"],
                "avg_turns": eval_res["avg_turns"],
                "p95_latency_ms": eval_res["p95_latency_ms"],
                "p99_latency_ms": eval_res["p99_latency_ms"],
                "illegal_actions": eval_res["illegal_actions"],
                "fallback_rate": eval_res["fallback_rate"],
            })

            total_wins += eval_res["wins"]
            total_losses += eval_res["losses"]
            total_draws += eval_res["draws"]
            total_games += eval_res["games"]

        agg_wr = (total_wins / total_games) * 100.0
        agg_low, agg_high = wilson_score_interval(total_wins, total_games, 0.95)
        print(f"--> AGGREGATE {c_name}: Win Rate = {agg_wr:.1f}% ({total_wins}/{total_games}) | 95% CI: [{agg_low}%, {agg_high}%]")

    # Write results to reports/deck_tournament.csv
    csv_path = os.path.join(BASE_DIR, "reports/deck_tournament.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "candidate", "opponent", "games", "wins", "losses", "draws",
            "win_rate", "ci_low", "ci_high", "avg_turns", "p95_latency_ms",
            "p99_latency_ms", "illegal_actions", "fallback_rate"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nWrote full tournament results to {csv_path}")


if __name__ == "__main__":
    run_full_deck_tournament()
