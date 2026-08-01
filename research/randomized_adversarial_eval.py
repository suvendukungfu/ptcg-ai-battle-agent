import random
import time
import statistics
import sys
import os
from typing import Dict, Any, List, Tuple
from kaggle_environments import make

sys.path.insert(0, os.path.abspath("."))
import main
from agent.card_database import init_card_database, get_all_cards, get_pokemon_data
from agent.state import GameState, parse_game_state
from agent.action_selector import select_action, select_heuristic_action
from agent.policy import rank_attack_options, rank_energy_attachment_options, rank_card_play_options
from agent.opponent_model import evaluate_opponent_threats

init_card_database()
ALL_CARDS = get_all_cards()

POKEMON_EX_IDS = [cid for cid, c in ALL_CARDS.items() if c.get("cardType") == 1 and (c.get("ex") or c.get("megaEx"))]
POKEMON_NONEX_IDS = [cid for cid, c in ALL_CARDS.items() if c.get("cardType") == 1 and not (c.get("ex") or c.get("megaEx")) and (c.get("stage1") or c.get("stage2"))]
POKEMON_BASIC_NONEX_IDS = [cid for cid, c in ALL_CARDS.items() if c.get("cardType") == 1 and c.get("basic") and not (c.get("ex") or c.get("megaEx"))]
TRAINER_IDS = [cid for cid, c in ALL_CARDS.items() if c.get("cardType") in (6, 7, 8, 9, 10)]
ENERGY_IDS = [1, 2, 3, 4, 5, 6, 7, 8]

# Ensure valid fallbacks if lists are empty
if not POKEMON_EX_IDS: POKEMON_EX_IDS = [723, 756, 678]
if not POKEMON_NONEX_IDS: POKEMON_NONEX_IDS = [345, 674, 666, 722]
if not POKEMON_BASIC_NONEX_IDS: POKEMON_BASIC_NONEX_IDS = [344, 721, 673, 677]


def generate_randomized_adversarial_scenario(archetype: str, seed: int) -> Dict[str, Any]:
    """
    Generates a randomized, legally consistent Pokémon TCG board state.
    """
    rng = random.Random(seed)
    
    # 1. Player (Our Agent) State
    our_active_id = rng.choice([344, 345])  # Dwebble or Crustle
    our_active_max_hp = 60 if our_active_id == 344 else 130
    our_active_hp = rng.randint(20, our_active_max_hp)
    our_active_energies = [1] * rng.randint(0, 3)
    
    our_active = {
        "id": our_active_id,
        "hp": our_active_hp,
        "maxHp": our_active_max_hp,
        "energies": our_active_energies
    }
    
    our_bench = []
    num_our_bench = rng.randint(0, 2)
    for _ in range(num_our_bench):
        b_id = rng.choice([344, 345])
        b_max_hp = 60 if b_id == 344 else 130
        our_bench.append({
            "id": b_id,
            "hp": rng.randint(30, b_max_hp),
            "maxHp": b_max_hp,
            "energies": [1] * rng.randint(0, 2)
        })
        
    our_prizes = rng.randint(1, 2) if archetype == "PRIZE_RACE" else rng.randint(1, 6)
    our_deck_count = rng.randint(3, 5) if archetype == "LOW_RESOURCE_ENDGAME" else rng.randint(10, 40)
    our_turn = rng.randint(8, 12) if archetype == "LOW_RESOURCE_ENDGAME" else rng.randint(1, 6)
    
    # 2. Opponent State based on Archetype
    if archetype == "EX_HEAVY":
        opp_active_id = rng.choice(POKEMON_EX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_EX_IDS) for _ in range(rng.randint(1, 2))]
        opp_energies_cnt = rng.randint(2, 4)
    elif archetype == "NONEX_HEAVY":
        opp_active_id = rng.choice(POKEMON_NONEX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_NONEX_IDS) for _ in range(rng.randint(1, 2))]
        opp_energies_cnt = rng.randint(2, 4)
    elif archetype == "MIXED_ATTACKERS":
        opp_active_id = rng.choice(POKEMON_EX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_NONEX_IDS) for _ in range(rng.randint(1, 2))]
        opp_energies_cnt = rng.randint(1, 3)
    elif archetype == "HIGH_ENERGY_RAMP":
        opp_active_id = rng.choice(POKEMON_NONEX_IDS + POKEMON_EX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_NONEX_IDS) for _ in range(rng.randint(1, 3))]
        opp_energies_cnt = rng.randint(3, 5)
    elif archetype == "LOW_ENERGY_SWARM":
        opp_active_id = rng.choice(POKEMON_BASIC_NONEX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_BASIC_NONEX_IDS) for _ in range(rng.randint(2, 3))]
        opp_energies_cnt = rng.randint(0, 1)
    elif archetype == "EVOLUTION_HEAVY":
        opp_active_id = rng.choice(POKEMON_BASIC_NONEX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_NONEX_IDS) for _ in range(rng.randint(1, 2))]
        opp_energies_cnt = rng.randint(1, 2)
    elif archetype == "BENCH_HEAVY":
        opp_active_id = rng.choice(POKEMON_NONEX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_NONEX_IDS + POKEMON_EX_IDS) for _ in range(3)]
        opp_energies_cnt = rng.randint(2, 3)
    elif archetype == "RESOURCE_DENIAL":
        opp_active_id = rng.choice(POKEMON_NONEX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_BASIC_NONEX_IDS) for _ in range(1)]
        opp_energies_cnt = rng.randint(1, 2)
    elif archetype == "PRIZE_RACE":
        opp_active_id = rng.choice(POKEMON_NONEX_IDS + POKEMON_EX_IDS)
        opp_bench_ids = [rng.choice(POKEMON_NONEX_IDS) for _ in range(1)]
        opp_energies_cnt = rng.randint(2, 3)
    else:  # LOW_RESOURCE_ENDGAME
        opp_active_id = rng.choice(POKEMON_EX_IDS)
        opp_bench_ids = []
        opp_energies_cnt = rng.randint(2, 3)
        
    opp_card = ALL_CARDS.get(opp_active_id, {})
    opp_active_max_hp = opp_card.get("hp", 120)
    opp_active_hp = rng.randint(30, max(40, opp_active_max_hp))
    opp_energy_type = opp_card.get("energyType", 6)
    
    opp_active = {
        "id": opp_active_id,
        "hp": opp_active_hp,
        "maxHp": opp_active_max_hp,
        "energies": [opp_energy_type] * opp_energies_cnt
    }
    
    opp_bench = []
    for b_id in opp_bench_ids:
        b_card = ALL_CARDS.get(b_id, {})
        b_max_hp = b_card.get("hp", 100)
        opp_bench.append({
            "id": b_id,
            "hp": rng.randint(40, max(50, b_max_hp)),
            "maxHp": b_max_hp,
            "energies": [opp_energy_type] * rng.randint(0, 3)
        })
        
    opp_prizes = rng.randint(1, 2) if archetype == "PRIZE_RACE" else rng.randint(1, 6)
    opp_hand_count = rng.randint(1, 2) if archetype == "RESOURCE_DENIAL" else rng.randint(3, 7)
    
    # 3. Construct Legal Action Options for Player 0 (Main Phase select_type = 0)
    options = []
    
    # Attack Option
    options.append({"type": 7, "text": "Attack Active"})
    
    # Energy Attachment Options
    options.append({"type": 8, "inPlayArea": 4, "text": "Attach Grass Energy to Active"})
    for bi in range(len(our_bench)):
        options.append({"type": 8, "inPlayArea": 5, "inPlayIndex": bi, "text": f"Attach Grass Energy to Bench #{bi}"})
        
    # Basic Pokemon to Bench (if bench has space < 3)
    if len(our_bench) < 3:
        options.append({"type": 1, "id": 344, "text": "Play Dwebble to Bench"})
        
    # Evolution to Crustle (if active or bench has Dwebble)
    if our_active_id == 344:
        options.append({"type": 3, "id": 345, "inPlayArea": 4, "text": "Evolve Active Dwebble to Crustle"})
    for bi, b in enumerate(our_bench):
        if b.get("id") == 344:
            options.append({"type": 3, "id": 345, "inPlayArea": 5, "inPlayIndex": bi, "text": f"Evolve Benched Dwebble #{bi} to Crustle"})
            
    # Trainer Cards in Hand
    if our_deck_count > 5:
        options.append({"type": 0, "id": 1092, "text": "Play Secret Box / Research"})
    options.append({"type": 0, "id": 1121, "text": "Play Ultra Ball Search"})
    if len(opp_bench) > 0:
        options.append({"type": 0, "id": 1262, "text": "Play Boss's Orders / Gust"})
        
    # Pass Option
    options.append({"type": 14, "text": "Pass Turn"})
    
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": options
        },
        "current": {
            "yourIndex": 0,
            "turn": our_turn,
            "players": [
                {
                    "active": [our_active],
                    "bench": our_bench,
                    "hand": [{"id": 1}, {"id": 345}, {"id": 1121}],
                    "prize": list(range(1, our_prizes + 1)),
                    "deckCount": our_deck_count,
                    "discard": []
                },
                {
                    "active": [opp_active],
                    "bench": opp_bench,
                    "hand": opp_hand_count,
                    "prize": list(range(1, opp_prizes + 1)),
                    "deckCount": max(5, 45 - our_turn * 3),
                    "discard": []
                }
            ]
        }
    }
    
    return obs


def evaluate_decision_quality(obs: Dict[str, Any], choice: List[int]) -> Dict[str, Any]:
    """
    Rigorously scores the strategic decision quality of the selected action.
    """
    options = obs["select"]["option"]
    if not choice or choice[0] < 0 or choice[0] >= len(options):
        return {"legal": False, "score": -100.0, "defect": "ILLEGAL_INDEX"}
        
    selected_opt = options[choice[0]]
    opt_type = selected_opt.get("type")
    card_id = selected_opt.get("id")
    in_play_area = selected_opt.get("inPlayArea")
    
    state = parse_game_state(obs)
    opp_model = evaluate_opponent_threats(state)
    
    quality_score = 50.0
    defect = None
    
    # 1. Zero-Bench Check: If bench is 0 and basic is playable, did agent bench it?
    if len(state.your_bench) == 0:
        has_basic_play = any(o.get("type") == 1 and o.get("id") == 344 for o in options)
        if has_basic_play:
            if opt_type == 1 and card_id == 344:
                quality_score += 40.0  # Proper BENCH_FIRST execution!
            elif opt_type == 0 and card_id == 1092:
                quality_score -= 50.0  # Played draw without benching
                defect = "MISSED_BENCH_FIRST"
                
    # 2. Anti-Deckout Check
    if state.your_deck_count <= 5:
        if card_id == 1092:  # Draw card
            quality_score -= 80.0
            defect = "SUICIDE_DECKOUT_DRAW"
            
    # 3. Non-EX Breaker Threat Check
    if state.your_active and state.your_active.get("id") == 345:  # Crustle
        has_breaker = opp_model.primary_threat and not opp_model.primary_threat.is_ex and opp_model.primary_threat.effective_damage >= 120.0
        if has_breaker:
            # Check energy attachment: Did it over-attach to active (>=3) instead of backup bench?
            if opt_type == 8:
                active_energies = len(state.your_active.get("energies", []))
                if in_play_area == 4 and active_energies >= 2 and len(state.your_bench) > 0:
                    quality_score -= 20.0  # Over-attached to doomed active
                elif in_play_area == 5:
                    quality_score += 30.0  # Smart backup ramp!
                    
    # 4. Decisive Game-Winning Attack Check
    if state.your_prizes <= 1:
        if opt_type == 7:  # Attack
            quality_score += 50.0
            
    return {"legal": True, "score": quality_score, "defect": defect}


def run_randomized_adversarial_benchmark(num_scenarios: int = 500):
    print("==================================================================")
    print(f"RUNNING {num_scenarios} RANDOMIZED ADVERSARIAL BOARD SCENARIOS")
    print("==================================================================")
    
    archetypes = [
        "EX_HEAVY",
        "NONEX_HEAVY",
        "MIXED_ATTACKERS",
        "HIGH_ENERGY_RAMP",
        "LOW_ENERGY_SWARM",
        "EVOLUTION_HEAVY",
        "BENCH_HEAVY",
        "RESOURCE_DENIAL",
        "PRIZE_RACE",
        "LOW_RESOURCE_ENDGAME",
    ]
    
    results_by_archetype = {a: {"count": 0, "b_score": 0.0, "d_score": 0.0, "d_better": 0, "b_better": 0, "ties": 0, "d_defects": 0, "b_defects": 0} for a in archetypes}
    
    all_d_latencies = []
    all_b_latencies = []
    
    for i in range(num_scenarios):
        archetype = archetypes[i % len(archetypes)]
        seed = 100000 + i * 37
        obs = generate_randomized_adversarial_scenario(archetype, seed)
        
        # Test Candidate D
        t0 = time.perf_counter()
        choice_d = select_action(obs)
        t_d = (time.perf_counter() - t0) * 1000.0
        all_d_latencies.append(t_d)
        eval_d = evaluate_decision_quality(obs, choice_d)
        
        # Test Candidate B
        state = parse_game_state(obs)
        t0 = time.perf_counter()
        choice_b = select_heuristic_action(state)
        t_b = (time.perf_counter() - t0) * 1000.0
        all_b_latencies.append(t_b)
        eval_b = evaluate_decision_quality(obs, choice_b)
        
        # Record
        r = results_by_archetype[archetype]
        r["count"] += 1
        r["d_score"] += eval_d["score"]
        r["b_score"] += eval_b["score"]
        
        if eval_d["defect"]: r["d_defects"] += 1
        if eval_b["defect"]: r["b_defects"] += 1
        
        if eval_d["score"] > eval_b["score"]:
            r["d_better"] += 1
        elif eval_b["score"] > eval_d["score"]:
            r["b_better"] += 1
        else:
            r["ties"] += 1
            
    print("\n--- RESULTS ACROSS ALL 10 ADVERSARIAL ARCHETYPES ---")
    total_d_wins = 0
    total_b_wins = 0
    total_ties = 0
    
    for a in archetypes:
        r = results_by_archetype[a]
        cnt = r["count"]
        avg_d = r["d_score"] / cnt
        avg_b = r["b_score"] / cnt
        total_d_wins += r["d_better"]
        total_b_wins += r["b_better"]
        total_ties += r["ties"]
        print(f"{a:<22} | D Avg: {avg_d:5.1f} | B Avg: {avg_b:5.1f} | D Win: {r['d_better']:2d} | B Win: {r['b_better']:2d} | Tie: {r['ties']:2d} | D Defects: {r['d_defects']} | B Defects: {r['b_defects']}")
        
    print("\n==================================================================")
    print("AGGREGATE ADVERSARIAL METRICS")
    print("==================================================================")
    print(f"Total Scenarios Evaluated: {num_scenarios}")
    print(f"Candidate D Preferred: {total_d_wins} ({total_d_wins / num_scenarios * 100:.1f}%)")
    print(f"Candidate B Preferred: {total_b_wins} ({total_b_wins / num_scenarios * 100:.1f}%)")
    print(f"Equivalent Strategic Choices: {total_ties} ({total_ties / num_scenarios * 100:.1f}%)")
    print(f"Candidate D Mean Latency: {statistics.mean(all_d_latencies):.3f} ms | P95: {statistics.quantiles(all_d_latencies, n=20)[18]:.3f} ms")
    print(f"Candidate B Mean Latency: {statistics.mean(all_b_latencies):.3f} ms | P95: {statistics.quantiles(all_b_latencies, n=20)[18]:.3f} ms")
    
    return results_by_archetype

if __name__ == "__main__":
    run_randomized_adversarial_benchmark(500)
