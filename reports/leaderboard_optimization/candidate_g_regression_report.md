# Candidate G Regression Gate & Safety Report

Generated at: 2026-08-16 08:36:00 UTC

---

## 1. Regression Gate Evaluation

To be eligible for future testing, Candidate G must satisfy the 12 strict gate criteria:

| Gate Condition | Required Threshold | Observed (G8) | Status |
| :--- | :--- | :---: | :---: |
| **1. Non-EX Performance** | Material improvement or parity | 83.6% vs 82.1% (+1.5%) | **PASS** |
| **2. EX Performance** | Zero regression ($\ge 95\%$) | 100.0% vs 100.0% (0.0%) | **PASS** |
| **3. Opening Consistency** | $\ge 90.0\%$ | 96.5% | **PASS** |
| **4. Duraludon Matchup** | $\ge 80.0\%$ | 85.0% | **PASS** |
| **5. Cinderace Matchup** | $\ge 65.0\%$ | 70.0% | **PASS** |
| **6. Alakazam Matchup** | $\ge 80.0\%$ | 90.0% | **PASS** |
| **7. Trevenant Matchup** | $\ge 80.0\%$ | 90.0% | **PASS** |
| **8. Illegal Actions** | Exactly 0 | **0** | **PASS** |
| **9. Fallback Rate** | Exactly 0.0% | **0.0%** | **PASS** |
| **10. Runtime Errors** | Exactly 0 | **0** | **PASS** |
| **11. Decision Latency** | P95 < 15.0 ms | **5.12 ms** | **PASS** |
| **12. Multi-Seed Stability** | Passes across 2,000 games | **88.5% across 2,000 games** | **PASS** |

---

## 2. Safety & Protocol Compliance

- **Rollback Safety**: Candidate B (`submission_candidate_b.tar.gz`) is 100% preserved.
- **Candidate F Integrity**: Candidate F (`submission_candidate_f.tar.gz`) is 100% preserved.
- **Isolation**: Candidate G research conducted entirely on isolated branch `candidate-g-research`.
