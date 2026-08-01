"""
Deep diagnostic: Trace a single Non-EX Swarm game to understand
WHY the heuristic bot loses when playing Alakazam against Crustle.
"""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.abspath("."))
from kaggle_environments import make
from agent.card_database import init_card_database, get_card_name
from agent.utils import reset_diagnostics, get_diagnostics
from agent.action_selector import select_action, select_heuristic_action
from agent.state import parse_game_state

init_card_database()

E0 = [344]*4 + [345]*4 + [1092] + [1121]*2 + [1145]*2 + [1227]*4 + [1262]*2 + [1]*41

NON_EX_SWARM = [
    741, 741, 741, 741, 742, 742, 742, 742, 743, 743, 743, 743,
    65, 65, 66, 66, 66, 66,
    1079, 1079, 1079, 1086, 1086, 1086, 1086,
    1152, 1152, 1152, 1152, 1225, 1225, 1225, 1225, 1231, 1231, 1231, 1231,
] + [5]*23

def test_agent(obs, config=None):
    if obs.get("select") is None:
        return list(E0)
    return select_action(obs)

opp_log = []
crustle_log = []

def traced_opp(obs, config=None):
    if obs.get("select") is None:
        return list(NON_EX_SWARM)
    state = parse_game_state(obs)
    action = select_heuristic_action(state)
    
    active_id = state.your_active.get("id") if state.your_active else None
    active_hp = state.your_active.get("hp") if state.your_active else None
    active_e = len(state.your_active.get("energies", [])) if state.your_active else 0
    bench_ids = [b.get("id") for b in state.your_bench if b]
    opp_active = state.opp_active.get("id") if state.opp_active else None
    opp_hp = state.opp_active.get("hp") if state.opp_active else None
    
    # Log option types
    opt_types = []
    for opt in state.options:
        if isinstance(opt, dict):
            ot = opt.get("type", -1)
            oid = opt.get("id", 0)
            opt_types.append(f"t{ot}:{get_card_name(oid) if oid else '?'}")
    
    entry = {
        "step": obs.get("step", "?"),
        "select_type": state.select_type,
        "my_active": f"{get_card_name(active_id)}(HP{active_hp},E{active_e})" if active_id else "None",
        "my_bench": [get_card_name(b) for b in bench_ids],
        "vs": f"{get_card_name(opp_active)}(HP{opp_hp})" if opp_active else "None",
        "action": action,
        "n_opts": len(state.options),
        "opt_sample": opt_types[:8],
        "prizes": f"me:{state.your_prizes} opp:{state.opp_prizes}",
    }
    opp_log.append(entry)
    return action

reset_diagnostics()
env = make("cabt")
steps = env.run([test_agent, traced_opp])

final = steps[-1]
print(f"Game: {len(steps)} steps | P1(Crustle) reward={final[0].reward} status={final[0].status} | P2(Alakazam) reward={final[1].reward} status={final[1].status}")
print(f"\nDiag: {get_diagnostics()}")

print(f"\n=== ALAKAZAM BOT DECISION TRACE ({len(opp_log)} decisions) ===")
for i, e in enumerate(opp_log):
    print(f"  [{i:>3}] Step {e['step']:>3} | st={e['select_type']} | {e['my_active']:<30} | bench={e['my_bench']}")
    print(f"        vs {e['vs']:<20} | prizes={e['prizes']} | action={e['action']} | opts({e['n_opts']})={e['opt_sample'][:5]}")

# Check if Alakazam ever appeared
all_actives = [e['my_active'] for e in opp_log]
print(f"\nActive Pokémon used by Alakazam bot: {Counter(all_actives).most_common()}")
