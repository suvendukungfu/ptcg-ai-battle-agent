# PTCG AI Battle Agent — Performance Engineering & Latency Report

**Benchmark Date**: 2026-08-14 05:59:13

## 1. Latency Profile

| Metric | Value | Budget Target | Status |
|---|---|---|---|
| **Average Latency** | **1.391 ms** | < 10.0 ms | **PASS** |
| **P50 Latency (Median)** | **1.185 ms** | < 5.0 ms | **PASS** |
| **P95 Latency** | **3.145 ms** | < 25.0 ms | **PASS** |
| **P99 Latency** | **3.723 ms** | < 50.0 ms | **PASS** |
| **Maximum Latency** | **3.889 ms** | < 200.0 ms | **PASS** |
| **Throughput** | **146.1 decisions/sec** | > 100.0 | **PASS** |

## 2. Robustness & Zero-Crash Guarantees

- **Total Decisions Evaluated**: 33
- **Invalid / Forfeited Games**: 0 (0.0%)
- **Exceptions Caught**: 0
- **Fallback Rate**: 0.00%
- **Search vs Heuristic Ratio**: 26 search / 7 heuristic

## 3. Resource & Memory Footprint

- **Process RSS Memory**: 216.1 MiB (Well within Kaggle 12.2 GiB RAM budget)
- **Memory Growth**: +4.2 MiB across 2 complete games
