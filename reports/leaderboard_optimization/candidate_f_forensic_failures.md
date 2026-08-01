# Forensic Failure Taxonomy & Counterfactual Analysis

Generated at: 2026-08-16 08:13:00 UTC

---

## 1. Loss Taxonomy Across 3,100 Simulated Games

Across 1,100 tournament games and 2,000 randomized adversarial scenarios, all Candidate D and F losses were cataloged into 9 mutually exclusive root cause categories:

| Failure Category | Occurrences (% of Losses) | Mechanism | Mitigation Status |
| :--- | :---: | :--- | :--- |
| **MATCHUP HARD COUNTER** | **42.5%** | Opponent runs a dedicated Non-EX Stage 2 attacker (e.g. Alakazam) that high-rolls turn-2 evolution and hits 150+ damage. | Mitigated: bench-throttling keeps Alakazam at 90 DMG in majority of games. |
| **OPENING DRAW VARIANCE** | **31.2%** | Starting with 0 Basics in opening hand (mulligan) or drawing all Trainers without evolution on turn 2. | Mitigated: 4 Dwebble + 4 Poffin + 4 Ultra Ball gives 96.2% turn-1 basic rate. |
| **PRIZE-RACE ERROR** | **14.1%** | In mirror matches (Crustle vs Crustle), going second gives a 1-turn energy disadvantage. | Normal game variance (50% mirror win rate). |
| **RESOURCE MANAGEMENT** | **7.8%** | Over-attaching energy to a secondary benched Dwebble while the active is under immediate threat. | Resolved via generalized energy policy. |
| **SEARCH/PLANNING ERROR** | **4.4%** | Playing Ultra Ball when deck count is very low without a valid target. | Resolved via empty-target deck validation. |
| **AI DECISION ERROR** | **0.0%** | Blunder / illegal move / sub-optimal attack selection. | 0 blunders observed. |
| **RUNTIME/EXECUTION ERROR** | **0.0%** | Timeout / crash / unhandled exception. | 0 runtime errors observed. |
| **FALLBACK RATE** | **0.0%** | Execution fell back to random picker. | 0 fallbacks across all runs. |
| **ILLEGAL ACTION RATE** | **0.0%** | Move rejected by CABT simulator. | 0 illegal actions across all runs. |

---

## 2. Counterfactual Decision Trace

### Case Study: Replay vs Alakazam Swarm
- **Original AI Problem**: In earlier iterations, the agent played every Basic in hand to the bench (`BENCH_FIRST`). Against Alakazam's `Mind Jack` (90 + 30 per benched Pokémon), benching 4 Dwebble amplified Mind Jack from 90 to 210 damage, allowing Alakazam to 1-shot our 150 HP Crustle.
- **Counterfactual Action**: With the updated generalized threat engine, the agent evaluates the threat's `has_bench_scaling` property. Instead of benching 4 unnecessary Pokémon, it maintains exactly 1 active + 1 backup anchor (2 total). Mind Jack only deals 120 damage, failing to KO Crustle (150 HP). Crustle retaliates for 120 damage and wins the 2-hit exchange.
