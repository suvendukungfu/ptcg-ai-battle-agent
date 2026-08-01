from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from agent.state import GameState


class StrategicGoal(str, Enum):
    GOAL_WIN_NOW = "GOAL_WIN_NOW"
    GOAL_PREPARE_ATTACKER = "GOAL_PREPARE_ATTACKER"
    GOAL_TAKE_TWO_PRIZE_KO = "GOAL_TAKE_TWO_PRIZE_KO"
    GOAL_COUNTER_CRUSTLE = "GOAL_COUNTER_CRUSTLE"
    GOAL_ELIMINATE_BREAKER = "GOAL_ELIMINATE_BREAKER"
    GOAL_PROTECT_ACTIVE = "GOAL_PROTECT_ACTIVE"
    GOAL_BUILD_BENCH = "GOAL_BUILD_BENCH"
    GOAL_ANTI_DECKOUT = "GOAL_ANTI_DECKOUT"
    GOAL_TEMPO_DEVELOPMENT = "GOAL_TEMPO_DEVELOPMENT"


@dataclass
class GoalState:
    primary_goal: StrategicGoal
    secondary_goal: StrategicGoal
    goal_rationale: str
    attack_priority_bonus: float = 0.0
    energy_priority_bonus: float = 0.0
    evolution_priority_bonus: float = 0.0
    gust_priority_bonus: float = 0.0


class GoalPlanner:
    """
    Goal-Based Strategic Planner.
    Identifies macro objectives based on prize counts, board state,
    opponent threats, and deck exhaustion, providing structured goal modifiers to action selection.
    """

    @staticmethod
    def identify_goal(state: GameState) -> GoalState:
        turn = getattr(state, "turn", 1)
        deck = getattr(state, "deck", []) or getattr(state, "your_hand", [])
        deck_count = getattr(state, "your_deck_count", len(deck))
        your_prizes = getattr(state, "your_prizes", 6)
        your_active = getattr(state, "your_active", None)
        your_bench = getattr(state, "your_bench", [])
        opp_active = getattr(state, "opp_active", None) or getattr(state, "opponent_active", None)

        # 1. Anti-Deckout Goal (P0 Safety)
        if deck_count <= 5 and turn >= 8:
            return GoalState(
                primary_goal=StrategicGoal.GOAL_ANTI_DECKOUT,
                secondary_goal=StrategicGoal.GOAL_WIN_NOW,
                goal_rationale="Deck count is <= 5 cards. Prioritizing immediate victory lines and prohibiting draw supporters.",
                attack_priority_bonus=3000.0,
                energy_priority_bonus=0.0,
                evolution_priority_bonus=0.0,
                gust_priority_bonus=2000.0,
            )

        # 2. Match-Point Win-Now Goal (P0 Offense)
        if your_prizes <= 2:
            return GoalState(
                primary_goal=StrategicGoal.GOAL_WIN_NOW,
                secondary_goal=StrategicGoal.GOAL_TAKE_TWO_PRIZE_KO,
                goal_rationale="Match-point threshold reached (<= 2 prizes). Prioritizing lethal knockout actions and decisive gust plays.",
                attack_priority_bonus=4000.0,
                energy_priority_bonus=1000.0,
                evolution_priority_bonus=500.0,
                gust_priority_bonus=3500.0,
            )

        # 3. Non-EX Breaker Elimination Goal
        from agent.evaluator import is_target_immune_to_ex, is_ex_attacker
        if is_target_immune_to_ex(your_active):
            all_opp = ([opp_active] if opp_active else []) + [b for b in getattr(state, "opp_bench", []) if b]
            has_powered_nonex = any(not is_ex_attacker(o) and len(o.get("energies", [])) >= 2 for o in all_opp if isinstance(o, dict))
            if has_powered_nonex:
                return GoalState(
                    primary_goal=StrategicGoal.GOAL_ELIMINATE_BREAKER,
                    secondary_goal=StrategicGoal.GOAL_PREPARE_ATTACKER,
                    goal_rationale="Opponent has a powered non-ex breaker capable of damaging our Safeguard wall. Prioritizing breaker elimination and backup bench ramp.",
                    attack_priority_bonus=2000.0,
                    energy_priority_bonus=1800.0,
                    evolution_priority_bonus=1500.0,
                    gust_priority_bonus=3000.0,
                )

        # 4. Crustle Safeguard Counterplay Goal (When facing opponent Safeguard)
        if is_target_immune_to_ex(opp_active):
            return GoalState(
                primary_goal=StrategicGoal.GOAL_COUNTER_CRUSTLE,
                secondary_goal=StrategicGoal.GOAL_PREPARE_ATTACKER,
                goal_rationale="Opponent Active is immune to ex attacks (Safeguard). Prioritizing non-ex single prize attacker or gusting bench.",
                attack_priority_bonus=1500.0,
                energy_priority_bonus=2000.0,
                evolution_priority_bonus=2500.0,
                gust_priority_bonus=3500.0,
            )

        # 5. Active Preservation Goal
        active_hp = your_active.get("hp", 150) if isinstance(your_active, dict) else getattr(your_active, "hp", 150) if your_active else 150
        if your_active and active_hp <= 60 and len(your_bench) > 0:
            return GoalState(
                primary_goal=StrategicGoal.GOAL_PROTECT_ACTIVE,
                secondary_goal=StrategicGoal.GOAL_PREPARE_ATTACKER,
                goal_rationale="Active tank is heavily damaged. Prioritizing switch preservation or energy recovery tool.",
                attack_priority_bonus=1000.0,
                energy_priority_bonus=1500.0,
                evolution_priority_bonus=1000.0,
                gust_priority_bonus=500.0,
            )

        # 6. Build Bench & Prepare Attacker (Early Game Setup)
        active_energies = your_active.get("energies", []) if isinstance(your_active, dict) else getattr(your_active, "energies", []) if your_active else []
        if len(your_bench) < 2 or (your_active and len(active_energies) < 2):
            return GoalState(
                primary_goal=StrategicGoal.GOAL_BUILD_BENCH,
                secondary_goal=StrategicGoal.GOAL_PREPARE_ATTACKER,
                goal_rationale="Board setup incomplete. Prioritizing bench establishment and initial energy acceleration.",
                attack_priority_bonus=500.0,
                energy_priority_bonus=2500.0,
                evolution_priority_bonus=2000.0,
                gust_priority_bonus=800.0,
            )

        # 7. Default General Tempo
        return GoalState(
            primary_goal=StrategicGoal.GOAL_TEMPO_DEVELOPMENT,
            secondary_goal=StrategicGoal.GOAL_PREPARE_ATTACKER,
            goal_rationale="Standard game state. Maintaining steady prize progression and board tempo.",
            attack_priority_bonus=1500.0,
            energy_priority_bonus=1000.0,
            evolution_priority_bonus=800.0,
            gust_priority_bonus=1200.0,
        )
