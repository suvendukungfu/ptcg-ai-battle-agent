import time
import statistics
import os
import sys
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.utils import DIAGNOSTICS, reset_diagnostics, get_diagnostics

def run_benchmark_series(opponent_name_or_fn, num_games=50, series_label=""):
    print(f"\n=======================================================")
    print(f"RUNNING BENCHMARK: {series_label} ({num_games} Full Matches)")
    print(f"=======================================================")
    
    wins = 0
    losses = 0
    ties = 0
    latencies = []
    step_counts = []
    illegal_actions = 0
    fallbacks = 0
    
    env = make("cabt")
    
    start_all = time.perf_counter()
    for g in range(num_games):
        reset_diagnostics()
        t0 = time.perf_counter()
        
        # Alternate seat positions: even games Player 0, odd games Player 1
        if g % 2 == 0:
            agents = [main.agent, opponent_name_or_fn]
            our_idx = 0
        else:
            agents = [opponent_name_or_fn, main.agent]
            our_idx = 1
            
        steps = env.run(agents)
        t_game = (time.perf_counter() - t0) * 1000.0
        
        final_step = steps[-1]
        stat = final_step[our_idx].status
        rew = final_step[our_idx].reward
        
        step_counts.append(len(steps))
        diag = get_diagnostics()
        if diag.get("avg_decision_time_ms", 0) > 0:
            latencies.append(diag["avg_decision_time_ms"])
            
        fallbacks += diag.get("fallback_decisions", 0)
        
        if stat == "ERROR" or stat == "INVALID":
            illegal_actions += 1
            losses += 1
        elif rew == 1:
            wins += 1
        elif rew == -1:
            losses += 1
        else:
            ties += 1
            
        if (g + 1) % 10 == 0:
            print(f"  Game {g+1:02d}/{num_games}: Wins={wins} Losses={losses} Ties={ties} (WR: {(wins/(g+1))*100:.1f}%)")
            
    total_time = time.perf_counter() - start_all
    win_rate = (wins / num_games) * 100.0
    p95_lat = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else (max(latencies) if latencies else 0.0)
    avg_lat = statistics.mean(latencies) if latencies else 0.0
    avg_steps = statistics.mean(step_counts)
    
    print(f"\n--- {series_label} Results ---")
    print(f"  Win Rate: {win_rate:.1f}% ({wins}/{num_games})")
    print(f"  Illegal Actions: {illegal_actions}")
    print(f"  Fallback Decisions: {fallbacks}")
    print(f"  Avg Latency per decision: {avg_lat:.3f} ms")
    print(f"  P95 Game Latency: {p95_lat:.3f} ms")
    print(f"  Avg Game Length: {avg_steps:.1f} steps")
    print(f"  Total Benchmark Time: {total_time:.2f}s")
    
    return {
        "series": series_label,
        "games": num_games,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate": win_rate,
        "illegal_actions": illegal_actions,
        "fallbacks": fallbacks,
        "avg_latency_ms": avg_lat,
        "p95_latency_ms": p95_lat,
        "avg_steps": avg_steps
    }

if __name__ == "__main__":
    results = []
    
    # 1. 50 Matches vs Random Bot
    res_rand = run_benchmark_series("random", num_games=50, series_label="Candidate B vs Random Bot")
    results.append(res_rand)
    
    # 2. 50 Matches vs Heuristic Bellibolt Baseline
    from agent.deck_policy import DEFAULT_BELLIBOLT_DECK
    def heuristic_bot(obs, config=None):
        if obs.get("select") is None:
            return list(DEFAULT_BELLIBOLT_DECK)
        from agent.action_selector import select_heuristic_action
        from agent.state import parse_game_state
        state = parse_game_state(obs)
        return select_heuristic_action(state)
        
    res_heur = run_benchmark_series(heuristic_bot, num_games=50, series_label="Candidate B vs Heuristic Bot")
    results.append(res_heur)
    
    # 3. 50 Self-Play Matches
    res_self = run_benchmark_series(main.agent, num_games=50, series_label="Candidate B Self-Play")
    results.append(res_self)
    
    print("\n=======================================================")
    print("ALL CANDIDATE B BENCHMARKS COMPLETED SUCCESSFULLY")
    print("=======================================================")
