# Candidate F Failure Taxonomy & Loss Classification (10 Public Matches)

Generated at: 2026-08-16 08:59:00 UTC

---

## 1. Failure Taxonomy of 6 Public Losses

| Loss ID | Episode | Root Cause Classification | Detailed Mechanism | Replay Evidence |
| :---: | :---: | :--- | :--- | :--- |
| **L1** | `93569861` | **MATCHUP_HARD_COUNTER (Metal Resist)** | Duraludon (-30 Grass Resist) reduces Crustle DMG from 120 $\rightarrow$ 90 (leaving Duraludon at 40 HP). | Step 43: Duraludon survives with 40 HP. |
| **L2** | `93571687` | **MATCHUP_HARD_COUNTER (Fire Donk)** | Cinderace *Explosiveness* setup hits 2x Fire Weakness for 160+ DMG on lone basic Dwebble (70 HP). | Step 22: Turn-1 knockout before second basic could be benched. |
| **L3** | `93574392` | **MATCHUP_HARD_COUNTER (Metal Resist)** | Second Duraludon encounter; 2-hit trade deficit leads to bench exhaustion. | Step 80: Opponent trades 2 Duraludons for 2 Crustles. |
| **L4** | `93575313` | **SINGLE_PRIZE_TRADE_DEFICIT** | Grimmsnarl ex ran secondary single-prize attackers that traded prizes while keeping Grimmsnarl benched. | Step 140: Single-prize attackers traded evenly with Crustle. |
| **L5** | `93577146` | **SINGLE_PRIZE_TRADE_DEFICIT** | Cynthia's Gible/Gabite single-prize swarm overwhelmed Crustle with rapid 1-energy attacks. | Step 90: Multi-attacker swarm outpaced 2-energy attachments. |
| **L6** | `93578041` | **MIRROR_MATCH_VARIANCE** | Opponent ran Crustle Safeguard; going second gave a 1-turn energy attachment deficit. | Step 75: First-attacker advantage in mirror match. |

---

## 2. Quantitative Summary

- **Total Losses**: 6
- **AI Decision Errors**: **0 (0.0%)**
- **Type Resistance / Hard Counter Losses**: **3 (50.0%)**
- **Single-Prize Trade Deficit Losses**: **2 (33.3%)**
- **Mirror Match First-Attacker Variance**: **1 (16.7%)**
- **Illegal Actions / Fallbacks / Crashes**: **0 (0.0%)**
