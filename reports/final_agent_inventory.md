# PTCG AI Battle Challenge — Final Agent Inventory & Architecture Audit

**Target Submission**: Kaggle Pokémon TCG AI Battle Challenge Simulation  
**Deadline**: August 16, 2026  
**Architecture Root**: `agent/` (Canonical Production Pipeline)  
**Entry Point**: `main.py` -> `agent.action_selector.select_action`

---

## 1. Deck Inventory & Structure (`deck.csv` / `agent/deck_policy.py`)

- **Current Deck List**:
  - `721` Tadbulb (Basic Lightning, 70 HP) $\times 2$
  - `722` Bellibolt (Stage 1 Lightning, 140 HP, non-ex attacker) $\times 4$
  - `723` Bellibolt ex (Stage 1 Lightning, 350 HP, 2-Prize ex tank/attacker) $\times 4$
  - `1092` Professor's Research (Supporter, Discard hand & Draw 7) $\times 1$
  - `1121` Ultra Ball (Item, Discard 2 to search any Pokémon) $\times 2$
  - `1145` Switch (Item, Swap Active with Benched) $\times 2$
  - `1163` Heavy Baton (Tool, Preserve up to 3 Basic Energy on KO) $\times 2$
  - `1219` Electric Generator (Item, Look at top 5 cards, attach up to 2 Basic Lightning to Benched Lightning) $\times 4$
  - `1227` Nest Ball (Item, Search deck for Basic Pokémon to Bench) $\times 4$
  - `1262` Boss's Orders (Supporter, Switch Opponent Active with Benched) $\times 2$
  - `3` Basic Lightning Energy $\times 33$
  - **Total**: Exactly 60 cards.

- **Deck Archetype**: Lightning Ramp / Heavy ex Tank (`Bellibolt ex Engine`).
- **Initial Structural Risk Identified**: 
  - The deck runs $8$ Stage 1 evolutions (`722` $\times 4$, `723` $\times 4$) but only $2$ Basic Tadbulbs (`721` $\times 2$).
  - If a Tadbulb is prized or KO'd early, the remaining 8 evolution cards become dead draws.
  - Hypergeometric opening hand probability of drawing at least 1 Basic with only 2 Basics in 60 cards: $P(X \ge 1) = 1 - \frac{\binom{58}{7}}{\binom{60}{7}} \approx 22.4\%$ without mulligans. In CABT, mulligans occur, but prize-locking 1 Tadbulb leaves only 1 in deck.

---

## 2. Module Inventory & Policy Logic

### 2.1 Action Pipeline (`agent/action_selector.py`)
1. **State Ingestion**: `agent.state.parse_game_state(obs)` extracts active, bench, hand, discard, prize count, energy attachments, and legal option bounds.
2. **Belief Tracker**: Updates legal Bayesian hypergeometric probability distributions over opponent hand ($P(\text{Energy})$, $P(\text{Boss})$, $P(\text{Evolution})$).
3. **Strategic Goal Planner**: Evaluates game state macro conditions (`WIN_NOW`, `PREPARE_ATTACKER`, `COUNTER_CRUSTLE`, `PROTECT_ACTIVE`, `BUILD_BENCH`, `ANTI_DECKOUT`).
4. **Shallow Risk-Aware Search**: Executes 1-2 ply forward lookahead projection (`project_action`), evaluates terminal board values, and subtracts opponent retaliation threats.
5. **Fallback to Tactical Heuristic**: When search is inapplicable or budget-constrained, prioritizes attack $\to$ energy $\to$ card plays $\to$ pass.
6. **Deterministic Validation**: Sanitizes selections via `make_distinct_choice`.

### 2.2 Board Value Function (`agent/evaluator.py`)
- $\text{Value}(S) = w_{\text{prize}} \Delta P + w_{\text{active\_hp}} \text{HP}_{\%} + w_{\text{energy}} E + w_{\text{attackers}} N_{\text{viable}} - w_{\text{retaliation}} - w_{\text{safeguard\_penalty}}$.
- Recognizes Safeguard immunity on opponent Active (`345`, `533`, `542`, or skill text `"prevent all damage"` + `"ex"` / `"mysterious rock inn"`).
- Distinguishes ex attackers (`723`, `ex=True`) from non-ex single prize attackers (`722`).

### 2.3 Forward Search & Retaliation Engine (`agent/search.py`)
- Forward projections simulate damage, KO prize drops, energy additions, and evolution HP increases.
- Retaliation engine estimates expected opponent counter-attack: $E[\text{Retaliation}] = P(\text{Attack}) \cdot \text{EffDamage} + P(\text{Gust}) \cdot P(\text{Attack}) \cdot \text{BenchThreat}$.

### 2.4 Dynamic Risk Controller (`agent/risk_model.py`)
- Adjusts aggression bonus ($0.8\text{--}1.6\times$) and retaliation aversion ($0.5\text{--}1.8\times$) based on prize difference ($P_{\text{own}} - P_{\text{opp}}$).

### 2.5 Opponent Threat Modeling (`agent/opponent_model.py`)
- Calculates exact hypergeometric probability $P(X \ge 1)$ of opponent holding specific cards based on:
  - Total opponent deck count $N$
  - Number of revealed copies in discard/board
  - Opponent hand size $n$
- **Zero Hidden Information Leakage**: Strictly queries observable parameters.

---

## 3. Key Findings & Discrepancies to Address

1. **`goals.py` Crustle ID Discrepancy**: `goals.py` checked `opp_active_id in (558,)` while `evaluator.py` checked `(345, 533, 542)` and parsed skills. `goals.py` should import and call `is_target_immune_to_ex(opp_active)`.
2. **Basic Pokémon Ratio**: 2 Tadbulbs vs 8 Evolutions is highly fragile. We must test 4 Tadbulb / 3 Bellibolt / 3 Bellibolt ex ratios in the Deck Search phase.
3. **Electric Generator Logic**: Electric Generator only attaches to Benched Lightning Pokémon. The agent must ensure Tadbulb/Bellibolt is on Bench before playing Generator.
