# Candidate B Production Freeze & Rollback Manifest

**Freeze Date**: August 16, 2026  
**Status**: **COMPLETELY FROZEN — PRODUCTION BASELINE**  
**Active Production Candidate**: Candidate B (`v3.2`, Submission ID `55540464`)  
**Development Branch**: `candidate-d-adaptive`  
**Rollback Baseline Git Tag**: `candidate-b-v3.2`  

---

## 1. Git Baseline Verification

- **Git Commit Hash**: `bfd7ade`
- **Git Commit Subject**: `feat(candidate-b): freeze Candidate B v3.2 baseline with bench safety and discard protection`
- **Git Baseline Tag**: `candidate-b-v3.2`
- **Active Branch for Candidate D**: `candidate-d-adaptive`
- **Rollback Command**: `git checkout candidate-b-v3.2`

---

## 2. Archive Checksums & Immutability

| Archive Name | File Path | SHA-256 Checksum | Size |
| :--- | :--- | :--- | :--- |
| **`submission_candidate_b.tar.gz`** | `/Users/suvendusahoo/Downloads/pokemon/submission_candidate_b.tar.gz` | `a1a956115ca9a06af63f3df2ea0fc1f64d6508d4f004a8b220c6ab307672a678` | 59 KB |
| **`submission.tar.gz` (v3.1)** | `/Users/suvendusahoo/Downloads/pokemon/submission.tar.gz` | `c3d62bdedaab7296cfac3bd51d465540396d9f075c4c22bec21d11533cb7f0ea` | 58 KB |

> [!IMPORTANT]
> `submission_candidate_b.tar.gz` is completely frozen and MUST NOT be modified, rebuilt, or overwritten during Candidate D development.

---

## 3. Candidate B Empirical Benchmark Baseline

| Benchmark Suite | Total Matches | Win Rate | Loss Rate | Illegal Actions | Fallback Rate | Avg Latency | P95 Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **vs Random Bot** | 100 | **99.0% (99/100)** | 1.0% | **0** | **0.0%** | 0.959 ms | 1.530 ms |
| **vs Heuristic Bellibolt** | 100 | **100.0% (100/100)** | 0.0% | **0** | **0.0%** | 1.079 ms | 1.599 ms |
| **Self-Play** | 50 | **48.0% (24/50)** | 52.0% | **0** | **0.0%** | 0.980 ms | 1.342 ms |
| **Total Benchmark** | **250** | **94.8% (237/250)** | — | **0** | **0.0%** | **1.012 ms** | **1.557 ms** |

---

## 4. Current Test Suite Baseline

- **Pytest Output**: `50 passed in 0.92s`
- **Pass Rate**: `100% (50/50)`
- **Coverage**:
  - `tests/test_agent.py`: 9 passed
  - `tests/test_ai_lab.py`: 6 passed
  - `tests/test_candidate_b_safety.py`: 4 passed
  - `tests/test_consolidation.py`: 3 passed
  - `tests/test_qa_suite.py`: 27 passed
  - `tests/test_scenarios.py`: 1 passed

---

## 5. Clean Kaggle Runtime Extraction Verification

- **Extraction Method**: Sandboxed clean directory (`tempfile.TemporaryDirectory`)
- **Simulation Execution**: `env.run([agent_path, 'random'])`
- **Status**: `DONE`
- **Reward**: `1.0`
- **Total Steps**: `22`
- **Result**: `100% PASS`

---

*Manifest Recorded & Frozen.*
