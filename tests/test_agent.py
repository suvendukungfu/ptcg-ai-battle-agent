import os
import sys
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from agent.state import parse_game_state, GameState
from agent.evaluator import (
    is_ex_attacker,
    is_target_immune_to_ex,
    calculate_immunity_multiplier,
    evaluate_board_value,
    estimate_raw_damage,
)
from agent.search import (
    shallow_risk_aware_search,
    project_action,
    estimate_opponent_counterattack,
)
from agent.opponent_model import (
    calculate_hypergeometric_prob,
    estimate_energy_probability,
    estimate_gust_probability,
    estimate_evolution_probability,
    estimate_next_attack_probability,
    estimate_opponent_threat,
)
from agent.risk_model import determine_risk_profile
from agent.fallback import deterministic_fallback, make_distinct_choice
from kaggle_environments import make


def test_deck_loading_and_validation():
    deck = main.load_and_validate_deck()
    assert isinstance(deck, list)
    assert len(deck) == 60
    assert all(isinstance(card_id, int) for card_id in deck)


def test_agent_turn_0_deck_submission():
    obs = {"select": None, "current": None}
    res = main.agent(obs)
    assert isinstance(res, list)
    assert len(res) == 60
    assert all(isinstance(c, int) for c in res)


def test_hypergeometric_probability_math():
    # 60 cards, 20 successes, draw 7 -> P(X >= 1) > 0.90
    p = calculate_hypergeometric_prob(60, 20, 7)
    assert 0.90 <= p <= 1.0

    # 0 successes -> P = 0.0
    assert calculate_hypergeometric_prob(60, 0, 7) == 0.0

    # Sample size 0 -> P = 0.0
    assert calculate_hypergeometric_prob(60, 10, 0) == 0.0


def test_opponent_model_estimations():
    obs = {
        "select": {"type": 0, "option": []},
        "current": {
            "yourIndex": 0,
            "players": [
                {"prize": [1, 2], "active": [{"id": 723, "hp": 350, "maxHp": 350, "energies": [3, 3]}]},
                {
                    "prize": [1, 2, 3, 4, 5],
                    "deckCount": 35,
                    "handCount": 5,
                    "active": [{"id": 723, "hp": 350, "maxHp": 350, "energies": [3]}],
                    "bench": [{"id": 721, "hp": 150}],
                    "discard": [1092, 3],
                },
            ],
        },
    }
    state = parse_game_state(obs)
    p_attack = estimate_next_attack_probability(state)
    assert 0.0 <= p_attack <= 1.0

    p_gust = estimate_gust_probability(state)
    assert 0.0 <= p_gust <= 1.0

    threat = estimate_opponent_threat(state)
    assert "threat_level" in threat
    assert threat["expected_damage"] >= 0.0


def test_state_projection_and_retaliation():
    obs = {
        "select": {
            "type": 0,
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"type": 7, "index": 0},  # Attack
            ],
        },
        "current": {
            "yourIndex": 0,
            "players": [
                {"active": [{"id": 723, "hp": 350, "energies": [3, 3, 3]}], "prize": [1]},
                {"active": [{"id": 721, "hp": 100}], "prize": [1, 2, 3]},
            ],
        },
    }
    state = parse_game_state(obs)
    projected, bonus = project_action(state, 0)
    assert projected.your_prizes == 0  # KO achieved -> 0 prizes remaining!
    assert bonus > 0.0

    retaliation = estimate_opponent_counterattack(projected)
    assert isinstance(retaliation, float)


def test_dynamic_risk_profiles():
    # Test Match Point
    obs_mp = {
        "select": {"type": 0, "option": []},
        "current": {
            "yourIndex": 0,
            "players": [
                {"prize": [1], "deckCount": 30},
                {"prize": [1, 2, 3, 4, 5, 6], "deckCount": 30},
            ],
        },
    }
    s_mp = parse_game_state(obs_mp)
    risk_mp = determine_risk_profile(s_mp)
    assert risk_mp.mode == "MATCH_POINT_RUSH"
    assert risk_mp.aggression_bonus >= 2.0

    # Test Anti-Deckout
    obs_do = {
        "select": {"type": 0, "option": []},
        "current": {
            "yourIndex": 0,
            "players": [
                {"prize": [1, 2, 3], "deckCount": 3},
                {"prize": [1, 2, 3], "deckCount": 30},
            ],
        },
    }
    s_do = parse_game_state(obs_do)
    risk_do = determine_risk_profile(s_do)
    assert risk_do.mode == "ANTI_DECKOUT"


def test_deterministic_fallback():
    # Empty options
    assert deterministic_fallback({}) == []
    assert deterministic_fallback(None) == []

    # Valid options
    sel = {"minCount": 1, "maxCount": 2, "option": [{"type": 1}, {"type": 2}, {"type": 3}]}
    choice = deterministic_fallback(sel)
    assert len(choice) == 2
    assert choice == [0, 1]

    # Distinct choice helper
    res = make_distinct_choice([5, 0, 1], n_opts=3, max_cnt=2)
    assert len(res) == 2
    assert res == [0, 1]


def test_path_resolution_independent_of_cwd(tmp_path):
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        deck = main.load_and_validate_deck()
        assert len(deck) == 60
    finally:
        os.chdir(original_cwd)


def test_full_game_simulation():
    main.reset_diagnostics()
    env = make("cabt", debug=False)
    env.run([main.agent, main.agent])

    assert len(env.steps) > 0
    final_step = env.steps[-1]

    assert final_step[0].status != "INVALID"
    assert final_step[1].status != "INVALID"

    diag = main.get_diagnostics()
    assert diag["decisions"] > 0
    assert diag["exceptions"] == 0
    assert diag["max_decision_time_ms"] < 1000.0
