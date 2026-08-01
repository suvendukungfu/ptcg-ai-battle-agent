# Candidate FINAL Live Optimization & Final Submission Report

Generated at: 2026-08-16 19:10:00 UTC
Competition Time Remaining: Final Hours

---

## 1. Candidate M Live Production Baseline

| Metric | Candidate M Live Value |
| :--- | :---: |
| **Submission Ref ID** | **`55554838`** |
| **Current Public Score** | **`641.5`** (Peak: `655.7`) |
| **Current Public Record** | **11 Wins / 11 Losses (50.00% WR)** across 22 public games |
| **EX Harvest Record** | 100% vs Garchomp ex (2-0), Ogerpon ex (2-0), Dragapult ex (1-0), Starmie ex (1-0), Mirrors (2-0) |

---

## 2. 20,000 Paired Seed-Matched Evaluation (M vs FINAL)

| Matchup Archetype | Candidate M (Live Baseline) | Candidate FINAL | Net Delta ($\Delta$) |
| :--- | :---: | :---: | :---: |
| **Grimmsnarl / Froslass** | **78.0%** | 77.9% | -0.2% |
| **Crustle Safeguard Mirror** | 48.9% | **50.2%** | **+1.3%** |
| **Mega Lucario ex Box** | 93.4% | **94.6%** | **+1.2%** |
| **Alakazam Swarm** | 81.6% | **82.9%** | **+1.3%** |
| **Trevenant / Brambleghast** | 47.6% | **49.3%** | **+1.7%** |
| **OVERALL (20,000 Games)** | **69.80%** (6,980 / 10,000) | **70.78%** (7,078 / 10,000) | **+0.98%** ($p = 0.12$) |

---

## 3. Package Checksums & Sandbox Verification

- `submission_candidate_final.tar.gz` (SHA256: `c1a4dd50720d3786c5db2496c810680e16299458ac67da81078ec206a566adf9`)
- `submission_candidate_m.tar.gz` (SHA256: `69edc45917c4240320a2bddffd86e9909e8d37b6f1bc1ca354700e0922d4c579`) [LIVE]
- Clean extraction in `/tmp/final_test` verified: CABT sandbox passed (`['DONE', 'DONE']`), 62/62 pytests passed.
- **Kaggle Submission Status: NOT SUBMITTED (Local Standby Only)**.

---

## 4. Final Strategic Evaluation

- Candidate FINAL achieved a **+0.98% paired delta** across 20,000 games.
- The 95% confidence intervals overlap (`[69.88% – 70.69%]`), yielding $p = 0.12$.
- Because the delta is below the strict +1.0% statistical threshold ($+0.98\%$) and Candidate M has already built a rating foundation of **641.5–655.7**, resetting the Bayesian rating to $\mu=600$ in the final hours carries significant downside risk.
- **FINAL RECOMMENDATION: KEEP CANDIDATE M LIVE**.
