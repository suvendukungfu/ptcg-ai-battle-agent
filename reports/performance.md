# PTCG AI Battle Agent — Performance Engineering & Latency Report

**Benchmark Date**: 2026-08-14 05:55:00

## 1. Latency Profile

| Metric | Value | Budget Target | Status |
|---|---|---|---|
| **Average Latency** | **1.556 ms** | < 10.0 ms | **PASS** |
| **P50 Latency (Median)** | **1.228 ms** | < 5.0 ms | **PASS** |
| **P95 Latency** | **3.986 ms** | < 25.0 ms | **PASS** |
| **P99 Latency** | **5.546 ms** | < 50.0 ms | **PASS** |
| **Maximum Latency** | **8.895 ms** | < 200.0 ms | **PASS** |
| **Throughput** | **142.9 decisions/sec** | > 100.0 | **PASS** |

## 2. Robustness & Zero-Crash Guarantees

- **Total Decisions Evaluated**: 398
- **Invalid / Forfeited Games**: 0 (0.0%)
- **Exceptions Caught**: 0
- **Fallback Rate**: 0.00%
- **Search vs Heuristic Ratio**: 329 search / 69 heuristic

## 3. Resource & Memory Footprint

- **Process RSS Memory**: 135.3 MiB (Well within Kaggle 12.2 GiB RAM budget)
- **Memory Growth**: -49.8 MiB across 10 complete games
