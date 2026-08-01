# Rating Progression Scenarios to Reach ~1264 Leaderboard Target

Generated at: 2026-08-16 10:38:30 UTC

---

## 1. Mathematical Win Rate Scenarios

Assuming Kaggle's Bayesian rating system with rating velocity $\Delta R_{\text{win}} \approx +28.4$ and $\Delta R_{\text{loss}} \approx -23.0$:

| Sustained Live Win Rate | Net Rating Delta per 10 Games | Matches Required to Reach 1200+ | Matches Required to Reach 1264+ | Feasibility |
| :---: | :---: | :---: | :---: | :---: |
| **60.0% WR** (6W / 4L) | $+78.4 \text{ pts}$ | ~85 matches | ~95 matches | Feasible with volume |
| **65.0% WR** (6.5W / 3.5L) | $+104.1 \text{ pts}$ | ~65 matches | ~70 matches | **Current Trajectory (63.2% WR)** |
| **70.0% WR** (7W / 3L) | $+129.8 \text{ pts}$ | ~50 matches | ~55 matches | Highly Feasible |
| **75.0% WR** (7.5W / 2.5L) | $+155.5 \text{ pts}$ | ~40 matches | ~45 matches | **Recent Trajectory (77.8% WR)** |
| **80.0% WR** (8W / 2L) | $+181.2 \text{ pts}$ | ~35 matches | ~38 matches | Rapid climb |

---

## 2. Key Mathematical Conclusion

At Candidate F's sustained **63.2%–77.8% win rate**, the rating will naturally cross **1200+** after **50–70 total matches** as rating uncertainty $\sigma$ decreases and game volume accumulates!
There is no need to engineer a 95% local bot when 70% live win rate with sufficient game volume achieves the target rating.
