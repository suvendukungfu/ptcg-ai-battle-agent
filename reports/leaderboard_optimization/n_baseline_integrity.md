# Candidate N Baseline Integrity & Production Freeze

Generated at: 2026-08-16 16:10:00 UTC
Branch: `candidate-n-m-froslass-swarm`

---

## 1. Protected Archive Checksums

| File | SHA256 Checksum | Status / Role |
| :--- | :--- | :--- |
| `submission_candidate_m.tar.gz` | `69edc45917c4240320a2bddffd86e9909e8d37b6f1bc1ca354700e0922d4c579` | **LIVE ACTIVE KAGGLE AGENT (Submission 55554838, Score 655.7)** |
| `submission_candidate_b.tar.gz` | `a1a956115ca9a06af63f3df2ea0fc1f64d6508d4f004a8b220c6ab307672a678` | **Protected Rollback Baseline (Tag `candidate-b-v3.2`, Score 595.5)** |
| `submission_candidate_f.tar.gz` | `81dba2fc4c27552c099b603e05ea987585c037b693c9f68022aff52c82b6ce73` | **Historical Production Baseline (Score 486.8)** |

---

## 2. Invariants & Isolation Protocol

- Live Candidate M remains completely untouched on Kaggle.
- All Candidate N policy experiments are strictly isolated to `candidate-n-m-froslass-swarm`.
- Exact 100% pure Candidate M deck is preserved (4 Dwebble, 4 Crustle, 1 Secret Box, 16 Trainers, 35 Grass Energy).
