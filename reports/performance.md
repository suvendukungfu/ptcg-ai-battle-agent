# PTCG AI Battle Agent — Performance Engineering & Latency Report

**Benchmark Date**: 2026-08-14 06:15:33

## 1. Latency Profile

| Metric | Value | Budget Target | Status |
|---|---|---|---|
| **Average Latency** | **1.707 ms** | < 10.0 ms | **PASS** |
| **P50 Latency (Median)** | **1.449 ms** | < 5.0 ms | **PASS** |
| **P95 Latency** | **4.079 ms** | < 25.0 ms | **PASS** |
| **P99 Latency** | **5.153 ms** | < 50.0 ms | **PASS** |
| **Maximum Latency** | **10.022 ms** | < 200.0 ms | **PASS** |
| **Throughput** | **144.4 decisions/sec** | > 100.0 | **PASS** |

## 2. Robustness & Zero-Crash Guarantees

- **Total Decisions Evaluated**: 551
- **Invalid / Forfeited Games**: 0 (0.0%)
- **Exceptions Caught**: 0
- **Fallback Rate**: 0.00%
- **Search vs Heuristic Ratio**: 459 search / 92 heuristic

## 3. Resource & Memory Footprint

- **Process RSS Memory**: 113.6 MiB (Well within Kaggle 12.2 GiB RAM budget)
- **Memory Growth**: -71.0 MiB across 10 complete games
