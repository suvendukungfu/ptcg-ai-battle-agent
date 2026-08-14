import time
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
