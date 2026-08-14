import os
import sys
import json
from typing import Dict, Any, List, Optional
from kaggle_environments import make
from agent.state import parse_game_state, GameState
from agent.card_database import get_card_name, get_card
from agent.search import project_action
from agent.evaluator import evaluate_board_value, is_target_immune_to_ex, is_ex_attacker
from agent.opponent_model import estimate_opponent_threat, classify_opponent_archetype


class ReplayParser:
    """Extracts rich analytics, timeline progressions, and decision explainability from episode steps."""

    @staticmethod
    def parse_episode_steps(steps: List[List[Dict[str, Any]]], agent_seat: int = 0) -> Dict[str, Any]:
        """
        Parse raw environment step logs into comprehensive replay timeline and metrics.
        """
        timeline: List[Dict[str, Any]] = []
        prize_trajectory: List[Dict[str, Any]] = []
        hp_trajectory: List[Dict[str, Any]] = []
        energy_trajectory: List[Dict[str, Any]] = []
        decisions: List[Dict[str, Any]] = []
        attacks_log: List[Dict[str, Any]] = []
        kos_log: List[Dict[str, Any]] = []

        seen_opp_cards: set = set()
        prev_opp_prizes = 6
        prev_your_prizes = 6

        for step_idx, step_data in enumerate(steps):
            if len(step_data) <= agent_seat:
                continue

            agent_step = step_data[agent_seat]
            obs = agent_step.get("observation", {})
            action = agent_step.get("action")

            if not isinstance(obs, dict) or not obs.get("current"):
                continue

            state = parse_game_state(obs)
            curr = obs.get("current", {})

            # Track revealed opponent cards
            if state.opp_active:
                seen_opp_cards.add(state.opp_active.get("id", 0))
            for b in state.opp_bench:
                seen_opp_cards.add(b.get("id", 0))
            for d in state.opp_discard:
                seen_opp_cards.add(d.get("id", 0) if isinstance(d, dict) else d)

            # Check KOs
            if state.opp_prizes < prev_opp_prizes:
                kos_log.append({
                    "turn": state.turn,
                    "step": step_idx,
                    "taker": "OPPONENT",
                    "prizes_taken": prev_opp_prizes - state.opp_prizes,
                })
                prev_opp_prizes = state.opp_prizes

            if state.your_prizes < prev_your_prizes:
                kos_log.append({
                    "turn": state.turn,
                    "step": step_idx,
                    "taker": "YOU",
                    "prizes_taken": prev_your_prizes - state.your_prizes,
                })
                prev_your_prizes = state.your_prizes

            # Trajectory curves
            your_active_hp = state.your_active.get("hp", 0) if state.your_active else 0
            opp_active_hp = state.opp_active.get("hp", 0) if state.opp_active else 0

            prize_trajectory.append({
                "step": step_idx,
                "turn": state.turn,
                "your_prizes": state.your_prizes,
                "opp_prizes": state.opp_prizes,
                "prize_diff": state.opp_prizes - state.your_prizes,
            })

            hp_trajectory.append({
                "step": step_idx,
                "turn": state.turn,
                "your_active_hp": your_active_hp,
                "opp_active_hp": opp_active_hp,
            })

            energy_trajectory.append({
                "step": step_idx,
                "turn": state.turn,
                "your_energies": state.total_your_energies,
                "opp_energies": state.total_opp_energies,
            })

            # Decision Point Explainability
            if state.options and action is not None:
                explanation = ReplayParser._generate_decision_explanation(state, action)
                decisions.append(explanation)

            timeline_step = {
                "step": step_idx,
                "turn": state.turn,
                "select_type": state.select_type,
                "your_active": state.your_active,
                "opp_active": state.opp_active,
                "your_bench_count": len(state.your_bench),
                "opp_bench_count": len(state.opp_bench),
                "your_hand_count": len(state.your_hand),
                "opp_hand_count": state.opp_hand_count,
                "your_prizes": state.your_prizes,
                "opp_prizes": state.opp_prizes,
                "action": action,
            }
            timeline.append(timeline_step)

        archetype = classify_opponent_archetype(seen_opp_cards)

        final_step = steps[-1]
        reward = final_step[agent_seat].reward
        winner = "YOU" if reward == 1 else ("OPPONENT" if reward == -1 else "DRAW")

        return {
            "winner": winner,
            "reward": reward,
            "total_steps": len(steps),
            "total_turns": max([t["turn"] for t in timeline], default=1),
            "opponent_archetype": archetype,
            "prize_trajectory": prize_trajectory,
            "hp_trajectory": hp_trajectory,
            "energy_trajectory": energy_trajectory,
            "decisions": decisions,
            "kos_log": kos_log,
            "timeline": timeline,
        }

    @staticmethod
    def _generate_decision_explanation(state: GameState, chosen_indices: List[int]) -> Dict[str, Any]:
        """Generate structured contrastive decision explanation."""
        options_detail: List[Dict[str, Any]] = []

        chosen_idx = chosen_indices[0] if chosen_indices else -1
        chosen_opt = state.options[chosen_idx] if (0 <= chosen_idx < len(state.options)) else None

        for idx, opt in enumerate(state.options):
            if not isinstance(opt, dict):
                continue
            opt_type = opt.get("type", -1)
            cid = opt.get("id", 0)
            cname = get_card_name(cid) if cid else f"Action #{opt_type}"

            proj, bonus = project_action(state, idx)
            val = evaluate_board_value(proj) + bonus
            is_chosen = (idx in chosen_indices)

            options_detail.append({
                "index": idx,
                "type": opt_type,
                "name": cname,
                "card_id": cid,
                "projected_value": round(val, 1),
                "action_bonus": round(bonus, 1),
                "is_chosen": is_chosen,
            })

        # Sort options by projected value
        options_detail.sort(key=lambda x: x["projected_value"], reverse=True)

        chosen_rationale: List[str] = []
        if chosen_opt:
            c_type = chosen_opt.get("type", -1)
            if c_type == 7:  # Attack
                if state.opp_active and state.opp_active.get("hp", 0) <= 160:
                    chosen_rationale.append("Secured Immediate Knockout & Prize advantage")
                else:
                    chosen_rationale.append("Applied high offensive pressure to opponent active")
            elif c_type == 8:
                chosen_rationale.append("Accelerated energy setup for primary attacker")
            elif c_type in (3, 4):
                chosen_rationale.append("Evolved Pokemon into Stage 1 / ex heavy attacker")
            elif chosen_opt.get("id") == 1219:
                chosen_rationale.append("Electric Generator energy acceleration")
            elif chosen_opt.get("id") == 1262:
                chosen_rationale.append("Gust effect (Boss's Orders) targeting vulnerable bench Pokemon")
            else:
                chosen_rationale.append("Maximized board value and resource efficiency")

        return {
            "turn": state.turn,
            "select_type": state.select_type,
            "chosen_indices": chosen_indices,
            "chosen_rationale": chosen_rationale,
            "options": options_detail,
        }
