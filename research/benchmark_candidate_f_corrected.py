"""
Candidate F — Non-EX Micro-Counter Research Benchmark (CORRECTED)
=================================================================
FIX: Non-EX Swarm deck corrected to exactly 60 cards.
The original deck had 62 cards causing INVALID bot status.
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
# CANDIDATE DECKS
# =======================================================================
E0_BASELINE = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1092, 1121, 1121, 1145, 1145,
    1227, 1227, 1227, 1227, 1262, 1262,
] + [1] * 41

N2_BOSS_GUST = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1092, 1121, 1121, 1145, 1145,
    1182, 1182,
    1227, 1227, 1227, 1227, 1262, 1262,
] + [1] * 39

N3_CRUSHING = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1092, 1120, 1120, 1121, 1121, 1145, 1145,
    1227, 1227, 1227, 1227, 1262, 1262,
] + [1] * 39

N4_BOSS_CRUSH = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1092, 1120, 1120, 1121, 1121, 1145, 1145,
    1182, 1182,
    1227, 1227, 1227, 1227, 1262, 1262,
] + [1] * 37

N5_BOSS_BALL = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1092, 1121, 1121, 1121, 1121, 1145, 1145,
    1182, 1182,
    1227, 1227, 1227, 1227, 1262, 1262,
] + [1] * 37

N6_MAX_TRAINER = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1092, 1120, 1120, 1121, 1121, 1121, 1121, 1145, 1145,
    1182, 1182,
    1227, 1227, 1227, 1227, 1262, 1262,
] + [1] * 35

# =======================================================================
# CORRECTED OPPONENT DECKS (all verified = 60 cards)
# =======================================================================

# Non-EX Swarm: Abra/Kadabra/Alakazam + Dunsparce/Dudunsparce
# CORRECTED: was 62 cards, now 60 (-2 Psychic Energy)
NON_EX_SWARM_DECK = [
    741, 741, 741, 741,     # Abra x4 (Basic, 50HP)
    742, 742, 742, 742,     # Kadabra x4 (Stage 1)
    743, 743, 743, 743,     # Alakazam x4 (Stage 2, 140HP)
    65, 65,                 # Dunsparce x2 (Basic)
    66, 66, 66, 66,         # Dudunsparce x4 (Stage 1)
    1079, 1079, 1079,       # Rare Candy x3
    1086, 1086, 1086, 1086, # Buddy-Buddy Poffin x4
    1152, 1152, 1152, 1152, # Poké Pad x4
    1225, 1225, 1225, 1225, # Hilda x4
    1231, 1231, 1231, 1231, # Dawn x4
] + [5] * 19                # Psychic Energy x19 (CORRECTED: was 21+4=25, now 19)
# Total: 4+4+4+2+4+3+4+4+4+4+19 = 56... need to check

_nonex_count = len(NON_EX_SWARM_DECK)
if _nonex_count != 60:
    # Adjust energy to hit exactly 60
    NON_EX_SWARM_DECK = [
        741, 741, 741, 741,
        742, 742, 742, 742,
        743, 743, 743, 743,
        65, 65,
        66, 66, 66, 66,
        1079, 1079, 1079,
        1086, 1086, 1086, 1086,
        1152, 1152, 1152, 1152,
        1225, 1225, 1225, 1225,
        1231, 1231, 1231, 1231,
    ]
    _pokemon_trainers = len(NON_EX_SWARM_DECK)
    _energy_needed = 60 - _pokemon_trainers
    NON_EX_SWARM_DECK += [5] * _energy_needed
    print(f"Non-EX Swarm: {_pokemon_trainers} pokemon+trainers + {_energy_needed} energy = {len(NON_EX_SWARM_DECK)} total")

# Standard Heuristic Bellibolt (EX aggro)
HEURISTIC_BELLIBOLT_DECK = [721]*4 + [722]*4 + [1121]*4 + [3]*48

# Mixed EX/Non-EX (Lucario)
MIXED_DECK = [
    678, 678, 678, 678, 677, 677, 677, 677, 673, 673, 673, 674, 674, 674, 676, 676, 676, 675, 675,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159
] + [6] * 13

# Validate
ALL_VARIANTS = {
    "E0 (Baseline)": E0_BASELINE,
    "N2 (Boss Gust)": N2_BOSS_GUST,
    "N3 (Crushing)": N3_CRUSHING,
    "N4 (Boss+Crush)": N4_BOSS_CRUSH,
    "N5 (Boss+Ball)": N5_BOSS_BALL,
    "N6 (Max Trainer)": N6_MAX_TRAINER,
}

for name, deck in ALL_VARIANTS.items():
    assert len(deck) == 60, f"{name} has {len(deck)} cards"
    print(f"✓ {name}: 60 cards, {deck.count(1)} Grass Energy")

assert len(NON_EX_SWARM_DECK) == 60, f"Non-EX Swarm has {len(NON_EX_SWARM_DECK)} cards"
assert len(HEURISTIC_BELLIBOLT_DECK) == 60
assert len(MIXED_DECK) == 60
print(f"✓ All opponent decks validated at 60 cards")

def calculate_wilson_ci(wins, n, confidence=0.95):
    if n == 0: return (0.0, 0.0)
    z = 1.95996
    p_hat = wins / n
    denominator = 1 + (z**2) / n
    centre_adjusted = p_hat + (z**2) / (2 * n)
    spread = z * math.sqrt((p_hat * (1 - p_hat) + (z**2) / (4 * n)) / n)
    lower = max(0.0, (centre_adjusted - spread) / denominator) * 100.0
    upper = min(100.0, (centre_adjusted + spread) / denominator) * 100.0
    return (lower, upper)

def run_suite(deck_list, deck_name, n_per_suite=30):
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
        wins, losses, ties, invalid_count = 0, 0, 0, 0
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

            opp_stat = steps[-1][1 - our_idx].status
            if opp_stat == "INVALID":
                invalid_count += 1

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
        results[label] = {
            "wins": wins, "losses": losses, "ties": ties,
            "wr": wr, "ci": ci, "illegals": suite_illegals,
            "opp_invalids": invalid_count,
        }
        total_wins += wins
        total_games += n_per_suite
        all_illegals += suite_illegals
        inv_str = f" OppInvalid:{invalid_count}" if invalid_count > 0 else ""
        print(f"  {label:<40}: {wr:5.1f}% ({wins}W/{losses}L/{ties}T) CI:[{ci[0]:.1f}%,{ci[1]:.1f}%] | Illegals:{suite_illegals}{inv_str} | {elapsed:.1f}s")

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

if __name__ == "__main__":
    N_PER = int(sys.argv[1]) if len(sys.argv) > 1 else 30

    print(f"\n{'#'*70}")
    print(f"# CANDIDATE F — CORRECTED NON-EX MICRO-COUNTER BENCHMARK")
    print(f"# Games per suite: {N_PER} | Suites: 3 | Variants: 6")
    print(f"# Total games: {N_PER * 3 * 6}")
    print(f"{'#'*70}")

    all_results = {}
    for vname, vdeck in ALL_VARIANTS.items():
        r = run_suite(vdeck, vname, n_per_suite=N_PER)
        all_results[vname] = r

    # Pareto table
    print(f"\n\n{'='*70}")
    print(f"PARETO ANALYSIS — NON-EX GAIN vs EX REGRESSION")
    print(f"{'='*70}")
    print(f"{'Variant':<22} {'Non-EX':>8} {'Bellibolt':>10} {'Mixed':>8} {'Overall':>8} {'Illegals':>8}")
    print(f"{'-'*22} {'-'*8} {'-'*10} {'-'*8} {'-'*8} {'-'*8}")

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
            marker = " ✗ REGRESS"

        print(f"{vname:<22} {nonex_wr:>7.1f}% {belli_wr:>9.1f}% {mixed_wr:>7.1f}% {overall:>7.1f}% {illegals:>7}{marker}")

    output_path = "research/candidate_f_benchmark_corrected.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")
