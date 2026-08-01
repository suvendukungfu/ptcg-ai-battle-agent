# 2,000 Randomized Adversarial Scenario Evaluation Report

Generated at: 2026-08-16 08:13:15 UTC
Dataset: 2,000 Distinct Legal Game Scenarios (Seeds 10000 – 11999)

---

## 1. Scenario Distribution & Adversarial Stress Tests

The 2,000-scenario suite tested the Top 2 candidates across randomized conditions:
1. **EX-Heavy Boards**: Multi-prize heavy hitters (Bellibolt EX, Raging Bolt ex, Starmie ex).
2. **Non-EX Swarms**: Single-prize high-damage attackers (Alakazam, Trevenant, Rillaboom).
3. **Control / Gust Boards**: Aggressive Boss's Orders disruption and energy denial.
4. **Endgame / Low Resource Scenarios**: Deck counts < 5, prize counts at 1–1 match point.
5. **Randomized Opening Hands**: Extreme variance (1 Basic + 6 Energy, 7 Trainers, mulligans).

---

## 2. Quantitative Results

| Candidate | Total Scenarios | Wins | Losses | Draws | Win Rate | 95% Confidence Interval | Invalid Actions | P50 Latency | P95 Latency | P99 Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Candidate D (Generalized Engine)** | **1,000** | **756** | **244** | **0** | **75.6%** | **[72.8% – 78.2%]** | **0** | **0.82 ms** | **9.58 ms** | **14.2 ms** |
| **F0 Crustle Baseline** | 1,000 | 684 | 316 | 0 | **68.4%** | [65.4% – 71.2%] | 0 | 0.80 ms | 8.10 ms | 12.8 ms |

---

## 3. Generalization & Overfitting Verification

- **Card ID Audit**: **Zero hardcoded card IDs** in the core decision engine (`agent/damage_model.py`, `agent/opponent_model.py`, `agent/evaluator.py`, `agent/policy.py`).
- **Opponent Independence**: The engine derives all combat metrics (HP, damage, stage, EX status, Safeguard, bench-scaling) dynamically from `data/EN Card Data.csv`.
- **Latency Stability**: Maximum P99 latency across all 2,000 scenarios is 14.2 ms, far below the 1,000 ms Kaggle timeout budget.
