import time
import math
import statistics
import sys
import os
from typing import Dict, Any, List, Tuple
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.card_database import init_card_database
from agent.utils import reset_diagnostics, get_diagnostics
from agent.action_selector import select_action, select_heuristic_action
from agent.state import parse_game_state

init_card_database()

# Candidate Decks
E0_BASELINE = [
    344, 344, 344, 344, 345, 345, 345, 345, 1092, 1121, 1121, 1145, 1145, 1227, 1227, 1227, 1227, 1262, 1262
] + [1] * 41

E3_GUST_CONTROL = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1182, 1182, 1182, 1182,  # Boss's Orders (4)
    1121, 1121, 1121, 1121,  # Ultra Ball (4)
    1086, 1086, 1086, 1086,  # Buddy-Buddy Poffin (4)
    1227, 1227, 1227, 1227,  # Lillie's Determination (4)
    1262, 1262,              # Surfing Beach (2)
    1092,                    # Secret Box (1)
] + [1] * 33

E4_ENERGY_DENIAL = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1081, 1081, 1081, 1081,  # Enhanced Hammer (4)
    1197, 1197, 1197, 1197,  # Xerosic's Machinations (4)
    1182, 1182, 1182,        # Boss's Orders (3)
    1121, 1121, 1121, 1121,  # Ultra Ball (4)
    1086, 1086, 1086, 1086,  # Buddy-Buddy Poffin (4)
    1227, 1227, 1227,        # Lillie's (3)
    1092,                    # Secret Box (1)
] + [1] * 29

# Opponent Test Suites
EX_HEAVY_DECK = [
    756, 756, 756, 756, 755, 755, 755, 755,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159
] + [0] * 24

NON_EX_SWARM_DECK = [
    741, 741, 741, 741, 742, 742, 742, 742, 743, 743, 743, 743,
    65, 65, 66, 66, 66, 66,
    1079, 1079, 1079, 1086, 1086, 1086, 1086,
    1152, 1152, 1152, 1152, 1225, 1225, 1225, 1225, 1231, 1231, 1231, 1231,
    19, 19, 19, 19
] + [5] * 21

MIXED_DECK = [
    678, 678, 678, 678, 677, 677, 677, 677, 673, 673, 673, 674, 674, 674, 676, 676, 676, 675, 675,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159
] + [6] * 13

HEURISTIC_BELLIBOLT_DECK = [721]*4 + [722]*4 + [1121]*4 + [3]*48

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

def run_suite(deck_list: List[int], deck_name: str, n_per_suite: int = 50):
    print(f"\n==================================================================")
    print(f"BENCHMARKING: {deck_name} (Total: {n_per_suite * 4} Games)")
    print(f"==================================================================")
    
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
        ("1. EX-Heavy (Mega Kangaskhan)", make_bot(EX_HEAVY_DECK)),
        ("2. Non-EX Swarm (Stage 2 Alakazam)", make_bot(NON_EX_SWARM_DECK)),
        ("3. Mixed EX/Non-EX (Lucario/Hariyama)", make_bot(MIXED_DECK)),
        ("4. Standard Heuristic (Bellibolt)", make_bot(HEURISTIC_BELLIBOLT_DECK)),
    ]
    
    env = make("cabt")
    results = {}
    total_wins, total_games = 0, 0
    all_latencies = []
    
    for label, opp in suites:
        wins, losses, ties = 0, 0, 0
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
            
            if stat in ("ERROR", "INVALID"):
                losses += 1
            elif rew == 1:
                wins += 1
            elif rew == -1:
                losses += 1
            else:
                ties += 1
                
        wr = (wins / n_per_suite) * 100.0
        ci = calculate_wilson_ci(wins, n_per_suite)
        results[label] = {"wins": wins, "losses": losses, "ties": ties, "wr": wr, "ci": ci}
        total_wins += wins
        total_games += n_per_suite
        print(f"  {label:<40}: {wr:5.1f}% ({wins}W/{losses}L/{ties}T) | 95% CI: [{ci[0]:.1f}%, {ci[1]:.1f}%]")
        
    overall_wr = (total_wins / total_games) * 100.0
    overall_ci = calculate_wilson_ci(total_wins, total_games)
    mean_lat = statistics.mean(all_latencies) if all_latencies else 0.0
    p95_lat = statistics.quantiles(all_latencies, n=20)[18] if len(all_latencies) >= 20 else 0.0
    
    print(f"\n  OVERALL WIN RATE: {overall_wr:.1f}% ({total_wins}/{total_games}) | 95% CI: [{overall_ci[0]:.1f}%, {overall_ci[1]:.1f}%]")
    print(f"  Mean Latency: {mean_lat:.3f} ms | P95 Latency: {p95_lat:.3f} ms")
    
    return {
        "name": deck_name,
        "results": results,
        "overall_wr": overall_wr,
        "overall_ci": overall_ci,
        "mean_lat": mean_lat,
        "p95_lat": p95_lat,
    }

if __name__ == "__main__":
    r_e0 = run_suite(E0_BASELINE, "E0 (Current Baseline Crustle)", n_per_suite=50)
    r_e3 = run_suite(E3_GUST_CONTROL, "E3 (Crustle + Gust/Poffin Package)", n_per_suite=50)
    r_e4 = run_suite(E4_ENERGY_DENIAL, "E4 (Crustle + Energy Denial Package)", n_per_suite=50)
