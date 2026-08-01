import json
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_card, get_pokemon_data

init_card_database()

def analyze_episode(ep_id: int):
    print(f"\n==================================================================")
    print(f"ANALYZING PUBLIC EPISODE {ep_id}")
    print(f"==================================================================")
    
    replay_path = f"reports/kaggle_candidate_d/public_{ep_id}/episode-{ep_id}-replay.json"
    with open(replay_path, "r") as f:
        replay = json.load(f)
        
    steps = replay.get("steps", [])
    print(f"Total Steps: {len(steps)}")
    
    last_step = steps[-1]
    p0 = last_step[0]
    p1 = last_step[1]
    
    # Identify decks
    vis0 = steps[0][0].get("visualize", [])
    p0_deck = vis0[0]["action"][0] if vis0 else []
    p1_deck = vis0[0]["action"][1] if vis0 else []
    
    p0_counts = Counter(p0_deck)
    p1_counts = Counter(p1_deck)
    
    is_p0_ours = (344 in p0_counts and 345 in p0_counts)
    is_p1_ours = (344 in p1_counts and 345 in p1_counts)
    
    our_idx = 0 if is_p0_ours else 1
    opp_idx = 1 if is_p0_ours else 0
    
    print(f"Our Player Index: Player {our_idx}")
    print(f"Opponent Player Index: Player {opp_idx}")
    
    our_stat = last_step[our_idx].get("status")
    our_rew = last_step[our_idx].get("reward")
    opp_stat = last_step[opp_idx].get("status")
    opp_rew = last_step[opp_idx].get("reward")
    
    print(f"Our Result: Status={our_stat}, Reward={our_rew} -> {'WIN (+1.0)' if our_rew == 1 else 'LOSS (-1.0)' if our_rew == -1 else 'TIE (0.0)'}")
    print(f"Opponent Result: Status={opp_stat}, Reward={opp_rew}")
    
    # Inspect Opponent Deck
    opp_deck = p0_deck if our_idx == 1 else p1_deck
    opp_counts = Counter(opp_deck)
    print("\nOpponent Deck Composition:")
    ex_cards = []
    non_ex_pkmn = []
    trainers = []
    for cid, cnt in opp_counts.items():
        cname = get_card_name(cid)
        card = get_card(cid)
        if card and (card.get("ex") or card.get("megaEx")):
            ex_cards.append(f"{cname} (x{cnt})")
        elif card and card.get("cardType") == 0:
            non_ex_pkmn.append(f"{cname} (x{cnt})")
        elif card and card.get("cardType") in (1, 2, 3, 4):
            trainers.append(f"{cname} (x{cnt})")
            
    print(f"  EX Pokémon: {', '.join(ex_cards) if ex_cards else 'NONE'}")
    print(f"  Non-EX Pokémon: {', '.join(non_ex_pkmn) if non_ex_pkmn else 'NONE'}")
    print(f"  Key Trainers: {', '.join(trainers[:6]) if trainers else 'NONE'}")
    
    # Inspect Logs
    log_path = f"reports/kaggle_candidate_d/public_{ep_id}/episode-{ep_id}-agent-{our_idx}-logs.json"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
                stderrs = [l[0].get("stderr", "") for l in logs if l and isinstance(l, list) and isinstance(l[0], dict)]
                non_empty = [e for e in stderrs if e]
                print(f"\nAgent Telemetry: {len(logs)} steps | Stderr errors: {len(non_empty)}")
                durations = [l[0].get("duration", 0.0) for l in logs if l and isinstance(l, list) and isinstance(l[0], dict)]
                if durations:
                    print(f"Latency: Mean={sum(durations)/len(durations)*1000:.2f}ms, Max={max(durations)*1000:.2f}ms")
            except Exception as e:
                print(f"Log parse error: {e}")
                
    return {
        "episode_id": ep_id,
        "our_idx": our_idx,
        "reward": our_rew,
        "status": our_stat,
        "steps": len(steps),
        "opp_ex": ex_cards,
        "opp_nonex": non_ex_pkmn,
    }

if __name__ == "__main__":
    r1 = analyze_episode(93504748)
    r2 = analyze_episode(93505666)
