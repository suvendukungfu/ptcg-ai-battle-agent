# Candidate N (PTCG NEXUS v3.6) Live Experiment & Submission Readiness Report

Generated at: 2026-08-16 16:32:00 UTC
Branch: `candidate-n-live-experiment`

---

## 1. Candidate M Live Production State

| Metric | Candidate M Live Value | Role |
| :--- | :---: | :--- |
| **Submission Ref ID** | **`55554838`** | Active Kaggle Simulation Agent |
| **Current Public Score** | **`655.7`** | **Peak Leaderboard Score** |
| **Current Rank** | **~2751** | Top 40% of Ladder |
| **Public Record** | **11 Wins / 10 Losses (52.38% WR)** | 21 Public Episodes |
| **EX Win Rate** | **58.8%** (100% vs Garchomp, Ogerpon, Dragapult, Starmie) | Dominant Tier-1 EX Harvesting |

---

## 2. 20,000 Paired Seed-Matched Benchmark (M vs N)

| Metric | Candidate M (Live Baseline) | Candidate N (Froslass / Swarm Policy) | Net Delta ($\Delta$) | Statistical Significance |
| :--- | :---: | :---: | :---: | :--- |
| **Overall Paired Win Rate** | **70.23%** (7,023 / 10,000) | **70.38%** (7,038 / 10,000) | **+0.15%** | Indistinguishable ($p=0.81$) |
| **95% Confidence Interval** | `[69.33% – 71.12%]` | `[69.48% – 71.27%]` | Overlap: `[69.48% – 71.12%]` | Statistically Overlapping |
| **Grimmsnarl / Froslass WR** | 76.9% | **77.4%** | **+0.5%** | Minor edge |
| **Crustle Safeguard Mirror WR**| 49.2% | **49.3%** | **+0.1%** | Parity |
| **Mega Lucario ex WR** | **94.3%** | 94.2% | -0.1% | Undefeated |
| **Alakazam Swarm WR** | **82.5%** | 82.2% | -0.3% | Parity |
| **Trevenant / Bramble WR** | 49.8% | **50.3%** | **+0.5%** | Parity |
| **Opening Consistency** | **96.2%** | **96.2%** | 0.0% | Exact Pure Deck Preserved |
| **Energy Consistency** | **96.2%** | **96.2%** | 0.0% | Pure 35 Grass Energy |
| **Illegal Actions** | **0** | **0** | 0 | Flawless |
| **Fallback Actions** | **0** | **0** | 0 | Flawless |
| **Runtime Errors** | **0** | **0** | 0 | Flawless |
| **P95 Latency** | **6.50 ms** | **6.48 ms** | -0.02 ms | Well below 1000ms limit |
| **P99 Latency** | **10.80 ms** | **10.75 ms** | -0.05 ms | Strict safety |

---

## 3. Package & Verification

- `submission_candidate_n.tar.gz` (SHA256: `32b588164fee4c7ed1195efc154ec8e83e0e4cf72a5ef8c3d340322675889984`)
- Clean extraction in `/tmp/n_test` passed CABT sandbox (`['DONE', 'DONE']`) and all 62 unit tests (`62 passed in 2.36s`).
- **Kaggle Submission Status: NOT SUBMITTED (Local Standby Only)**.

---

## 4. Final Recommendation

**RECOMMENDATION: KEEP M (OR TEST N ON KAGGLE AS EXPERIMENT)**

- Candidate M is actively performing on Kaggle at **655.7** (peak across all submissions).
- Candidate N has identical safety and structure, with a +0.15% local paired delta.
- If testing a new submission slot today, Candidate N is 100% verified and ready. Otherwise, Candidate M can continue playing.
