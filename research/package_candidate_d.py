import tarfile
import os
from pathlib import Path

def create_candidate_d_archive():
    target_archive = "submission_candidate_d.tar.gz"
    if os.path.exists(target_archive):
        os.remove(target_archive)
        
    required_files = [
        "main.py",
        "deck.csv",
    ]
    required_dirs = [
        "agent",
        "data",
    ]
    
    with tarfile.open(target_archive, "w:gz") as tar:
        for f in required_files:
            if os.path.isfile(f):
                tar.add(f, arcname=f)
                print(f"Added file: {f}")
            else:
                raise FileNotFoundError(f"Missing required file: {f}")
                
        for d in required_dirs:
            if os.path.isdir(d):
                for root, _, files in os.walk(d):
                    for file in files:
                        if file.endswith(".py") or file.endswith(".csv") or file.endswith(".json"):
                            if "__pycache__" not in root:
                                full_path = os.path.join(root, file)
                                tar.add(full_path, arcname=full_path)
                                print(f"Added file: {full_path}")
            else:
                raise FileNotFoundError(f"Missing required dir: {d}")
                
    size_kb = os.path.getsize(target_archive) / 1024.0
    print(f"\nSuccessfully built {target_archive} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    create_candidate_d_archive()
