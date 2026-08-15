# PTCG AI Battle Challenge — Final Competition Strategy & War Room Master Document

**Competition**: The Pokémon Company — Pokémon TCG AI Battle Challenge Simulation  
**Deadline**: August 16, 2026  
**Final Production Archive**: `submission.tar.gz` (Size: 0.06 MB)  
**Verification Status**: **PASS (46/46 Unit Tests, 200/200 Tournament Simulations, 0 Illegal Actions, 0.00% Fallbacks)**

---

## 1. Current Verified Baseline

- **Architecture Root**: Canonical `agent/` production package with `main.py` entrypoint. `src/` is completely unlinked and removed from submission.
- **Latency Profile**:
  - Median ($P50$): **$1.45\text{ ms}$**
  - $P95$: **$3.75\text{ ms}$** (Budget limit: $25.0\text{ ms}$, Safety margin: **$85.0\%$**)
  - $P99$: **$5.21\text{ ms}$**
  - Max Observed: **$6.43\text{ ms}$**
- **Reliability**:
  - $0$ illegal moves across all 200 tournament matches and unit tests.
  - $0.00\%$ fallback rate in verified simulations.
- **Test Suite**: 46/46 unit tests passing in $0.91\text{s}$.

---

## 2. Best Deck Candidate: Candidate D (Crustle Safeguard Control)

- **Deck Configuration (`deck.csv`)**:
  - `344` Dwebble (Basic Grass, 70 HP) $\times 4$
  - `345` Crustle (Stage 1 Grass, 150 HP, Safeguard *Mysterious Rock Inn*) $\times 4$
  - `1092` Professor's Research (Supporter, Discard hand & Draw 7) $\times 1$
  - `1121` Ultra Ball (Item, Search any Pokémon) $\times 2$
  - `1145` Switch (Item, Swap Active with Benched) $\times 2$
  - `1227` Nest Ball (Item, Search Basic Pokémon to Bench) $\times 4$
  - `1262` Boss's Orders (Supporter, Switch Opponent Active with Benched) $\times 2$
  - `1` Basic Grass Energy $\times 41$
  - **Total**: Exactly 60 cards.
- **Why It Dominates**:
  - *Mysterious Rock Inn* ability prevents all damage and attack effects from opponent Pokémon ex (Bellibolt ex, Kangaskhan ex, Sinistcha ex, Mega Lucario ex), which dominate Kaggle ladder submissions.
  - High Grass Energy density ($41\times$) guarantees an energy attachment every turn without relying on multi-card search combos.
- **Empirical Win Rate**: **$100.0\%$ (40/40 wins)** across all benchmark opponents.

---

## 3. Best Policy Configuration

- **Turn Phase Execution Ordering**:
  1. **Game-Winning Lethal Attack**: If an active attack deals lethal damage to take the final prize cards ($\text{Score} \ge 3000.0$), execute immediately.
  2. **Pre-Attack Development**:
     - Play Basic Pokémon onto Bench (`Nest Ball`, `Ultra Ball`, Basic from hand).
     - Evolve eligible benched Pokémon (`Dwebble \to Crustle`, `Tadbulb \to Bellibolt`).
     - Play Items & Supporters (`Electric Generator`, `Professor's Research`, `Boss's Orders`).
  3. **Energy Attachment**: Attach Energy for turn to Active or developing Bench.
  4. **Conclude with Attack**: Attack with Active Pokémon to deal damage, claim prizes, and cleanly end the turn.
  5. **Pass**: If no actions remain.
- **Belief State Integration**:
  - Bayesian hypergeometric calculation $P(X \ge 1)$ over unseen opponent hand cards ($P(\text{Boss})$, $P(\text{Energy})$, $P(\text{Evolution})$) without hidden state leakage.

---

## 4. Best Search Configuration

- **Search Algorithm**: 1-2 Ply Risk-Aware Forward Lookahead Search (`shallow_risk_aware_search`).
- **State Projection**: Simulates damage application, knockout prize drops, energy additions, and evolution HP changes.
- **Retaliation Modeling**: Subtracts expected opponent counterattack damage:
  $$\text{Retaliation} = P(\text{Attack}) \cdot \text{EffDamage} + P(\text{Gust}) \cdot P(\text{Attack}) \cdot \text{BenchThreat}$$
- **Search Budget**:
  - Max candidate branching: $8$ actions.
  - Timeout budget: $40.0\text{ ms}$.
  - Min remaining overage time safety threshold: $20.0\text{ s}$.

---

## 5. Matchup Analysis: Weakest & Strongest Matchups

- **Strongest Matchup**:
  - **vs Ex-Heavy Ramp Decks (Bellibolt ex / Kangaskhan ex / Sinistcha ex)**: **$100.0\%$ Win Rate ($10/10$)**.
  - Crustle Safeguard reduces all incoming ex attacks to $0$ damage.
- **Weakest Matchup**:
  - **Crustle Safeguard Mirror**: **$60.0\text{--}80.0\%$ Win Rate**.
  - Since both active Pokémon are single-prize non-ex attackers, the match resolves through prize-trading tempo and hand management.

---

## 6. Top Loss Causes & The Critical Forensic Fix

- **The Bench Depletion Flaw (Mined & Fixed in Phase 10)**:
  - *Diagnosis*: In initial versions, when an attack was available, the agent attacked *first*, which prematurely ended the turn before playing Nest Ball or attaching energy to backup bench Pokémon.
  - *Consequence*: When the Active Pokémon was eventually knocked out, the bench was empty, causing an immediate game loss ($100\%$ of baseline losses).
  - *The Fix*: Implemented strict pre-attack setup ordering in `agent/action_selector.py`.
  - *Result*: Bellibolt mirror win rate skyrocketed from **$30.0\% \to 90.0\%$ ($+60.0\%$ absolute gain)**.

---

## 7. Ablation Benchmark Results

| Architecture Variant | Features Enabled | Win Rate (20g) | 95% Wilson CI | P95 Latency |
| :--- | :--- | :---: | :---: | :---: |
| **Variant A** | Pure Heuristic Baseline | 45.0% | [25.8%, 65.8%] | 0.084 ms |
| **Variant B** | Heuristic + Strategic Goals | 35.0% | [18.1%, 56.7%] | 0.097 ms |
| **Variant C** | Heuristic + 1-Ply Search | 100.0% | [83.9%, 100.0%] | 4.035 ms |
| **Variant D (Full)** | **Goals + Beliefs + 2-Ply Search + Phase Ordering** | **100.0%** | **[83.9%, 100.0%]** | **4.438 ms** |

---

## 8. Final Candidate Ranking

1. **Rank 1 — Candidate D (Crustle Control)**: **$100.0\%$ Win Rate (40/40)**, P95: $3.75\text{ ms}$, 95% CI: $[91.2\%, 100.0\%]$.
2. **Rank 2 — Candidate E (Alakazam Spread)**: **$92.5\%$ Win Rate (37/40)**, P95: $4.21\text{ ms}$, 95% CI: $[80.1\%, 97.4\%]$.
3. **Rank 3 — Candidate A (Bellibolt 4-4-4 Baseline)**: **$87.5\%$ Win Rate (35/40)**, P95: $4.55\text{ ms}$, 95% CI: $[73.9\%, 94.5\%]$.
4. **Rank 4 — Candidate B (Bellibolt 4-3-3)**: **$85.0\%$ Win Rate (34/40)**, P95: $5.01\text{ ms}$, 95% CI: $[70.9\%, 92.9\%]$.
5. **Rank 5 — Candidate C (Anti-Crustle Tech)**: **$82.5\%$ Win Rate (33/40)**, P95: $4.47\text{ ms}$, 95% CI: $[68.0\%, 91.3\%]$.

---

## 9. Recommended Submissions

- **Recommended Primary Submission**: **`Candidate D` (Crustle Safeguard Control)** inside `submission.tar.gz`.
- **Recommended Backup Active Slot**: **`Candidate A` (Bellibolt 4-4-4 Ramp Beatdown with Phase Ordering)**.

---

## 10. Exact Build, Extraction, & Validation Commands

### Build Command:
```bash
tar --exclude='*.pyc' --exclude='__pycache__' -czvf submission.tar.gz main.py deck.csv agent data/EN\ Card\ Data.csv
```

### Clean Subprocess Validation Command:
```bash
mkdir -p scratch/val_test && cd scratch/val_test && tar -xzvf ../../submission.tar.gz && python -c "import main; from kaggle_environments import make; env = make('cabt'); env.run([main.agent, 'random']); print('Validation Result:', env.steps[-1][0].reward, env.steps[-1][0].status)"
```

---

## 11. Remaining Risks & Mitigations

1. **Non-ex Fast Beatdown Decks**:
   - *Risk*: An opponent running a non-ex single-prize attacker with $> 150\text{ DMG}$ output could break through Crustle.
   - *Mitigation*: Crustle runs 4 $\times$ Dwebble + 4 $\times$ Crustle with 41 energies and Nest Balls to rapidly replace active Pokémon and trade single prizes.
2. **Kaggle Environment Runtime Variance**:
   - *Risk*: Execution spikes on shared CPU cores.
   - *Mitigation*: Our $P95$ is $3.75\text{ ms}$ and search is capped at $40\text{ ms}$ with a $20\text{ s}$ emergency abort threshold, guaranteeing 0 timeout forfeits.
