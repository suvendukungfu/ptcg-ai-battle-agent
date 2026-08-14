import pytest
import os
import math
from agent.state import GameState
from agent.belief_state import BeliefStateTracker, BeliefDistribution
from agent.goals import GoalPlanner, StrategicGoal, GoalState
from agent.decomposition import ScoreDecomposer, ValueDecomposition
from analytics.mistake_miner import MistakeMiner, MistakeDatabase, MistakeCategory, DetectedMistake
from analytics.meta_predictor import MetaPredictor, DeckEvaluation
from research.experience_memory import ExperienceMemory, ExperienceStep


def test_belief_state_tracker_probabilities():
    tracker = BeliefStateTracker()
    state = GameState(
        turn=4,
        your_active={"id": 723, "hp": 350, "maxHp": 350, "energies": [3, 3]},
        opp_active={"id": 721, "hp": 150, "maxHp": 150, "energies": [3]},
        opp_hand_count=5,
        opp_deck_count=35,
        opp_discard=[{"id": 3}, {"id": 3}, {"id": 1092}]
    )

    beliefs = tracker.update_beliefs(state)
    assert isinstance(beliefs, BeliefDistribution)
    assert 0.0 <= beliefs.p_boss_gust <= 1.0
    assert 0.0 <= beliefs.p_energy <= 1.0
    assert 0.0 <= beliefs.p_switch <= 1.0
    assert 0.0 <= beliefs.p_evolution <= 1.0
    assert beliefs.hand_size == 5
    assert beliefs.total_unseen_cards == 40


def test_goal_planner_transitions():
    # 1. Match point goal test
    match_point_state = GameState(
        your_prizes=1,
        opp_prizes=4,
        your_active={"id": 723, "hp": 350, "maxHp": 350, "energies": [3, 3]},
        your_bench=[{"id": 721, "hp": 150, "maxHp": 150, "energies": [3]}, {"id": 722, "hp": 180, "maxHp": 180, "energies": []}]
    )
    goal = GoalPlanner.identify_goal(match_point_state)
    assert goal.primary_goal == StrategicGoal.GOAL_WIN_NOW
    assert goal.attack_priority_bonus >= 3000.0

    # 2. Anti-deckout goal test
    deckout_state = GameState(
        turn=10,
        your_deck_count=3,
        your_prizes=3,
        opp_prizes=3,
    )
    goal = GoalPlanner.identify_goal(deckout_state)
    assert goal.primary_goal == StrategicGoal.GOAL_ANTI_DECKOUT

    # 3. Crustle Safeguard counterplay test
    crustle_state = GameState(
        opp_active={"id": 558, "hp": 120, "maxHp": 120},  # Crustle
        your_prizes=4,
        opp_prizes=4,
        your_bench=[{"id": 721, "hp": 150, "maxHp": 150, "energies": [3]}, {"id": 722, "hp": 180, "maxHp": 180, "energies": []}]
    )
    goal = GoalPlanner.identify_goal(crustle_state)
    assert goal.primary_goal == StrategicGoal.GOAL_COUNTER_CRUSTLE


def test_score_decomposition():
    decomp = ScoreDecomposer.decompose_action_value(
        base_value=2500.0,
        action_type=0,  # Attack
        is_knockout=True,
        your_prizes=2,
        opp_prizes=4,
        retaliation_threat=0.2,
        energy_count=2,
        goal_bonus=500.0
    )

    assert isinstance(decomp, ValueDecomposition)
    assert decomp.threat_reduction_component == 3500.0
    assert decomp.win_probability_component == 4000.0
    assert decomp.prize_advantage_component == 2400.0
    assert decomp.retaliation_risk_penalty > 0.0
    assert decomp.total_score > 0.0
    assert "Knockout" in decomp.rationale


def test_mistake_miner():
    mock_replay = {
        "game_id": "test_game_1",
        "timeline": [
            {"turn": 1, "your_prizes": 6, "opp_prizes": 6},
            {"turn": 2, "your_prizes": 4, "opp_prizes": 6},
        ],
        "decisions": {
            0: {
                "options": [
                    {"index": 0, "name": "Pass", "projected_value": -500.0, "is_chosen": True, "action_bonus": 0.0, "type": 14},
                    {"index": 1, "name": "Electro Bullet (Lethal KO)", "projected_value": 4500.0, "is_chosen": False, "action_bonus": 3500.0, "type": 0}
                ]
            }
        }
    }

    mistakes = MistakeMiner.mine_mistakes_from_replay(mock_replay)
    assert len(mistakes) == 1
    m = mistakes[0]
    assert m.category == MistakeCategory.MISSED_OPPORTUNITY
    assert m.score_delta == 5000.0
    assert m.severity == "HIGH"


def test_meta_predictor():
    rankings = MetaPredictor.get_all_deck_rankings()
    assert len(rankings) >= 4
    top_deck = rankings[0]
    assert isinstance(top_deck, DeckEvaluation)
    assert top_deck.expected_win_rate >= 50.0
    assert top_deck.robustness_score > 0.0
    assert len(top_deck.confidence_interval_95) == 2
    assert top_deck.confidence_interval_95[0] <= top_deck.confidence_interval_95[1]


def test_experience_memory(tmp_path):
    mem = ExperienceMemory(storage_dir=str(tmp_path))
    step = ExperienceStep(
        game_id="g_100",
        step_index=0,
        turn=1,
        player_seat=0,
        state_summary={"prizes": 6},
        legal_options=[0, 1],
        selected_action=[1],
        alternative_scores=[{"opt": 0, "val": 100.0}],
        opponent_belief={"p_gust": 0.2},
        reward=1.0,
        is_terminal=True,
        outcome="WIN"
    )

    mem.store_episode("g_100", [step])
    stats = mem.get_dataset_statistics()
    assert stats["total_steps"] == 1
    assert stats["total_games"] == 1
    assert stats["wins"] == 1
    assert stats["win_rate_pct"] == 100.0
