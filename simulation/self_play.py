import os
import sys
import time
import json
from typing import Dict, Any, List, Optional, Callable

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaggle_environments import make
from kaggle_environments.envs.cabt import cabt
import main
from agent.utils import get_diagnostics, reset_diagnostics


def run_self_play(
    num_games: int = 10,
    agent_p0: Optional[Callable] = None,
    agent_p1: Optional[Callable] = None,
    swap_seats: bool = True,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Run multi-game self-play simulation series with seat-swapping to eliminate first-player bias.
    """
    reset_diagnostics()
    agent_p0 = agent_p0 or main.agent
    agent_p1 = agent_p1 or main.agent

    wins_p0 = 0
    wins_p1 = 0
    draws = 0
    invalids = 0
    total_steps = 0
    game_records: List[Dict[str, Any]] = []

    start_bench_t = time.perf_counter()

    for game_idx in range(num_games):
        env = make("cabt", debug=False)

        # Alternate seat order if swap_seats is True
        p0_first = (game_idx % 2 == 0) if swap_seats else True
        active_p0 = agent_p0 if p0_first else agent_p1
        active_p1 = agent_p1 if p0_first else agent_p0

        env.run([active_p0, active_p1])

        steps = len(env.steps)
        total_steps += steps
        final_step = env.steps[-1]

        s0_status = final_step[0].status
        s1_status = final_step[1].status
        s0_reward = final_step[0].reward
        s1_reward = final_step[1].reward

        if s0_status == "INVALID" or s1_status == "INVALID":
            invalids += 1
            winner_str = "INVALID"
        elif s0_reward == 1:
            wins_p0 += 1 if p0_first else 0
            wins_p1 += 0 if p0_first else 1
            winner_str = "Agent_0" if p0_first else "Agent_1"
        elif s1_reward == 1:
            wins_p1 += 1 if p0_first else 0
            wins_p0 += 0 if p0_first else 1
            winner_str = "Agent_1" if p0_first else "Agent_0"
        else:
            draws += 1
            winner_str = "DRAW"

        record = {
            "game_id": game_idx + 1,
            "p0_seat": 0 if p0_first else 1,
            "steps": steps,
            "winner": winner_str,
            "s0_reward": s0_reward,
            "s1_reward": s1_reward,
        }
        game_records.append(record)

        if verbose:
            print(f"Game {game_idx+1}/{num_games}: {winner_str} ({steps} steps)")

    elapsed_sec = time.perf_counter() - start_bench_t
    diag = get_diagnostics()

    win_rate_p0 = (wins_p0 / max(1, num_games)) * 100.0
    win_rate_p1 = (wins_p1 / max(1, num_games)) * 100.0
    avg_steps = total_steps / max(1, num_games)
    fallback_rate = diag.get("fallback_rate_pct", 0.0)

    summary = {
        "games": num_games,
        "wins_p0": wins_p0,
        "wins_p1": wins_p1,
        "draws": draws,
        "invalids": invalids,
        "win_rate_p0": win_rate_p0,
        "win_rate_p1": win_rate_p1,
        "avg_steps": avg_steps,
        "duration_sec": elapsed_sec,
        "diagnostics": diag,
        "game_records": game_records,
    }

    if verbose:
        print("\n" + "=" * 50)
        print("          SELF-PLAY SUMMARY REPORT")
        print("=" * 50)
        print(f"Total Games    : {num_games}")
        print(f"Wins P0        : {wins_p0} ({win_rate_p0:.1f}%)")
        print(f"Wins P1        : {wins_p1} ({win_rate_p1:.1f}%)")
        print(f"Draws          : {draws}")
        print(f"Invalids       : {invalids}")
        print(f"Avg Steps/Game : {avg_steps:.1f}")
        print(f"Total Duration : {elapsed_sec:.2f}s")
        print(f"Avg Decision   : {diag.get('avg_decision_time_ms', 0.0):.3f} ms")
        print(f"Max Decision   : {diag.get('max_decision_time_ms', 0.0):.3f} ms")
        print(f"Fallback Rate  : {fallback_rate:.2f}%")
        print("=" * 50)

    return summary
