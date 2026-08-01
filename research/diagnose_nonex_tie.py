"""
Diagnostic: Why do Non-EX Swarm games produce TIES instead of losses?
Examine a single game trace to confirm the heuristic bot can't evolve Alakazam.
"""
import sys, os, json
sys.path.insert(0, os.path.abspath("."))
from kaggle_environments import make
from agent.card_database import init_card_database
from agent.utils import reset_diagnostics
from agent.action_selector import select_action, select_heuristic_action
from agent.state import parse_game_state

init_card_database()

E0 = [344]*4 + [345]*4 + [1092] + [1121]*2 + [1145]*2 + [1227]*4 + [1262]*2 + [1]*41

NON_EX_SWARM = [
    741, 741, 741, 741, 742, 742, 742, 742, 743, 743, 743, 743,
    65, 65, 66, 66, 66, 66,
    1079, 1079, 1079, 1086, 1086, 1086, 1086,
    1152, 1152, 1152, 1152, 1225, 1225, 1225, 1225, 1231, 1231, 1231, 1231,
    19, 19, 19, 19
] + [5]*21

def test_agent(obs, config=None):
    if obs.get("select") is None:
        return list(E0)
    return select_action(obs)

step_log = []
def traced_bot(obs, config=None):
    if obs.get("select") is None:
        return list(NON_EX_SWARM)
    state = parse_game_state(obs)
    action = select_heuristic_action(state)
    
    # Log opponent state
    active = state.opp_active  # from opponent's perspective this is actually "your_active"
    your_active = state.your_active
    step_log.append({
        "step": obs.get("step", "?"),
        "select_type": state.select_type,
        "n_options": len(state.options),
        "your_active_id": your_active.get("id") if your_active else None,
        "your_active_hp": your_active.get("hp") if your_active else None,
        "your_active_energies": len(your_active.get("energies", [])) if your_active else 0,
        "your_bench": [b.get("id") for b in state.your_bench if b],
        "action": action,
    })
    return action

reset_diagnostics()
env = make("cabt")
steps = env.run([test_agent, traced_bot])

final = steps[-1]
print(f"Game length: {len(steps)} steps")
print(f"P1 reward: {final[0].reward}, status: {final[0].status}")
print(f"P2 reward: {final[1].reward}, status: {final[1].status}")
print()

# Show the last 20 decision points from the traced bot
print("=== OPPONENT (Alakazam) DECISION TRACE (last 30) ===")
for entry in step_log[-30:]:
    print(f"  Step {entry['step']:>3} | type={entry['select_type']} | opts={entry['n_options']:>2} | "
          f"active=ID{entry['your_active_id']}(HP{entry['your_active_hp']},E{entry['your_active_energies']}) | "
          f"bench={entry['your_bench']} | action={entry['action']}")

# Count what active Pokémon the opponent used
active_ids = [e['your_active_id'] for e in step_log if e['your_active_id']]
from collections import Counter
print(f"\nOpponent active Pokémon frequency: {Counter(active_ids)}")

# Check if Alakazam (743) or Kadabra (742) ever appeared
evolved = [e for e in step_log if e['your_active_id'] in (742, 743)]
print(f"Kadabra/Alakazam appearances in active: {len(evolved)}")
bench_evolved = [e for e in step_log if any(b in (742, 743) for b in e.get('your_bench', []))]
print(f"Kadabra/Alakazam appearances on bench: {len(bench_evolved)}")
