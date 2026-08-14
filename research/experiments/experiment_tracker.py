import os
import sys
import json
import time
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registry.json")


def get_git_commit() -> str:
    """Retrieve current git commit hash."""
    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        return commit
    except Exception:
        return "local_dev"


class ExperimentTracker:
    """Registry and logger for reproducible ML/AI research experiments."""

    def __init__(self, registry_file: str = REGISTRY_PATH):
        self.registry_file = registry_file
        self.experiments: List[Dict[str, Any]] = []
        self._load_registry()

    def _load_registry(self) -> None:
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    self.experiments = json.load(f)
            except Exception:
                self.experiments = []

    def save_registry(self) -> None:
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.experiments, f, indent=2)

    def log_experiment(
        self,
        experiment_id: str,
        agent_version: str,
        deck: str,
        policy_version: str,
        search_depth: int,
        search_budget: Dict[str, Any],
        seed: int,
        games: int,
        wins: int,
        losses: int,
        draws: int,
        win_rate: float,
        average_game_length: float,
        average_decision_time_ms: float,
        p95_latency_ms: float,
        fallback_rate: float,
        notes: str = "",
    ) -> Dict[str, Any]:
        """Record experiment result to persistent registry."""
        record = {
            "experiment_id": experiment_id,
            "date": datetime.now(timezone.utc).isoformat(),
            "git_commit": get_git_commit(),
            "agent_version": agent_version,
            "deck": deck,
            "policy_version": policy_version,
            "search_depth": search_depth,
            "search_budget": search_budget,
            "seed": seed,
            "games": games,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": round(win_rate, 2),
            "average_game_length": round(average_game_length, 2),
            "average_decision_time": round(average_decision_time_ms, 3),
            "P95_latency": round(p95_latency_ms, 3),
            "fallback_rate": round(fallback_rate, 3),
            "notes": notes,
        }

        self.experiments.append(record)
        self.save_registry()
        return record

    def list_experiments(self) -> List[Dict[str, Any]]:
        return list(self.experiments)
