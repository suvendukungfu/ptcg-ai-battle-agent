# PTCG AI Battle Agent — Performance Engineering & Latency Report

**Benchmark Date**: 2026-08-14 06:20:31

## 1. Latency Profile

| Metric | Value | Budget Target | Status |
|---|---|---|---|
| **Average Latency** | **2.209 ms** | < 10.0 ms | **PASS** |
| **P50 Latency (Median)** | **1.731 ms** | < 5.0 ms | **PASS** |
| **P95 Latency** | **4.784 ms** | < 25.0 ms | **PASS** |
| **P99 Latency** | **7.973 ms** | < 50.0 ms | **PASS** |
| **Maximum Latency** | **38.315 ms** | < 200.0 ms | **PASS** |
| **Throughput** | **144.0 decisions/sec** | > 100.0 | **PASS** |

## 2. Robustness & Zero-Crash Guarantees

- **Total Decisions Evaluated**: 576
- **Invalid / Forfeited Games**: 0 (0.0%)
- **Exceptions Caught**: 0
- **Fallback Rate**: 0.00%
- **Search vs Heuristic Ratio**: 495 search / 81 heuristic

## 3. Resource & Memory Footprint

- **Process RSS Memory**: 131.4 MiB (Well within Kaggle 12.2 GiB RAM budget)
- **Memory Growth**: +83.3 MiB across 10 complete games
