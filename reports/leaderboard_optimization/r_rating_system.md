# Kaggle Simulation Rating System Mechanics (Glicko-2 / TrueSkill Analysis)

Generated at: 2026-08-16 10:36:00 UTC

---

## 1. Rating Engine Architecture

Kaggle Simulation competitions implement a **Bayesian Skill Rating Engine (Glicko-2 / TrueSkill variant)**:
- **Skill Estimate Parameters**:
  - $\mu$ (Mean Skill Estimate): Initial value = 600.0.
  - $\sigma$ (Rating Deviation / Uncertainty RD): Initial value = 100.0 – 200.0.
  - $\tau$ (Volatility): Controls expected variance over time.
- **Displayed Public Score**:
  - The public leaderboard displays a **Conservative Skill Estimate** $\mu - k\sigma$ (or mean score $\mu$ adjusted by provisional uncertainty).
  - In provisional phases (first 10–25 matches), $\sigma$ is high, causing the displayed score to swing by $\pm 30-50$ points per match.

---

## 2. Key Properties of the Rating Engine

1. **Uncertainty Decay with Game Volume**:
   - As an agent plays more matches (50–100+ episodes), $\sigma$ decreases monotonically.
   - When $\sigma$ shrinks, the conservative lower bound converges towards the true skill mean $\mu$, which lifts the displayed rating when the agent maintains a $>50\%$ win rate.
2. **Opponent Rating Weighting**:
   - Defeating a high-rated opponent (e.g. 1000+ rating) awards significantly more points ($+35$ to $+50$) than defeating an unranked/provisional bot ($+10$ to $+15$).
   - Losing to a lower-rated provisional bot penalizes the rating heavily in the early phase.
3. **Batch Reconciliation**:
   - Ratings are recalculated periodically in batches, leading to temporary intermediate snapshot dips before catching up with recent winning streaks.
