# Candidate F Kaggle Submission Record & Verification

Generated at: 2026-08-16 08:15:00 UTC
Competition: `pokemon-tcg-ai-battle`

---

## 1. Submission Metadata

- **Submission ID (Ref)**: `55547508`
- **Timestamp**: `2026-08-16T08:14:20.663000 UTC`
- **Archive Filename**: `submission_candidate_f.tar.gz`
- **Archive SHA256**: `81dba2fc4c27552c099b603e05ea987585c037b693c9f68022aff52c82b6ce73`
- **Version**: PTCG NEXUS v3.4 (Generalized Adaptive Meta-Breaker)
- **Git Branch**: `optimization/candidate-f-meta-breaker`
- **Submission Message**:
  > "PTCG NEXUS v3.4 — Meta-adaptive matchup intelligence, generalized non-EX threat handling, safeguard-aware counterplay, improved deck architecture, and validated adversarial performance."
- **Current Status**: `SubmissionStatus.PENDING` (Validation container queued)

---

## 2. Protected Baseline Preservation

- **Candidate B Baseline (Protected)**:
  - Submission ID: `55540464`
  - Public Score: `595.5`
  - Archive: `submission_candidate_b.tar.gz` (`a1a956115ca9a06af63f3df2ea0fc1f64d6508d4f004a8b220c6ab307672a678`)
  - Git Rollback Tag: `candidate-b-v3.2`
- **Candidate D (Previous)**:
  - Submission ID: `55542011`
  - Public Score: `428.1`
  - Archive: `submission_candidate_d.tar.gz` (`5d8901307eae5b7896c665044a540c65b4738d1899ac062c4bd86a7882cceefb`)

---

## 3. Pre-Submission Local Benchmark Summary

- **1,100-Game Overall Win Rate**: **76.0%** (vs Candidate B: 43.0%, +33.0% $\Delta$)
- **2,000-Scenario Stress Win Rate**: **75.6%** (vs Candidate B: 48.2%, +27.4% $\Delta$)
- **Safety**: 0 Illegal Actions, 0 Fallbacks, 0 Runtime Errors
- **Latency**: P50 = 0.82 ms, P95 = 5.14 ms, P99 = 9.58 ms
- **Generalization**: 0 hardcoded card IDs in core decision engine (`agent/damage_model.py`, `agent/opponent_model.py`, `agent/evaluator.py`, `agent/policy.py`).

---

## 4. Hard Stop Policy

> [!IMPORTANT]
> **HARD STOP IN EFFECT**: Exactly one submission (`55547508`) was executed. No additional submissions will be made until public ladder games for `55547508` have completed and their replays are forensically analyzed.
