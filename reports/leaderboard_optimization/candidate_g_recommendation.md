# Candidate G8 vs Candidate F: Paired Statistical Audit & Kaggle Decision

Generated at: 2026-08-16 08:45:00 UTC
Benchmark Scale: 2,500 Seed-Matched Games (250 Identical Seeds $\times$ 5 Core Archetypes $\times$ 2 Candidates)

---

## 1. Paired Seed-Matched Statistical Evaluation

| Matchup Archetype | Candidate F (G0 Baseline) | Candidate G8 (Anti-Weakness / Potion) | Net Delta ($\Delta$) | Seed-by-Seed Differentials |
| :--- | :---: | :---: | :---: | :--- |
| **Vs Mega Lucario ex (EX Aggro)** | **94.0%** (235/250) | 91.2% (228/250) | **-2.8%** (Regression) | F won 20 seeds, G8 won 13 seeds, 217 identical |
| **Vs Alakazam Non-EX (Stage 2 Swarm)** | **81.6%** (204/250) | 75.2% (188/250) | **-6.4%** (Regression) | F won 53 seeds, G8 won 37 seeds, 160 identical |
| **Vs Duraludon Non-EX (Metal Resist)** | 74.0% (185/250) | **83.6%** (209/250) | **+9.6%** (Improvement) | G8 won 49 seeds, F won 25 seeds, 176 identical |
| **Vs Hop's Trevenant (Non-EX Single)** | 81.2% (203/250) | **88.8%** (222/250) | **+7.6%** (Improvement) | G8 won 43 seeds, F won 24 seeds, 183 identical |
| **Vs Cinderace Non-EX (Turn-1 Donk)** | 51.2% (128/250) | 50.8% (127/250) | **-0.4%** (Parity) | G8 won 56 seeds, F won 57 seeds, 137 identical |
| **OVERALL (2,500 Games)** | **76.40%** | **77.92%** | **+1.52%** | **95% Confidence Intervals Substantially Overlap** |

---

## 2. 95% Confidence Intervals & Statistical Significance

- **Candidate F 95% CI**: `[73.97% – 78.67%]`
- **Candidate G8 95% CI**: `[75.54% – 80.13%]`
- **Confidence Interval Overlap**: **TRUE (Overlapping interval: [75.54% – 78.67%])**
- **Statistical Significance**: **NOT SIGNIFICANT ($p = 0.38$)**.

---

## 3. Kaggle Decision Standard: Risk Assessment

### Risk Classification: **MEDIUM RISK**
1. **Improvement is small (+1.52%)** and fails to achieve statistical significance.
2. **Trade-Off Imbalance**:
   - G8 improves survival against Duraludon (+9.6%) and Trevenant (+7.6%) by healing chip damage.
   - However, drawing Super Potion instead of Basic Grass Energy in early turns slightly delays Turn-2 attacking against fast setup decks, causing a **-2.8% regression against Mega Lucario ex** and a **-6.4% regression against Alakazam Swarms**.
3. **Cinderace Invariant**: Super Potion cannot prevent a Turn-1 Fire Weakness Donk because potions cannot be played before taking lethal damage on Turn 1/2.

---

## 4. Archive Verification & Standby Status

- `submission_candidate_b.tar.gz`: `a1a956115ca9a06af63f3df2ea0fc1f64d6508d4f004a8b220c6ab307672a678` (Protected Baseline)
- `submission_candidate_d.tar.gz`: `5d8901307eae5b7896c665044a540c65b4738d1899ac062c4bd86a7882cceefb` (Protected Archive)
- `submission_candidate_f.tar.gz`: `81dba2fc4c27552c099b603e05ea987585c037b693c9f68022aff52c82b6ce73` (**Live Active Kaggle Candidate**)
- `submission_candidate_g8.tar.gz`: `07b7fe749c69562a670b36fd83dcd7992a4b303a067ec69c1b3c2457913e1cef` (**LOCAL STANDBY ONLY — NOT FOR SUBMISSION**)

---

## 5. Final Strategic Recommendation

**HONEST RECOMMENDATION: KEEP CANDIDATE F LIVE — DO NOT SUBMIT G8**

- The evidence does NOT establish that G8 has a higher expected Kaggle leaderboard rating than Candidate F.
- Candidate F has demonstrated peak live performance (622.9 rating, Rank ~3265) and 100% EX suppression.
- We will continue monitoring Candidate F's live trajectory.

---

> [!IMPORTANT]
> **ABSOLUTE HARD STOP ENFORCED**: `kaggle competitions submit` was NOT run. `submission_candidate_g8.tar.gz` remains local-only. Candidate F remains untouched and live on the leaderboard.
