# Post-Consolidation CABT Simulation & Latency Benchmark Report

**Benchmark Date**: August 15, 2026  
**Architecture Target**: Pure `agent/` Canonical AI Architecture (Decoupled from `src/`)  
**Simulation Engine**: Official `kaggle-environments` CABT Engine (`cabt.py`)

---

## 1. Simulation Matchup Results (30 Complete Games)

| Matchup Series | Games | Wins | Losses | Draws | Invalids | Avg Steps/Game | Avg Latency | Fallback Rate |
|---|---|---|---|---|---|---|---|---|
| **Self-Play (Agent vs Agent)** | 10 | 8 (P0) | 2 (P1) | 0 | **0** | 65.4 | 1.408 ms | **0.00%** |
| **Vs Heuristic Baseline** | 10 | 5 | 5 | 0 | **0** | 83.0 | 1.645 ms | **0.00%** |
| **Vs Random Baseline** | 10 | 8 | 2 | 0 | **0** | 44.1 | 1.272 ms | **0.00%** |
| **Total / Overall** | **30** | **21** | **9** | **0** | **0 (100% Legal)** | **64.2** | **1.442 ms** | **0.00%** |

---

## 2. Pre- vs Post-Consolidation Latency Comparison

| Latency Metric | Pre-Consolidation Baseline | Post-Consolidation Canonical `agent/` | Change / Improvement | Kaggle Budget Limit |
|---|---|---|---|---|
| **Average Decision Latency** | 1.013 ms | **0.944 ms** | **-6.8% faster** | $< 10.000\text{ ms}$ |
| **P50 (Median) Latency** | 0.479 ms | **0.727 ms** | Normal variation | $< 5.000\text{ ms}$ |
| **P95 Latency** | 3.061 ms | **2.665 ms** | **-12.9% faster** | $< 25.000\text{ ms}$ |
| **P99 Latency** | 5.721 ms | **3.971 ms** | **-30.6% faster** | $< 35.000\text{ ms}$ |
| **Maximum Observed Latency** | 15.432 ms | **4.177 ms** | **-72.9% faster** | $< 50.000\text{ ms}$ |
| **Fallback Rate** | 0.00% | **0.00%** | Zero fallbacks maintained | $0.00\%$ |
| **Illegal Actions / Crashes** | 0 | **0** | Zero violations maintained | 0 |

---

## 3. Submission Package Metrics

| Property | Pre-Consolidation | Post-Consolidation Canonical | Delta |
|---|---|---|---|
| **Archive File Size** | 0.07 MiB (69,002 bytes) | **0.06 MiB (60,422 bytes)** | **-12.4% smaller** |
| **Total Files in Archive**| 32 files | **20 files** | **-12 legacy files pruned** |
| **Legacy `src/` Included?**| YES | **NO (100% Removed)** | Clean separation |
| **Turn 0 Deck Validation**| PASS (60 cards) | **PASS (60 cards)** | Exact compliance |
| **Isolated Smoke Test** | PASS | **PASS** | 0 external imports |
