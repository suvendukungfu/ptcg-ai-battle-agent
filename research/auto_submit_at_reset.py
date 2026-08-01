"""
Auto-Submit at UTC Quota Reset Script.
Waits until 00:00:05 UTC, then submits Candidate FINAL to Kaggle using the verified .venv Kaggle CLI.
"""

import time
import subprocess
from datetime import datetime, timezone, timedelta

def get_seconds_until_reset() -> float:
    now = datetime.now(timezone.utc)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=5, microsecond=0)
    return (tomorrow - now).total_seconds()

def main():
    sec = get_seconds_until_reset()
    if sec > 0:
        now = datetime.now(timezone.utc)
        print(f"[{now.strftime('%H:%M:%S UTC')}] Waiting {sec/3600:.2f} hours ({int(sec)}s) until 00:00:05 UTC...")
        time.sleep(sec)
    
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}] UTC Quota reset reached! Submitting Candidate FINAL...")
    
    # 1. Verify Hash
    shasum = subprocess.check_output(["shasum", "-a", "256", "submission_candidate_final.tar.gz"], text=True).strip()
    print("Archive SHA256:", shasum)
    
    # 2. Submit via .venv/bin/kaggle CLI
    cmd = [
        ".venv/bin/kaggle", "competitions", "submit", "pokemon-tcg-ai-battle",
        "-f", "submission_candidate_final.tar.gz",
        "-m", "PTCG NEXUS v4.0 — Dynamic threat denial, auxiliary single-prize optimization, pure-energy consistency."
    ]
    sub_proc = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", sub_proc.stdout)
    print("STDERR:", sub_proc.stderr)
    
    # 3. Fetch submissions
    time.sleep(5)
    list_cmd = [".venv/bin/kaggle", "competitions", "submissions", "pokemon-tcg-ai-battle", "--format", "json"]
    list_proc = subprocess.run(list_cmd, capture_output=True, text=True)
    print("Submissions JSON:\n", list_proc.stdout)

if __name__ == "__main__":
    main()
