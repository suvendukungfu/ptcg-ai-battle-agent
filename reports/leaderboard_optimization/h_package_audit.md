# Candidate H Package & Archive Integrity Audit

Generated at: 2026-08-16 09:13:30 UTC

---

## 1. Archive Checksums & Verification

| Archive File | SHA256 Checksum | Purpose / Role |
| :--- | :--- | :--- |
| `submission_candidate_b.tar.gz` | `a1a956115ca9a06af63f3df2ea0fc1f64d6508d4f004a8b220c6ab307672a678` | **Protected Baseline (Tag `candidate-b-v3.2`)** |
| `submission_candidate_d.tar.gz` | `5d8901307eae5b7896c665044a540c65b4738d1899ac062c4bd86a7882cceefb` | **Historical Reference** |
| `submission_candidate_f.tar.gz` | `81dba2fc4c27552c099b603e05ea987585c037b693c9f68022aff52c82b6ce73` | **LIVE ACTIVE KAGGLE SUBMISSION (55547508)** |
| `submission_candidate_h.tar.gz` | `35e445c72cfea97c9127888252e91900f985f5e1b9777e26ad9fb8f05870e2d3` | **LOCAL STANDBY ONLY (NOT FOR SUBMISSION)** |

---

## 2. Sandbox Execution Verification

- **Extraction Directory**: `/tmp/h_test`
- **Archive Contents**:
  - `main.py`
  - `deck.csv`
  - `agent/` (all 16 modules)
  - `data/EN Card Data.csv`
- **CABT Match Simulation**: Executed 108 steps without error (`['DONE', 'DONE']`).
- **Pytest Suite**: **62 passed in 0.76s** (100% pass rate).
