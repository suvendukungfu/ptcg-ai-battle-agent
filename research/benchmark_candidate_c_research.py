import time
import statistics
import os
import sys
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.utils import DIAGNOSTICS, reset_diagnostics, get_diagnostics

def run_suite(agent_fn, num_games=50, opp="random", label=""):
    print(f"\n--- Benchmark: {label} ({num_games} matches vs {opp}) ---")
    wins, losses, ties = 0, 0, 0
    latencies = []
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
        rew = steps[-1][our_idx].reward
        stat = steps[-1][our_idx].status
        
        diag = get_diagnostics()
        if diag.get("avg_decision_time_ms", 0) > 0:
            latencies.append(diag["avg_decision_time_ms"])
            
        if stat == "ERROR" or stat == "INVALID":
            losses += 1
        elif rew == 1:
            wins += 1
        elif rew == -1:
            losses += 1
        else:
            ties += 1
            
    win_rate = (wins / num_games) * 100.0
    avg_lat = statistics.mean(latencies) if latencies else 0.0
    p95_lat = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else (max(latencies) if latencies else 0.0)
    print(f"  Result: {win_rate:.1f}% Win Rate ({wins}/{num_games}) | Avg Latency: {avg_lat:.3f}ms | P95: {p95_lat:.3f}ms")
    return {"win_rate": win_rate, "wins": wins, "losses": losses, "avg_lat": avg_lat, "p95_lat": p95_lat}

if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING CANDIDATE B VS CANDIDATE C COMPREHENSIVE RESEARCH BENCHMARK")
    print("==================================================================")
    
    # 1. 100 matches vs Random
    run_suite(main.agent, num_games=100, opp="random", label="Candidate B vs Random")
    
    # 2. 100 matches vs Heuristic Bellibolt
    from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
    def heuristic_bot(obs, config=None):
        if obs.get("select") is None:
            return list(DEFAULT_BELLIBOLT_DECK)
        from agent.action_selector import select_heuristic_action
        from agent.state import parse_game_state
        state = parse_game_state(obs)
        return select_heuristic_action(state)
        
    run_suite(main.agent, num_games=100, opp=heuristic_bot, label="Candidate B vs Heuristic Bellibolt")
    
    # 3. 50 Self-Play Matches
    run_suite(main.agent, num_games=50, opp=main.agent, label="Candidate B Self-Play")
