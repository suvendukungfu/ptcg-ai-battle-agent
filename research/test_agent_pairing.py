import os
import sys
sys.path.insert(0, os.path.abspath("."))
from kaggle_environments import make
from research.run_deck_tournament import load_deck_from_file, create_agent_with_deck
from research.opponents.scripted_alakazam import scripted_alakazam_agent

def create_scripted_opponent(deck_cards, agent_logic):
    deck_copy = list(deck_cards)
    def agent(obs, config=None):
        if not isinstance(obs, dict):
            return []
        select = obs.get("select")
        if select is None:
            return list(deck_copy)
        return agent_logic(obs, config)
    return agent

deck_b = load_deck_from_file("research/deck_candidates/B_bellibolt_consistency_4_3_3.csv")
deck_d = load_deck_from_file("research/deck_candidates/D_crustle_control.csv")
deck_e = load_deck_from_file("research/deck_candidates/E_alakazam_psychic.csv")

agent_d = create_agent_with_deck(deck_d)
agent_alakazam = create_scripted_opponent(deck_e, scripted_alakazam_agent)

env = make("cabt", debug=True)
env.run([agent_d, agent_alakazam])
print(f"Game finished in {len(env.steps)} steps. Rewards: {env.steps[-1][0].reward}, {env.steps[-1][1].reward}")
print("Status:", [s.status for s in env.steps[-1]])
