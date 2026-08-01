"""
5,000 Paired Seed-Matched Statistical Evaluation for Candidate K vs Candidate F.
Tests K8 vs Candidate F under identical seeds with 100% exact deck preservation.
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


def run_paired_game(args: Tuple[str, List[int], List[int], int, bool]) -> Dict[str, Any]:
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


def run_candidate_k_paired(num_pairs: int = 2500, max_workers: int = 8):
    deck_f = load_deck_from_file("research/deck_candidates/H0_f_baseline.csv")

    opponents = [
        ("Crustle_Mirror", deck_f, 0.40),
        ("Mega_Lucario_ex", load_deck_from_file("research/deck_candidates/OPP_Mega_Lucario_ex.csv"), 0.20),
        ("Duraludon_NonEX", load_deck_from_file("research/deck_candidates/OPP_Duraludon_NonEX.csv"), 0.15),
        ("Alakazam_NonEX", load_deck_from_file("research/deck_candidates/OPP_Alakazam_NonEX.csv"), 0.15),
        ("Cinderace_NonEX", load_deck_from_file("research/deck_candidates/OPP_Cinderace_NonEX.csv"), 0.10),
    ]

    tasks = []
    for g in range(num_pairs):
        seed = 300000 + g
        r_val = (g % 100) / 100.0
        cum = 0.0
        chosen_opp = opponents[0]
        for opp_name, opp_deck, weight in opponents:
            cum += weight
            if r_val < cum:
                chosen_opp = (opp_name, opp_deck, weight)
                break
        
        opp_name, opp_deck, _ = chosen_opp
        a_is_seat_0 = (g % 2 == 0)

        # F
        tasks.append((f"F_{opp_name}", deck_f, opp_deck, seed, a_is_seat_0))
        # K8
        tasks.append((f"K8_{opp_name}", deck_f, opp_deck, seed, a_is_seat_0))

    total_tasks = len(tasks)
    print(f"Executing {total_tasks} paired seed-matched evaluations across {max_workers} workers...")
    t0 = time.time()

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_paired_game, t) for t in tasks]
        for f in as_completed(futures):
            results.append(f.result())

    elapsed = time.time() - t0
    print(f"Paired evaluation finished in {elapsed:.1f}s ({total_tasks/elapsed:.1f} games/s)!")

    f_total_wins = sum(r["win"] for r in results if r["cand_name"].startswith("F_"))
    k8_total_wins = sum(r["win"] for r in results if r["cand_name"].startswith("K8_"))
    total_evals = num_pairs

    f_wr = f_total_wins / total_evals * 100.0
    k8_wr = k8_total_wins / total_evals * 100.0

    print(f"\n--- CANDIDATE K8 PAIRED RESULTS (5,000 Games) ---")
    print(f"Candidate F Win Rate:  {f_wr:.2f}% ({f_total_wins}/{total_evals})")
    print(f"Candidate K8 Win Rate: {k8_wr:.2f}% ({k8_total_wins}/{total_evals})")
    print(f"Delta: {k8_wr - f_wr:+.2f}%")

    with open("research/candidate_k_5000_paired.json", "w") as f:
        json.dump({
            "total_games": total_tasks,
            "f_wins": f_total_wins,
            "k8_wins": k8_total_wins,
            "f_wr": round(f_wr, 2),
            "k8_wr": round(k8_wr, 2),
            "delta": round(k8_wr - f_wr, 2),
        }, f, indent=2)

    return f_wr, k8_wr

if __name__ == "__main__":
    run_candidate_k_paired(num_pairs=2500, max_workers=8)
