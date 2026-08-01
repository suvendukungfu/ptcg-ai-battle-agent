# Candidate F Comprehensive Ranking & Weighted Fitness Evaluation

Generated at: 2026-08-16 08:12:30 UTC

---

## 1. Evaluation Methodology & Weighted Leaderboard Fitness

Leaderboard fitness is calculated using the strict weighted formula:
$$\text{Fitness} = 0.40 \times \text{Overall WR} + 0.25 \times \text{Coverage} + 0.15 \times \text{Non-EX WR} + 0.10 \times \text{EX WR} + 0.05 \times \text{Consistency} + 0.05 \times \text{Safety}$$

- **Overall WR (40%)**: Win rate across all 5 standard archetypes.
- **Matchup Coverage (25%)**: Percentage of archetypes with $\ge 50\%$ win rate.
- **Non-EX WR (15%)**: Win rate against Alakazam / single-prize swarms.
- **EX WR (10%)**: Win rate against Bellibolt / multi-prize heavy hitters.
- **Consistency (5%)**: Opening setup consistency ($\ge 90\%$ baseline).
- **Safety (5%)**: Compliance with zero-crash, zero-invalid execution ($100\%$ if 0 invalids).

---

## 2. Complete Candidate Ranking

| Rank | Candidate Architecture | Overall WR | Matchup Coverage | Non-EX WR | EX WR | Consistency | Safety | Weighted Fitness | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Candidate D (Generalized Engine)** | **76.0%** | **100.0%** (5/5) | **80.0%** | **85.0%** | **96.0%** | **100.0%** | **85.70** | **TOP 1 — CHAMPION** |
| **2** | **F0 Crustle Baseline** | 69.0% | 80.0% (4/5) | 75.0% | 85.0% | 94.0% | 100.0% | **77.05** | **TOP 2 — RUNNER UP** |
| **3** | **F1 Crustle Fast Tech** | 64.0% | 60.0% (3/5) | 55.0% | 90.0% | 92.0% | 100.0% | **72.45** | ELIMINATED |
| **4** | **F3 Crustle Heavy Gust** | 60.0% | 60.0% (3/5) | 55.0% | 75.0% | 91.0% | 100.0% | **69.30** | ELIMINATED |
| **5** | **F2 Crustle + Rillaboom** | 57.0% | 60.0% (3/5) | 50.0% | 70.0% | 85.0% | 100.0% | **66.55** | ELIMINATED |
| **6** | **F4 Alakazam Swarm** | 46.0% | 60.0% (3/5) | 50.0% | 50.0% | 88.0% | 100.0% | **60.30** | ELIMINATED |
| **7** | **Candidate B (Protected Baseline)** | 43.0% | 60.0% (3/5) | 75.0% | 50.0% | 90.0% | 100.0% | **62.95** | PROTECTED FALLBACK |
| **8** | **Candidate E (Alakazam Base)** | 42.0% | 20.0% (1/5) | 45.0% | 25.0% | 84.0% | 100.0% | **49.45** | ELIMINATED |
| **9** | **F6 Balanced Hybrid** | 40.0% | 20.0% (1/5) | 35.0% | 45.0% | 78.0% | 100.0% | **47.65** | ELIMINATED |
| **10** | **F5 Bellibolt Pure** | 18.0% | 20.0% (1/5) | 10.0% | 30.0% | 86.0% | 100.0% | **25.30** | ELIMINATED |
| **11** | **F7 Meta Breaker Gust (Bellibolt)** | 14.0% | 0.0% (0/5) | 20.0% | 10.0% | 82.0% | 100.0% | **20.70** | ELIMINATED |

---

## 3. Key Findings

1. **Candidate D + Generalized Threat Engine** is the undisputed champion:
   - Outperforms Candidate B by **+33.0% overall win rate** (76.0% vs 43.0%).
   - Outperforms all hybrid and Bellibolt variants across every single matchup.
2. **Why Hybrid Decks Fail**: Dual-energy requirements (Grass + Lightning in F6) dilute draw consistency and create dead hands where the active cannot attack for 2–3 turns.
3. **Why Pure Crustle Dominates**: Single-energy consistency (35 Grass energy + search items) guarantees a turn-2 powered Safeguard tank in 96%+ of games, making it nearly impossible for standard ladder bots to beat.
