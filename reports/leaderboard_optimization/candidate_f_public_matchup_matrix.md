# Candidate F Live Kaggle Public Matchup Matrix & Performance Monitor

Generated at: 2026-08-16 08:28:00 UTC
Submission ID: `55547508` (PTCG NEXUS v3.4)
Current Live Public Rating: **`556.7`**
Current Rank: Approximately ~3450

---

## 1. Cumulative Public Match Statistics

| Metric | Candidate F Live Performance |
| :--- | :---: |
| **Current Live Score** | **`556.7`** |
| **Score Delta vs Previous Match** | **`-66.2`** (from 622.9) |
| **Score Delta vs Candidate D** | **`+128.6`** (from 428.1) |
| **Score Delta vs Candidate B** | **`-38.8`** (from 595.5) |
| **Total Public Matches** | **3** |
| **Record (W / L / D)** | **1 Win / 2 Losses / 0 Draws** |
| **Overall Public Win Rate** | **33.3%** |
| **EX Archetype Win Rate** | **100.0% (1 / 1)** |
| **Non-EX Archetype Win Rate** | **0.0% (0 / 2)** |
| **Metal-Resistance Win Rate** | **0.0% (0 / 1)** |
| **Fire-Weakness Win Rate** | **0.0% (0 / 1)** |
| **Aggro Win Rate** | **50.0% (1 / 2)** |
| **Control Win Rate** | **0.0% (0 / 1)** |
| **Average Game Length** | **75.0 Steps** |
| **AI Decision Errors** | **0** |
| **Illegal Actions** | **0** |
| **Fallback Rate** | **0.0%** |
| **Runtime Errors / Timeouts** | **0** |
| **Deck Limitation Losses** | **1** (Metal Resistance deficit) |
| **Hard Counter / Variance Losses**| **1** (Turn-1 Fire Weakness Donk) |

---

## 2. Complete Public Episode History

### Episode #1: `93569861` (Loss -1)
- **Opponent Archetype**: Pure Metal Basic Non-EX (Duraludon #169)
- **Game Length**: 75 Steps
- **Key Dynamic**: Duraludon had natural Grass Resistance (-30 damage), reducing Crustle's damage to 90 (surviving at 40 HP). Opponent won via bench exhaustion.
- **Classification**: `MATCHUP_HARD_COUNTER / RESISTANCE_LIMITATION`
- **AI Execution**: Flawless (0 errors, 2.3 ms average latency).

### Episode #2: `93570797` (Win +1)
- **Opponent Archetype**: Mega Lucario ex (#678) / Fighting Box (Solrock, Lunatone, Makuhita, Riolu)
- **Game Length**: 127 Steps
- **Key Dynamic**: Crustle's *Safeguard* ability completely negated 100% of damage from Mega Lucario ex (440 HP). Crustle took **0 damage** (150/150 HP), landed repeated 120-damage hits, knocked out Mega Lucario ex for 3 prizes at once (6 $\rightarrow$ 3), and cleanly swept the board on step 126.
- **Classification**: `TACTICAL DOMINANCE / SAFEGUARD LOCK`
- **AI Execution**: Flawless (0 errors, sub-10ms decision latency).

### Episode #3: `93571687` (Loss -1)
- **Opponent Archetype**: Stage 2 Fire Setup Aggro (Cinderace #666)
- **Game Length**: 23 Steps
- **Key Dynamic**: Opponent used Cinderace's *Explosiveness* setup ability to start directly in the Active spot with a 160 HP Stage 2 Fire attacker. Cinderace hit Grass Weakness (2x damage) on turn 1/2 for 160+ damage, knocking out lone active Dwebble (70 HP) before a second basic could be benched.
- **Classification**: `MATCHUP_HARD_COUNTER & OPENING_DRAW_VARIANCE (Fire Weakness Donk)`
- **AI Execution**: Flawless (0 errors, 1.2 ms decision latency).

---

## 3. Production Health & Protocol Status

- **Code Freeze**: **ENFORCED**. No code modifications permitted during live monitoring.
- **Rollback Safety**: `candidate-b-v3.2` (`submission_candidate_b.tar.gz`) remains protected and untouched.
- **Target**: Continue monitoring public ladder matches to collect at least 5–10 public games before considering any strategic deck adjustments.
