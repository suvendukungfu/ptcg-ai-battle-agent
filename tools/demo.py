#!/usr/bin/env python3
import os
import sys
import time

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from kaggle_environments import make
from kaggle_environments.envs.cabt import cabt
import main
from agent.state import parse_game_state
from agent.belief_state import BeliefStateTracker
from agent.goals import GoalPlanner
from agent.decomposition import ScoreDecomposer
from analytics.replay_parser import ReplayParser
from analytics.mistake_miner import MistakeMiner


def run_interactive_demo():
    print("=" * 70)
    print("      PTCG AI LAB — AUTONOMOUS GAME INTELLIGENCE DEMO")
    print("=" * 70)
    print("Demonstrating:")
    print("  1. Bayesian Belief State (Tracking hidden opponent hand probabilities)")
    print("  2. Goal-Based Strategic Planning (Macro tactical orientation)")
    print("  3. 2-Ply Lookahead Search & Counterfactual Evaluation")
    print("  4. Explainable Action Value Decomposition")
    print("  5. Post-Match Mistake Mining & Robustness Evaluation")
    print("=" * 70)
    print()

    print("[1/3] Initializing simulation match: Production_Agent_V2 vs Random_Baseline...")
    env = make("cabt", debug=False)
    env.run([main.agent, cabt.random_agent])
    print(f"Match completed successfully in {len(env.steps)} steps.")
    print()

    print("[2/3] Analyzing key decision points and Bayesian belief trajectory...")
    parsed_replay = ReplayParser.parse_episode_steps(env.steps, agent_seat=0)
    timeline = parsed_replay.get("timeline", [])

    tracker = BeliefStateTracker()
    decisions = parsed_replay.get("decisions", {})

    for idx, item in enumerate(timeline[:5]):  # Show first 5 key steps
        turn = item["turn"]
        print(f"\n--- Turn {turn} (Step {idx}) ---")
        p0 = item.get("your_active")
        p1 = item.get("opp_active")
        p0_desc = f"Card #{p0['id']} (HP: {p0['hp']}/{p0['maxHp']})" if p0 else "Empty"
        p1_desc = f"Card #{p1['id']} (HP: {p1['hp']}/{p1['maxHp']})" if p1 else "Empty"
        print(f"Board State : Active: {p0_desc} | Opponent: {p1_desc}")
        print(f"Prizes Left : You: {item['your_prizes']} | Opponent: {item['opp_prizes']}")

        # Dummy GameState for belief tracking demonstration
        state = parse_game_state(env.steps[idx][0]["observation"])
        beliefs = tracker.update_beliefs(state)
        goal = GoalPlanner.identify_goal(state)

        print(f"Macro Goal  : {goal.primary_goal} -> {goal.goal_rationale}")
        print(f"Belief State: P(Boss/Gust): {beliefs.p_boss_gust*100:.1f}% | P(Energy): {beliefs.p_energy*100:.1f}% | P(Switch): {beliefs.p_switch*100:.1f}%")

        if idx in decisions or str(idx) in decisions:
            dec = decisions.get(idx) or decisions.get(str(idx))
            print("Candidate Action Tree:")
            for opt in dec.get("options", []):
                chosen_mark = "[CHOSEN]   " if opt.get("is_chosen") else "[REJECTED] "
                print(f"  {chosen_mark} Option {opt.get('index')}: {opt.get('name')} | Value: {opt.get('projected_value'):+.1f} | Bonus: +{opt.get('action_bonus')}")

    print()
    print("[3/3] Post-Match Intelligence Summary:")
    winner = parsed_replay.get("winner")
    print(f"  Match Result   : {winner}")
    print(f"  Prizes Claimed : {6 - timeline[-1]['your_prizes']} (You) vs {6 - timeline[-1]['opp_prizes']} (Opponent)")
    print(f"  Total KOs      : {len(parsed_replay.get('kos_log', []))}")

    mistakes = MistakeMiner.mine_mistakes_from_replay(parsed_replay)
    print(f"  Mistakes Mined : {len(mistakes)} detected blunders/missed lines.")
    for m in mistakes[:3]:
        print(f"    - [{m.category}] {m.explanation} (Delta: {m.score_delta:+.1f})")

    print()
    print("=" * 70)
    print("  Demo complete. To explore full interactive UI, launch:")
    print("  $ uvicorn dashboard.backend.app:app --host 0.0.0.0 --port 8000")
    print("=" * 70)


if __name__ == "__main__":
    run_interactive_demo()
