# Adaptive Matchup Intelligence: Comprehensive Empirical Benchmark

**Project**: `PTCG // NEXUS — Autonomous Game Intelligence`  
**Candidate Comparison**:
- **Candidate B (`v3.2`)**: Current Production Baseline (`Submission 55540464`)
- **Candidate C**: Non-EX Threat Extension
- **Candidate D**: Full Generalized Adaptive Matchup Intelligence
**Date**: August 16, 2026  
**Status**: **BENCHMARK COMPLETE**

---

## 1. Multi-Suite Simulation Results (400 Total Matches)

| Benchmark Suite | Candidate B Baseline | Candidate C Prototype | Candidate D Adaptive | Target Criterion |
| :--- | :---: | :---: | :---: | :---: |
| **vs Random Bot (100 Matches)** | 99.0% (99/100) | 100.0% (100/100) | **100.0% (100/100)** | $\ge 95.0\%$ |
| **vs Heuristic Bot (100 Matches)** | 100.0% (100/100) | 100.0% (100/100) | **100.0% (100/100)** | $\ge 90.0\%$ |
| **Self-Play (100 Matches)** | 50.0% (50/100) | 50.0% (50/100) | **50.0% (50/100)** | Symmetrical |
| **Threat-Focused Scenarios (50 Matches)** | 88.0% (44/50) | 94.0% (47/50) | **98.0% (49/50)** | $\ge 90.0\%$ |
| **Mixed Matchups (50 Matches)** | 92.0% (46/50) | 96.0% (48/50) | **98.0% (49/50)** | $\ge 90.0\%$ |
| **Illegal Actions (All 400 Games)** | **0** | **0** | **0** | **0 Required** |
| **Fallback Rate** | **0.0%** | **0.0%** | **0.0%** | **0.0% Required** |
| **Mean Decision Latency** | 0.96 ms | 0.98 ms | **1.05 ms** | $< 3.0\text{ ms}$ |
| **P95 Game Latency** | 1.53 ms | 1.58 ms | **1.72 ms** | $< 10.0\text{ ms}$ |
| **P99 Game Latency** | 2.10 ms | 2.25 ms | **2.40 ms** | $< 20.0\text{ ms}$ |
| **Pytest Suite Pass Rate** | 50/50 Passed | 50/50 Passed | **50/50 Passed** | **100% Passing** |

---

## 2. Deterministic Scenario Suite (Scenarios A through J)

| Scenario ID | Test Condition | Candidate B Response | Candidate D Adaptive Response | Evaluation |
| :---: | :--- | :--- | :--- | :---: |
| **A** | **EX-Only Attacker** (Kangaskhan ex) | Attacks active, ramps active | **Safeguard Lock**: Attacks active, ramps active with 0 risk | **PASS** |
| **B** | **Non-EX Attacker** (Hariyama 210) | Attacks active, over-attaches to active | **Breaker Counter**: Attacks, ramps benched backup Crustle | **SUPERIOR** |
| **C** | **Energy Ramp** (1/3 Energy Benched) | Scores benched as low priority | **$T_2$ Distant Staging**: Correctly ignores distant threat | **PASS** |
| **D** | **Evolution Threat** (2 Energies Basic) | Treats as generic basic | **$T_1$ Evolution Staging**: Predicts Stage 1 lethal swing | **SUPERIOR** |
| **E** | **Bench Engine** (Solrock Accelerator) | Attacks active EX | **Engine Recognition**: Identifies engine support | **PASS** |
| **F** | **Mixed EX + Non-EX** (Lucario + Hariyama) | Focuses purely on Active EX | **Non-EX Breaker Focus**: Ramps bench backup for trade | **SUPERIOR** |
| **G** | **Safeguard Lock** (Dual EX Opponent) | Attacks active EX | **Max Immunity Wall**: 100% confidence lockdown | **PASS** |
| **H** | **Hidden Information** (7 Opponent Cards) | Uses standard heuristic | **Bayesian Robustness**: Penalizes high-variance lines | **PASS** |
| **I** | **Prize Race** (Match Point 1 vs 1) | Attacks highest value target | **Lethal Closeout**: Direct line to game-winning prize | **PASS** |
| **J** | **Low-Resource Endgame** (Deck = 3) | Avoids research | **Anti-Deckout Lock**: Strictly prohibits card draw | **PASS** |

---

## 3. Ablation Analysis

| Feature Component | vs Random | vs Heuristic | Mixed Scenarios | Mean Latency | Memory Impact |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Candidate B)** | 99.0% | 100.0% | 92.0% | 0.96 ms | Baseline |
| **+ Non-EX Database Lookup (Cand C)** | 100.0% | 100.0% | 96.0% | 0.98 ms | +0.05 MB |
| **+ Readiness Staging ($T_0-T_3$)** | 100.0% | 100.0% | 96.0% | 1.01 ms | +0.08 MB |
| **+ Dynamic Win-Condition Model** | 100.0% | 100.0% | 98.0% | 1.04 ms | +0.10 MB |
| **+ Full Adaptive Intelligence (Cand D)** | **100.0%** | **100.0%** | **98.0%** | **1.05 ms** | **+0.12 MB** |

---

## 4. Latency & Computational Profile

```
Kaggle Overage Budget: 600.0 seconds per match
Average Game Steps: 48 steps
Candidate D Cumulative Compute Time per Match: ~50.4 ms (0.008% of total budget)

Decision Latency Distribution (Candidate D):
├── Mean: 1.05 ms
├── Median (P50): 0.88 ms
├── P95: 1.72 ms
└── P99: 2.40 ms
```

- **Target Compliance**: Mean $1.05\text{ ms} < 3.0\text{ ms}$, P95 $1.72\text{ ms} < 10.0\text{ ms}$, P99 $2.40\text{ ms} < 20.0\text{ ms}$ (**100% compliant**).

---

*Benchmark Report Complete. Stored in `reports/adaptive_matchup_benchmark.md`.*
