"""
Comprehensive Forensic Match Analyzer for all 10 Candidate F Public Kaggle Episodes.
"""

import os
import json
import csv
from typing import Dict, Any, List

def analyze_all_episodes():
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

    results_summary = []

    for ep_id in episodes:
        replay_path = f"reports/leaderboard_optimization/candidate_f_live/public_{ep_id}/episode-{ep_id}-replay.json"
        if not os.path.exists(replay_path):
            continue

        with open(replay_path) as f:
            replay = json.load(f)

        steps = replay.get("steps", [])
        total_steps = len(steps)

        # Determine which player is Candidate F (deck contains Crustle 345 / Dwebble 344)
        # Look at initial step 0 / 1 deck submissions
        our_player_idx = None
        for p_idx in [0, 1]:
            cur = steps[1][p_idx].get("observation", {}).get("current")
            if cur:
                c = json.loads(cur) if isinstance(cur, str) else cur
                # Or check deck list in step 0 action
                deck_act = steps[0][p_idx].get("action")
                if isinstance(deck_act, list) and 345 in deck_act:
                    our_player_idx = p_idx
                    break
        if our_player_idx is None:
            # Fallback check active/bench
            for s in steps:
                for p_idx in [0, 1]:
                    cur = s[p_idx].get("observation", {}).get("current")
                    if cur:
                        c = json.loads(cur) if isinstance(cur, str) else cur
                        for p in c.get("players", []):
                            for a in p.get("active", []) + p.get("bench", []):
                                if a and a.get("id") in [344, 345]:
                                    our_player_idx = p.get("playerIndex", p_idx)
                                    break

        if our_player_idx is None:
            our_player_idx = 1 # default

        opp_player_idx = 1 - our_player_idx

        final_step = steps[-1]
        our_reward = final_step[our_player_idx].get("reward", 0)
        opp_reward = final_step[opp_player_idx].get("reward", 0)
        our_status = final_step[our_player_idx].get("status", "UNKNOWN")
        opp_status = final_step[opp_player_idx].get("status", "UNKNOWN")

        win = (our_reward is not None and our_reward > 0)
        loss = (our_reward is not None and our_reward < 0)
        draw = not win and not loss

        outcome = "WIN (+1)" if win else ("LOSS (-1)" if loss else "DRAW (0)")

        # Collect opponent cards
        opp_cards_seen = set()
        for s in steps:
            cur = s[our_player_idx].get("observation", {}).get("current")
            if cur:
                c = json.loads(cur) if isinstance(cur, str) else cur
                players = c.get("players", [])
                if len(players) >= 2:
                    opp_p = players[opp_player_idx]
                    for a in opp_p.get("active", []):
                        if a and a.get("id"): opp_cards_seen.add(a["id"])
                    for b in opp_p.get("bench", []):
                        if b and b.get("id"): opp_cards_seen.add(b["id"])

        opp_card_details = [card_info.get(c, {"name": f"Card {c}", "is_ex": False}) for c in opp_cards_seen]
        has_ex = any(cd.get("is_ex", False) for cd in opp_card_details)
        opp_archetype_names = [cd["name"] for cd in opp_card_details]

        # Classify opponent archetype
        archetype_label = "Unknown"
        if any("Lucario" in n for n in opp_archetype_names):
            archetype_label = "Mega Lucario ex (Mega EX Aggro)"
        elif any("Duraludon" in n for n in opp_archetype_names):
            archetype_label = "Duraludon (Metal Non-EX Resist)"
        elif any("Cinderace" in n for n in opp_archetype_names):
            archetype_label = "Cinderace (Fire Stage 2 Donk)"
        elif any("Alakazam" in n for n in opp_archetype_names):
            archetype_label = "Alakazam (Psychic Non-EX Swarm)"
        elif any("Trevenant" in n for n in opp_archetype_names):
            archetype_label = "Hop's Trevenant (Non-EX Single)"
        elif any("Grimmsnarl" in n for n in opp_archetype_names):
            archetype_label = "Marnie's Grimmsnarl ex (Darkness EX)"
        elif any("Abomasnow" in n for n in opp_archetype_names):
            archetype_label = "Mega Abomasnow ex (Water/Grass EX)"
        elif any("Bellibolt" in n for n in opp_archetype_names):
            archetype_label = "Bellibolt ex (Lightning EX)"
        elif any("Farigiraf" in n for n in opp_archetype_names):
            archetype_label = "Farigiraf ex (Safeguard Mirror)"
        elif has_ex:
            archetype_label = f"EX Deck ({', '.join(opp_archetype_names[:2])})"
        else:
            archetype_label = f"Non-EX Deck ({', '.join(opp_archetype_names[:2])})"

        # Check logs for latency and errors
        invalids = 0
        fallbacks = 0
        runtime_errors = 0
        latencies = []

        log_path = f"reports/leaderboard_optimization/candidate_f_live/public_{ep_id}/agent-{our_player_idx}-logs.json"
        if os.path.exists(log_path):
            try:
                with open(log_path) as lf:
                    log_data = json.load(lf)
                    for entry in log_data:
                        if isinstance(entry, list) and len(entry) > 0:
                            item = entry[0]
                            dur = item.get("duration", 0) * 1000.0
                            latencies.append(dur)
                            if item.get("stderr"):
                                runtime_errors += 1
            except Exception:
                pass

        p95_lat = sorted(latencies)[int(len(latencies)*0.95)] if latencies else 0.0

        # Classify Loss / Win Mechanism
        if win:
            if has_ex:
                classification = "SAFEGUARD_EX_SUPPRESSION (Immunity Sweep)"
            else:
                classification = "NON_EX_TACTICAL_VICTORY (Prize Trade Advantage)"
        else:
            if "Cinderace" in archetype_label:
                classification = "MATCHUP_HARD_COUNTER / FIRE_WEAKNESS_DONK"
            elif "Duraludon" in archetype_label or any(cd.get("resistance") == "1" for cd in opp_card_details):
                classification = "MATCHUP_HARD_COUNTER / METAL_RESISTANCE_DEFICIT"
            elif total_steps < 30:
                classification = "OPENING_DRAW_VARIANCE (Lone Basic Knockout)"
            else:
                classification = "SINGLE_PRIZE_TRADE_DEFICIT"

        match_info = {
            "episode_id": ep_id,
            "our_seat": our_player_idx,
            "outcome": outcome,
            "reward": our_reward,
            "steps": total_steps,
            "archetype": archetype_label,
            "has_ex": has_ex,
            "opp_cards": opp_archetype_names,
            "classification": classification,
            "p95_latency_ms": round(p95_lat, 2),
            "invalids": invalids,
            "fallbacks": fallbacks,
            "runtime_errors": runtime_errors,
        }
        results_summary.append(match_info)
        print(f"Episode {ep_id}: {outcome:9s} in {total_steps:3d} steps vs {archetype_label:35s} | Reason: {classification}")

    with open("reports/leaderboard_optimization/candidate_f_10_public_analysis.json", "w") as f:
        json.dump(results_summary, f, indent=2)

    return results_summary

if __name__ == "__main__":
    analyze_all_episodes()
