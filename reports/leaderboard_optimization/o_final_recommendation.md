# Candidate O (PTCG NEXUS v3.7) Final Recommendation & Evaluation Report

Generated at: 2026-08-16 16:55:30 UTC
Branch: `candidate-o-froslass-auxiliary`

---

## 1. Candidate M Live Production Baseline

- **Current Live Public Score**: **`655.7`** (Peak rating across all submissions)
- **Current Rank**: **~2751**
- **Live Match Record**: **11 Wins / 10 Losses (52.38% Win Rate)** across 21 public episodes
- **Recent Momentum**: Won latest public match vs Teal Mask Ogerpon ex Box (Ep `93668816`)

---

## 2. 5,000 Paired Seed-Matched Benchmark (M vs O)

| Matchup Archetype | Candidate M (Live Baseline) | Candidate O (Froslass / Auxiliary Policy) | Net Delta ($\Delta$) |
| :--- | :---: | :---: | :---: |
| **Grimmsnarl / Froslass** | **75.9%** | 75.5% | -0.4% |
| **Crustle Safeguard Mirror** | **50.7%** | **50.7%** | 0.0% (Parity) |
| **Mega Lucario ex Box** | 93.6% | **94.0%** | **+0.4%** |
| **Alakazam Swarm** | **79.5%** | 77.6% | -1.9% |
| **Trevenant / Brambleghast** | 44.4% | **48.4%** | **+4.0%** |
| **OVERALL (5,000 Games)** | **70.52%** | **70.60%** | **+0.08%** ($p = 0.94$) |

---

## 3. Package & Verification

- `submission_candidate_o.tar.gz` (SHA256: `bb38415c74a2226a85491fa1a84d6678b79301b4d71160055badc8b5fcdfb91e`)
- Clean extraction in `/tmp/o_test` passed CABT sandbox (`['DONE', 'DONE']`) and all 62 unit tests (`62 passed in 2.01s`).
- **Kaggle Submission Status: NOT SUBMITTED (Local Standby Only)**.

---

## 4. Final Strategic Decision

**DECISION: KEEP CANDIDATE M LIVE**

- Candidate O produces a statistically negligible +0.08% delta ($p = 0.94$).
- Submitting Candidate O would reset the live rating ($\mu=600, \sigma=200$) right before the 8-hour competition deadline, destroying Candidate M's peak rating of **655.7**.
- Candidate M remains live to accumulate matches and let $\sigma$ uncertainty compress before close.
