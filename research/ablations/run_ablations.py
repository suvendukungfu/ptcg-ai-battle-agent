import os
import sys
import json
import time
from typing import Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from research.ablations.ablation_configs import ABLATION_VARIANTS
from simulation.tournament import run_tournament

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def run_ablation_study(games_per_pairing: int = 6, verbose: bool = True) -> Dict[str, Any]:
    """Execute ablation tournament across variants A through F."""
    contestants = {k: v["agent"] for k, v in ABLATION_VARIANTS.items()}

    if verbose:
        print("=" * 70)
        print("          STARTING COMPREHENSIVE ABLATION STUDY (A -> F)")
        print("=" * 70)

    results = run_tournament(
        contestants=contestants,
        games_per_pairing=games_per_pairing,
        initial_elo=1500.0,
        verbose=verbose,
    )

    out_path = os.path.join(REPORTS_DIR, "ablation_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    if verbose:
        print(f"\nAblation study results successfully written to: {out_path}")

    return results


if __name__ == "__main__":
    run_ablation_study(games_per_pairing=4, verbose=True)
