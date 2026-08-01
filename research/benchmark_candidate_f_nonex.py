"""
Candidate F — Non-EX Micro-Counter Research Benchmark
=====================================================

Research Variants N1-N6:
  N1: Damage Boost — Kieran supporter (+30 damage to Active Pokémon ex/V → repurpose for raw +30 any)
      Actually Kieran only boosts vs ex/V — not useful for Non-EX.
      Instead: use higher-damage Grass attackers if they exist.

  N2: Boss's Orders Gust — 2x Boss's Orders for targeting pre-evolution basics
      Deck: -2 Grass Energy, +2 Boss's Orders (1182)

  N3: Crushing Hammer Disruption — 2x Crushing Hammer for energy denial
      Deck: -2 Grass Energy, +2 Crushing Hammer (1120)

  N4: Boss + Crushing Combined — 2 Boss's Orders + 2 Crushing Hammer  
      Deck: -4 Grass Energy, +2 Boss's Orders (1182), +2 Crushing Hammer (1120)

  N5: Boss + Extra Ultra Ball consistency — 2 Boss's Orders + 2 Ultra Ball
      Deck: -4 Grass Energy, +2 Boss's Orders (1182), +2 Ultra Ball (1121)

  N6: Maximum Trainer Package — 2 Boss + 2 Crushing + 2 Ultra Ball
      Deck: -6 Grass Energy, +2 Boss (1182), +2 Crushing (1120), +2 Ultra Ball (1121)

All variants preserve:
  - Pure Grass energy base
  - 4x Dwebble / 4x Crustle core
  - No additional Pokémon lines (no brick risk)
  - AI code is UNCHANGED

Key test: Do disruption/gust tools allow the existing Crustle engine 
to overcome the 140-HP Non-EX breakpoint by sniping pre-evolutions?
"""

import time
import math
import statistics
import sys
import os
import json
from typing import Dict, Any, List, Tuple
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.card_database import init_card_database
from agent.utils import reset_diagnostics, get_diagnostics
from agent.action_selector import select_action, select_heuristic_action
from agent.state import parse_game_state

init_card_database()

# =======================================================================
# REFERENCE: E0 BASELINE (Current Candidate D production deck)
# =======================================================================
E0_BASELINE = [
    344, 344, 344, 344,   # Dwebble x4
    345, 345, 345, 345,   # Crustle x4
    1092,                 # Secret Box x1
    1121, 1121,           # Ultra Ball x2
    1145, 1145,           # Mega Signal x2
    1227, 1227, 1227, 1227,  # Lillie's Determination x4
    1262, 1262,           # Surfing Beach x2
] + [1] * 41              # Grass Energy x41

# =======================================================================
# MICRO-VARIANTS N2-N6 (Trainer-only substitutions, no new Pokémon)
# =======================================================================

# N2: Boss's Orders Gust Package
N2_BOSS_GUST = [
    344, 344, 344, 344,
    345, 345, 345, 345,
    1092,
    1121, 1121,
    1145, 1145,
    1182, 1182,              # Boss's Orders x2 (NEW)
    1227, 1227, 1227, 1227,
    1262, 1262,
] + [1] * 39                 # Grass Energy x39 (-2)

# N3: Crushing Hammer Disruption
N3_CRUSHING = [
    344, 344, 344, 344,
    345, 345, 345, 345,
    1092,
    1120, 1120,              # Crushing Hammer x2 (NEW)
    1121, 1121,
    1145, 1145,
    1227, 1227, 1227, 1227,
    1262, 1262,
] + [1] * 39                 # Grass Energy x39 (-2)

# N4: Boss + Crushing Combined
N4_BOSS_CRUSH = [
    344, 344, 344, 344,
    345, 345, 345, 345,
    1092,
    1120, 1120,              # Crushing Hammer x2 (NEW)
    1121, 1121,
    1145, 1145,
    1182, 1182,              # Boss's Orders x2 (NEW)
    1227, 1227, 1227, 1227,
    1262, 1262,
] + [1] * 37                 # Grass Energy x37 (-4)

# N5: Boss + Extra Consistency (more Ultra Ball)
N5_BOSS_BALL = [
    344, 344, 344, 344,
    345, 345, 345, 345,
    1092,
    1121, 1121, 1121, 1121,  # Ultra Ball x4 (+2)
    1145, 1145,
    1182, 1182,              # Boss's Orders x2 (NEW)
    1227, 1227, 1227, 1227,
    1262, 1262,
] + [1] * 37                 # Grass Energy x37 (-4)

# N6: Maximum Trainer Package
N6_MAX_TRAINER = [
    344, 344, 344, 344,
    345, 345, 345, 345,
    1092,
    1120, 1120,              # Crushing Hammer x2
    1121, 1121, 1121, 1121,  # Ultra Ball x4 (+2)
    1145, 1145,
    1182, 1182,              # Boss's Orders x2
    1227, 1227, 1227, 1227,
    1262, 1262,
] + [1] * 35                 # Grass Energy x35 (-6)

# Validate all decks
ALL_VARIANTS = {
    "E0 (Baseline)": E0_BASELINE,
    "N2 (Boss Gust)": N2_BOSS_GUST,
    "N3 (Crushing Hammer)": N3_CRUSHING,
    "N4 (Boss + Crushing)": N4_BOSS_CRUSH,
    "N5 (Boss + Ultra Ball)": N5_BOSS_BALL,
    "N6 (Max Trainer)": N6_MAX_TRAINER,
}

for name, deck in ALL_VARIANTS.items():
    assert len(deck) == 60, f"{name} has {len(deck)} cards, expected 60"
    grass_count = deck.count(1)
    print(f"✓ {name}: 60 cards, {grass_count} Grass Energy")

# =======================================================================
# OPPONENT SUITES (same as Candidate E study for comparability)
# =======================================================================

# Pure Non-EX Alakazam Stage 2 Swarm
NON_EX_SWARM_DECK = [
    741, 741, 741, 741, 742, 742, 742, 742, 743, 743, 743, 743,
    65, 65, 66, 66, 66, 66,
    1079, 1079, 1079, 1086, 1086, 1086, 1086,
    1152, 1152, 1152, 1152, 1225, 1225, 1225, 1225, 1231, 1231, 1231, 1231,
    19, 19, 19, 19
] + [5] * 21

# Standard Heuristic Bellibolt (EX aggro baseline)
HEURISTIC_BELLIBOLT_DECK = [721]*4 + [722]*4 + [1121]*4 + [3]*48

# Mixed EX/Non-EX Aggro (Lucario/Hariyama)
MIXED_DECK = [
    678, 678, 678, 678, 677, 677, 677, 677, 673, 673, 673, 674, 674, 674, 676, 676, 676, 675, 675,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159
] + [6] * 13

def calculate_wilson_ci(wins: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    if n == 0: return (0.0, 0.0)
    z = 1.95996
    p_hat = wins / n
    denominator = 1 + (z**2) / n
    centre_adjusted = p_hat + (z**2) / (2 * n)
    spread = z * math.sqrt((p_hat * (1 - p_hat) + (z**2) / (4 * n)) / n)
    lower = max(0.0, (centre_adjusted - spread) / denominator) * 100.0
    upper = min(100.0, (centre_adjusted + spread) / denominator) * 100.0
    return (lower, upper)

def run_suite(deck_list: List[int], deck_name: str, n_per_suite: int = 30):
    print(f"\n{'='*70}")
    print(f"BENCHMARKING: {deck_name}")
    print(f"{'='*70}")

    def test_agent(obs, config=None):
        if obs.get("select") is None:
            return list(deck_list)
        return select_action(obs)

    def make_bot(deck):
        def bot(obs, config=None):
            if obs.get("select") is None:
                return list(deck)
            state = parse_game_state(obs)
            return select_heuristic_action(state)
        return bot

    suites = [
        ("vs Non-EX Swarm (Alakazam)", make_bot(NON_EX_SWARM_DECK)),
        ("vs Standard Heuristic (Bellibolt)", make_bot(HEURISTIC_BELLIBOLT_DECK)),
        ("vs Mixed Aggro (Lucario)", make_bot(MIXED_DECK)),
    ]

    env = make("cabt")
    results = {}
    total_wins, total_games = 0, 0
    all_latencies = []
    all_illegals = 0

    for label, opp in suites:
        wins, losses, ties = 0, 0, 0
        suite_illegals = 0
        t0 = time.time()
        
        for g in range(n_per_suite):
            reset_diagnostics()
            if g % 2 == 0:
                agents = [test_agent, opp]
                our_idx = 0
            else:
                agents = [opp, test_agent]
                our_idx = 1
            steps = env.run(agents)
            rew = steps[-1][our_idx].reward
            stat = steps[-1][our_idx].status

            diag = get_diagnostics()
            lat = diag.get("avg_decision_time_ms", 0.0)
            if lat > 0: all_latencies.append(lat)
            il = diag.get("illegal_actions", 0)
            suite_illegals += il

            if stat in ("ERROR", "INVALID"):
                losses += 1
            elif rew == 1:
                wins += 1
            elif rew == -1:
                losses += 1
            else:
                ties += 1

        elapsed = time.time() - t0
        wr = (wins / n_per_suite) * 100.0
        ci = calculate_wilson_ci(wins, n_per_suite)
        results[label] = {"wins": wins, "losses": losses, "ties": ties, "wr": wr, "ci": ci, "illegals": suite_illegals}
        total_wins += wins
        total_games += n_per_suite
        all_illegals += suite_illegals
        print(f"  {label:<40}: {wr:5.1f}% ({wins}W/{losses}L/{ties}T) CI:[{ci[0]:.1f}%,{ci[1]:.1f}%] | Illegals:{suite_illegals} | {elapsed:.1f}s")

    overall_wr = (total_wins / total_games) * 100.0
    overall_ci = calculate_wilson_ci(total_wins, total_games)
    mean_lat = statistics.mean(all_latencies) if all_latencies else 0.0

    print(f"\n  OVERALL: {overall_wr:.1f}% ({total_wins}/{total_games}) CI:[{overall_ci[0]:.1f}%,{overall_ci[1]:.1f}%] | Illegals:{all_illegals} | Lat:{mean_lat:.1f}ms")

    return {
        "name": deck_name,
        "results": results,
        "overall_wr": overall_wr,
        "overall_ci": overall_ci,
        "mean_lat": mean_lat,
        "total_illegals": all_illegals,
    }

# =======================================================================
# MAIN: Run all variants
# =======================================================================
if __name__ == "__main__":
    N_PER = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    
    print(f"\n{'#'*70}")
    print(f"# CANDIDATE F — NON-EX MICRO-COUNTER RESEARCH BENCHMARK")
    print(f"# Games per suite: {N_PER} | Total suites: 3 | Variants: 6")
    print(f"# Total games: {N_PER * 3 * 6}")
    print(f"{'#'*70}")
    
    all_results = {}
    for vname, vdeck in ALL_VARIANTS.items():
        r = run_suite(vdeck, vname, n_per_suite=N_PER)
        all_results[vname] = r
    
    # Print Pareto analysis
    print(f"\n\n{'='*70}")
    print(f"PARETO ANALYSIS — NON-EX GAIN vs EX REGRESSION")
    print(f"{'='*70}")
    print(f"{'Variant':<25} {'Non-EX WR':>10} {'Bellibolt WR':>12} {'Mixed WR':>10} {'Overall':>10} {'Illegals':>8}")
    print(f"{'-'*25} {'-'*10} {'-'*12} {'-'*10} {'-'*10} {'-'*8}")
    
    e0_nonex = all_results["E0 (Baseline)"]["results"]["vs Non-EX Swarm (Alakazam)"]["wr"]
    e0_belli = all_results["E0 (Baseline)"]["results"]["vs Standard Heuristic (Bellibolt)"]["wr"]
    
    for vname, r in all_results.items():
        nonex_wr = r["results"]["vs Non-EX Swarm (Alakazam)"]["wr"]
        belli_wr = r["results"]["vs Standard Heuristic (Bellibolt)"]["wr"]
        mixed_wr = r["results"]["vs Mixed Aggro (Lucario)"]["wr"]
        overall = r["overall_wr"]
        illegals = r["total_illegals"]
        
        nonex_delta = nonex_wr - e0_nonex
        belli_delta = belli_wr - e0_belli
        
        marker = ""
        if nonex_delta > 5 and belli_delta >= -5:
            marker = " ★ PARETO"
        elif nonex_delta > 0 and belli_delta < -10:
            marker = " ✗ REGRESSION"
        
        print(f"{vname:<25} {nonex_wr:>9.1f}% {belli_wr:>11.1f}% {mixed_wr:>9.1f}% {overall:>9.1f}% {illegals:>7}{marker}")
    
    # Save results JSON
    output_path = "research/candidate_f_benchmark_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")
