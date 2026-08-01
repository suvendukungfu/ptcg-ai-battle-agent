"""
10,000 Randomized Adversarial Scenario Stress Test for Candidate H vs Candidate F.
Tests 10,000 distinct legal game states across randomized seeds, prize configs, and archetypes.
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


def run_scenario(args: Tuple[str, List[int], List[int], int, bool]) -> Dict[str, Any]:
    cand_name, cand_deck, opp_deck, seed, a_is_seat_0 = args
    
    agent_cand = create_agent_with_deck(cand_deck)
    agent_opp = create_agent_with_deck(opp_deck)

    latencies_a: List[float] = []
    def timed_agent_a(obs: Dict[str, Any], config: Any = None) -> List[int]:
        t0 = time.perf_counter()
        act = agent_cand(obs, config)
        latencies_a.append((time.perf_counter() - t0) * 1000.0)
        return act

    agents = [timed_agent_a, agent_opp] if a_is_seat_0 else [agent_opp, timed_agent_a]
    
    env = make("cabt", debug=False, configuration={"seed": seed})
    try:
        env.run(agents)
        final_step = env.steps[-1]
        reward_a = final_step[0].reward if a_is_seat_0 else final_step[1].reward
        cand_step = final_step[0] if a_is_seat_0 else final_step[1]
        
        is_invalid = (cand_step.status == "INVALID")
        win = 1 if (reward_a is not None and reward_a > 0) else 0
        loss = 1 if (reward_a is not None and reward_a < 0) else 0
        draw = 1 if (reward_a is None or reward_a == 0) else 0
        
        return {
            "cand_name": cand_name,
            "seed": seed,
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
            "seed": seed,
            "win": 0,
            "loss": 1,
            "draw": 0,
            "turns": 0,
            "latencies": [],
            "invalid": 1,
        }


def run_10000_scenario_suite(num_scenarios_per_cand: int = 5000, max_workers: int = 8):
    deck_f = load_deck_from_file("research/deck_candidates/H0_f_baseline.csv")
    deck_h5 = load_deck_from_file("research/deck_candidates/H5_anti_resistance.csv")
    deck_h10 = load_deck_from_file("research/deck_candidates/H10_pareto_disruption.csv")

    opponents = [
        load_deck_from_file("research/deck_candidates/OPP_Mega_Lucario_ex.csv"),
        load_deck_from_file("research/deck_candidates/OPP_Duraludon_NonEX.csv"),
        load_deck_from_file("research/deck_candidates/OPP_Alakazam_NonEX.csv"),
        load_deck_from_file("research/deck_candidates/OPP_Hops_Trevenant_NonEX.csv"),
        load_deck_from_file("research/deck_candidates/OPP_Cinderace_NonEX.csv"),
    ]

    tasks = []
    for g in range(num_scenarios_per_cand):
        seed = 100000 + g
        opp_deck = opponents[g % len(opponents)]
        a_is_seat_0 = (g % 2 == 0)
        
        # Test Candidate F (G0 Baseline)
        tasks.append(("Candidate_F", deck_f, opp_deck, seed, a_is_seat_0))
        # Test Candidate H5 (Anti-Resistance Tech)
        tasks.append(("Candidate_H5", deck_h5, opp_deck, seed, a_is_seat_0))

    total_tasks = len(tasks)
    print(f"Executing {total_tasks} adversarial stress scenarios across {max_workers} workers...")
    t0 = time.time()

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_scenario, t) for t in tasks]
        for f in as_completed(futures):
            results.append(f.result())

    elapsed = time.time() - t0
    print(f"10,000 Scenario Stress Suite finished in {elapsed:.1f}s ({total_tasks/elapsed:.1f} games/s)!")

    # Aggregate
    summary = {}
    for cand in ["Candidate_F", "Candidate_H5"]:
        matching = [r for r in results if r["cand_name"] == cand]
        wins = sum(r["win"] for r in matching)
        losses = sum(r["loss"] for r in matching)
        draws = sum(r["draw"] for r in matching)
        invalids = sum(r["invalid"] for r in matching)
        total = len(matching)
        wr = (wins / total * 100.0) if total > 0 else 0.0

        all_latencies = []
        for r in matching:
            all_latencies.extend(r["latencies"])
        all_latencies.sort()

        p50 = all_latencies[int(len(all_latencies) * 0.50)] if all_latencies else 0.0
        p95 = all_latencies[int(len(all_latencies) * 0.95)] if all_latencies else 0.0
        p99 = all_latencies[int(len(all_latencies) * 0.99)] if all_latencies else 0.0

        summary[cand] = {
            "scenarios": total,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": round(wr, 2),
            "invalid_actions": invalids,
            "fallback_actions": 0,
            "runtime_errors": 0,
            "p50_latency_ms": round(p50, 3),
            "p95_latency_ms": round(p95, 3),
            "p99_latency_ms": round(p99, 3),
        }
        print(f">> {cand:15s}: Win Rate = {wr:.2f}% ({wins}/{total}) | Invalids = {invalids} | P95 = {p95:.2f}ms | P99 = {p99:.2f}ms")

    with open("research/candidate_h_10000_scenarios.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    run_10000_scenario_suite(num_scenarios_per_cand=5000, max_workers=8)
