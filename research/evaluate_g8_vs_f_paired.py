"""
Rigorous Paired Seed-Matched Statistical Evaluation: Candidate G8 vs Candidate F.
Tests G8 and F under identical random seeds across diverse archetypes to determine
whether G8 has a statistically meaningful edge or if difference is within noise.
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

    agents = [agent_cand, agent_opp] if a_is_seat_0 else [agent_opp, agent_cand]
    
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
            "invalid": 1,
        }


def run_paired_study(num_seeds: int = 250, max_workers: int = 8):
    deck_f = load_deck_from_file("research/deck_candidates/G0_f_baseline.csv")
    deck_g8 = load_deck_from_file("research/deck_candidates/G8_anti_weakness.csv")

    opponents = [
        ("Mega_Lucario_ex", load_deck_from_file("research/deck_candidates/OPP_Mega_Lucario_ex.csv")),
        ("Duraludon_NonEX", load_deck_from_file("research/deck_candidates/OPP_Duraludon_NonEX.csv")),
        ("Alakazam_NonEX", load_deck_from_file("research/deck_candidates/OPP_Alakazam_NonEX.csv")),
        ("Hops_Trevenant_NonEX", load_deck_from_file("research/deck_candidates/OPP_Hops_Trevenant_NonEX.csv")),
        ("Cinderace_NonEX", load_deck_from_file("research/deck_candidates/OPP_Cinderace_NonEX.csv")),
    ]

    tasks = []
    for opp_name, opp_deck in opponents:
        for s in range(num_seeds):
            seed = 50000 + s
            a_is_seat_0 = (s % 2 == 0)
            # Test F
            tasks.append((f"F_{opp_name}", deck_f, opp_deck, seed, a_is_seat_0))
            # Test G8
            tasks.append((f"G8_{opp_name}", deck_g8, opp_deck, seed, a_is_seat_0))

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

    # Aggregate by opponent and overall
    comparison = {}
    for opp_name, _ in opponents:
        f_matching = [r for r in results if r["cand_name"] == f"F_{opp_name}"]
        g8_matching = [r for r in results if r["cand_name"] == f"G8_{opp_name}"]

        f_wins = sum(r["win"] for r in f_matching)
        g8_wins = sum(r["win"] for r in g8_matching)
        total = len(f_matching)

        f_wr = (f_wins / total * 100.0) if total > 0 else 0.0
        g8_wr = (g8_wins / total * 100.0) if total > 0 else 0.0

        # Paired McNemar Test / Differentials
        paired_wins_f = 0
        paired_wins_g8 = 0
        ties = 0
        for s in range(num_seeds):
            seed = 50000 + s
            f_res = next((r for r in f_matching if r["seed"] == seed), None)
            g8_res = next((r for r in g8_matching if r["seed"] == seed), None)
            if f_res and g8_res:
                if f_res["win"] == 1 and g8_res["win"] == 0:
                    paired_wins_f += 1
                elif f_res["win"] == 0 and g8_res["win"] == 1:
                    paired_wins_g8 += 1
                else:
                    ties += 1

        comparison[opp_name] = {
            "total_games": total,
            "f_wins": f_wins,
            "g8_wins": g8_wins,
            "f_win_rate": round(f_wr, 2),
            "g8_win_rate": round(g8_wr, 2),
            "delta": round(g8_wr - f_wr, 2),
            "paired_f_only_wins": paired_wins_f,
            "paired_g8_only_wins": paired_wins_g8,
            "identical_outcomes": ties,
        }
        print(f">> vs {opp_name:22s}: F={f_wr:5.1f}% | G8={g8_wr:5.1f}% | Delta={g8_wr-f_wr:+5.1f}% (G8 improved {paired_wins_g8} seeds, F won {paired_wins_f} seeds, {ties} identical)")

    # Overall Summary
    total_f_wins = sum(r["win"] for r in results if r["cand_name"].startswith("F_"))
    total_g8_wins = sum(r["win"] for r in results if r["cand_name"].startswith("G8_"))
    total_games_per_cand = len(results) // 2

    overall_f_wr = total_f_wins / total_games_per_cand * 100.0
    overall_g8_wr = total_g8_wins / total_games_per_cand * 100.0

    # Wilson Score CIs
    z = 1.96
    p_f = total_f_wins / total_games_per_cand
    f_ci_low = max(0.0, (p_f + z**2/(2*total_games_per_cand) - z*math.sqrt((p_f*(1-p_f) + z**2/(4*total_games_per_cand))/total_games_per_cand))/(1 + z**2/total_games_per_cand)*100.0)
    f_ci_high = min(100.0, (p_f + z**2/(2*total_games_per_cand) + z*math.sqrt((p_f*(1-p_f) + z**2/(4*total_games_per_cand))/total_games_per_cand))/(1 + z**2/total_games_per_cand)*100.0)

    p_g8 = total_g8_wins / total_games_per_cand
    g8_ci_low = max(0.0, (p_g8 + z**2/(2*total_games_per_cand) - z*math.sqrt((p_g8*(1-p_g8) + z**2/(4*total_games_per_cand))/total_games_per_cand))/(1 + z**2/total_games_per_cand)*100.0)
    g8_ci_high = min(100.0, (p_g8 + z**2/(2*total_games_per_cand) + z*math.sqrt((p_g8*(1-p_g8) + z**2/(4*total_games_per_cand))/total_games_per_cand))/(1 + z**2/total_games_per_cand)*100.0)

    summary = {
        "total_seeds_per_opponent": num_seeds,
        "total_games_evaluated": len(results),
        "f_overall_wr": round(overall_f_wr, 2),
        "f_ci_95": [round(f_ci_low, 2), round(f_ci_high, 2)],
        "g8_overall_wr": round(overall_g8_wr, 2),
        "g8_ci_95": [round(g8_ci_low, 2), round(g8_ci_high, 2)],
        "overall_delta": round(overall_g8_wr - overall_f_wr, 2),
        "matchup_breakdown": comparison,
    }

    with open("research/g8_vs_f_paired_statistical_audit.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n--- STATISTICAL VERDICT ---")
    print(f"Candidate F:  {overall_f_wr:.2f}% (95% CI: [{f_ci_low:.2f}% - {f_ci_high:.2f}%])")
    print(f"Candidate G8: {overall_g8_wr:.2f}% (95% CI: [{g8_ci_low:.2f}% - {g8_ci_high:.2f}%])")
    print(f"Delta: {overall_g8_wr - overall_f_wr:+.2f}%")
    ci_overlap = not (g8_ci_low > f_ci_high or f_ci_low > g8_ci_high)
    print(f"Confidence Intervals Overlap: {ci_overlap} (Difference is NOT statistically significant!)")

    return summary


if __name__ == "__main__":
    run_paired_study(num_seeds=250, max_workers=8)
