import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

import config
import agent.card_database as cdb

def run_data_verification():
    print("==================================================")
    print("      PTCG LOCAL DATA ACCESS VERIFICATION         ")
    print("==================================================")

    # 1. Competition path
    comp_path = config.get_competition_data_path()
    if not comp_path or not comp_path.exists():
        print("ERROR: Competition data path could not be located!")
        print("Please ensure kaggle data is downloaded or PTCG_DATA_PATH is set.")
        sys.exit(1)

    print(f"Competition path: {comp_path}")

    # 2. Number of files
    all_files = [p for p in comp_path.rglob("*") if p.is_file()]
    print(f"Number of files: {len(all_files)}")

    # 3. Card CSV path
    csv_path = cdb._find_card_csv()
    if not csv_path or not csv_path.exists():
        print("ERROR: 'EN Card Data.csv' was not found!")
        sys.exit(1)

    print(f"Card CSV path: {csv_path}")

    # 4. Number of cards
    cdb.init_card_database(force_reload=True)
    all_cards = cdb.get_all_cards()
    num_cards = len(all_cards)
    if num_cards == 0:
        print("ERROR: No cards could be loaded from the CSV database!")
        sys.exit(1)

    print(f"Number of cards: {num_cards}")

    # 5. First 5 card IDs & Names
    first_5_ids = list(sorted(all_cards.keys()))[:5]
    first_5_names = [cdb.get_card_name(cid) for cid in first_5_ids]
    print(f"First 5 card IDs: {first_5_ids}")
    print(f"First 5 card names: {first_5_names}")

    # 6. Engine path
    engine_dir = PROJECT_ROOT / "cg"
    if not engine_dir.exists():
        import kaggle_environments.envs.cabt.cg as cabt_cg
        engine_dir = Path(cabt_cg.__file__).parent
    print(f"Engine path: {engine_dir}")

    # 7. Sample submission path
    submission_path = PROJECT_ROOT / "submission.tar.gz"
    print(f"Sample submission path: {submission_path}")

    print("==================================================")
    print("SUCCESS: All local data and card assets verified!")
    print("==================================================")

if __name__ == "__main__":
    run_data_verification()
