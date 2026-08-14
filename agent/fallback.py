from typing import List, Dict, Any, Optional


def deterministic_fallback(select: Optional[Dict[str, Any]]) -> List[int]:
    """
    Deterministic, mathematical zero-crash guarantee fallback for legal action selection.
    Strictly satisfies:
    1. Returns a list of integers.
    2. Length is bounded by [minCount, maxCount].
    3. Every index satisfies 0 <= index < len(options).
    4. All chosen indices are unique.
    """
    if not select or not isinstance(select, dict):
        return []

    options = select.get("option", [])
    if not isinstance(options, list) or len(options) == 0:
        return []

    min_count = select.get("minCount", 1)
    max_count = select.get("maxCount", 1)

    if not isinstance(min_count, int) or min_count < 0:
        min_count = 1
    if not isinstance(max_count, int) or max_count < min_count:
        max_count = max(1, min_count)

    n_opts = len(options)
    target_count = min(max_count, n_opts)
    if target_count < min_count and n_opts >= min_count:
        target_count = min_count

    return list(range(target_count))


def make_distinct_choice(preferred_indices: List[int], n_opts: int, max_cnt: int, min_cnt: int = 1) -> List[int]:
    """
    Safely selects unique option indices from preferred_indices, filling remaining slots
    with available indices if needed until target count (bounded by min_cnt and max_cnt) is reached.
    """
    if n_opts <= 0:
        return []

    target_cnt = max(min_cnt, min(max_cnt, n_opts))
    chosen: List[int] = []

    for idx in preferred_indices:
        if isinstance(idx, int) and 0 <= idx < n_opts and idx not in chosen:
            chosen.append(idx)
            if len(chosen) == target_cnt:
                return chosen

    for idx in range(n_opts):
        if idx not in chosen:
            chosen.append(idx)
            if len(chosen) == target_cnt:
                return chosen

    return chosen
