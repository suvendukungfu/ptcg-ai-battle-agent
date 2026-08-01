# 10,000-Scenario Adversarial Evaluation for Candidate I

Generated at: 2026-08-16 09:50:30 UTC

---

## 1. 10,000 Scenario Quantitative Comparison

| Candidate | Scenarios | Wins | Losses | Win Rate | Invalids | Fallbacks | P95 Latency | P99 Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Candidate F (I0 Live)** | **5,000** | **3,859** | 1,141 | **77.18%** | **0** | **0** | **6.58 ms** | **10.88 ms** |
| **Candidate I3 (Tech)** | **5,000** | 3,764 | 1,236 | **75.28%** | **0** | **0** | **6.27 ms** | **10.63 ms** |

---

## 2. Quantitative Finding

- Across 10,000 randomized scenarios, **Candidate F (I0) achieves a +1.90% higher win rate** than any tech-diluted variant.
- Candidate F maintains 100% execution safety: 0 illegal moves, 0 fallbacks, 0 runtime errors, and sub-11ms P99 latency.
