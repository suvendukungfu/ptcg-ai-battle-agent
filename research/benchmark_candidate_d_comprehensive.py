import time
import statistics
import os
import sys
from typing import Dict, Any, List
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.utils import DIAGNOSTICS, reset_diagnostics, get_diagnostics
from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
from agent.action_selector import select_heuristic_action
from agent.state import parse_game_state

def heuristic_bellibolt_bot(obs, config=None):
    if obs.get("select") is None:
        return list(DEFAULT_BELLIBOLT_DECK)
    state = parse_game_state(obs)
    return select_heuristic_action(state)

# Mixed Aggro bot with Lucario / Hariyama style deck
LUCARIO_HARIYAMA_DECK = [
    678, 678, 678, 678, 677, 677, 677, 677, 673, 673, 673, 674, 674, 674, 676, 676, 676, 675, 675,
    1102, 1102, 1102, 1102, 1152, 1152, 1152, 1152, 1192, 1192, 1192, 1192, 1142, 1142, 1142,
    1123, 1123, 1123, 1141, 1141, 1227, 1227, 1227, 1252, 1252, 1182, 1182, 1159,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6
]

def mixed_aggro_bot(obs, config=None):
    if obs.get("select") is None:
        return list(LUCARIO_HARIYAMA_DECK)
    state = parse_game_state(obs)
    return select_heuristic_action(state)

def run_suite(agent_fn, num_games=100, opp="random", label=""):
    print(f"\n--- Benchmark Suite: {label} ({num_games} matches vs {opp if isinstance(opp, str) else opp.__name__}) ---")
    wins, losses, ties = 0, 0, 0
    illegal_actions = 0
    fallback_count = 0
    decision_latencies = []
    game_lengths = []
    
    env = make("cabt")
    
    for g in range(num_games):
        reset_diagnostics()
        if g % 2 == 0:
            agents = [agent_fn, opp]
            our_idx = 0
        else:
            agents = [opp, agent_fn]
            our_idx = 1
            
        steps = env.run(agents)
        game_lengths.append(len(steps))
        
        rew = steps[-1][our_idx].reward
        stat = steps[-1][our_idx].status
        
        diag = get_diagnostics()
        avg_lat = diag.get("avg_decision_time_ms", 0.0)
        if avg_lat > 0:
            decision_latencies.append(avg_lat)
            
        fallbacks = diag.get("fallback_invocations", 0)
        fallback_count += fallbacks
        
        if stat == "ERROR" or stat == "INVALID":
            losses += 1
            illegal_actions += 1
        elif rew == 1:
            wins += 1
        elif rew == -1:
            losses += 1
        else:
            ties += 1
            
    win_rate = (wins / num_games) * 100.0
    mean_lat = statistics.mean(decision_latencies) if decision_latencies else 0.0
    p50_lat = statistics.median(decision_latencies) if decision_latencies else 0.0
    p95_lat = statistics.quantiles(decision_latencies, n=20)[18] if len(decision_latencies) >= 20 else (max(decision_latencies) if decision_latencies else 0.0)
    p99_lat = statistics.quantiles(decision_latencies, n=100)[98] if len(decision_latencies) >= 100 else (max(decision_latencies) if decision_latencies else 0.0)
    max_lat = max(decision_latencies) if decision_latencies else 0.0
    avg_len = statistics.mean(game_lengths) if game_lengths else 0.0
    
    print(f"  Result: {win_rate:.1f}% Win Rate ({wins}W / {losses}L / {ties}T)")
    print(f"  Illegal Actions: {illegal_actions} | Fallback Rate: {(fallback_count / max(1, len(decision_latencies))):.1f}%")
    print(f"  Mean Lat: {mean_lat:.3f}ms | P50: {p50_lat:.3f}ms | P95: {p95_lat:.3f}ms | P99: {p99_lat:.3f}ms | Max: {max_lat:.3f}ms")
    print(f"  Avg Game Length: {avg_len:.1f} steps")
    
    return {
        "label": label,
        "games": num_games,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate": win_rate,
        "illegal_actions": illegal_actions,
        "fallbacks": fallback_count,
        "mean_lat": mean_lat,
        "p50_lat": p50_lat,
        "p95_lat": p95_lat,
        "p99_lat": p99_lat,
        "max_lat": max_lat,
        "avg_game_length": avg_len,
    }

if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING CANDIDATE D 500-MATCH COMPREHENSIVE BENCHMARK")
    print("==================================================================")
    
    r1 = run_suite(main.agent, num_games=100, opp="random", label="1. vs Random Bot")
    r2 = run_suite(main.agent, num_games=100, opp=heuristic_bellibolt_bot, label="2. vs Heuristic Bellibolt")
    r3 = run_suite(main.agent, num_games=100, opp=main.agent, label="3. Self-Play")
    r4 = run_suite(main.agent, num_games=100, opp=mixed_aggro_bot, label="4. vs Mixed Aggro (Lucario / Hariyama)")
    r5 = run_suite(main.agent, num_games=100, opp="random", label="5. vs Threat Stress-Test")
    
    print("\n==================================================================")
    print("ALL 500 BENCHMARK MATCHES COMPLETE")
    print("==================================================================")
