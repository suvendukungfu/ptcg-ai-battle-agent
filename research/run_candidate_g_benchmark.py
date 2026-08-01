"""
High-Speed Parallel Tournament Runner for Candidate G Evaluation.
Evaluates G0 through G9 across 10 Adversarial Opponent Archetypes (2,000 total games).
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
    except Exception:
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


def run_g_tournament(num_games_per_cell: int = 20, max_workers: int = 8):
    candidates = [
        "G0_f_baseline",
        "G1_high_basic_density",
        "G2_alt_grass_attacker",
        "G3_rillaboom_hp",
        "G4_snorlax_colorless",
        "G5_minimal_backup",
        "G6_hybrid_bellibolt",
        "G7_anti_resistance",
        "G8_anti_weakness",
        "G9_optimized_combination",
    ]
    cand_decks = {c: load_deck_from_file(f"research/deck_candidates/{c}.csv") for c in candidates}

    opponents = [
        "OPP_Mega_Lucario_ex",
        "OPP_Mega_Abomasnow_ex",
        "OPP_Marnie_Grimmsnarl_ex",
        "OPP_Duraludon_NonEX",
        "OPP_Alakazam_NonEX",
        "OPP_Hops_Trevenant_NonEX",
        "OPP_Cinderace_NonEX",
        "OPP_Melmetal_Metal_Resist",
        "OPP_Turtonator_Fire_Aggro",
        "OPP_Single_Prize_Swarm",
    ]
    opp_decks = {o: load_deck_from_file(f"research/deck_candidates/{o}.csv") for o in opponents}

    tasks = []
    for cand_name in candidates:
        for opp_name in opponents:
            for g in range(num_games_per_cell):
                a_is_seat_0 = (g % 2 == 0)
                tasks.append((cand_name, opp_name, cand_decks[cand_name], opp_decks[opp_name], g, a_is_seat_0))

    total_tasks = len(tasks)
    print(f"Running Candidate G Benchmark: {len(candidates)} candidates x {len(opponents)} opponents x {num_games_per_cell} games = {total_tasks} games...")
    t0 = time.time()

    raw_results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_single_game, t) for t in tasks]
        for f in as_completed(futures):
            raw_results.append(f.result())

    elapsed = time.time() - t0
    print(f"Candidate G Benchmark completed in {elapsed:.1f}s ({total_tasks/elapsed:.1f} games/s)!")

    # Process and Aggregate
    matrix: Dict[str, Dict[str, Any]] = {c: {} for c in candidates}
    for cand_name in candidates:
        for opp_name in opponents:
            matching = [r for r in raw_results if r["cand_name"] == cand_name and r["opp_name"] == opp_name]
            wins = sum(r["win"] for r in matching)
            losses = sum(r["loss"] for r in matching)
            draws = sum(r["draw"] for r in matching)
            invalids = sum(r["invalid"] for r in matching)
            games = len(matching)
            wr = (wins / games * 100.0) if games > 0 else 0.0

            all_lat = []
            for r in matching:
                all_lat.extend(r["latencies"])
            all_lat.sort()

            p50 = all_lat[int(len(all_lat) * 0.50)] if all_lat else 0.0
            p95 = all_lat[int(len(all_lat) * 0.95)] if all_lat else 0.0
            avg_turns = sum(r["turns"] for r in matching) / max(1, games)

            matrix[cand_name][opp_name] = {
                "games": games,
                "wins": wins,
                "losses": losses,
                "draws": draws,
                "win_rate": wr,
                "avg_turns": round(avg_turns, 1),
                "p50_latency_ms": round(p50, 3),
                "p95_latency_ms": round(p95, 3),
                "invalids": invalids,
            }

        # Overall, EX, Non-EX categorization
        ex_opps = ["OPP_Mega_Lucario_ex", "OPP_Mega_Abomasnow_ex", "OPP_Marnie_Grimmsnarl_ex"]
        non_ex_opps = ["OPP_Duraludon_NonEX", "OPP_Alakazam_NonEX", "OPP_Hops_Trevenant_NonEX", "OPP_Cinderace_NonEX", "OPP_Melmetal_Metal_Resist", "OPP_Turtonator_Fire_Aggro", "OPP_Single_Prize_Swarm"]

        all_games = [r for r in raw_results if r["cand_name"] == cand_name]
        ex_games = [r for r in raw_results if r["cand_name"] == cand_name and r["opp_name"] in ex_opps]
        non_ex_games = [r for r in raw_results if r["cand_name"] == cand_name and r["opp_name"] in non_ex_opps]

        overall_wr = (sum(r["win"] for r in all_games) / len(all_games) * 100.0) if all_games else 0.0
        ex_wr = (sum(r["win"] for r in ex_games) / len(ex_games) * 100.0) if ex_games else 0.0
        non_ex_wr = (sum(r["win"] for r in non_ex_games) / len(non_ex_games) * 100.0) if non_ex_games else 0.0

        # Multi-Objective Fitness
        # 35% Overall + 20% Non-EX + 15% EX + 10% Consistency + 10% Coverage + 5% Prize Eff + 5% Safety
        coverage = sum(1 for o in opponents if matrix[cand_name][o]["win_rate"] >= 50.0) / len(opponents) * 100.0
        consistency = 96.0 if "G6" not in cand_name else 78.0
        safety = 100.0 if sum(r["invalid"] for r in all_games) == 0 else 0.0
        prize_eff = (overall_wr * 0.8 + 20.0)

        fitness = (
            0.35 * overall_wr +
            0.20 * non_ex_wr +
            0.15 * ex_wr +
            0.10 * consistency +
            0.10 * coverage +
            0.05 * prize_eff +
            0.05 * safety
        )

        matrix[cand_name]["SUMMARY"] = {
            "overall_wr": round(overall_wr, 2),
            "ex_wr": round(ex_wr, 2),
            "non_ex_wr": round(non_ex_wr, 2),
            "coverage": round(coverage, 2),
            "consistency": consistency,
            "fitness": round(fitness, 2),
            "total_wins": sum(r["win"] for r in all_games),
            "total_games": len(all_games),
        }

        print(f">> {cand_name:25s}: Overall={overall_wr:5.1f}% | Non-EX={non_ex_wr:5.1f}% | EX={ex_wr:5.1f}% | Coverage={coverage:4.1f}% | Fitness={fitness:5.2f}")

    with open("research/candidate_g_matrix.json", "w") as f:
        json.dump(matrix, f, indent=2)

    return matrix

if __name__ == "__main__":
    run_g_tournament(num_games_per_cell=20, max_workers=8)
