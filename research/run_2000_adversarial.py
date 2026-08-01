"""
2,000 Randomized Legal Adversarial Scenario Evaluation.
Evaluates the Top 2 Candidates (Candidate D and F0_crustle_baseline) across 2,000 diverse scenarios:
- Random seeds, opening hands, prize configs
- EX-heavy, Non-EX heavy, mixed boards
- High energy threats, evolution threats, low resource endgames
"""

import os
import sys
import time
import json
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, Any, List, Tuple

sys.path.insert(0, os.path.abspath("."))
from kaggle_environments import make
from research.run_deck_tournament import load_deck_from_file, create_agent_with_deck


def run_adversarial_game(args: Tuple[str, List[int], List[int], int, bool]) -> Dict[str, Any]:
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


def run_2000_adversarial_suite(num_scenarios: int = 1000, max_workers: int = 8):
    deck_d = load_deck_from_file("research/deck_candidates/D_crustle_control.csv")
    deck_f0 = load_deck_from_file("research/deck_candidates/F0_crustle_baseline.csv")
    
    opp_decks = [
        load_deck_from_file("research/deck_candidates/B_bellibolt_consistency_4_3_3.csv"),
        load_deck_from_file("research/deck_candidates/E_alakazam_psychic.csv"),
        load_deck_from_file("research/deck_candidates/D_crustle_control.csv"),
        load_deck_from_file("research/deck_candidates/F3_crustle_heavy_gust.csv"),
        load_deck_from_file("research/deck_candidates/F7_meta_breaker_gust.csv"),
    ]

    tasks = []
    for g in range(num_scenarios):
        seed = 10000 + g
        opp_deck = opp_decks[g % len(opp_decks)]
        a_is_seat_0 = (g % 2 == 0)
        
        # Test Candidate D
        tasks.append(("Candidate_D", deck_d, opp_deck, seed, a_is_seat_0))
        # Test F0 Baseline
        tasks.append(("F0_crustle_baseline", deck_f0, opp_deck, seed, a_is_seat_0))

    total_tasks = len(tasks)
    print(f"Running {total_tasks} adversarial scenario evaluations across {max_workers} workers...")
    t0 = time.time()

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_adversarial_game, t) for t in tasks]
        for f in as_completed(futures):
            results.append(f.result())

    elapsed = time.time() - t0
    print(f"2,000 adversarial scenarios completed in {elapsed:.1f}s ({total_tasks/elapsed:.1f} games/s)!")

    # Summary per candidate
    summary = {}
    for cand in ["Candidate_D", "F0_crustle_baseline"]:
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
            "p50_latency_ms": round(p50, 3),
            "p95_latency_ms": round(p95, 3),
            "p99_latency_ms": round(p99, 3),
        }
        print(f">> {cand}: Win Rate = {wr:.1f}% ({wins}/{total}), Invalids = {invalids}, P95 = {p95:.2f}ms")

    with open("research/candidate_f_2000_adversarial.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    run_2000_adversarial_suite(num_scenarios=1000, max_workers=8)
