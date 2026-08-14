from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ValueDecomposition:
    """
    Structured breakdown of action evaluation score V(a) for explainable AI.
    Decomposes total valuation into explicit additive components.
    """
    win_probability_component: float = 0.0
    prize_advantage_component: float = 0.0
    board_advantage_component: float = 0.0
    energy_tempo_component: float = 0.0
    threat_reduction_component: float = 0.0
    retaliation_risk_penalty: float = 0.0
    resource_cost_penalty: float = 0.0
    total_score: float = 0.0
    rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ScoreDecomposer:
    """
    Decomposes aggregate search and heuristic evaluations into explainable factors.
    """

    @staticmethod
    def decompose_action_value(
        base_value: float,
        action_type: int,
        is_knockout: bool,
        your_prizes: int,
        opp_prizes: int,
        retaliation_threat: float,
        energy_count: int,
        goal_bonus: float = 0.0
    ) -> ValueDecomposition:
        win_comp = 0.0
        prize_comp = 0.0
        board_comp = 0.0
        energy_comp = 0.0
        threat_comp = 0.0
        retaliation_penalty = 0.0
        resource_cost = 0.0

        # Prize Advantage Component
        prize_diff = opp_prizes - your_prizes
        prize_comp = prize_diff * 1200.0

        # Knockout & Threat Reduction Component
        if is_knockout:
            threat_comp = 3500.0
            if your_prizes <= 2:
                win_comp = 4000.0

        # Energy Tempo Component
        if action_type == 8:  # Energy attach
            energy_comp = 800.0 + (energy_count * 200.0)
        elif action_type == 2:  # Trainer item
            energy_comp = 1500.0

        # Board Advantage & Goal Bonus
        board_comp = 500.0 + goal_bonus

        # Retaliation Risk Penalty
        retaliation_penalty = retaliation_threat * 1800.0

        total = (
            win_comp
            + prize_comp
            + board_comp
            + energy_comp
            + threat_comp
            - retaliation_penalty
            - resource_cost
        )

        rationale_parts = []
        if is_knockout:
            rationale_parts.append("Secures decisive Knockout")
        if retaliation_threat < 0.3:
            rationale_parts.append("Low counterplay retaliation risk")
        if action_type == 8:
            rationale_parts.append("Accelerates energy tempo")
        if prize_diff > 0:
            rationale_parts.append(f"Maintains +{prize_diff} prize lead")

        rationale = " | ".join(rationale_parts) if rationale_parts else "Standard tactical line execution"

        return ValueDecomposition(
            win_probability_component=round(win_comp, 1),
            prize_advantage_component=round(prize_comp, 1),
            board_advantage_component=round(board_comp, 1),
            energy_tempo_component=round(energy_comp, 1),
            threat_reduction_component=round(threat_comp, 1),
            retaliation_risk_penalty=round(retaliation_penalty, 1),
            resource_cost_penalty=round(resource_cost, 1),
            total_score=round(total, 1),
            rationale=rationale,
        )
