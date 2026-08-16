import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional


DIAGNOSTICS: Dict[str, Any] = {
    "decisions": 0,
    "search_decisions": 0,
    "heuristic_decisions": 0,
    "fallback_decisions": 0,
    "exceptions": 0,
    "total_decision_time_ms": 0.0,
    "max_decision_time_ms": 0.0,
    "option_types_selected": {},
    "attacks_selected": 0,
    "kos_achieved": 0,
    "games_completed": 0,
}


def reset_diagnostics() -> None:
    """Reset all diagnostic telemetry counters."""
    global DIAGNOSTICS
    DIAGNOSTICS["decisions"] = 0
    DIAGNOSTICS["search_decisions"] = 0
    DIAGNOSTICS["heuristic_decisions"] = 0
    DIAGNOSTICS["fallback_decisions"] = 0
    DIAGNOSTICS["exceptions"] = 0
    DIAGNOSTICS["total_decision_time_ms"] = 0.0
    DIAGNOSTICS["max_decision_time_ms"] = 0.0
    DIAGNOSTICS["option_types_selected"] = {}
    DIAGNOSTICS["attacks_selected"] = 0
    DIAGNOSTICS["kos_achieved"] = 0
    DIAGNOSTICS["games_completed"] = 0


def get_diagnostics() -> Dict[str, Any]:
    """Retrieve diagnostic telemetry snapshot with calculated averages."""
    diag = dict(DIAGNOSTICS)
    total_decs = max(1, diag["decisions"])
    diag["avg_decision_time_ms"] = diag["total_decision_time_ms"] / total_decs
    fallback_rate = (diag["fallback_decisions"] / total_decs) * 100.0
    diag["fallback_rate_pct"] = fallback_rate
    return diag


def track_telemetry(chosen_indices: List[int], options: List[Dict[str, Any]]) -> None:
    """Update telemetry counts for selected actions."""
    n_opts = len(options)
    for idx in chosen_indices:
        if 0 <= idx < n_opts:
            opt = options[idx]
            if isinstance(opt, dict) and "type" in opt:
                opt_t = opt["type"]
                DIAGNOSTICS["option_types_selected"][opt_t] = DIAGNOSTICS["option_types_selected"].get(opt_t, 0) + 1
                if opt_t == 7:  # Attack
                    DIAGNOSTICS["attacks_selected"] += 1


def get_runtime_root() -> Path:
    """
    Robust runtime root directory resolver compatible with:
    A. Normal Python imports
    B. Direct script execution
    C. Kaggle simulation loader using exec() where __file__ is undefined
    D. Kaggle evaluation container (/kaggle_simulations/agent/)
    E. Clean extracted submission directories in isolation
    F. Local CABT test environments
    """
    # 1. Kaggle remote evaluation container
    kaggle_agent_dir = Path("/kaggle_simulations/agent")
    if kaggle_agent_dir.is_dir():
        return kaggle_agent_dir

    # 2. Check __file__ if defined in this module
    try:
        if "__file__" in globals() and globals()["__file__"]:
            file_path = Path(globals()["__file__"]).resolve()
            if file_path.parent.name == "agent":
                return file_path.parent.parent
            return file_path.parent
    except Exception:
        pass

    # 3. Check current working directory for signature files
    cwd = Path.cwd().resolve()
    if (cwd / "deck.csv").is_file() or (cwd / "main.py").is_file():
        return cwd
    if (cwd / "agent").is_dir():
        return cwd

    # 4. Check sys.path entries
    for p in sys.path:
        if p:
            cand = Path(p).resolve()
            if (cand / "deck.csv").is_file() or (cand / "agent").is_dir():
                return cand

    # 5. Default to current working directory
    return cwd


def resolve_runtime_path(relative_path: str) -> Path:
    """
    Resolve a project-relative file or directory path reliably across all execution contexts.
    """
    root = get_runtime_root()
    target = (root / relative_path).resolve()
    if target.exists():
        return target

    # Fallback search across alternate locations
    direct = Path(relative_path).resolve()
    if direct.exists():
        return direct

    cwd_target = (Path.cwd() / relative_path).resolve()
    if cwd_target.exists():
        return cwd_target

    for p in sys.path:
        if p:
            sys_target = (Path(p) / relative_path).resolve()
            if sys_target.exists():
                return sys_target

    return target
