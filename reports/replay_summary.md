# Pokémon TCG Replay Analysis & Opponent Modeling Summary

## 1. Overall Performance Metrics
- **Total Episodes Analyzed**: 50
- **Overall Agent Win Rate**: **72.0%** (36 Wins / 14 Losses / 0 Draws)
- **Average Game Length**: **69.6 steps**
- **Total Decisions Evaluated**: 1941
- **Detected Strategic Mistakes**: 2

---

## 2. Meta Archetype Distribution & Matchup Win Rates

| Opponent Archetype | Games | Frequency | Wins | Losses | Win Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bellibolt_Lightning** | 49 | 98.0% | 35 | 14 | **71.4%** |
| **Lightning_Standard** | 1 | 2.0% | 1 | 0 | **100.0%** |

---

## 3. Common Opening Patterns & Sequences

### A. Common Winning Sequences
1. **Early Tadbulb (721) Setup**: Benching Tadbulb on Turn 1 and attaching Lightning Energy.
2. **Fast Evolution (Turn 2-3)**: Evolving into Bellibolt ex (723) with Heavy Baton (1163) or Electric Generator (1219) acceleration.
3. **Continuous Pressure**: Delivering 160-200 damage attacks per turn, knocking out opponent active Pokémon in 1-2 hits.
4. **Targeted Gust Finish**: Using Boss's Orders (1262) to drag a low-HP benched Pokémon for the game-winning final prize.

### B. Common Losing Sequences
1. **Energy Starvation**: Failing to draw/attach energy in the first 2 turns, leaving active Tadbulb vulnerable.
2. **Pre-Evolution Active Knockout**: Opponent landing an early KO on unevolved Tadbulb before Bellibolt ex hits the field.
3. **Bench Deficit**: Having 0 backup attackers on the bench when active Bellibolt ex is knocked out.

---

## 4. Frequent Agent Mistakes & Action Loss Correlations

- **Mistakes Identified**: 2 occurrences across 1941 decisions (0.10% error rate).
- **Primary Loss Driver**: Turns where energy attachment was deferred in favor of redundant benching.
- **Immunity Block Rate**: 0.00% (Crustle/ex-immunity handler successfully prevented invalid ex-attacks).

---

## 5. Top 5 Highest-Impact Improvements for Agent Upgrade

1. **Active Evolution Priority Maximization**: Prioritize search items (Ultra Ball 1121, Nest Ball 1227) strictly toward completing Bellibolt ex (723) evolution on Turn 2.
2. **Bench Redundancy Maintenance**: Ensure at least one backup Tadbulb is benched and receiving energy before over-committing excess energy to an already-powered active attacker.
3. **Aggressive Gusting (Boss's Orders 1262)**: Trigger Boss's Orders immediately whenever the opponent benches an energy-heavy or low-HP ex target to secure multi-prize KOs.
4. **Energy Acceleration Timing (Electric Generator 1219)**: Fire Electric Generator before normal energy attachment to maximize turn attachment efficiency.
5. **Retreat Preservation Logic**: Enable strategic retreats when active HP is <40 to deny opponent prize cards and pivot to a healthy Bellibolt ex.
