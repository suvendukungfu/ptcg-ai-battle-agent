# Candidate M Submission Decision & 20,000-Game Scorecard

Generated at: 2026-08-16 11:06:00 UTC
Branch: `candidate-m-live-meta-breakthrough`

---

## 1. Candidate F Live Kaggle State

- **Current Known Rating**: **`492.2`** (Snapshot taken during Glicko-2 reconciliation)
- **Peak Public Rating**: **`622.9`**
- **Live Public Record**: **12 Wins / 7 Losses (63.16% Cumulative WR)**
- **Recent Live WR (Games 11–19)**: **77.78% (7W / 2L)**

---

## 2. 20,000 Paired Seed-Matched Benchmark

| Metric | Candidate F (Live Production) | Candidate M (Live-Meta Breakthrough) | Net Delta ($\Delta$) | Statistical Significance |
| :--- | :---: | :---: | :---: | :--- |
| **Overall Paired Win Rate** | **68.25%** (6,825 / 10,000) | **67.90%** (6,790 / 10,000) | **-0.35%** | Indistinguishable ($p=0.60$) |
| **95% Confidence Interval** | `[67.33% – 69.16%]` | `[66.98% – 68.81%]` | Overlap: `[67.33% – 68.81%]` | Statistically Overlapping |
| **Crustle Safeguard Mirror WR** | **51.1%** | 49.8% | -1.3% | F Advantage |
| **Mega Lucario ex (EX Aggro) WR**| **94.1%** | 93.4% | -0.7% | Parity |
| **Duraludon (Metal Resist) WR** | 76.2% | **78.5%** | **+2.3%** | M Advantage |
| **Alakazam (Psychic Swarm) WR** | 81.5% | **81.9%** | **+0.4%** | Parity |
| **Cinderace (Fire Donk) WR** | **48.8%** | 47.8% | -1.0% | Parity |
| **Opening Consistency** | **96.2%** | **96.2%** | 0.0% | Exact Pure Deck Preserved |
| **Energy Consistency** | **96.2%** | **96.2%** | 0.0% | Pure 35 Grass Energy |
| **Illegal Actions** | **0** | **0** | 0 | Flawless |
| **Fallback Actions** | **0** | **0** | 0 | Flawless |
| **Runtime Errors** | **0** | **0** | 0 | Flawless |

---

## 3. Expected Leaderboard Value & Risk Assessment

- **Expected Benefit**: None. Candidate M improves Duraludon by +2.3%, but regresses by -1.3% in the dominant mirror matchup (which constitutes >55% of the live ladder).
- **Expected Risk**: High. Submitting Candidate M would reset rating confidence ($\mu=600, \sigma=200$) without providing a statistical advantage over Candidate F.

---

## 4. Final Classification & Recommendation

**CLASSIFICATION: B) PROMISING BUT NOT PROVEN**

**DECISION: KEEP CANDIDATE F LIVE (DO NOT SUBMIT)**

- Candidate F remains live on the Kaggle leaderboard (Submission `55547508`).
- `submission_candidate_m.tar.gz` (SHA256: `cf09c327dd6c183a0a9f86da2bff75b2df2d468e62ac206760d5612af75caf7c`) is verified and archived on local standby.

---

> [!IMPORTANT]
> **ABSOLUTE HARD STOP ENFORCED**: `kaggle competitions submit` was NOT executed. Candidate F remains live on the leaderboard.
