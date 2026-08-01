"""
High-Speed Parallel Tournament Runner for Candidate F vs Baselines.
Evaluates Candidate B, Candidate D, Candidate E, and F0 through F7 across all 5 archetypes
using multiprocessing for maximum speed.
"""

import os
import sys
import time
import json
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, Any, List, Tuple

sys.path.insert(0, os.path.abspath("."))
from kaggle_environments import make
from research.run_deck_tournament import load_deck_from_file, create_agent_with_deck


def run_single_game(args: Tuple[str, str, List[int], List[int], int, bool]) -> Dict[str, Any]:
    cand_name, opp_name, cand_deck, opp_deck, game_idx, a_is_seat_0 = args
    
    agent_cand = create_agent_with_deck(cand_deck)
    agent_opp = create_agent_with_deck(opp_deck)

    latencies_a: List[float] = []
    def timed_agent_a(obs: Dict[str, Any], config: Any = None) -> List[int]:
        t0 = time.perf_counter()
        act = agent_cand(obs, config)
        latencies_a.append((time.perf_counter() - t0) * 1000.0)
        return act

    agents = [timed_agent_a, agent_opp] if a_is_seat_0 else [agent_opp, timed_agent_a]
    
    env = make("cabt", debug=False)
    try:
        env.run(agents)
        final_step = env.steps[-1]
        reward_0 = final_step[0].reward
        reward_1 = final_step[1].reward
        reward_a = reward_0 if a_is_seat_0 else reward_1
        
        cand_step = final_step[0] if a_is_seat_0 else final_step[1]
        is_invalid = (cand_step.status == "INVALID")
        
        win = 1 if (reward_a is not None and reward_a > 0) else 0
        loss = 1 if (reward_a is not None and reward_a < 0) else 0
        draw = 1 if (reward_a is None or reward_a == 0) else 0
        
        return {
            "cand_name": cand_name,
            "opp_name": opp_name,
            "win": win,
            "loss": loss,
            "draw": draw,
            "turns": len(env.steps),
            "latencies": latencies_a,
            "invalid": 1 if is_invalid else 0,
        }
    except Exception as e:
        return {
            "cand_name": cand_name,
            "opp_name": opp_name,
            "win": 0,
            "loss": 1,
            "draw": 0,
            "turns": 0,
            "latencies": [],
            "invalid": 1,
        }


def run_parallel_tournament(num_games_per_pairing: int = 20, max_workers: int = 8):
    deck_files = {
        "Candidate_B": "research/deck_candidates/B_bellibolt_consistency_4_3_3.csv",
        "Candidate_D": "research/deck_candidates/D_crustle_control.csv",
        "Candidate_E": "research/deck_candidates/E_alakazam_psychic.csv",
        "F0_crustle_baseline": "research/deck_candidates/F0_crustle_baseline.csv",
        "F1_crustle_fast_tech": "research/deck_candidates/F1_crustle_fast_tech.csv",
        "F2_crustle_rillaboom": "research/deck_candidates/F2_crustle_rillaboom.csv",
        "F3_crustle_heavy_gust": "research/deck_candidates/F3_crustle_heavy_gust.csv",
        "F4_alakazam_swarm": "research/deck_candidates/F4_alakazam_swarm.csv",
        "F5_bellibolt_pure": "research/deck_candidates/F5_bellibolt_pure.csv",
        "F6_balanced_hybrid": "research/deck_candidates/F6_balanced_hybrid.csv",
        "F7_meta_breaker_gust": "research/deck_candidates/F7_meta_breaker_gust.csv",
    }
    decks = {k: load_deck_from_file(v) for k, v in deck_files.items()}

    opponents = {
        "Alakazam_NonEX": decks["F4_alakazam_swarm"],
        "Bellibolt_EX": decks["Candidate_B"],
        "Crustle_Safeguard": decks["Candidate_D"],
        "Heavy_Gust_Control": decks["F3_crustle_heavy_gust"],
        "Meta_Breaker_Aggro": decks["F7_meta_breaker_gust"],
    }

    candidates = list(decks.keys())
    tasks = []

    for cand_name in candidates:
        for opp_name, opp_deck in opponents.items():
            for g in range(num_games_per_pairing):
                a_is_seat_0 = (g % 2 == 0)
                tasks.append((cand_name, opp_name, decks[cand_name], opp_deck, g, a_is_seat_0))

    total_tasks = len(tasks)
    print(f"Executing {total_tasks} tournament games across {max_workers} parallel workers...")
    t0 = time.time()

    raw_results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_single_game, t) for t in tasks]
        for f in as_completed(futures):
            raw_results.append(f.result())

    elapsed = time.time() - t0
    print(f"All {total_tasks} games finished in {elapsed:.1f}s ({total_tasks/elapsed:.1f} games/s)!")

    # Aggregate results
    matrix: Dict[str, Dict[str, Any]] = {c: {} for c in candidates}
    for cand_name in candidates:
        for opp_name in opponents.keys():
            matching = [r for r in raw_results if r["cand_name"] == cand_name and r["opp_name"] == opp_name]
            wins = sum(r["win"] for r in matching)
            losses = sum(r["loss"] for r in matching)
            draws = sum(r["draw"] for r in matching)
            invalids = sum(r["invalid"] for r in matching)
            games = len(matching)
            wr = (wins / games * 100.0) if games > 0 else 0.0

            all_latencies = []
            for r in matching:
                all_latencies.extend(r["latencies"])
            all_latencies.sort()

            p50 = all_latencies[int(len(all_latencies) * 0.50)] if all_latencies else 0.0
            p95 = all_latencies[int(len(all_latencies) * 0.95)] if all_latencies else 0.0
            p99 = all_latencies[int(len(all_latencies) * 0.99)] if all_latencies else 0.0
            avg_turns = sum(r["turns"] for r in matching) / max(1, games)

            # Wilson Score 95% CI
            if games > 0:
                z = 1.96
                p = wins / games
                denom = 1.0 + z**2 / games
                center = (p + z**2 / (2 * games)) / denom
                spread = z * math.sqrt((p * (1 - p) + z**2 / (4 * games)) / games) / denom
                ci_low = max(0.0, (center - spread) * 100.0)
                ci_high = min(100.0, (center + spread) * 100.0)
            else:
                ci_low, ci_high = 0.0, 0.0

            matrix[cand_name][opp_name] = {
                "games": games,
                "wins": wins,
                "losses": losses,
                "draws": draws,
                "win_rate": wr,
                "ci_low": round(ci_low, 2),
                "ci_high": round(ci_high, 2),
                "avg_turns": round(avg_turns, 1),
                "p50_latency_ms": round(p50, 3),
                "p95_latency_ms": round(p95, 3),
                "p99_latency_ms": round(p99, 3),
                "illegal_actions": invalids,
            }

        # Candidate overall
        all_c_games = [r for r in raw_results if r["cand_name"] == cand_name]
        c_wins = sum(r["win"] for r in all_c_games)
        c_total = len(all_c_games)
        c_wr = (c_wins / c_total * 100.0) if c_total > 0 else 0.0
        matrix[cand_name]["OVERALL"] = {
            "win_rate": round(c_wr, 2),
            "wins": c_wins,
            "games": c_total,
        }

    # Save to JSON
    with open("research/candidate_f_tournament_matrix.json", "w") as f:
        json.dump(matrix, f, indent=2)

    # Generate Markdown Table
    md = "# Candidate F Full Tournament Matchup Matrix\n\n"
    md += f"Generated at {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n"
    md += f"Total Games Evaluated: {total_tasks}\n\n"

    headers = ["Candidate", "Alakazam (Non-EX)", "Bellibolt (EX)", "Crustle (Safeguard)", "Heavy Gust Control", "Meta Breaker Aggro", "Overall WR"]
    md += "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for cand_name in candidates:
        row = [f"**{cand_name}**"]
        for opp_name in ["Alakazam_NonEX", "Bellibolt_EX", "Crustle_Safeguard", "Heavy_Gust_Control", "Meta_Breaker_Aggro"]:
            d = matrix[cand_name].get(opp_name, {})
            wr = d.get("win_rate", 0.0)
            ci_l = d.get("ci_low", 0.0)
            ci_h = d.get("ci_high", 0.0)
            row.append(f"{wr:.1f}% ({ci_l:.0f}-{ci_h:.0f}%)")
        ov = matrix[cand_name]["OVERALL"]["win_rate"]
        row.append(f"**{ov:.1f}%**")
        md += "| " + " | ".join(row) + " |\n"

    with open("reports/leaderboard_optimization/candidate_f_matchup_matrix.md", "w") as f:
        f.write(md)

    print("\n" + md)
    return matrix


if __name__ == "__main__":
    run_parallel_tournament(num_games_per_pairing=20, max_workers=8)
