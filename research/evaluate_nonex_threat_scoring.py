import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_pokemon_data
from agent.state import GameState
from agent.evaluator import is_target_immune_to_ex, is_ex_attacker, calculate_immunity_multiplier

init_card_database()

def evaluate_nonex_board_threat(state: GameState) -> dict:
    """
    Candidate C Generalized Non-ex Threat Evaluator.
    Calculates true un-Safeguarded threat from opponent active and bench.
    """
    our_active = state.your_active
    our_is_safeguarded = is_target_immune_to_ex(our_active)
    our_active_hp = float(our_active.get("hp", 100)) if our_active else 100.0
    
    threats = []
    all_opp = ([state.opp_active] if state.opp_active else []) + [b for b in state.opp_bench if b]
    
    for pkmn in all_opp:
        cid = pkmn.get("id", 0)
        card = get_card(cid)
        pdata = get_pokemon_data(cid)
        
        is_ex = is_ex_attacker(pkmn) or (card and (card.get("ex") or card.get("megaEx")))
        energies = pkmn.get("energies", [])
        energy_cnt = len(energies) if isinstance(energies, list) else 0
        hp = float(pkmn.get("hp", 100))
        
        # Estimate damage
        if cid == 674:  # Hariyama
            base_dmg = 210.0
            attack_cost = 3
        elif cid == 678:  # Mega Lucario ex
            base_dmg = 240.0
            attack_cost = 2
        elif cid == 666:  # Cinderace
            base_dmg = 100.0
            attack_cost = 1
        elif cid in (723, 756):  # Bellibolt ex / Kangaskhan ex
            base_dmg = 160.0
            attack_cost = 2
        elif card and card.get("stage1"):
            base_dmg = 120.0
            attack_cost = 2
        else:
            base_dmg = float(max(20, energy_cnt * 30))
            attack_cost = 2
            
        # Check Safeguard penetration
        if our_is_safeguarded and is_ex:
            effective_dmg = 0.0
            is_safeguard_blocked = True
        else:
            effective_dmg = base_dmg
            is_safeguard_blocked = False
            
        energy_distance = max(0, attack_cost - energy_cnt)
        is_attack_ready = (energy_distance == 0)
        is_lethal = (effective_dmg >= our_active_hp)
        
        # Calculate threat score
        threat_score = 0.0
        if not is_safeguard_blocked:
            threat_score += effective_dmg * (1.0 if is_attack_ready else (0.6 if energy_distance == 1 else 0.2))
            if is_lethal and is_attack_ready:
                threat_score += 300.0  # Massive priority threat!
                
        threats.append({
            "card_id": cid,
            "name": card.get("name") if card else f"Card #{cid}",
            "is_ex": is_ex,
            "is_safeguard_blocked": is_safeguard_blocked,
            "energy_cnt": energy_cnt,
            "effective_dmg": effective_dmg,
            "is_attack_ready": is_attack_ready,
            "is_lethal": is_lethal,
            "threat_score": threat_score
        })
        
    threats.sort(key=lambda x: x["threat_score"], reverse=True)
    return {
        "our_active_safeguarded": our_is_safeguarded,
        "primary_threat": threats[0] if threats else None,
        "all_threats": threats
    }

# Test Scenario: Episode 93482398 Turn 5 board state
state = GameState(
    your_active={"id": 345, "hp": 130, "energies": [1, 1]},
    your_bench=[{"id": 345, "hp": 130, "energies": [1]}],
    opp_active={"id": 678, "hp": 260, "energies": [6, 6]},  # Mega Lucario ex (2 energies)
    opp_bench=[{"id": 674, "hp": 140, "energies": [6, 6, 6]}], # Hariyama (3 energies)
)

res = evaluate_nonex_board_threat(state)
print("=== NON-EX THREAT EVALUATION ON EPISODE 93482398 STATE ===")
print(f"Our Active Safeguarded: {res['our_active_safeguarded']}")
print("\nThreat Ranking:")
for t in res["all_threats"]:
    print(f"  • {t['name']:<20} | Is EX: {str(t['is_ex']):<5} | Safeguard Blocked: {str(t['is_safeguard_blocked']):<5} | Ready: {str(t['is_attack_ready']):<5} | Effective Dmg: {t['effective_dmg']:.0f} | Threat Score: {t['threat_score']:.1f}")

primary = res["primary_threat"]
print(f"\nIdentified #1 Target / Threat: {primary['name']} (Score: {primary['threat_score']:.1f})")
