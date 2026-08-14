import os
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ExperienceStep:
    game_id: str
    step_index: int
    turn: int
    player_seat: int
    state_summary: Dict[str, Any]
    legal_options: List[Any]
    selected_action: List[int]
    alternative_scores: List[Dict[str, Any]]
    opponent_belief: Dict[str, float]
    reward: float
    is_terminal: bool
    outcome: Optional[str] = None  # "WIN", "LOSS", "DRAW"


class ExperienceMemory:
    """
    Offline Replay Experience Database.
    Persists structured state-action-reward-outcome trajectories for policy improvement,
    mistake mining, behavior analysis, and counterfactual evaluation.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            storage_dir = os.path.join(base_dir, "research", "experiments", "memory")
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.memory_file = os.path.join(self.storage_dir, "experience_dataset.jsonl")

    def store_episode(self, game_id: str, steps: List[ExperienceStep]):
        """Append full game trajectory to experience memory."""
        with open(self.memory_file, "a", encoding="utf-8") as f:
            for step in steps:
                f.write(json.dumps(asdict(step)) + "\n")

    def query_experiences(
        self,
        outcome_filter: Optional[str] = None,
        min_turn: int = 1,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Query experiences filtered by outcome or game phase."""
        if not os.path.exists(self.memory_file):
            return []

        results = []
        with open(self.memory_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                exp = json.loads(line.strip())
                if outcome_filter and exp.get("outcome") != outcome_filter:
                    continue
                if exp.get("turn", 1) < min_turn:
                    continue
                results.append(exp)
                if len(results) >= limit:
                    break
        return results

    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Compute aggregate experience memory stats."""
        if not os.path.exists(self.memory_file):
            return {"total_steps": 0, "total_games": 0, "wins": 0, "losses": 0}

        total_steps = 0
        games = set()
        wins = 0
        losses = 0

        with open(self.memory_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                exp = json.loads(line.strip())
                total_steps += 1
                games.add(exp.get("game_id"))
                if exp.get("is_terminal"):
                    if exp.get("outcome") == "WIN":
                        wins += 1
                    elif exp.get("outcome") == "LOSS":
                        losses += 1

        return {
            "total_steps": total_steps,
            "total_games": len(games),
            "wins": wins,
            "losses": losses,
            "win_rate_pct": round(wins / max(1, wins + losses) * 100.0, 1),
        }
