# Submission Runtime & Packaging Forensic Audit

**Target File**: `submission.tar.gz`  
**Evaluation Scope**: File structure, dependency resolution, execution contract compliance, and archive size.

---

## 1. Archive Manifest & Structure

- **Archive Size**: **0.07 MiB** (69,002 bytes).
- **Kaggle Maximum Limit**: **197.7 MiB** (200,000,000 bytes) — **PASS (Utilizing < 0.04% of budget)**.
- **Top-Level File List**:
  - `main.py`
  - `deck.csv`
  - `agent/__init__.py`
  - `agent/action_selector.py`
  - `agent/belief_state.py`
  - `agent/card_database.py`
  - `agent/deck_policy.py`
  - `agent/decomposition.py`
  - `agent/evaluator.py`
  - `agent/fallback.py`
  - `agent/goals.py`
  - `agent/opponent_model.py`
  - `agent/policy.py`
  - `agent/risk_model.py`
  - `agent/search.py`
  - `agent/state.py`
  - `agent/utils.py`
  - `data/EN Card Data.csv`
  - `src/` (Legacy prototype modules)

---

## 2. Isolated Execution Verification

A simulated clean extraction was performed in an isolated scratch directory without repository context:

```bash
mkdir -p /tmp/submission_test
tar -xzf submission.tar.gz -C /tmp/submission_test
cd /tmp/submission_test
python3 -c "
import main
deck = main.agent({'select': None})
print('Turn 0 deck length:', len(deck))
assert len(deck) == 60
mock_obs = {
    'yourIndex': 0,
    'turn': 1,
    'current': {
        'player': [
            {'active': {'id': 723, 'hp': 350, 'maxHp': 350, 'energy': [3, 3]}, 'bench': [], 'prizes': [1,2,3,4,5,6], 'hand': [{'id': 3}], 'deck': 30, 'discard': []},
            {'active': {'id': 721, 'hp': 150, 'maxHp': 150, 'energy': []}, 'bench': [], 'prizes': [1,2,3,4,5,6], 'hand': 5, 'deck': 35, 'discard': []}
        ]
    },
    'select': {
        'context': 0,
        'type': 0,
        'minCount': 1,
        'maxCount': 1,
        'option': [
            {'index': 0, 'type': 0, 'damage': 160, 'name': 'Electro Bullet'},
            {'index': 1, 'type': 14, 'name': 'Pass'}
        ]
    }
}
action = main.agent(mock_obs)
print('Decision returned:', action)
assert action in ([0], [1])
"
```

**Results**:
- Deck load test: **PASS** (60 integer card IDs).
- Decision loop test: **PASS** (Returned `[0]`).
- Zero path dependencies on local Mac filesystem paths.

---

## 3. Critical Dependency Findings

1. **`cg` Module**:
   - `cg/` binaries (`libcg.so`, `libcg.dylib`) are **not** needed inside `submission.tar.gz`. The Kaggle platform environment automatically executes `agent(obs)` inside its own harness where `kaggle-environments` has `cg` pre-installed.
2. **`src/` Module Dependency**:
   - `agent/action_selector.py` imports `src.shallow_search`. Because of this import, `src/` must remain in `submission.tar.gz` until `agent/action_selector.py` is consolidated to import directly from `agent.search`.
3. **`data/EN Card Data.csv`**:
   - `data/EN Card Data.csv` is 202 KB. `agent/card_database.py` includes a hardcoded fallback dictionary for the key cards in case the CSV is missing. Including the CSV allows full lookup of any unexpected opponent card on the ladder.
