import os
import json
import sys
sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card_name, get_pokemon_data

init_card_database()

REPLAYS_DIR = "reports/leaderboard_optimization/replays"
OUT_DIR = "reports/leaderboard_optimization"

def identify_deck_archetype(names_str):
    if "Alakazam" in names_str:
        return "Non-EX Alakazam Swarm"
    if "Trevenant" in names_str:
        return "Non-EX Trevenant Control"
    if "Bellibolt" in names_str or "Tadbulb" in names_str:
        return "EX Bellibolt Aggro"
    if "Lucario" in names_str or "Hariyama" in names_str:
        return "Mixed Aggro"
    if "Grimmsnarl" in names_str:
        return "EX Grimmsnarl"
    
    if "ex" in names_str:
        return "EX Variant"
    return "Unknown Non-EX"

def analyze_replays():
    files = [f for f in os.listdir(REPLAYS_DIR) if f.endswith(".json")]
    matches = []
    
    wins = 0
    losses = 0
    ties = 0
    
    for f in files:
        ep_id = f.replace("episode_", "").replace(".json", "")
        path = os.path.join(REPLAYS_DIR, f)
        
        with open(path, "r") as fh:
            try:
                data = json.load(fh)
            except:
                print(f"Skipping {f} (invalid JSON)")
                continue
                
        steps = data.get("steps", [])
        if not steps:
            continue
            
        final_step = steps[-1]
        
        info = data.get("info", {})
        team_names = info.get("TeamNames", ["Agent 0", "Agent 1"])
        
        # Determine our idx
        our_idx = 0
        if "suvendusahoo" in team_names[1].lower() or "candidate" in team_names[1].lower():
            our_idx = 1
            
        our_reward = final_step[our_idx].get("reward", 0)
        
        opp_idx = 1 - our_idx
        opp_cards_played = set()
        
        # Reconstruct opponent deck from observations
        # Kaggle replays: obs contains "players" or we can just scan the actions
        # For simplicity, let's scan the action space of the opponent.
        for step in steps:
            opp_obs = step[opp_idx].get("observation", {})
            if "options" in opp_obs:
                pass
            
            # Since Kaggle replays format the observation weirdly, let's just grep the entire step object for card IDs
            # or look at the logs.
            pass
            
        # As a heuristic, let's look at the action traces in the logs or the actual state if it's stored.
        # Often the replay JSON stores the full state. Let's look at `state` string if available.
        # For now, let's parse the replay json properly.
        # actually, kaggle replays don't store full state. They store observations.
        # The opponent's active and bench pokemon are visible in our observation!
        for step in steps:
            our_obs = step[our_idx].get("observation", {})
            opp_active = our_obs.get("opp_active", {})
            opp_bench = our_obs.get("opp_bench", [])
            
            if isinstance(opp_active, dict) and "id" in opp_active:
                opp_cards_played.add(opp_active["id"])
            if isinstance(opp_bench, list):
                for b in opp_bench:
                    if isinstance(b, dict) and "id" in b:
                        opp_cards_played.add(b["id"])
                        
            # Also check options in our observation for target selection
            for opt in our_obs.get("options", []):
                if isinstance(opt, dict) and "id" in opt:
                    pass

        names = [get_card_name(c) for c in opp_cards_played if get_card_name(c) is not None]
        names_str = " ".join(names)
        archetype = identify_deck_archetype(names_str) if names_str else "Unknown"

        result = "TIE"
        if our_reward == 1:
            result = "WIN"
            wins += 1
        elif our_reward == -1:
            result = "LOSS"
            losses += 1
        else:
            ties += 1
            
        matches.append({
            "id": ep_id,
            "length": len(steps),
            "result": result,
            "archetype": archetype,
            "status": final_step[our_idx].get("status", ""),
            "opp_cards": names
        })

    with open(f"{OUT_DIR}/complete_match_history.md", "w") as f:
        f.write(f"# Candidate D Match History\n\n")
        f.write(f"Total Games Analyzed: {len(matches)}\n")
        f.write(f"Wins: {wins}, Losses: {losses}, Ties: {ties}\n\n")
        
        f.write("| Episode ID | Result | Archetype | Length | Status | Opponent Cards Seen |\n")
        f.write("|---|---|---|---|---|---|\n")
        for m in sorted(matches, key=lambda x: int(x["id"]) if x["id"].isdigit() else 0, reverse=True):
            f.write(f"| {m['id']} | **{m['result']}** | {m['archetype']} | {m['length']} | {m['status']} | {', '.join(m['opp_cards'][:5])}... |\n")

if __name__ == "__main__":
    analyze_replays()
