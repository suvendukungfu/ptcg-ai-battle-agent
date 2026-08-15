import os
import sys
import time
import numpy as np
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.self_play import run_self_play
from research.baselines import heuristic_v1_agent
from kaggle_environments.envs.cabt.cabt import random_agent
import main
from agent.utils import get_diagnostics, reset_diagnostics

def run_benchmarks():
    print("==================================================")
    print("   POST-CONSOLIDATION CABT SIMULATION BENCHMARK   ")
    print("==================================================")

    # 1. Self-Play (10 games)
    print("\n[1/3] Running 10 Self-Play Matches (Agent vs Agent)...")
    res_self = run_self_play(num_games=10, agent_p0=main.agent, agent_p1=main.agent, swap_seats=True, verbose=False)
    print(f"      Self-Play: P0 Wins={res_self['wins_p0']} | P1 Wins={res_self['wins_p1']} | Draws={res_self['draws']} | Invalids={res_self['invalids']}")
    print(f"      Avg Steps={res_self['avg_steps']:.1f} | Duration={res_self['duration_sec']:.2f}s | Avg Latency={res_self['diagnostics']['avg_decision_time_ms']:.3f}ms")

    # 2. Vs Heuristic Baseline (10 games)
    print("\n[2/3] Running 10 Matches vs Heuristic Baseline...")
    res_heur = run_self_play(num_games=10, agent_p0=main.agent, agent_p1=heuristic_v1_agent, swap_seats=True, verbose=False)
    print(f"      Vs Heuristic: Wins={res_heur['wins_p0']} ({(res_heur['wins_p0']/10)*100:.1f}%) | Losses={res_heur['wins_p1']} | Invalids={res_heur['invalids']}")
    print(f"      Avg Steps={res_heur['avg_steps']:.1f} | Duration={res_heur['duration_sec']:.2f}s | Avg Latency={res_heur['diagnostics']['avg_decision_time_ms']:.3f}ms")

    # 3. Vs Random Baseline (10 games)
    print("\n[3/3] Running 10 Matches vs Random Baseline...")
    res_rand = run_self_play(num_games=10, agent_p0=main.agent, agent_p1=random_agent, swap_seats=True, verbose=False)
    print(f"      Vs Random: Wins={res_rand['wins_p0']} ({(res_rand['wins_p0']/10)*100:.1f}%) | Losses={res_rand['wins_p1']} | Invalids={res_rand['invalids']}")
    print(f"      Avg Steps={res_rand['avg_steps']:.1f} | Duration={res_rand['duration_sec']:.2f}s | Avg Latency={res_rand['diagnostics']['avg_decision_time_ms']:.3f}ms")

    # 4. Detailed Latency Profiling (100 decision steps)
    print("\n[4/4] Profiling Latency Percentiles (P50, P95, P99, Max)...")
    from kaggle_environments import make
    env = make("cabt", debug=False)
    env.run([main.agent, main.agent])

    step_latencies: List[float] = []
    for step in env.steps:
        for agent_state in step:
            obs = agent_state.observation
            if obs and obs.get("select") is not None:
                t0 = time.perf_counter()
                main.agent(obs)
                t1 = time.perf_counter()
                step_latencies.append((t1 - t0) * 1000.0)

    p50 = np.percentile(step_latencies, 50)
    p95 = np.percentile(step_latencies, 95)
    p99 = np.percentile(step_latencies, 99)
    max_lat = np.max(step_latencies)
    mean_lat = np.mean(step_latencies)

    print(f"      P50 Latency : {p50:.3f} ms")
    print(f"      P95 Latency : {p95:.3f} ms")
    print(f"      P99 Latency : {p99:.3f} ms")
    print(f"      Max Latency : {max_lat:.3f} ms")
    print(f"      Mean Latency: {mean_lat:.3f} ms")

    return {
        "self_play": res_self,
        "vs_heuristic": res_heur,
        "vs_random": res_rand,
        "latency": {
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "max": max_lat,
            "mean": mean_lat,
        }
    }

if __name__ == "__main__":
    run_benchmarks()
