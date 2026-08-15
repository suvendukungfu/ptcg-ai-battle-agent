# PTCG AI Battle Challenge — Comprehensive Deck Candidate Tournament Report

**Date**: August 16, 2026  
**Total Games Simulated**: 200 matches across 5 distinct candidates $\times$ 4 benchmark opponents.  
**Engine**: Official Kaggle CABT environment with alternating seat assignments.

---

## 1. Empirical Leaderboard & Win Rates

| Rank | Candidate | Core Strategy | Random (10g) | Heuristic (10g) | Crustle Wall (10g) | Alakazam (10g) | Overall Win Rate (40g) | 95% Wilson CI | P95 Latency |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Candidate D (Crustle Control)** | Safeguard Immunity Wall | **100.0%** (10/10) | **100.0%** (10/10) | **60.0%** (6/10) | **90.0%** (9/10) | **87.5% (35/40)** | **[73.9%, 94.5%]** | **2.99ms** |
| **#2** | **Candidate B (Bellibolt 4-3-3)** | Balanced Evolution/Energy | 80.0% (8/10) | 10.0% (1/10) | 30.0% (3/10) | 80.0% (8/10) | **50.0% (20/40)** | [35.2%, 64.8%] | 5.79ms |
| **#3** | **Candidate A (Bellibolt 4-4-4)** | Baseline ex Heavy Beatdown | 90.0% (9/10) | 10.0% (1/10) | 0.0% (0/10) | 70.0% (7/10) | **42.5% (17/40)** | [28.5%, 57.8%] | 4.56ms |
| **#4** | **Candidate C (Anti-Crustle Tech)** | Hybrid non-ex + ex | 60.0% (6/10) | 20.0% (2/10) | 10.0% (1/10) | 40.0% (4/10) | **32.5% (13/40)** | [20.1%, 48.0%] | 4.94ms |
| **#5** | **Candidate E (Alakazam Spread)** | Stage 2 Psychic Spread | 50.0% (5/10) | 0.0% (0/10) | 30.0% (3/10) | 50.0% (5/10) | **32.5% (13/40)** | [20.1%, 48.0%] | 3.83ms |

---

## 2. Deep Matchup Insights

1. **Crustle Safeguard (`Candidate D`) is the Dominant Standout**:
   - Out of 40 games, Candidate D won **35 games (87.5%)**.
   - Achieved a **100% win rate against both Random Bot and Bellibolt Heuristic**.
   - Safeguard (*Mysterious Rock Inn*) makes Crustle completely immune to all attacks from Pokémon ex (Bellibolt ex, Kangaskhan ex, Sinistcha ex), which dominate competitive meta submissions.
2. **Bellibolt ex vs Crustle is an Auto-Loss without Non-ex Attackers**:
   - Candidate A had a **0.0% win rate (0/10)** vs Crustle Wall.
   - Bellibolt ex deals $0$ damage to Crustle due to Safeguard, resulting in a slow prize defeat.
3. **Bellibolt Mirror Weakness Identified**:
   - When playing the Bellibolt deck, our agent won only 10% against Heuristic Bellibolt because Heuristic attacks aggressively every turn without spending actions on non-essential item setup.
   - This points directly to an **Action Priority Ordering** issue in `agent/action_selector.py` that we will analyze and solve in Phase 10 & 11!
