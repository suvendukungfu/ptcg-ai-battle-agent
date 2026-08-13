import os
from pathlib import Path
from typing import Optional

def get_competition_data_path() -> Optional[Path]:
    """
    Locate the Kaggle competition data directory dynamically.
    Checks in order:
    1. PTCG_DATA_PATH environment variable.
    2. Local ./data or ./kaggle_data directory if present.
    3. kagglehub default cache directory (~/.cache/kagglehub/competitions/pokemon-tcg-ai-battle).
    4. Calls kagglehub.competition_download if available.
    """
    # 1. Check environment variable
    env_path = os.environ.get("PTCG_DATA_PATH")
    if env_path:
        p = Path(env_path).expanduser().resolve()
        if p.exists():
            return p

    # 2. Check local directories in workspace
    project_root = Path(__file__).parent.resolve()
    for candidate_dir in ("data", "kaggle_data"):
        local_cand = project_root / candidate_dir
        if local_cand.exists() and any(local_cand.iterdir()):
            return local_cand

    # 3. Check kagglehub cache directory
    kagglehub_cache = Path.home() / ".cache" / "kagglehub" / "competitions" / "pokemon-tcg-ai-battle"
    if kagglehub_cache.exists():
        # Find latest version subdirectory if present
        versions = sorted(kagglehub_cache.glob("*"), key=os.path.getmtime, reverse=True)
        for v in versions:
            if v.is_dir():
                return v
        return kagglehub_cache

    # 4. Attempt dynamic kagglehub resolution
    try:
        import kagglehub
        path_str = kagglehub.competition_download("pokemon-tcg-ai-battle")
        if path_str:
            p = Path(path_str).expanduser().resolve()
            if p.exists():
                return p
    except Exception:
        pass

    return None
