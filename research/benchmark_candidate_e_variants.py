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

# Decks
E0_CRUSTLE_BASELINE = [
    344, 344, 344, 344, 345, 345, 345, 345, 1092, 1121, 1121, 1145, 1145, 1227, 1227, 1227, 1227, 1262, 1262
] + [1] * 41

E3_CRUSTLE_GUST_POFFIN = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1182, 1182, 1182, 1182,  # Boss's Orders (4)
    1121, 1121, 1121, 1121,  # Ultra Ball (4)
    1086, 1086, 1086, 1086,  # Buddy-Buddy Poffin (4)
    1227, 1227, 1227, 1227,  # Lillie's Determination (4)
    1262, 1262,              # Surfing Beach (2)
    1092,                    # Secret Box (1)
] + [1] * 33

E4_CRUSTLE_ENERGY_DENIAL = [
    344, 344, 344, 344, 345, 345, 345, 345,
    1081, 1081, 1081, 1081,  # Enhanced Hammer (4)
    1197, 1197, 1197, 1197,  # Xerosic's Machinations (4)
    1182, 1182, 1182,        # Boss's Orders (3)
    1121, 1121, 1121, 1121,  # Ultra Ball (4)
    1086, 1086, 1086, 1086,  # Buddy-Buddy Poffin (4)
    1227, 1227, 1227,        # Lillie's (3)
    1092,                    # Secret Box (1)
] + [1] * 29

E5_HYBRID_BELLIBOLT = [
    344, 344, 344, 344, 345, 345, 345, 345,
    721, 721, 721, 721, 722, 722, 722, 722,  # Bellibolt 160-DMG line
    1182, 1182, 1182,        # Boss's Orders (3)
    1086, 1086, 1086, 1086,  # Buddy-Buddy Poffin (4)
    1121, 1121, 1121, 1121,  # Ultra Ball (4)
    1227, 1227, 1227,        # Lillie's (3)
    1092,                    # Secret Box (1)
] + [3] * 29                 # Lightning Energy

# Opponent Decks
ALAKAZAM_DECK = [
    741, 741, 741, 741, 742, 742, 742, 742, 743, 743, 743, 743,
    65, 65, 66, 66, 66, 66,
    1079, 1079, 1079, 1086, 1086, 1086, 1086,
    1152, 1152, 1152, 1152, 1225, 1225, 1225, 1225, 1231, 1231, 1231, 1231,
    19, 19, 19, 19, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
]

LUCARIO_HARIYAMA_DECK = [
    678, 678, 678, 678, 677, 677, 677, 677, 673, 673, 673, 674, 674, 674, 676, 676, 676, 675, 675,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6
]

MEGA_KANGASKHAN_EX_DECK = [
    756, 756, 756, 756, 755, 755, 755, 755,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def calculate_wilson_ci(wins: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    if n == 0: return (0.0, 0.0)
    z = 1.95996 # for 95%
    p_hat = wins / n
    denominator = 1 + (z**2) / n
    centre_adjusted = p_hat + (z**2) / (2 * n)
    spread = z * math.sqrt((p_hat * (1 - p_hat) + (z**2) / (4 * n)) / n)
    lower = max(0.0, (centre_adjusted - spread) / denominator) * 100.0
    upper = min(100.0, (centre_adjusted + spread) / denominator) * 100.0
    return (lower, upper)

def evaluate_deck_variant(deck_list: List[int], deck_name: str, num_games_per_suite: int = 50):
    print(f"\n==================================================================")
    print(f"BENCHMARKING DECK VARIANT: {deck_name}")
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
        
    opponents = [
        ("1. vs Random Bot", "random"),
        ("2. vs Heuristic Bellibolt", make_bot([721]*4+[722]*4+[1121]*4+[3]*48)),
        ("3. vs EX-Heavy (Mega Kangaskhan ex)", make_bot(MEGA_KANGASKHAN_EX_DECK)),
        ("4. vs Mixed (Mega Lucario + Hariyama)", make_bot(LUCARIO_HARIYAMA_DECK)),
        ("5. vs Non-EX Swarm (Stage 2 Alakazam)", make_bot(ALAKAZAM_DECK)),
    ]
    
    env = make("cabt")
    total_wins, total_losses, total_ties = 0, 0, 0
    all_latencies = []
    suite_results = {}
    
    for label, opp in opponents:
        wins, losses, ties = 0, 0, 0
        for g in range(num_games_per_suite):
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
            
            if stat == "ERROR" or stat == "INVALID":
                losses += 1
            elif rew == 1:
                wins += 1
            elif rew == -1:
                losses += 1
            else:
                ties += 1
                
        wr = (wins / num_games_per_suite) * 100.0
        ci = calculate_wilson_ci(wins, num_games_per_suite)
        suite_results[label] = {"wins": wins, "losses": losses, "ties": ties, "wr": wr, "ci": ci}
        total_wins += wins
        total_losses += losses
        total_ties += ties
        print(f"  {label:<38}: {wr:5.1f}% ({wins}W / {losses}L / {ties}T) | 95% CI: [{ci[0]:.1f}%, {ci[1]:.1f}%]")
        
    total_games = num_games_per_suite * len(opponents)
    overall_wr = (total_wins / total_games) * 100.0
    overall_ci = calculate_wilson_ci(total_wins, total_games)
    mean_lat = statistics.mean(all_latencies) if all_latencies else 0.0
    p95_lat = statistics.quantiles(all_latencies, n=20)[18] if len(all_latencies) >= 20 else 0.0
    
    print(f"\n  OVERALL: {overall_wr:.1f}% ({total_wins}/{total_games}) | 95% CI: [{overall_ci[0]:.1f}%, {overall_ci[1]:.1f}%]")
    print(f"  Mean Latency: {mean_lat:.3f} ms | P95 Latency: {p95_lat:.3f} ms")
    
    return {
        "name": deck_name,
        "total_games": total_games,
        "wins": total_wins,
        "losses": total_losses,
        "ties": total_ties,
        "wr": overall_wr,
        "ci": overall_ci,
        "suite_results": suite_results,
        "mean_lat": mean_lat,
        "p95_lat": p95_lat,
    }

if __name__ == "__main__":
    r_e0 = evaluate_deck_variant(E0_CRUSTLE_BASELINE, "E0 (Current Crustle Baseline)", num_games_per_suite=50)
    r_e3 = evaluate_deck_variant(E3_CRUSTLE_GUST_POFFIN, "E3 (Crustle + Boss / Poffin / Ultra Ball)", num_games_per_suite=50)
    r_e4 = evaluate_deck_variant(E4_CRUSTLE_ENERGY_DENIAL, "E4 (Crustle + Hammer / Denial)", num_games_per_suite=50)
    r_e5 = evaluate_deck_variant(E5_HYBRID_BELLIBOLT, "E5 (Hybrid Crustle 4-4 + Bellibolt 4-4)", num_games_per_suite=50)
