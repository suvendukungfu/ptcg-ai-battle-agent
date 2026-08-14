import os
import sys
import csv
from typing import Dict, Any, List

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_matchup_matrix(tournament_results: Dict[str, Any]) -> str:
    """Generate reports/matchup_matrix.csv from tournament results."""
    matchup_matrix = tournament_results.get("matchup_matrix", {})
    names = list(matchup_matrix.keys())

    csv_path = os.path.join(REPORTS_DIR, "matchup_matrix.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Agent / Archetype"] + names)

        for n1 in names:
            row = [n1]
            for n2 in names:
                if n1 == n2:
                    row.append("50.0%")
                else:
                    rec = matchup_matrix.get(n1, {}).get(n2, {"wins": 0, "losses": 0, "draws": 0})
                    tot = rec["wins"] + rec["losses"] + rec["draws"]
                    if tot > 0:
                        wr = (rec["wins"] / tot) * 100.0
                        row.append(f"{wr:.1f}%")
                    else:
                        row.append("N/A")
            writer.writerow(row)

    return csv_path
