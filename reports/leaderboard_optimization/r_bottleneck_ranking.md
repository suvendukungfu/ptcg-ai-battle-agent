# Leaderboard Bottleneck Ranking (H1 to H10)

Generated at: 2026-08-16 10:39:30 UTC

---

## 1. Bottleneck Evaluation Matrix

| Hypothesis | Factor | Evidence from Forensic Study | Importance | Confidence | Rank |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **H5** | **Game Volume / Episode Count** | 19 games is still in the provisional $\sigma$ uncertainty phase; 50–100 games needed for convergence. | **CRITICAL** | **VERY HIGH** | **#1** |
| **H3** | **Rating Uncertainty ($\sigma$) Decay** | Conservative lower bound suppresses score early; contracts with volume. | **CRITICAL** | **VERY HIGH** | **#2** |
| **H10** | **Batch Rating Update Timing** | Asynchronous Glicko-2 updates create temporary snapshot dips before catching up. | **HIGH** | **HIGH** | **#3** |
| **H7** | **Hidden Live Meta (Mirrors)** | 55.6% of recent matches are Crustle Mirrors (Candidate F wins 80% of them). | **HIGH** | **VERY HIGH** | **#4** |
| **H1** | **Bot Win Rate** | Candidate F already achieves 63.2%–77.8% live win rate; 100% vs EX. | **OPTIMAL** | **RESOLVED** | **#5** |
| **H8** | **Local Simulator Mismatch** | Local benchmark tests flat 10-meta vs live ladder's 55.6% mirror concentration. | **MODERATE** | **RESOLVED** | **#6** |
