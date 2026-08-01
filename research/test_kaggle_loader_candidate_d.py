import tempfile
import tarfile
import os
import sys
from pathlib import Path
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable

def test_candidate_d_kaggle_extraction():
    archive_path = "submission_candidate_d.tar.gz"
    assert os.path.isfile(archive_path), "submission_candidate_d.tar.gz not found"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(tmp_path)
            
        main_file = tmp_path / "main.py"
        deck_file = tmp_path / "deck.csv"
        agent_dir = tmp_path / "agent"
        data_file = tmp_path / "data" / "EN Card Data.csv"
        
        assert main_file.is_file(), "main.py missing from archive root"
        assert deck_file.is_file(), "deck.csv missing from archive root"
        assert agent_dir.is_dir(), "agent/ missing from archive root"
        assert data_file.is_file(), "data/EN Card Data.csv missing from archive"
        
        # Verify no illegal development folders
        assert not (tmp_path / "src").exists(), "src/ must NOT be in submission archive"
        assert not (tmp_path / "tests").exists(), "tests/ must NOT be in submission archive"
        assert not (tmp_path / "research").exists(), "research/ must NOT be in submission archive"
        
        print("1. Archive Structure & Exclusions: 100% PASS")
        
        # Test get_last_callable exactly as Kaggle does
        with open(main_file, "r") as f:
            raw_code = f.read()
            
        callable_agent = get_last_callable(raw_code, path=str(main_file))
        assert callable_agent is not None, "get_last_callable failed to extract agent"
        print("2. Kaggle get_last_callable: 100% PASS")
        
        # Test full simulation execution in clean directory
        env = make("cabt")
        steps = env.run([str(main_file), "random"])
        
        p0_status = steps[-1][0].status
        p0_reward = steps[-1][0].reward
        print(f"3. CABT Clean Execution: Status={p0_status}, Reward={p0_reward}, Steps={len(steps)}")
        assert p0_status == "DONE", f"Agent status was {p0_status}"
        print("\nALL KAGGLE RUNTIME TESTS PASSED WITH 100% COMPLIANCE!")

if __name__ == "__main__":
    test_candidate_d_kaggle_extraction()
