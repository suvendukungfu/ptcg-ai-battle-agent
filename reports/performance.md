# PTCG AI Battle Agent — Performance Engineering & Latency Report

**Benchmark Date**: 2026-08-14 06:09:35

## 1. Latency Profile

| Metric | Value | Budget Target | Status |
|---|---|---|---|
| **Average Latency** | **1.884 ms** | < 10.0 ms | **PASS** |
| **P50 Latency (Median)** | **1.523 ms** | < 5.0 ms | **PASS** |
| **P95 Latency** | **4.256 ms** | < 25.0 ms | **PASS** |
| **P99 Latency** | **4.832 ms** | < 50.0 ms | **PASS** |
| **Maximum Latency** | **45.377 ms** | < 200.0 ms | **PASS** |
| **Throughput** | **155.7 decisions/sec** | > 100.0 | **PASS** |

## 2. Robustness & Zero-Crash Guarantees

- **Total Decisions Evaluated**: 267
- **Invalid / Forfeited Games**: 0 (0.0%)
- **Exceptions Caught**: 0
- **Fallback Rate**: 0.00%
- **Search vs Heuristic Ratio**: 230 search / 37 heuristic

## 3. Resource & Memory Footprint

- **Process RSS Memory**: 96.4 MiB (Well within Kaggle 12.2 GiB RAM budget)
- **Memory Growth**: +54.2 MiB across 10 complete games
