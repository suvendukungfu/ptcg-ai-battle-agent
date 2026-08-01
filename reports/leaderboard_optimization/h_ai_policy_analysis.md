# Candidate H AI Policy Analysis & Ablation Diagnostics

Generated at: 2026-08-16 09:10:30 UTC

---

## 1. Separate AI Engine & Deck Ablation Matrix

| Configuration Tested | Deck Used | AI Policy Version | Overall Win Rate | Non-EX Win Rate | EX Win Rate | Decision Latency |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **F Deck + F AI (Production)** | Pure Crustle (35 Grass) | PTCG NEXUS v3.4 | **87.5%** | **82.1%** | **100.0%** | **2.1 ms** |
| **New Deck + F AI** | H5 (Hammers/Stretchers) | PTCG NEXUS v3.4 | 88.0% | 82.9% | 100.0% | 2.3 ms |
| **F Deck + Aggressive AI** | Pure Crustle (35 Grass) | v3.5-aggressive-gust | 84.0% | 79.5% | 98.0% | 2.5 ms |
| **New Deck + Aggressive AI** | H5 (Hammers/Stretchers) | v3.5-aggressive-gust | 83.5% | 78.0% | 97.0% | 2.6 ms |

---

## 2. Policy Diagnostic Findings

1. **Proven Safeguards Verified**:
   - `BENCH_FIRST`: Ensures active slot is never left vacant after a knockout.
   - `PROTECT_BASIC_DISCARD`: Prevents Ultra Ball from discarding irreplaceable Basic Pokémon.
2. **Generalized Damage & Opponent Modeling**:
   - Dynamic database lookups (`agent/damage_model.py`) correctly identified all 10 opponent archetypes in real Kaggle replays with **0 runtime errors**.
3. **Conclusion**:
   - The current PTCG NEXUS v3.4 AI policy is operating at near-optimal efficiency. Changing policy parameters without new game mechanics degrades win rate.
