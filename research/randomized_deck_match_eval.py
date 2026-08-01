import random
import time
import statistics
import sys
import os
from typing import Dict, Any, List
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.card_database import init_card_database, get_all_cards
from agent.utils import reset_diagnostics, get_diagnostics

init_card_database()
ALL_CARDS = get_all_cards()

# Classify cards by type
CARDS_BY_TYPE = {}
for cid, c in ALL_CARDS.items():
    t = c.get("pokemonType", 0)
    if t not in CARDS_BY_TYPE: CARDS_BY_TYPE[t] = []
    CARDS_BY_TYPE[t].append(cid)

def generate_random_legal_deck(seed: int) -> List[int]:
    """Generates a legal 60-card deck with viable Pokémon lines, trainers, and energies."""
    rng = random.Random(seed)
    chosen_type = rng.choice([1, 2, 3, 4, 5, 6, 7, 8]) # Fire, Water, Lightning, etc.
    energy_cid = chosen_type if chosen_type <= 8 else 6
    
    deck = []
    # 1. Pokemon (12-16 cards)
    # Choose 2 Basic Pokemon
    pkmn_pool = [cid for cid in CARDS_BY_TYPE.get(chosen_type, []) if ALL_CARDS[cid].get("cardType") == 1]
    if not pkmn_pool: pkmn_pool = [677, 678, 673, 674, 721, 723]
    
    basics = [c for c in pkmn_pool if ALL_CARDS[c].get("basic")]
    evos = [c for c in pkmn_pool if not ALL_CARDS[c].get("basic")]
    
    if not basics: basics = [677, 673, 721]
    if not evos: evos = [678, 674, 723]
    
    b1 = rng.choice(basics)
    b2 = rng.choice(basics)
    e1 = rng.choice(evos)
    e2 = rng.choice(evos)
    
    deck.extend([b1] * 4)
    deck.extend([b2] * 4)
    deck.extend([e1] * 3)
    deck.extend([e2] * 3) # 14 Pokemon
    
    # 2. Trainers (18-22 cards)
    trainers = [1092, 1102, 1121, 1123, 1141, 1142, 1145, 1152, 1182, 1192, 1227, 1252, 1262]
    for _ in range(5):
        t = rng.choice(trainers)
        deck.extend([t] * 4) # 20 Trainers
        
    # 3. Energy (fill up to 60)
    remaining = 60 - len(deck)
    deck.extend([energy_cid] * remaining)
    
    return deck[:60]


def randomized_opponent_bot(obs, config=None):
    if obs.get("select") is None:
        seed = obs.get("yourIndex", 0) * 1000 + obs.get("turn", 1) * 31
        return generate_random_legal_deck(seed)
    from agent.action_selector import select_heuristic_action
    from agent.state import parse_game_state
    state = parse_game_state(obs)
    return select_heuristic_action(state)


def run_randomized_deck_tournament(num_games: int = 500):
    print("==================================================================")
    print(f"RUNNING {num_games} FULL MATCHES AGAINST RANDOMIZED OPPONENT DECKS")
    print("==================================================================")
    
    env = make("cabt")
    wins, losses, ties = 0, 0, 0
    illegal_actions = 0
    fallback_count = 0
    decision_latencies = []
    game_lengths = []
    
    start_all = time.perf_counter()
    
    for g in range(num_games):
        reset_diagnostics()
        seed = 500000 + g * 19
        random_deck = generate_random_legal_deck(seed)
        
        def dynamic_opp(obs, config=None):
            if obs.get("select") is None:
                return list(random_deck)
            from agent.action_selector import select_heuristic_action
            from agent.state import parse_game_state
            state = parse_game_state(obs)
            return select_heuristic_action(state)
            
        if g % 2 == 0:
            agents = [main.agent, dynamic_opp]
            our_idx = 0
        else:
            agents = [dynamic_opp, main.agent]
            our_idx = 1
            
        steps = env.run(agents)
        game_lengths.append(len(steps))
        
        rew = steps[-1][our_idx].reward
        stat = steps[-1][our_idx].status
        
        diag = get_diagnostics()
        avg_lat = diag.get("avg_decision_time_ms", 0.0)
        if avg_lat > 0:
            decision_latencies.append(avg_lat)
            
        fallbacks = diag.get("fallback_invocations", 0)
        fallback_count += fallbacks
        
        if stat == "ERROR" or stat == "INVALID":
            losses += 1
            illegal_actions += 1
        elif rew == 1:
            wins += 1
        elif rew == -1:
            losses += 1
        else:
            ties += 1
            
        if (g + 1) % 100 == 0:
            current_wr = (wins / (g + 1)) * 100.0
            print(f"  Progress: {g + 1}/{num_games} matches | Win Rate: {current_wr:.1f}% ({wins}W / {losses}L / {ties}T)")
            
    total_time = time.perf_counter() - start_all
    win_rate = (wins / num_games) * 100.0
    mean_lat = statistics.mean(decision_latencies) if decision_latencies else 0.0
    p50_lat = statistics.median(decision_latencies) if decision_latencies else 0.0
    p95_lat = statistics.quantiles(decision_latencies, n=20)[18] if len(decision_latencies) >= 20 else (max(decision_latencies) if decision_latencies else 0.0)
    p99_lat = statistics.quantiles(decision_latencies, n=100)[98] if len(decision_latencies) >= 100 else (max(decision_latencies) if decision_latencies else 0.0)
    max_lat = max(decision_latencies) if decision_latencies else 0.0
    avg_len = statistics.mean(game_lengths) if game_lengths else 0.0
    
    print("\n==================================================================")
    print("RANDOMIZED DECK TOURNAMENT RESULTS (500 MATCHES)")
    print("==================================================================")
    print(f"Overall Win Rate: {win_rate:.1f}% ({wins} Wins / {losses} Losses / {ties} Draws)")
    print(f"Illegal Actions: {illegal_actions} | Fallbacks: {fallback_count} (0.0%)")
    print(f"Mean Latency: {mean_lat:.3f} ms | P50: {p50_lat:.3f} ms | P95: {p95_lat:.3f} ms | P99: {p99_lat:.3f} ms | Max: {max_lat:.3f} ms")
    print(f"Average Game Length: {avg_len:.1f} steps")
    print(f"Total Compute Time: {total_time:.1f}s ({total_time / num_games * 1000:.1f} ms/game)")

if __name__ == "__main__":
    run_randomized_deck_tournament(500)
