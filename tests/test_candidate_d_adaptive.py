import pytest
from typing import Dict, Any, List

from agent.state import GameState, parse_game_state
from agent.policy import (
    rank_card_play_options,
    rank_discard_options,
    rank_attack_options,
    rank_energy_attachment_options,
    rank_target_options,
)
from agent.opponent_model import (
    evaluate_opponent_threats,
    ThreatReadiness,
    ThreatCategory,
    classify_single_threat,
)
from agent.evaluator import (
    is_target_immune_to_ex,
    is_ex_attacker,
    calculate_immunity_multiplier,
    evaluate_board_value,
)
from agent.goals import GoalPlanner, StrategicGoal
from agent.action_selector import select_heuristic_action


# 1. Zero-Bench Opening Test
def test_zero_bench_opening_rule_preserved():
    """Verify BENCH_FIRST: basic Pokémon receives +350.0 priority when bench is 0."""
    state = GameState(
        your_active={"id": 344, "hp": 60, "energies": []},
        your_bench=[],
        your_hand=[{"id": 344}, {"id": 1121}],
        options=[
            {"type": 1, "id": 344, "text": "Play Dwebble to Bench"},
            {"type": 0, "id": 1121, "text": "Play Ultra Ball Search"},
        ],
        select_type=0, min_count=1, max_count=1
    )
    ranks = rank_card_play_options(state)
    assert ranks[0][0] == 0, f"Expected Play Dwebble to Bench (opt 0) to be #1, got {ranks[0]}"
    assert ranks[0][1] >= 350.0, f"Expected score >= 350.0, got {ranks[0][1]}"


# 2. Basic Discard Protection Test
def test_basic_discard_protection_preserved():
    """Verify PROTECT_BASIC_DISCARD: Basic Pokémon gets -5000.0 penalty when bench is 0."""
    state = GameState(
        your_active={"id": 344, "hp": 60, "energies": []},
        your_bench=[],
        your_hand=[{"id": 344}, {"id": 1}],
        options=[
            {"type": 0, "id": 344, "text": "Discard Dwebble"},
            {"type": 0, "id": 1, "text": "Discard Grass Energy"},
        ],
        select_type=1, min_count=1, max_count=1
    )
    ranks = rank_discard_options(state.options, state)
    assert ranks[0][0] == 1, "Expected Grass Energy (opt 1) to be preferred discard over Basic"
    assert ranks[1][1] <= -4000.0, "Expected severe penalty on discarding only Basic Pokemon"


# 3. EX + Safeguard Test
def test_ex_safeguard_immunity():
    """Verify Pokémon EX attacks against Crustle deal 0 effective damage and have 0 threat score."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[{"id": 345, "hp": 130, "energies": []}],
        opp_active={"id": 756, "hp": 300, "energies": [1, 1]},  # Mega Kangaskhan ex
        opp_bench=[],
    )
    threat = classify_single_threat(state.opp_active, state, is_active=True)
    assert threat.is_ex is True
    assert threat.is_safeguard_blocked is True
    assert threat.effective_damage == 0.0
    assert threat.threat_score <= 20.0


# 4. Non-EX Lethal Threat Test
def test_nonex_lethal_threat_detection():
    """Verify Non-EX attacker (e.g. 210 DMG) is correctly recognized as unblocked lethal breaker."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[{"id": 345, "hp": 130, "energies": [1]}],
        opp_active={"id": 674, "hp": 150, "energies": [6, 6, 6]},  # Hariyama 3 energies
        opp_bench=[],
    )
    threat = classify_single_threat(state.opp_active, state, is_active=True)
    assert threat.is_ex is False
    assert threat.is_safeguard_blocked is False
    assert threat.effective_damage >= 140.0
    assert threat.is_lethal is True
    assert threat.threat_score >= 350.0


# 5. Distant Non-EX Threat Test
def test_distant_nonex_threat_staging():
    """Verify Non-EX Pokémon with 0 energies is staged as T3_DISTANT and not over-penalized."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[],
        opp_active={"id": 674, "hp": 150, "energies": []},  # Hariyama with 0 energies
        opp_bench=[],
    )
    threat = classify_single_threat(state.opp_active, state, is_active=True)
    assert threat.readiness == ThreatReadiness.T3_DISTANT
    assert threat.threat_score < 100.0


# 6. Energy Ramp Readiness Test
def test_energy_ramp_threat_readiness():
    """Verify attacker with 1 missing energy is staged as T1_NEXT_TURN."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[],
        opp_active={"id": 723, "hp": 330, "energies": [4]},  # Bellibolt ex with 1 energy (needs 2)
        opp_bench=[],
    )
    threat = classify_single_threat(state.opp_active, state, is_active=True)
    assert threat.readiness == ThreatReadiness.T1_NEXT_TURN


# 7. Evolution Threat Detection
def test_evolution_threat_categorization():
    """Verify basic Pokémon with attached energy is tagged with EVOLUTION_THREAT."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[],
        opp_active={"id": 673, "hp": 70, "energies": [6, 6]},  # Makuhita with 2 energies
        opp_bench=[],
    )
    threat = classify_single_threat(state.opp_active, state, is_active=True)
    assert ThreatCategory.EVOLUTION_THREAT in threat.categories


# 8. Bench Engine Threat Detection
def test_bench_engine_threat_detection():
    """Verify benched threat evaluation correctly evaluates all benched Pokémon."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[{"id": 345, "hp": 130, "energies": []}],
        opp_active={"id": 678, "hp": 260, "energies": [6, 6]},  # Mega Lucario ex (blocked)
        opp_bench=[{"id": 674, "hp": 150, "energies": [6, 6, 6]}],  # Hariyama (ready!)
    )
    model = evaluate_opponent_threats(state)
    assert model.primary_threat is not None
    assert model.primary_threat.card_id == 674
    assert model.opponent_win_condition == "SAFEGUARD_BREAKER_PIVOT"


# 9. Prize Race Match-Point Urgency
def test_prize_race_goal_alignment():
    """Verify GOAL_WIN_NOW is activated at match point (your_prizes <= 2)."""
    state = GameState(
        your_prizes=1, opp_prizes=3, your_deck_count=20, turn=6,
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[{"id": 345, "hp": 130, "energies": []}],
    )
    goal = GoalPlanner.identify_goal(state)
    assert goal.primary_goal == StrategicGoal.GOAL_WIN_NOW
    assert goal.attack_priority_bonus >= 3000.0


# 10. Hidden Information Hand Size Estimation
def test_hidden_information_belief_update():
    """Verify Bayesian belief updates handle hidden hand size gracefully."""
    from agent.belief_state import BeliefStateTracker
    tracker = BeliefStateTracker()
    state = GameState(opp_hand_count=6, opp_deck_count=35, opp_discard=[])
    beliefs = tracker.update_beliefs(state)
    assert 0.0 <= beliefs.p_energy <= 1.0
    assert 0.0 <= beliefs.p_boss_gust <= 1.0


# 11. Low-Resource Anti-Deckout Test
def test_low_resource_anti_deckout():
    """Verify Professor's Research / draw cards are penalized with -10000 when deck <= 5."""
    state = GameState(
        your_deck_count=4, turn=9,
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[],
        your_hand=[{"id": 1092}],
        options=[{"type": 0, "id": 1092, "text": "Play Draw Supporter"}],
        select_type=0, min_count=1, max_count=1
    )
    ranks = rank_card_play_options(state)
    assert ranks[0][1] <= -5000.0, "Expected severe anti-deckout penalty on draw cards"


# 12. Mixed EX / Non-EX Matchup Prioritization
def test_mixed_ex_nonex_gust_targeting():
    """Verify that when active is Safeguarded, Gust targeting prioritizes benched non-EX breaker."""
    state = GameState(
        your_active={"id": 345, "hp": 130, "energies": [1, 1]},
        your_bench=[],
        opp_active={"id": 678, "hp": 260, "energies": [6, 6]},
        opp_bench=[
            {"id": 674, "hp": 150, "energies": [6, 6, 6]},  # Benched Hariyama (Non-EX)
            {"id": 756, "hp": 300, "energies": []},          # Benched Kangaskhan ex
        ],
        options=[
            {"type": 1, "id": 674, "inPlayArea": 5, "inPlayIndex": 0, "text": "Target Hariyama (Non-EX)"},
            {"type": 1, "id": 756, "inPlayArea": 5, "inPlayIndex": 1, "text": "Target Kangaskhan ex"},
        ],
        select_type=1, min_count=1, max_count=1
    )
    ranks = rank_target_options(state.options, state)
    assert ranks[0][0] == 0, f"Expected Non-EX Breaker (opt 0) to be #1 gust target, got {ranks[0]}"
