# Game Volume Impact & Provisional Uncertainty Decay

Generated at: 2026-08-16 10:39:00 UTC

---

## 1. Why Game Volume Dictates the Leaderboard Rating

In Bayesian skill estimation (Glicko-2 / TrueSkill):
1. **Conservative Skill Bound $\mu - 3\sigma$**:
   - At Game 10: $\mu \approx 850$, $\sigma \approx 120 \rightarrow \text{Score} = 850 - 360 = \mathbf{490}$.
   - At Game 50: $\mu \approx 950$, $\sigma \approx 50 \rightarrow \text{Score} = 950 - 150 = \mathbf{800}$.
   - At Game 100: $\mu \approx 1350$, $\sigma \approx 30 \rightarrow \text{Score} = 1350 - 90 = \mathbf{1260+}$.
2. **Submitting a New Candidate Resets Game Volume**:
   - Submitting a new bot (e.g. Candidate G, H, I, J, K, L) completely resets $\mu = 600$ and $\sigma = 200$.
   - Replacing an active submission after only 19 games destroys accumulated rating confidence and restarts the provisional climb from zero!

---

## 2. Recommendation

**Maintain Candidate F on the ladder without resubmission** to allow its $\sigma$ uncertainty to contract and let the 63.2%–77.8% win rate compound towards the ~1264 target rating.
