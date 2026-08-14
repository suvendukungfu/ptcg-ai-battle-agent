import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


class MistakeCategory:
    CRITICAL_MISTAKE = "CRITICAL_MISTAKE"
    MISSED_OPPORTUNITY = "MISSED_OPPORTUNITY"
    RESOURCE_MISTAKE = "RESOURCE_MISTAKE"
    TACTICAL_MISTAKE = "TACTICAL_MISTAKE"
    STRATEGIC_MISTAKE = "STRATEGIC_MISTAKE"


@dataclass
class DetectedMistake:
    game_id: str
    turn: int
    step: int
    category: str
    severity: str  # "HIGH", "MEDIUM", "LOW"
    chosen_action_desc: str
    optimal_action_desc: str
    score_delta: float
    explanation: str


class MistakeMiner:
    """
    Automated Mistake Mining and Counterfactual Analyzer.
    Analyzes game replays and decision logs to identify critical blunders,
    missed lethal opportunities, and sub-optimal resource plays.
    """

    @staticmethod
    def mine_mistakes_from_replay(replay: Dict[str, Any]) -> List[DetectedMistake]:
        mistakes: List[DetectedMistake] = []
        timeline = replay.get("timeline", [])
        decisions = replay.get("decisions", [])
        game_id = replay.get("game_id", "sim_episode")

        for step_idx, item in enumerate(timeline):
            turn = item.get("turn", 1)
            decision = None
            if isinstance(decisions, list):
                if step_idx < len(decisions):
                    decision = decisions[step_idx]
            elif isinstance(decisions, dict):
                decision = decisions.get(str(step_idx)) or decisions.get(step_idx)

            if not decision or not isinstance(decision, dict) or not decision.get("options"):
                continue

            options = decision["options"]
            chosen_opt = next((o for o in options if o.get("is_chosen")), None)
            best_opt = max(options, key=lambda o: o.get("projected_value", -99999.0))

            if not chosen_opt or chosen_opt == best_opt:
                continue

            score_diff = best_opt.get("projected_value", 0.0) - chosen_opt.get("projected_value", 0.0)

            # 1. Missed Opportunity: Winning KO was skipped
            if best_opt.get("action_bonus", 0.0) >= 3000.0 and score_diff > 2500.0:
                mistakes.append(DetectedMistake(
                    game_id=game_id,
                    turn=turn,
                    step=step_idx,
                    category=MistakeCategory.MISSED_OPPORTUNITY,
                    severity="HIGH",
                    chosen_action_desc=f"Option {chosen_opt.get('index')}: {chosen_opt.get('name')}",
                    optimal_action_desc=f"Option {best_opt.get('index')}: {best_opt.get('name')}",
                    score_delta=round(score_diff, 1),
                    explanation=f"Turn {turn}: Skipped lethal Knockout line yielding immediate prize advantage."
                ))

            # 2. Critical Mistake: Severe evaluation loss
            elif score_diff > 3500.0:
                mistakes.append(DetectedMistake(
                    game_id=game_id,
                    turn=turn,
                    step=step_idx,
                    category=MistakeCategory.CRITICAL_MISTAKE,
                    severity="HIGH",
                    chosen_action_desc=f"Option {chosen_opt.get('index')}: {chosen_opt.get('name')}",
                    optimal_action_desc=f"Option {best_opt.get('index')}: {best_opt.get('name')}",
                    score_delta=round(score_diff, 1),
                    explanation=f"Turn {turn}: Severe positional error resulting in massive board score degradation."
                ))

            # 3. Tactical Mistake: Retaliation risk neglected
            elif score_diff > 1500.0 and chosen_opt.get("type") in (0, 7):
                mistakes.append(DetectedMistake(
                    game_id=game_id,
                    turn=turn,
                    step=step_idx,
                    category=MistakeCategory.TACTICAL_MISTAKE,
                    severity="MEDIUM",
                    chosen_action_desc=f"Option {chosen_opt.get('index')}: {chosen_opt.get('name')}",
                    optimal_action_desc=f"Option {best_opt.get('index')}: {best_opt.get('name')}",
                    score_delta=round(score_diff, 1),
                    explanation=f"Turn {turn}: Tactical line committed to vulnerable spot without mitigating retaliation threat."
                ))

            # 4. Resource / Strategic Mistake
            elif score_diff > 800.0:
                mistakes.append(DetectedMistake(
                    game_id=game_id,
                    turn=turn,
                    step=step_idx,
                    category=MistakeCategory.RESOURCE_MISTAKE,
                    severity="LOW",
                    chosen_action_desc=f"Option {chosen_opt.get('index')}: {chosen_opt.get('name')}",
                    optimal_action_desc=f"Option {best_opt.get('index')}: {best_opt.get('name')}",
                    score_delta=round(score_diff, 1),
                    explanation=f"Turn {turn}: Sub-optimal resource expenditure or energy attachment target."
                ))

        return mistakes


class MistakeDatabase:
    """Database managing aggregated mistake logs across tournament runs."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "reports", "mistake_database.json")
        self.db_path = db_path
        self.records: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
            except Exception:
                self.records = []

    def record_mistakes(self, mistakes: List[DetectedMistake]):
        for m in mistakes:
            self.records.append(asdict(m))
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        counts = {
            MistakeCategory.CRITICAL_MISTAKE: 0,
            MistakeCategory.MISSED_OPPORTUNITY: 0,
            MistakeCategory.TACTICAL_MISTAKE: 0,
            MistakeCategory.RESOURCE_MISTAKE: 0,
            MistakeCategory.STRATEGIC_MISTAKE: 0,
        }
        for rec in self.records:
            cat = rec.get("category")
            if cat in counts:
                counts[cat] += 1

        return {
            "total_mistakes_mined": len(self.records),
            "breakdown": counts,
            "recent_mistakes": self.records[-10:] if self.records else []
        }
