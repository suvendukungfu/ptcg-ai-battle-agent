import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.state import GameState, parse_game_state
from agent.policy import rank_card_play_options, rank_discard_options, rank_target_options
from agent.action_selector import select_heuristic_action, select_action
from agent.evaluator import evaluate_board_value


def test_rule_1_bench_first_priority():
    """
    Test Rule 1: When Bench is empty and a legal Basic-to-Bench option exists,
    the agent must prioritize benching the Basic before playing discretionary Ultra Ball.
    """
    # Active Dwebble (60 HP), 0 Benched Pokemon
    # Hand has Dwebble, Ultra Ball, Nest Ball, Energy
    obs = {
        "select": {
            "type": 0,  # Main phase
            "minCount": 1,
            "maxCount": 1,
            "option": [
                {"type": 1, "id": 344, "text": "Play Dwebble to Bench"},  # Index 0: Bench Dwebble
                {"type": 0, "id": 1121, "text": "Play Ultra Ball"},       # Index 1: Ultra Ball
                {"type": 0, "id": 1145, "text": "Play Nest Ball"},        # Index 2: Nest Ball
                {"type": 14, "text": "Pass Turn"},                        # Index 3: Pass
            ]
        },
        "current": {
            "yourIndex": 0,
            "turn": 1,
            "players": [
                {
                    "active": [{"id": 344, "hp": 60, "energies": []}],
                    "bench": [],  # ZERO BENCH
                    "hand": [{"id": 344}, {"id": 1121}, {"id": 1145}, {"id": 1}],
                    "prize": [1, 2, 3, 4, 5, 6],
                    "discard": []
                },
                {
                    "active": [{"id": 666, "hp": 120, "energies": []}],
                    "bench": [{"id": 1030, "hp": 60, "energies": []}],
                    "hand": 5,
                    "prize": [1, 2, 3, 4, 5, 6],
                    "discard": []
                }
            ]
        }
    }
    
    state = parse_game_state(obs)
    ranks = rank_card_play_options(state)
    assert len(ranks) > 0
    # The top ranked option must be Index 0 (Play Dwebble to Bench)
    top_choice_idx = ranks[0][0]
    assert top_choice_idx == 0, f"Expected Option 0 (Play Dwebble to Bench), got Option {top_choice_idx}"
    
    # Action selector should also choose Option 0
    chosen = select_heuristic_action(state)
    assert chosen == [0], f"Action selector chose {chosen} instead of [0]"


def test_rule_2_protect_basic_discard_when_bench_empty():
    """
    Test Rule 2: When paying Ultra Ball discard cost with 0 Bench,
    the agent must NEVER select the Basic Pokemon if surplus Energy / Trainer options exist.
    """
    # Discard selection dialog: pick 2 cards from hand (Dwebble, Energy 1, Energy 2, Lillie)
    options = [
        {"id": 344, "text": "Dwebble (Basic)"},           # Index 0
        {"id": 1, "text": "Basic Grass Energy"},           # Index 1
        {"id": 1, "text": "Basic Grass Energy"},           # Index 2
        {"id": 1227, "text": "Lillie's Determination"},    # Index 3
    ]
    
    obs = {
        "select": {
            "type": 1,
            "context": "Discard",
            "minCount": 2,
            "maxCount": 2,
            "option": options
        },
        "current": {
            "yourIndex": 0,
            "turn": 1,
            "players": [
                {
                    "active": [{"id": 344, "hp": 60, "energies": []}],
                    "bench": [],  # ZERO BENCH
                    "hand": options,
                    "prize": [1, 2, 3, 4, 5, 6],
                    "discard": []
                },
                {
                    "active": [{"id": 666, "hp": 120, "energies": []}],
                    "bench": [],
                    "hand": 5,
                    "prize": [1, 2, 3, 4, 5, 6],
                    "discard": []
                }
            ]
        }
    }
    
    state = parse_game_state(obs)
    discard_ranks = rank_discard_options(options, state)
    
    # Check that Dwebble (Index 0) has a heavy negative score
    dwebble_score = next(score for idx, score in discard_ranks if idx == 0)
    assert dwebble_score <= -1000.0, f"Dwebble discard score should be heavily penalized, got {dwebble_score}"
    
    # Action selector should choose the 2 energies (Index 1 and Index 2)
    chosen = select_heuristic_action(state)
    assert 0 not in chosen, f"Dwebble (Index 0) was erroneously chosen for discard: {chosen}"
    assert set(chosen) == {1, 2} or set(chosen) == {1, 3} or set(chosen) == {2, 3}


def test_basic_discard_allowed_when_bench_security_established():
    """
    Test Rule 2 Exception: When Bench security is safely established (e.g. 2 Dwebbles on Bench),
    discarding a surplus Basic Pokemon is not globally prohibited.
    """
    options = [
        {"id": 344, "text": "Dwebble (Surplus Basic)"},    # Index 0
        {"id": 345, "text": "Crustle"},                   # Index 1
        {"id": 1227, "text": "Lillie"},                    # Index 2
    ]
    
    obs = {
        "select": {
            "type": 1,
            "context": "Discard",
            "minCount": 1,
            "maxCount": 1,
            "option": options
        },
        "current": {
            "yourIndex": 0,
            "turn": 3,
            "players": [
                {
                    "active": [{"id": 345, "hp": 130, "energies": [1, 1]}],
                    "bench": [
                        {"id": 344, "hp": 60, "energies": []},
                        {"id": 344, "hp": 60, "energies": []}
                    ],  # 2 BENCHED DWEBBLES ALREADY ESTABLISHED
                    "hand": options,
                    "prize": [1, 2, 3, 4, 5, 6],
                    "discard": []
                },
                {
                    "active": [{"id": 756, "hp": 300, "energies": [1, 1]}],
                    "bench": [],
                    "hand": 4,
                    "prize": [1, 2, 3, 4, 5, 6],
                    "discard": []
                }
            ]
        }
    }
    
    state = parse_game_state(obs)
    discard_ranks = rank_discard_options(options, state)
    
    dwebble_score = next(score for idx, score in discard_ranks if idx == 0)
    # Score should not be penalized to -5000.0 since bench is safe
    assert dwebble_score >= 0.0, f"Dwebble score should be non-negative when bench is safe, got {dwebble_score}"


def test_evaluator_zero_bench_fragility_penalty():
    """
    Test Evaluator: A fragile 60 HP Active with 0 Bench receives a vulnerability penalty.
    """
    state_no_bench = GameState(
        your_prizes=6,
        opp_prizes=6,
        your_active={"id": 344, "hp": 60, "maxHp": 60, "energies": []},
        your_bench=[],  # 0 bench
        opp_active={"id": 666, "hp": 120, "maxHp": 120, "energies": [1]}
    )
    
    state_with_bench = GameState(
        your_prizes=6,
        opp_prizes=6,
        your_active={"id": 344, "hp": 60, "maxHp": 60, "energies": []},
        your_bench=[{"id": 344, "hp": 60, "maxHp": 60, "energies": []}],  # 1 bench
        opp_active={"id": 666, "hp": 120, "maxHp": 120, "energies": [1]}
    )
    
    val_no_bench = evaluate_board_value(state_no_bench)
    val_with_bench = evaluate_board_value(state_with_bench)
    
    # Board with bench must be substantially higher due to security + presence
    diff = val_with_bench - val_no_bench
    assert diff >= 150.0, f"Expected bench security advantage >= 150.0, got {diff}"
