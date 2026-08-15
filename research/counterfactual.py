import os
import sys
import copy
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.state import GameState, parse_game_state
from agent.evaluator import (
    evaluate_board_value,
    estimate_raw_damage,
    get_target_hp,
    get_target_prize_value,
    calculate_immunity_multiplier,
)
from agent.opponent_model import (
    estimate_next_attack_probability,
    estimate_gust_probability,
    estimate_opponent_threat,
)
from agent.risk_model import determine_risk_profile
from agent.decomposition import ScoreDecomposer, ValueDecomposition
from agent.search import project_action, estimate_opponent_counterattack


@dataclass
class ActionEvaluation:
    option_index: int
    option_desc: str
    option_type: int
    raw_action_bonus: float
    projected_board_value: float
    retaliation_risk: float
    net_score: float
    value_decomposition: Dict[str, float]
    is_chosen: bool = False
    is_counterfactual_best: bool = False
    score_delta_to_best: float = 0.0


class CounterfactualEngine:
    """
    Offline Research Engine: Evaluates chosen decisions against all candidate legal alternatives.
    Calculates exact score decompositions and identifies alternative optimal lines.
    """

    @staticmethod
    def evaluate_decision_point(
        state: GameState,
        chosen_action: List[int],
    ) -> Dict[str, Any]:
        """
        Perform exhaustive offline valuation of all legal options at a decision point.
        """
        options = state.options
        n_opts = len(options)
        if n_opts == 0:
            return {"options": [], "best_index": None, "chosen_index": None, "blunder": False}

        risk_profile = determine_risk_profile(state)
        evaluations: List[ActionEvaluation] = []

        chosen_idx = chosen_action[0] if chosen_action and 0 <= chosen_action[0] < n_opts else -1

        for idx, opt in enumerate(options):
            opt_type = opt.get("type", -1) if isinstance(opt, dict) else -1
            opt_name = opt.get("name") or opt.get("cardName") or f"Option_{idx}_type_{opt_type}"

            # 1. Project action state transition
            proj_state, action_bonus = project_action(state, idx)

            # 2. Evaluate projected board state
            board_val = evaluate_board_value(proj_state)

            # 3. Estimate opponent counter-attack retaliation
            retaliation = estimate_opponent_counterattack(proj_state)

            # 4. Decompose score
            decomp: ValueDecomposition = ScoreDecomposer.decompose_state(
                proj_state,
                action_bonus=action_bonus,
                retaliation_risk=retaliation,
            )

            # 5. Calculate net score with dynamic risk modulation
            net_score = (
                board_val
                + (action_bonus * risk_profile.aggression_bonus)
                - (retaliation * risk_profile.retaliation_weight)
            )

            is_chosen = (idx == chosen_idx)

            evaluations.append(
                ActionEvaluation(
                    option_index=idx,
                    option_desc=str(opt_name),
                    option_type=opt_type,
                    raw_action_bonus=action_bonus,
                    projected_board_value=board_val,
                    retaliation_risk=retaliation,
                    net_score=net_score,
                    value_decomposition=decomp.to_dict(),
                    is_chosen=is_chosen,
                )
            )

        # Sort to find counterfactual best
        evaluations.sort(key=lambda x: x.net_score, reverse=True)
        best_eval = evaluations[0]
        best_eval.is_counterfactual_best = True

        for ev in evaluations:
            ev.score_delta_to_best = best_eval.net_score - ev.net_score

        chosen_eval = next((e for e in evaluations if e.is_chosen), None)
        blunder = False
        mistake_severity = "NONE"
        score_gap = 0.0

        if chosen_eval and chosen_eval.option_index != best_eval.option_index:
            score_gap = best_eval.net_score - chosen_eval.net_score
            if score_gap >= 150.0:
                blunder = True
                mistake_severity = "CRITICAL"
            elif score_gap >= 50.0:
                blunder = True
                mistake_severity = "MODERATE"
            elif score_gap >= 15.0:
                mistake_severity = "MINOR"

        return {
            "turn": state.turn,
            "select_type": state.select_type,
            "chosen_index": chosen_idx,
            "best_index": best_eval.option_index,
            "chosen_desc": chosen_eval.option_desc if chosen_eval else "None",
            "best_desc": best_eval.option_desc,
            "score_gap": score_gap,
            "blunder": blunder,
            "severity": mistake_severity,
            "evaluations": [asdict(e) for e in evaluations],
        }
