import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from research.run_deck_tournament import evaluate_pairing, load_deck_from_file, create_agent_with_deck

async def optimize_decks():
    print("Running Alakazam vs Crustle (With improved AI)")
    
    deck_d = load_deck_from_file("research/deck_candidates/D_crustle_control.csv")
    deck_alakazam = load_deck_from_file("research/deck_candidates/E_alakazam_psychic.csv")
    
    agent_d = create_agent_with_deck(deck_d)
    agent_alakazam = create_agent_with_deck(deck_alakazam)
    
    print("\n[Matchup] Alakazam (Agent E) vs Crustle (Agent D)")
    res_a_vs_d = evaluate_pairing(agent_alakazam, agent_d, num_games=20)
    print("Alakazam vs Crustle:", res_a_vs_d)

if __name__ == "__main__":
    asyncio.run(optimize_decks())
