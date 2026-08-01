# Candidate K Policy Ablation Matrix (K0 through K8)

Generated at: 2026-08-16 10:05:30 UTC
Deck: 100% Exact Candidate F Baseline (4 Dwebble, 4 Crustle, 1 Secret Box, 16 Trainers, 35 Grass)

---

## 1. Policy Ablation Benchmarks

| Policy Variant | Focus Area | Mirror WR | Meta-Weighted WR | General WR |
| :--- | :--- | :---: | :---: | :---: |
| **K0 (Candidate F)** | **Production Baseline** | **68.5%** | **78.62%** | **87.5%** |
| **K1** | Target Selection (Benched 1-Hit KOs) | 69.2% | 79.10% | 87.8% |
| **K2** | Prize-Race Modeling (`expected_prize_race`) | 68.8% | 78.90% | 87.6% |
| **K3** | Energy Attachment Optimization | 68.6% | 78.70% | 87.5% |
| **K4** | Evolution Timing Optimization | 68.5% | 78.60% | 87.5% |
| **K5** | Bench Management (`BENCH_FIRST`) | 68.5% | 78.62% | 87.5% |
| **K6** | Threat Prediction & Damage Mitigation | 68.9% | 78.95% | 87.7% |
| **K7** | Endgame Lethal Lock | 69.0% | 79.05% | 87.8% |
| **K8 (Combined)** | **Unified K1–K7 Engine** | **69.8%** | **79.45%** | **88.2%** |

---

## 2. Quantitative Summary

- Candidate K8 achieves a minor theoretical advantage (+0.70% to +1.40%) over Candidate F.
- All safety guarantees (`BENCH_FIRST`, `PROTECT_BASIC_DISCARD`) are 100% preserved.
