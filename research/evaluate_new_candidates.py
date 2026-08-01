import os
import sys

sys.path.insert(0, os.path.abspath("."))
from research.run_deck_tournament import evaluate_pairing, load_deck_from_file, create_agent_with_deck

def evaluate_candidates():
    print("Evaluating Candidate D (Crustle) vs Alakazam (Our AI vs Our AI)")
    
    deck_d = load_deck_from_file("research/deck_candidates/D_crustle_control.csv")
    deck_alakazam = load_deck_from_file("research/deck_candidates/E_alakazam_psychic.csv")
    
    agent_d = create_agent_with_deck(deck_d)
    agent_alakazam = create_agent_with_deck(deck_alakazam)
    
    print("Matchup: Candidate D (Crustle) vs Candidate E (Alakazam)")
    results_d_vs_a = evaluate_pairing(agent_d, agent_alakazam, num_games=10)
    print("Crustle vs Alakazam:", results_d_vs_a)
    
    print("\nMatchup: Candidate E (Alakazam) vs Candidate D (Crustle)")
    results_a_vs_d = evaluate_pairing(agent_alakazam, agent_d, num_games=10)
    print("Alakazam vs Crustle:", results_a_vs_d)

if __name__ == "__main__":
    evaluate_candidates()
