import json
import glob
import os
import pandas as pd
from collections import defaultdict

df = pd.read_csv("data/EN Card Data.csv")
id_to_name = dict(zip(df["Card ID"], df["Card Name"]))

ROOT = "reports/leaderboard_optimization/candidate_m_live"

files = sorted(
    glob.glob(ROOT + "/public_*/episode-*-replay.json"),
    key=lambda x: int(os.path.basename(os.path.dirname(x)).split("_")[-1])
)

print(f"Total Public Replay Files Found: {len(files)}")

episodes_data = []
archetype_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "draws": 0, "total": 0})

for path in files:
    ep_id = int(os.path.basename(os.path.dirname(path)).split("_")[-1])
    with open(path) as f:
        try:
            d = json.load(f)
        except Exception as e:
            continue

    steps = d.get("steps", [])
    if len(steps) < 2:
        continue

    m_seat = None
    opp_cards_seen = set()
    opp_archetype = "Unknown"
    is_mirror = False
    
    for s in steps:
        obs0 = s[0].get("observation", {})
        cur = obs0.get("current")
        if cur and isinstance(cur, dict):
            players = cur.get("players", [])
            if len(players) >= 2:
                # Extract all card IDs seen for p0 and p1
                p0_card_ids = []
                p1_card_ids = []

                if players[0].get("active"):
                    p0_card_ids.extend([c.get("id") for c in players[0]["active"] if isinstance(c, dict)])
                if players[0].get("bench"):
                    p0_card_ids.extend([c.get("id") for c in players[0]["bench"] if isinstance(c, dict)])

                if players[1].get("active"):
                    p1_card_ids.extend([c.get("id") for c in players[1]["active"] if isinstance(c, dict)])
                if players[1].get("bench"):
                    p1_card_ids.extend([c.get("id") for c in players[1]["bench"] if isinstance(c, dict)])

                p0_names = [id_to_name.get(cid, "") for cid in p0_card_ids if cid]
                p1_names = [id_to_name.get(cid, "") for cid in p1_card_ids if cid]

                p0_has_dwebble = any("Dwebble" in n or "Crustle" in n for n in p0_names)
                p1_has_dwebble = any("Dwebble" in n or "Crustle" in n for n in p1_names)

                if p0_has_dwebble and not p1_has_dwebble:
                    m_seat = 0
                elif p1_has_dwebble and not p0_has_dwebble:
                    m_seat = 1
                elif p0_has_dwebble and p1_has_dwebble:
                    is_mirror = True
                    opp_archetype = "Crustle Safeguard Mirror"
                    if m_seat is None:
                        m_seat = 0

                if m_seat is not None:
                    opp_p_ids = p1_card_ids if m_seat == 0 else p0_card_ids
                    for cid in opp_p_ids:
                        name = id_to_name.get(cid)
                        if name:
                            opp_cards_seen.add(name)

    if m_seat is None:
        m_seat = 0

    if not is_mirror:
        opp_names_str = " ".join(opp_cards_seen)
        if "Lucario" in opp_names_str or "Riolu" in opp_names_str:
            opp_archetype = "Mega Lucario ex Box"
        elif "Duraludon" in opp_names_str:
            opp_archetype = "Duraludon (Metal Resist)"
        elif "Cinderace" in opp_names_str or "Scorbunny" in opp_names_str or "Raboot" in opp_names_str:
            opp_archetype = "Cinderace (Fire Weakness)"
        elif "Alakazam" in opp_names_str or "Abra" in opp_names_str or "Kadabra" in opp_names_str:
            opp_archetype = "Alakazam Swarm"
        elif "Trevenant" in opp_names_str or "Phantump" in opp_names_str:
            opp_archetype = "Trevenant Non-EX"
        elif any("ex" in n.lower() for n in opp_cards_seen):
            ex_cards = [n for n in opp_cards_seen if "ex" in n.lower()]
            opp_archetype = f"{ex_cards[0]} Box" if ex_cards else "EX Box"
        elif len(opp_cards_seen) > 0:
            clean_names = [n for n in opp_cards_seen if n and not n.isdigit() and "Energy" not in n]
            opp_archetype = f"Non-EX ({', '.join(clean_names[:2])})" if clean_names else "Single-Prize Non-EX"
        else:
            opp_archetype = "Non-EX Archetype"

    final_step = steps[-1]
    m_step = final_step[m_seat]
    r_m = m_step.get("reward")
    status_m = m_step.get("status")

    if r_m is not None and r_m > 0:
        result = "WIN"
    elif r_m is not None and r_m < 0:
        result = "LOSS"
    else:
        result = "DRAW/UNKNOWN"

    archetype_stats[opp_archetype]["total"] += 1
    if result == "WIN":
        archetype_stats[opp_archetype]["wins"] += 1
    elif result == "LOSS":
        archetype_stats[opp_archetype]["losses"] += 1
    else:
        archetype_stats[opp_archetype]["draws"] += 1

    clean_opp_cards = [n for n in opp_cards_seen if n and not n.isdigit() and "Energy" not in n]
    episodes_data.append({
        "ep_id": ep_id,
        "m_seat": m_seat,
        "result": result,
        "reward": r_m,
        "steps": len(steps),
        "status": status_m,
        "opp_archetype": opp_archetype,
        "opp_cards": clean_opp_cards[:4],
    })

print()
print("=" * 85)
print("CANDIDATE M (PTCG NEXUS v3.5) — 21 PUBLIC EPISODES ACCURATE FORENSICS")
print("=" * 85)

total_matches = len(episodes_data)
wins = sum(1 for e in episodes_data if e["result"] == "WIN")
losses = sum(1 for e in episodes_data if e["result"] == "LOSS")
draws = sum(1 for e in episodes_data if e["result"] == "DRAW/UNKNOWN")

print(f"Total Public Episodes: {total_matches}")
print(f"Candidate M Wins     : {wins}")
print(f"Candidate M Losses   : {losses}")
print(f"Candidate M Draws    : {draws}")
print(f"Live Win Rate        : {wins/total_matches*100:.2f}%")

print()
print("=" * 85)
print("MATCHUP ARCHETYPE PERFORMANCE MATRIX")
print("=" * 85)
print(f"{'Opponent Archetype':<34} | {'Record (W-L)':<14} | {'Win Rate':<10}")
print("-" * 68)

for arch, st in sorted(archetype_stats.items(), key=lambda x: x[1]["total"], reverse=True):
    tot = st["total"]
    w = st["wins"]
    l = st["losses"]
    wr = f"{w/tot*100:.1f}%" if tot > 0 else "0.0%"
    print(f"{arch:<34} | {w}W - {l}L        | {wr:<10}")

print()
print("=" * 85)
print("EPISODE-BY-EPISODE FORENSICS")
print("=" * 85)
print(f"{'Episode ID':<12} | {'Result':<6} | {'Seat':<6} | {'Steps':<6} | {'Opponent Archetype':<30} | {'Opponent Key Cards'}")
print("-" * 98)

for e in episodes_data:
    cards_str = ", ".join(e["opp_cards"]) if e["opp_cards"] else "N/A"
    print(f"{e['ep_id']:<12} | {e['result']:<6} | Seat {e['m_seat']} | {e['steps']:<6} | {e['opp_archetype']:<30} | {cards_str}")
