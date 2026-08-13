import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

def download_and_inspect_data():
    print("==================================================")
    print("  Kaggle Competition Data Downloader (kagglehub)  ")
    print("==================================================")
    
    try:
        import kagglehub
    except ImportError:
        print("ERROR: kagglehub is not installed! Please run 'pip install kagglehub'.")
        sys.exit(1)

    print("Initiating download for 'pokemon-tcg-ai-battle'...")
    try:
        path_str = kagglehub.competition_download('pokemon-tcg-ai-battle')
    except Exception as e:
        print(f"\n[DOWNLOAD FAILED] {e}")
        print("\nNOTE: Kaggle requires authentication to download competition files.")
        print("Please ensure one of the following:")
        print("  1. You have placed 'kaggle.json' in '~/.kaggle/kaggle.json'")
        print("  2. Or set environment variables:")
        print("     export KAGGLE_USERNAME='your_username'")
        print("     export KAGGLE_KEY='your_api_key'")
        print("  3. And accepted competition rules on Kaggle: https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/rules")
        print("  4. Or if you downloaded files manually, set:")
        print("     export PTCG_DATA_PATH='/path/to/extracted_files'")
        return None

    data_path = Path(path_str).resolve()
    print(f"\nSUCCESS: Competition data downloaded/located at:")
    print(f"  {data_path}\n")

    # 4. Recursively list downloaded files
    print("--------------------------------------------------")
    print("Downloaded Files & Directory Structure:")
    all_files = sorted(list(data_path.rglob("*")))
    
    file_inventory = {
        "ptcg_engine": [],
        "sample_submission": [],
        "card_data_en": None,
        "card_data_jp": None,
        "card_id_pdf_en": None,
        "card_id_pdf_jp": None,
        "python_files": [],
        "configs": [],
        "sdk_api": [],
        "all_files_count": 0,
    }

    for p in all_files:
        if p.is_file():
            file_inventory["all_files_count"] += 1
            rel = p.relative_to(data_path)
            size_kb = p.stat().st_size / 1024.0
            size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024.0:.2f} MB"
            print(f"  - {rel} ({size_str})")

            # Categorize files
            name_lower = p.name.lower()
            if "en card data.csv" in name_lower or "card_data_en" in name_lower:
                file_inventory["card_data_en"] = p
            elif "jp card data.csv" in name_lower or "card_data_jp" in name_lower:
                file_inventory["card_data_jp"] = p
            elif "card_id_list_en" in name_lower and name_lower.endswith(".pdf"):
                file_inventory["card_id_pdf_en"] = p
            elif "card_id_list_jp" in name_lower and name_lower.endswith(".pdf"):
                file_inventory["card_id_pdf_jp"] = p
            elif "sample_submission" in str(p) or "submission" in name_lower:
                file_inventory["sample_submission"].append(p)
            elif "engine" in str(p).lower() or "ptcg" in str(p).lower() or "cg" in str(p).lower():
                file_inventory["ptcg_engine"].append(p)

            if p.suffix == ".py":
                file_inventory["python_files"].append(p)
            elif p.suffix in (".json", ".yaml", ".yml", ".toml"):
                file_inventory["configs"].append(p)

    print("--------------------------------------------------")
    print(f"Total Files Identified: {file_inventory['all_files_count']}")
    print(f"  - EN Card Data CSV: {file_inventory['card_data_en']}")
    print(f"  - JP Card Data CSV: {file_inventory['card_data_jp']}")
    print(f"  - Card ID PDF (EN): {file_inventory['card_id_pdf_en']}")
    print(f"  - Card ID PDF (JP): {file_inventory['card_id_pdf_jp']}")
    print(f"  - Sample Submissions: {len(file_inventory['sample_submission'])} files")
    print(f"  - Python Scripts: {len(file_inventory['python_files'])} files")
    print("==================================================")
    return data_path

if __name__ == "__main__":
    download_and_inspect_data()
