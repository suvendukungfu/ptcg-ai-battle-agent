import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from research.run_deck_tournament import evaluate_pairing, load_deck_from_file, create_agent_with_deck

async def optimize_decks():
    print("Running Automated Deck Search / Meta Evaluation")
    
    deck_d = load_deck_from_file("research/deck_candidates/D_crustle_control.csv")
    deck_alakazam = load_deck_from_file("research/deck_candidates/E_alakazam_psychic.csv")
    deck_bellibolt = load_deck_from_file("research/deck_candidates/B_bellibolt_consistency_4_3_3.csv")
    
    agent_d = create_agent_with_deck(deck_d)
    agent_alakazam = create_agent_with_deck(deck_alakazam)
    agent_bellibolt = create_agent_with_deck(deck_bellibolt)
    
    # We evaluate Alakazam against Bellibolt (EX Aggro)
    print("\n[Matchup 1] Alakazam (Agent E) vs Bellibolt (EX Meta)")
    res_a_vs_b = evaluate_pairing(agent_alakazam, agent_bellibolt, num_games=20)
    print("Alakazam vs Bellibolt:", res_a_vs_b)
    
    # We evaluate Crustle against Bellibolt
    print("\n[Matchup 2] Crustle (Agent D) vs Bellibolt (EX Meta)")
    res_d_vs_b = evaluate_pairing(agent_d, agent_bellibolt, num_games=20)
    print("Crustle vs Bellibolt:", res_d_vs_b)

if __name__ == "__main__":
    asyncio.run(optimize_decks())
