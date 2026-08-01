"""
Comprehensive 1000+ Game Tournament Runner for Candidate F vs Baselines.
Evaluates Candidate B, Candidate D, Candidate E, and Candidate F variants (F0-F7)
across all opponent archetypes using the full, legal generalized engine.
"""

import os
import sys
import time
import json
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath("."))
from research.run_deck_tournament import evaluate_pairing, load_deck_from_file, create_agent_with_deck


def load_all_tournament_decks():
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
    decks = {}
    for name, path in deck_files.items():
        if os.path.exists(path):
            decks[name] = load_deck_from_file(path)
    return decks


def run_full_tournament_matrix(num_games_per_cell: int = 20):
    decks = load_all_tournament_decks()

    # Define Key Adversarial Archetype Opponents
    opponents = {
        "Alakazam_NonEX": ("F4_alakazam_swarm", decks["F4_alakazam_swarm"]),
        "Bellibolt_EX": ("Candidate_B", decks["Candidate_B"]),
        "Crustle_Safeguard": ("Candidate_D", decks["Candidate_D"]),
        "Heavy_Gust_Control": ("F3_crustle_heavy_gust", decks["F3_crustle_heavy_gust"]),
        "Meta_Breaker_Aggro": ("F7_meta_breaker_gust", decks["F7_meta_breaker_gust"]),
    }

    candidates_to_test = [
        "Candidate_B",
        "Candidate_D",
        "Candidate_E",
        "F0_crustle_baseline",
        "F1_crustle_fast_tech",
        "F2_crustle_rillaboom",
        "F3_crustle_heavy_gust",
        "F4_alakazam_swarm",
        "F5_bellibolt_pure",
        "F6_balanced_hybrid",
        "F7_meta_breaker_gust",
    ]

    results_matrix: Dict[str, Dict[str, Any]] = {}

    print(f"Starting Comprehensive Tournament ({len(candidates_to_test)} candidates x {len(opponents)} archetypes x {num_games_per_cell} games = {len(candidates_to_test)*len(opponents)*num_games_per_cell} games)...")
    t0 = time.time()

    for cand_name in candidates_to_test:
        if cand_name not in decks:
            continue
        results_matrix[cand_name] = {}
        cand_deck = decks[cand_name]
        cand_agent = create_agent_with_deck(cand_deck)

        print(f"\n--- Testing {cand_name} ---")
        total_wins = 0
        total_games = 0

        for opp_label, (opp_deck_name, opp_deck) in opponents.items():
            opp_agent = create_agent_with_deck(opp_deck)
            res = evaluate_pairing(cand_agent, opp_agent, num_games=num_games_per_cell)
            win_rate = res.get("win_rate", 0.0)
            wins = res.get("wins", 0)
            games = res.get("games", num_games_per_cell)

            total_wins += wins
            total_games += games
            results_matrix[cand_name][opp_label] = res
            print(f"  vs {opp_label:20s}: {win_rate:5.1f}% ({wins:2d}/{games:2d}) | P95: {res.get('p95_latency_ms', 0):.2f}ms | Avg Turns: {res.get('avg_turns', 0):.1f}")

        overall_wr = (total_wins / total_games * 100.0) if total_games > 0 else 0.0
        results_matrix[cand_name]["OVERALL"] = {
            "win_rate": overall_wr,
            "wins": total_wins,
            "games": total_games,
        }
        print(f"  >> {cand_name} OVERALL: {overall_wr:.1f}% ({total_wins}/{total_games})")

    elapsed = time.time() - t0
    print(f"\nTournament completed in {elapsed:.1f}s.")

    # Save JSON results
    with open("research/candidate_f_tournament_matrix.json", "w") as f:
        json.dump(results_matrix, f, indent=2)

    # Generate Markdown Table
    md_content = "# Candidate F Matchup Matrix & Benchmark Comparison\n\n"
    md_content += f"Generated at {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n"
    md_content += f"Total Games Evaluated: {len(candidates_to_test) * len(opponents) * num_games_per_cell}\n\n"

    headers = ["Candidate", "Alakazam (Non-EX)", "Bellibolt (EX)", "Crustle (Safeguard)", "Heavy Gust Control", "Meta Breaker Aggro", "Overall WR"]
    md_content += "| " + " | ".join(headers) + " |\n"
    md_content += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for cand_name in candidates_to_test:
        if cand_name not in results_matrix:
            continue
        row = [cand_name]
        for opp_label in ["Alakazam_NonEX", "Bellibolt_EX", "Crustle_Safeguard", "Heavy_Gust_Control", "Meta_Breaker_Aggro"]:
            wr = results_matrix[cand_name].get(opp_label, {}).get("win_rate", 0.0)
            row.append(f"{wr:.1f}%")
        ov = results_matrix[cand_name].get("OVERALL", {}).get("win_rate", 0.0)
        row.append(f"**{ov:.1f}%**")
        md_content += "| " + " | ".join(row) + " |\n"

    os.makedirs("reports/leaderboard_optimization", exist_ok=True)
    matrix_path = "reports/leaderboard_optimization/candidate_f_matchup_matrix.md"
    with open(matrix_path, "w") as f:
        f.write(md_content)
    print(f"Saved matchup matrix report to: {matrix_path}")

    return results_matrix


if __name__ == "__main__":
    run_full_tournament_matrix(num_games_per_cell=20)
