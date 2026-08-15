# Architecture Consolidation Audit: `agent/` vs `src/`

**Status**: FORENSIC AUDIT COMPLETE  
**Primary Goal**: Safely unify and eliminate dual-architecture duplication between `agent/` and `src/` while maintaining 100% test passing rates and zero regression.

---

## 1. Executive Summary & File Mapping

The repository currently contains two parallel code structures:
- `agent/`: The modernized, unified, fully-typed production architecture (Layer A) supporting Bayesian belief tracking, strategic goal planning, and score decomposition.
- `src/`: The initial prototype architecture.

| Functional Component | `agent/` (Modern) | `src/` (Legacy) | Active in `main.py`? | Recommended Target |
|---|---|---|---|---|
| **Game State Representation** | `agent/state.py` (`GameState`, `parse_game_state`) | `src/state_evaluator.py` (`GameState`, `parse_game_state`) | `agent/state.py` | Consolidate to `agent/state.py` |
| **Card Database & Lookup** | `agent/card_database.py` (Typed caching + fallback) | `src/card_database.py` (Identical fallback dict) | `agent/card_database.py` | Consolidate to `agent/card_database.py` |
| **Opponent Modeling** | `agent/opponent_model.py` + `agent/belief_state.py` (Bayesian) | `src/opponent_model.py` (Heuristic prob estimation) | `agent/belief_state.py` + `src/opponent_model.py` | Unify into `agent/opponent_model.py` |
| **Search & Lookahead** | `agent/search.py` (2-Ply state projection) | `src/shallow_search.py` (1-2 Ply search) | `src/shallow_search.py` (via `action_selector.py`) | Unify into `agent/search.py` |
| **Evaluation & Value Function** | `agent/evaluator.py` + `agent/decomposition.py` | `src/state_evaluator.py` + `src/value_function.py` | `agent/evaluator.py` | Unify into `agent/evaluator.py` |
| **Tactical Policy & Ranking** | `agent/policy.py` (`rank_attack_options`, etc.) | `src/attack_evaluator.py`, `src/energy_policy.py`, `src/target_selector.py` | `agent/policy.py` | Consolidated in `agent/policy.py` |
| **Immunity & Safeguard** | `agent/evaluator.py` (`is_target_immune_to_ex`) | `src/immunity_handler.py` | `agent/evaluator.py` | Consolidated in `agent/evaluator.py` |

---

## 2. Key Differences & Architectural Comparison

### A. Which implementation is actually used by `main.py`?
`main.py` imports `agent.action_selector`. However, `agent/action_selector.py` line 11 imports `src.shallow_search`. Thus, at runtime:
1. State parsing uses `agent.state`.
2. Goal planning uses `agent.goals`.
3. Bayesian belief state uses `agent.belief_state`.
4. Search lookahead currently invokes `src.shallow_search.shallow_risk_aware_search`.
5. Heuristic fallback uses `agent.policy`.

### B. Which implementation is stronger?
- **`agent/` is significantly stronger**:
  - `agent/state.py` includes comprehensive normalization of bench, energies, and turn context.
  - `agent/belief_state.py` features exact hypergeometric Bayesian counting for unseen card estimation.
  - `agent/goals.py` provides macro situational modifiers (Safeguard bypass, match point lethal priority, anti-deckout threshold).
  - `agent/decomposition.py` provides explainable additive valuation for research and dashboard telemetry.

### C. Which files in `src/` are dead/legacy?
- `src/bench_trainer_policy.py`: Completely superseded by `agent/policy.py`.
- `src/energy_policy.py`: Superseded by `agent/policy.py::rank_energy_attachment_options`.
- `src/target_selector.py`: Superseded by `agent/policy.py::rank_target_options`.
- `src/immunity_handler.py`: Superseded by `agent/evaluator.py::is_target_immune_to_ex`.
- `src/card_database.py`: Duplicate of `agent/card_database.py`.

### D. Are there conflicting algorithms?
- In `src/opponent_model.py`, energy attachment probability is calculated using an empirical linear approximation ($P = \min(1.0, 0.4 + 0.1 \times \text{turn})$).
- In `agent/belief_state.py`, energy attachment probability is calculated using rigorous hypergeometric distribution math:
  $$P(X \ge 1) = 1 - \frac{\binom{N - K}{n}}{\binom{N}{n}}$$
  where $N$ is unseen cards, $K$ is remaining energies in deck+hand, and $n$ is opponent hand size.
- **Resolution**: The Bayesian hypergeometric calculation in `agent/` is mathematically superior, uncertainty-aware, and provides exact posterior estimates.

---

## 3. Safe Consolidation Roadmap (Future Phase)

When proceeding with consolidation:
1. **Redirect Search in `agent/action_selector.py`**:
   - Update `agent/action_selector.py` to directly use `agent.search.shallow_risk_aware_search` instead of `src.shallow_search`.
2. **Update Test Imports in `tests/test_qa_suite.py`**:
   - Change imports in `tests/test_qa_suite.py` from `src.*` to `agent.*`.
3. **Validate Packaging**:
   - Update `tools/build_submission.sh` to stage only `agent/`, `main.py`, and `deck.csv`, reducing archive size to under **0.03 MiB**.
4. **Run Full Verification**:
   - Execute `pytest tests/ -v` and `python tools/benchmark.py` to confirm identical or improved performance.
