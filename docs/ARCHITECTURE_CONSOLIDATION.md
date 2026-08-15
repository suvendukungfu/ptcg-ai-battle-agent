# Architecture Consolidation Audit: `agent/` (Canonical Architecture)

**Consolidation Status**: **COMPLETED & VERIFIED**  
**Production Runtime**: Pure `main.py` $\to$ `agent/` (Zero `src/` runtime dependencies)  
**Verification Date**: August 15, 2026

---

## 1. Architectural Evolution: Before vs After

### Before Consolidation
```text
main.py
  └── agent/action_selector.py
        ├── agent/state.py
        ├── agent/belief_state.py
        ├── agent/goals.py
        ├── src/shallow_search.py  <-- Legacy Cross-Import Dependency
        │     ├── src/state_evaluator.py
        │     ├── src/value_function.py
        │     ├── src/attack_evaluator.py
        │     ├── src/immunity_handler.py
        │     └── src/opponent_model.py
        └── agent/policy.py

Packaging: submission.tar.gz included agent/, src/, data/, deck.csv, main.py (32 files, 0.07 MiB)
```

### After Consolidation (Current State)
```text
main.py
  └── agent/action_selector.py
        ├── agent/state.py (Comprehensive typed GameState + normalization)
        ├── agent/belief_state.py (Hypergeometric Bayesian belief updating)
        ├── agent/goals.py (Strategic goal identification & state modulation)
        ├── agent/search.py (1-2 Ply lookahead with dynamic risk profile)
        ├── agent/evaluator.py (Unified board value & damage estimation)
        ├── agent/opponent_model.py (Bayesian threat estimation & archetype classification)
        ├── agent/policy.py (Tactical candidate ranking: attack, energy, trainer, target)
        ├── agent/deck_policy.py (Turn 0 deck loader & validator)
        ├── agent/fallback.py (Deterministic bounded fallback)
        └── agent/utils.py (Performance diagnostics & telemetry)

Packaging: submission.tar.gz includes ONLY agent/, data/, deck.csv, main.py (20 files, 0.06 MiB)
Legacy src/ remains outside the production submission for reference only.
```

---

## 2. Implementation Comparison & Rationales

| Responsibility | Canonical Module (`agent/`) | Superseded Module (`src/`) | Consolidation Rationale |
|---|---|---|---|
| **Search Engine** | `agent/search.py` | `src/shallow_search.py` | `agent/search.py` incorporates dynamic risk modulation (`aggression_bonus`, `retaliation_weight`), robust bounded option selection via `agent.fallback.make_distinct_choice`, and 220.0 prize valuation. |
| **Opponent Model** | `agent/opponent_model.py` + `agent/belief_state.py` | `src/opponent_model.py` | `agent/` uses exact hypergeometric math ($P(X \ge 1) = 1 - \frac{\binom{N-K}{n}}{\binom{N}{n}}$) with dynamic archetype recognition rather than fixed heuristic approximations. |
| **Game State** | `agent/state.py` | `src/state_evaluator.py` | `agent/state.py` provides typed helper properties (`total_your_energies`, `total_opp_energies`, `prize_differential`, `is_match_point`) and cross-version observation normalization. |
| **Value Function** | `agent/evaluator.py` | `src/value_function.py` | `agent/evaluator.py` unifies board evaluation, damage estimation, immunity calculation, and target prize values in a single high-cohesion module. |
| **Action Policies** | `agent/policy.py` | `src/attack_evaluator.py`, `src/energy_policy.py`, `src/target_selector.py` | `agent/policy.py` consolidates separate fragmented policies into clean ranking functions. |
| **Card Database** | `agent/card_database.py` | `src/card_database.py` | Identical schema with in-memory caching and hardcoded starter fallback. |

---

## 3. Verification & Benchmark Summary

1. **Test Suite**: **46 / 46 tests passing** in **1.40s** (including dedicated regression tests in `tests/test_consolidation.py`).
2. **Submission Archive**:
   - Packaged size: **0.06 MiB** (60,422 bytes).
   - Clean isolated extraction smoke test: **PASS** (Zero `src` modules imported into `sys.modules`).
3. **Simulation Stability**:
   - 30 complete CABT games executed (10 Self-Play, 10 vs Heuristic, 10 vs Random).
   - **0 Invalids / Illegal Actions**, **0.00% Fallback Rate**.
   - P95 Decision Latency: **2.665 ms** (down from 3.061 ms).
   - Maximum Observed Latency: **4.177 ms** (down from 15.432 ms).
