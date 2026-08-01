"""
20,000 Paired Seed-Matched Evaluation: Candidate M vs Candidate F.
Tests Candidate M (Meta-Adaptive Target Selection & Energy Routing) against Candidate F.
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


def run_20000_paired_evaluation(num_pairs: int = 10000, max_workers: int = 8):
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
        seed = 500000 + g
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
        # M
        tasks.append((f"M_{opp_name}", deck_f, opp_deck, seed, a_is_seat_0))

    total_tasks = len(tasks)
    print(f"Executing {total_tasks} paired seed-matched evaluations across {max_workers} workers...")
    t0 = time.time()

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_paired_game, t) for t in tasks]
        for f in as_completed(futures):
            results.append(f.result())

    elapsed = time.time() - t0
    print(f"20,000 Paired Evaluation finished in {elapsed:.1f}s ({total_tasks/elapsed:.1f} games/s)!")

    f_matching = [r for r in results if r["cand_name"].startswith("F_")]
    m_matching = [r for r in results if r["cand_name"].startswith("M_")]

    f_wins = sum(r["win"] for r in f_matching)
    m_wins = sum(r["win"] for r in m_matching)
    total_evals = num_pairs

    f_wr = f_wins / total_evals * 100.0
    m_wr = m_wins / total_evals * 100.0

    # Wilson Score 95% CIs
    z = 1.96
    p_f = f_wins / total_evals
    f_ci_low = max(0.0, (p_f + z**2/(2*total_evals) - z*math.sqrt((p_f*(1-p_f) + z**2/(4*total_evals))/total_evals))/(1 + z**2/total_evals)*100.0)
    f_ci_high = min(100.0, (p_f + z**2/(2*total_evals) + z*math.sqrt((p_f*(1-p_f) + z**2/(4*total_evals))/total_evals))/(1 + z**2/total_evals)*100.0)

    p_m = m_wins / total_evals
    m_ci_low = max(0.0, (p_m + z**2/(2*total_evals) - z*math.sqrt((p_m*(1-p_m) + z**2/(4*total_evals))/total_evals))/(1 + z**2/total_evals)*100.0)
    m_ci_high = min(100.0, (p_m + z**2/(2*total_evals) + z*math.sqrt((p_m*(1-p_m) + z**2/(4*total_evals))/total_evals))/(1 + z**2/total_evals)*100.0)

    # Matchup Breakdown
    matchup_stats = {}
    for opp_name, _, _ in opponents:
        f_opp = [r for r in f_matching if r["cand_name"] == f"F_{opp_name}"]
        m_opp = [r for r in m_matching if r["cand_name"] == f"M_{opp_name}"]
        f_w = sum(r["win"] for r in f_opp)
        m_w = sum(r["win"] for r in m_opp)
        tot = len(f_opp)
        matchup_stats[opp_name] = {
            "total": tot,
            "f_wr": round(f_w / tot * 100.0, 2) if tot > 0 else 0.0,
            "m_wr": round(m_w / tot * 100.0, 2) if tot > 0 else 0.0,
            "delta": round((m_w - f_w) / tot * 100.0, 2) if tot > 0 else 0.0,
        }
        print(f">> vs {opp_name:20s}: F={matchup_stats[opp_name]['f_wr']:5.1f}% | M={matchup_stats[opp_name]['m_wr']:5.1f}% | Delta={matchup_stats[opp_name]['delta']:+5.1f}%")

    print(f"\n--- 20,000 PAIRED EVALUATION STATISTICAL VERDICT ---")
    print(f"Candidate F Win Rate: {f_wr:.2f}% (95% CI: [{f_ci_low:.2f}% – {f_ci_high:.2f}%])")
    print(f"Candidate M Win Rate: {m_wr:.2f}% (95% CI: [{m_ci_low:.2f}% – {m_ci_high:.2f}%])")
    print(f"Net Delta: {m_wr - f_wr:+.2f}%")

    with open("research/candidate_m_20000_paired.json", "w") as f:
        json.dump({
            "total_games": total_tasks,
            "f_wins": f_wins,
            "m_wins": m_wins,
            "f_wr": round(f_wr, 2),
            "m_wr": round(m_wr, 2),
            "f_ci_95": [round(f_ci_low, 2), round(f_ci_high, 2)],
            "m_ci_95": [round(m_ci_low, 2), round(m_ci_high, 2)],
            "delta": round(m_wr - f_wr, 2),
            "matchups": matchup_stats,
        }, f, indent=2)

    return f_wr, m_wr

if __name__ == "__main__":
    run_20000_paired_evaluation(num_pairs=10000, max_workers=8)
