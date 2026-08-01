# Candidate F Full Tournament Results & Forensic Analysis

Generated at: 2026-08-16 08:12:00 UTC
Competition: `pokemon-tcg-ai-battle`
Benchmark Scale: 1,100 Deep Tournament Games + 2,000 Randomized Adversarial Scenarios

---

## 1. Executive Summary & Matchup Matrix

The comprehensive 1,100-game tournament evaluated 11 candidate architectures against the 5 primary adversarial archetypes in CABT (Alakazam Non-EX Swarm, Bellibolt EX Aggro, Crustle Safeguard Wall, Heavy Gust Disruption, and Meta Breaker Aggro).

| Candidate Architecture | Alakazam (Non-EX) | Bellibolt (EX) | Crustle (Safeguard) | Heavy Gust Control | Meta Breaker Aggro | Overall Win Rate | 95% Confidence Interval | Invalids / Errors |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Candidate D (Generalized Engine)** | **80.0%** | **85.0%** | **50.0%** | **65.0%** | **100.0%** | **76.0%** | **[66.8% – 83.3%]** | **0** |
| **F0 Crustle Baseline** | 75.0% | 85.0% | 30.0% | 55.0% | 100.0% | **69.0%** | [59.3% – 77.2%] | 0 |
| **F1 Crustle Fast Tech (Shaymin)** | 55.0% | 90.0% | 30.0% | 45.0% | 100.0% | **64.0%** | [54.2% – 72.7%] | 0 |
| **F3 Crustle Heavy Gust** | 55.0% | 75.0% | 20.0% | 50.0% | 100.0% | **60.0%** | [50.2% – 69.0%] | 0 |
| **F2 Crustle + Rillaboom** | 50.0% | 70.0% | 40.0% | 25.0% | 100.0% | **57.0%** | [47.2% – 66.3%] | 0 |
| **F4 Alakazam Swarm** | 50.0% | 50.0% | 25.0% | 35.0% | 70.0% | **46.0%** | [36.6% – 55.6%] | 0 |
| **Candidate B (Protected Baseline)** | 75.0% | 50.0% | 5.0% | 15.0% | 70.0% | **43.0%** | [33.7% – 52.8%] | 0 |
| **Candidate E (Alakazam Base)** | 45.0% | 25.0% | 15.0% | 30.0% | 95.0% | **42.0%** | [32.8% – 51.8%] | 0 |
| **F6 Balanced Hybrid (Bellibolt/Crustle)**| 35.0% | 45.0% | 15.0% | 20.0% | 85.0% | **40.0%** | [30.9% – 49.8%] | 0 |
| **F5 Bellibolt Pure** | 10.0% | 30.0% | 0.0% | 0.0% | 50.0% | **18.0%** | [11.7% – 26.7%] | 0 |
| **F7 Meta Breaker Gust (Bellibolt)** | 20.0% | 10.0% | 0.0% | 0.0% | 40.0% | **14.0%** | [8.6% – 22.0%] | 0 |

---

## 2. Statistical Metrics & Latency Performance

- **Safety Compliance**: **0 Illegal Actions**, **0 Fallbacks**, **0 Runtime Errors** across all 3,100 simulated games.
- **Latency**:
  - P50 Decision Latency: **0.82 ms**
  - P95 Decision Latency: **5.14 ms**
  - P99 Decision Latency: **9.58 ms**
  - Max Allowed: 1,000.0 ms (Operates well within Kaggle safety limits: < 1.0% of timeout threshold).

---

## 3. Forensic Analysis by Archetype

### A. Non-EX Matchup Performance (Alakazam Swarm)
- **Candidate D** achieved **80.0% Win Rate** vs Alakazam Non-EX.
- Root Cause of Superiority: Candidate D's generalized damage model correctly calculates that benched Pokémon increase Mind Jack's conditional damage. Under the updated policy, the agent minimizes unnecessary benching against bench-scaling threats, restricting Alakazam to its base 90 damage (which requires 2 turns to KO Crustle's 150 HP), while Crustle 2-hit KOs Alakazam with 100% opening consistency.

### B. EX Matchup Performance (Bellibolt EX)
- **Candidate D** achieved **85.0% Win Rate** vs Bellibolt EX.
- Crustle's `Safeguard` ability completely shuts down Bellibolt EX (0 damage). Even when Bellibolt runs Non-EX attackers, they require 3 energy attachments (3 turns) versus Crustle's 2 energy attachments, winning the prize race decisively.

### C. Control & Gust Matchup Performance
- Against Heavy Gust Control, Candidate D maintained a **65.0% Win Rate**, utilizing `BENCH_FIRST` safety and prompt backup charging.
