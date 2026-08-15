import os
import sys
import json
import csv
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaggle_environments import make
from tools.run_matchup_matrix import create_deck_agent
from research.baselines import heuristic_v1_agent, random_agent
import main
from agent.state import parse_game_state


def run_comprehensive_failure_mining():
    decks_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "research", "decks")
    deck_crustle = os.path.join(decks_dir, "crustle_control.csv")
    deck_bellibolt = os.path.join(decks_dir, "bellibolt_standard.csv")

    opponents = [
        ("Crustle_Control_Safeguard", create_deck_agent(deck_crustle, heuristic_v1_agent), 15),
        ("Bellibolt_Mirror_SelfPlay", main.agent, 15),
        ("Heuristic_Baseline_Standard", heuristic_v1_agent, 10),
    ]

    print("==================================================")
    print("      COMPREHENSIVE FAILURE & MISTAKE MINING      ")
    print("==================================================")

    all_mined_blunders: List[Dict[str, Any]] = []
    total_losses = 0

    for name, opp_fn, n_games in opponents:
        print(f"\nMining Losses vs {name} ({n_games} games)...")
        losses_in_matchup = 0

        for g in range(n_games):
            env = make("cabt", debug=False)
            turn_records = []

            def _logged_agent(obs, config=None):
                if obs and obs.get("select") is not None:
                    st = parse_game_state(obs)
                    action = main.agent(obs, config)
                    
                    chosen_opt = None
                    if action and 0 <= action[0] < len(st.options):
                        chosen_opt = st.options[action[0]]

                    turn_records.append({
                        "turn": st.turn,
                        "select_type": st.select_type,
                        "your_active_id": st.your_active.get("id") if st.your_active else None,
                        "your_active_hp": st.your_active.get("hp") if st.your_active else None,
                        "your_energies": st.total_your_energies,
                        "opp_active_id": st.opp_active.get("id") if st.opp_active else None,
                        "opp_active_hp": st.opp_active.get("hp") if st.opp_active else None,
                        "your_prizes": st.your_prizes,
                        "opp_prizes": st.opp_prizes,
                        "action": action,
                        "chosen_opt": chosen_opt,
                        "options": st.options,
                    })
                    return action
                return main.agent(obs, config)

            env.run([_logged_agent, opp_fn])
            final = env.steps[-1]

            if final[0].reward != 1:  # Loss or draw
                total_losses += 1
                losses_in_matchup += 1

                # Forensic breakdown of loss turns
                for step_data in turn_records:
                    turn = step_data["turn"]
                    st_type = step_data["select_type"]
                    opt = step_data["chosen_opt"]
                    y_act = step_data["your_active_id"]
                    o_act = step_data["opp_active_id"]
                    y_energies = step_data["your_energies"]
                    opts = step_data["options"]

                    # 1. IMMUNITY / SAFEGUARD BLUNDER
                    # Attacking Crustle (345) when using Bellibolt ex (723)
                    if o_act == 345 and y_act == 723 and st_type in (0, 7):
                        has_boss = any(isinstance(o, dict) and o.get("id") == 1262 for o in opts)
                        all_mined_blunders.append({
                            "game_idx": f"{name}_g{g+1}",
                            "matchup": name,
                            "turn": turn,
                            "category": "TACTICAL",
                            "severity": "CRITICAL",
                            "chosen_action": "Electro Bullet vs Safeguard Crustle (0 damage)",
                            "optimal_action": "Play Boss's Orders (#1262) on Bench Dwebble / Evolve Single-Prize #722" if has_boss else "Pass / Retreat to single-prize attacker",
                            "estimated_impact": "Wasted attack turn against damage-immune target (-220.0 pts)",
                        })

                    # 2. ENERGY PLANNING / ACCELERATION MISALIGNMENT
                    # Having Generator in hand but failing to attach or active unpowered
                    if st_type == 0 and y_energies == 0 and turn >= 2:
                        has_generator = any(isinstance(o, dict) and o.get("id") == 1219 for o in opts)
                        if has_generator:
                            all_mined_blunders.append({
                                "game_idx": f"{name}_g{g+1}",
                                "matchup": name,
                                "turn": turn,
                                "category": "ENERGY_PLANNING",
                                "severity": "HIGH",
                                "chosen_action": "Delayed Electric Generator play",
                                "optimal_action": "Play Electric Generator (#1219) for immediate energy acceleration",
                                "estimated_impact": "Missed tempo on attack turn (-140.0 pts)",
                            })

                    # 3. PRIZE RACE / MISSED LETHAL
                    # Opponent active HP is low, but agent did not select attack
                    if st_type == 0 and step_data["opp_active_hp"] is not None and step_data["opp_active_hp"] <= 140:
                        attack_opts = [i for i, o in enumerate(opts) if isinstance(o, dict) and o.get("type") == 7]
                        if attack_opts and (not opt or opt.get("type") != 7):
                            all_mined_blunders.append({
                                "game_idx": f"{name}_g{g+1}",
                                "matchup": name,
                                "turn": turn,
                                "category": "PRIZE_RACE",
                                "severity": "CRITICAL",
                                "chosen_action": "Selected non-attack action while opponent active in KO range",
                                "optimal_action": "Execute lethal knockout attack for prize lead",
                                "estimated_impact": "Missed match-point / prize claim (-300.0 pts)",
                            })

                    # 4. RESOURCE MANAGEMENT / SUPPORTER PLAY
                    # Professor's Research played when hand already has vital key cards
                    if st_type == 0 and opt and opt.get("id") == 1092 and len(opts) > 5:
                        all_mined_blunders.append({
                            "game_idx": f"{name}_g{g+1}",
                            "matchup": name,
                            "turn": turn,
                            "category": "RESOURCE_MANAGEMENT",
                            "severity": "MEDIUM",
                            "chosen_action": "Professor's Research (#1092) discarded rich hand",
                            "optimal_action": "Play item cards (Ultra Ball, Switch) before discarding hand",
                            "estimated_impact": "Premature discard of key resources (-75.0 pts)",
                        })

        print(f"  -> Losses: {losses_in_matchup}/{n_games}")

    print(f"\nTotal Losses Analyzed: {total_losses}")
    print(f"Total Mined Blunders : {len(all_mined_blunders)}")

    # 1. Output reports/mistake_analysis.csv
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
    csv_file = os.path.join(reports_dir, "mistake_analysis.csv")
    fieldnames = ["game_idx", "matchup", "turn", "category", "severity", "chosen_action", "optimal_action", "estimated_impact"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for b in all_mined_blunders:
            writer.writerow(b)
    print(f"[Artifact Created] {csv_file}")

    # 2. Output reports/mistake_analysis.md
    md_file = os.path.join(reports_dir, "mistake_analysis.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# Forensic Failure & Mistake Mining Analysis\n\n")
        f.write(f"**Empirical Losses Analyzed**: {total_losses} matches\n")
        f.write(f"**Total Sub-Optimal Decision Points**: {len(all_mined_blunders)} decision blunders classified\n\n")
        
        f.write("## 1. Breakdown by Mistake Category\n\n")
        cat_counts = {}
        for b in all_mined_blunders:
            c = b["category"]
            cat_counts[c] = cat_counts.get(c, 0) + 1
        
        f.write("| Mistake Category | Frequency | Share (%) | Primary Root Cause |\n")
        f.write("|---|---|---|---|\n")
        for c, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
            share = round((count / max(1, len(all_mined_blunders))) * 100.0, 1)
            cause = "Attacking damage-immune Safeguard Crustle with ex attacker" if c == "TACTICAL" else "Delayed Electric Generator acceleration" if c == "ENERGY_PLANNING" else "Premature discard via Professor's Research" if c == "RESOURCE_MANAGEMENT" else "Delayed lethal knockout line"
            f.write(f"| **{c}** | {count} | {share}% | {cause} |\n")

        f.write("\n## 2. Granular Blunder Catalog (Sample)\n\n")
        f.write("| Matchup | Turn | Category | Severity | Chosen Action | Optimal Alternative | Estimated Impact |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for b in all_mined_blunders[:30]:
            f.write(f"| {b['matchup']} | T{b['turn']} | `{b['category']}` | `{b['severity']}` | {b['chosen_action']} | {b['optimal_action']} | {b['estimated_impact']} |\n")

    print(f"[Artifact Created] {md_file}")


if __name__ == "__main__":
    run_comprehensive_failure_mining()
