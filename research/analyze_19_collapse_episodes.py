"""
Full 19-Episode Forensic Analyzer & Meta Shift Detector for Candidate F.
"""

import os
import json
import csv
from typing import Dict, Any, List

def analyze_all_19_episodes():
    episodes = [
        93569861,
        93570797,
        93571687,
        93572601,
        93573491,
        93574392,
        93575313,
        93576224,
        93577146,
        93578041,
        93578958,
        93579869,
        93580784,
        93581692,
        93582613,
        93583569,
        93584447,
        93585347,
        93586267,
    ]

    card_names = {}
    card_info = {}
    with open("data/EN Card Data.csv") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cid = int(r["Card ID"])
            card_names[cid] = r["Card Name"]
            card_info[cid] = {
                "name": r["Card Name"],
                "stage": int(r.get("Evolution Stage", 0)) if r.get("Evolution Stage") else 0,
                "is_ex": (r.get("isEX") == "True"),
                "hp": int(r.get("HP", 0)) if r.get("HP") else 0,
                "weakness": r.get("Weakness", ""),
                "resistance": r.get("Resistance", ""),
            }

    results = []

    for idx, ep_id in enumerate(episodes):
        replay_path = f"reports/leaderboard_optimization/candidate_f_collapse/public_{ep_id}/episode-{ep_id}-replay.json"
        if not os.path.exists(replay_path):
            continue

        with open(replay_path) as f:
            replay = json.load(f)

        steps = replay.get("steps", [])
        total_steps = len(steps)

        our_p_idx = None
        for p in [0, 1]:
            cur = steps[1][p].get("observation", {}).get("current")
            if cur:
                c = json.loads(cur) if isinstance(cur, str) else cur
                deck_act = steps[0][p].get("action")
                if isinstance(deck_act, list) and 345 in deck_act:
                    our_p_idx = p
                    break
        if our_p_idx is None:
            our_p_idx = 1

        opp_p_idx = 1 - our_p_idx

        final_step = steps[-1]
        our_reward = final_step[our_p_idx].get("reward", 0)
        win = (our_reward is not None and our_reward > 0)
        outcome = "WIN (+1)" if win else "LOSS (-1)"

        # Collect opponent cards
        opp_cards_seen = set()
        for s in steps:
            cur = s[our_p_idx].get("observation", {}).get("current")
            if cur:
                c = json.loads(cur) if isinstance(cur, str) else cur
                players = c.get("players", [])
                if len(players) >= 2:
                    opp_p = players[opp_p_idx]
                    for a in opp_p.get("active", []) + opp_p.get("bench", []):
                        if a and a.get("id"): opp_cards_seen.add(a["id"])

        opp_card_details = [card_info.get(c, {"name": f"Card {c}", "is_ex": False}) for c in opp_cards_seen]
        has_ex = any(cd.get("is_ex", False) for cd in opp_card_details)
        opp_names = [cd["name"] for cd in opp_card_details]

        # Archetype identification
        archetype = "Unknown"
        if any("Lucario" in n for n in opp_names):
            archetype = "Mega Lucario ex (Mega EX Aggro)"
        elif any("Duraludon" in n for n in opp_names):
            archetype = "Duraludon (Metal Non-EX Resist)"
        elif any("Cinderace" in n for n in opp_names):
            archetype = "Cinderace (Fire Stage 2 Donk)"
        elif any("Gible" in n or "Garchomp" in n for n in opp_names):
            archetype = "Cynthia's Gible/Gabite (Dragon/Fighting Non-EX)"
        elif any("Grimmsnarl" in n for n in opp_names):
            archetype = "Marnie's Grimmsnarl ex (Darkness EX)"
        elif any("Crustle" in n for n in opp_names):
            archetype = "Crustle Safeguard (Mirror)"
        elif any("Budew" in n or "Fezandipiti" in n for n in opp_names):
            archetype = "Multi-Prize EX Box (Fezandipiti)"
        elif any("Alakazam" in n for n in opp_names):
            archetype = "Alakazam (Psychic Non-EX Swarm)"
        elif any("Charizard" in n for n in opp_names):
            archetype = "Charizard ex (Fire EX Aggro)"
        elif any("Starmie" in n for n in opp_names):
            archetype = "Mega Starmie ex (Water EX)"
        elif any("Mewtwo" in n for n in opp_names):
            archetype = "Mewtwo ex (Psychic EX)"
        elif any("Pikachu" in n or "Bellibolt" in n for n in opp_names):
            archetype = "Lightning Aggro (Bellibolt/Pikachu)"
        elif has_ex:
            archetype = f"EX Deck ({', '.join(opp_names[:2])})"
        else:
            archetype = f"Non-EX Deck ({', '.join(opp_names[:2])})"

        # Loss classification
        if win:
            loss_cat = "N/A (VICTORY)"
        else:
            if "Cinderace" in archetype:
                loss_cat = "LOSS_TURN_1_DONK / FIRE_WEAKNESS"
            elif "Duraludon" in archetype or any(cd.get("resistance") == "1" for cd in opp_card_details):
                loss_cat = "LOSS_TYPE_RESISTANCE (Metal -30 Deficit)"
            elif total_steps < 30:
                loss_cat = "LOSS_OPENING_BRICK / EARLY_DONK"
            elif "Mirror" in archetype:
                loss_cat = "LOSS_MATCHUP_VARIANCE (Mirror 1st Attacker)"
            else:
                loss_cat = "LOSS_NONEX_PRIZE_RACE / SINGLE_PRIZE_DEFICIT"

        sample_group = "Batch 1 (Games 1-10)" if idx < 10 else "Batch 2 (Games 11-19)"

        item = {
            "game_number": idx + 1,
            "episode_id": ep_id,
            "sample_group": sample_group,
            "outcome": outcome,
            "reward": our_reward,
            "steps": total_steps,
            "archetype": archetype,
            "has_ex": has_ex,
            "opp_names": opp_names,
            "loss_classification": loss_cat,
        }
        results.append(item)
        print(f"Game {idx+1:2d} (Ep {ep_id}): {outcome:9s} in {total_steps:3d} steps vs {archetype:40s} | {sample_group} | {loss_cat}")

    with open("reports/leaderboard_optimization/candidate_f_19_public_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    analyze_all_19_episodes()
