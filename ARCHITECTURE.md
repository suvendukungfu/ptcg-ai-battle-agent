# PTCG AI Battle Agent Architecture & Technical Specification

## 1. Engine & Simulator
The simulation engine used for **The Pokémon Company – PTCG AI Battle Challenge** is the **`cabt`** engine, which is integrated natively into the `kaggle-environments` Python package.

- **Backend**: C++ compiled shared library (`libcg.dylib` on macOS, `libcg.so` / `libcg-arm64.so` on Linux, `cg.dll` on Windows) bound via `ctypes`.
- **Environment Execution**:
  ```python
  from kaggle_environments import make
  from kaggle_environments.envs.cabt import cabt

  env = make("cabt", debug=True)
  env.run([agent1, agent2])
  ```

---

## 2. Agent Contract & Control Flow
The Kaggle runner invokes the entrypoint function `agent(obs: dict) -> list[int]` defined in `main.py`.

### Phase 1: Deck Submission (Turn 0)
- **Condition**: `obs["select"] is None`
- **Output**: Returns a `list[int]` containing exactly 60 card IDs representing the deck.
- **Source**: Loaded from `deck.csv` at submission root or specified in code.

### Phase 2: Action Selection (Turns 1..N)
- **Condition**: `obs["select"] is not None`
- **Output**: Returns a `list[int]` containing chosen indices from `obs["select"]["option"]`.
- **Constraint**: Length of returned list MUST equal `obs["select"]["maxCount"]` (or be between `minCount` and `maxCount`). Indices must be within `0 <= idx < len(obs["select"]["option"])`.

---

## 3. Data Structures & Observations

### Observation Payload (`obs`)
```json
{
  "remainingOverageTime": 600,
  "step": 0,
  "select": { ... },
  "logs": [ ... ],
  "current": { ... },
  "search_begin_input": "..."
}
```

### `obs["select"]` (Legal Action Context)
- `type` (int): SelectType enum.
- `context` (int): SelectContext enum (e.g., `0` for Main turn choice).
- `minCount` (int): Minimum required selected options.
- `maxCount` (int): Maximum required selected options.
- `option` (list[dict]): Array of valid option dicts. Each option contains:
  - `type` (int): OptionType enum (e.g. Card, Attack, Retreat, Pass).
  - Additional context fields: `index`, `area`, `inPlayArea`, `inPlayIndex`.

### `obs["current"]` (Game Board State)
- `yourIndex` (int): 0 or 1.
- `turn` (int): Current turn counter.
- `result` (int): `-1` (in-progress), `0` (player 0 win), `1` (player 1 win), `2` (draw).
- `stadiumPlayed`, `supporterPlayed`, `energyAttached`, `retreated` (bool): Action flags for the active turn.
- `players` (list[dict]): State of Player 0 and Player 1.
  - `active` (list[dict]): Active Pokémon details (`id`, `hp`, `maxHp`, `energies`, `tools`, `preEvolution`).
  - `bench` (list[dict]): Benched Pokémon details.
  - `hand` (list[dict]): Cards in hand.
  - `handCount`, `deckCount`, `discard`, `prize` (list/int): Zone metrics.
  - Special conditions: `poisoned`, `burned`, `asleep`, `paralyzed`, `confused`.

---

## 4. Deck Specification (`deck.csv`)
- **Format**: Plain text / CSV with 60 integer card IDs.
- **Starter Deck Baseline**:
  - `721` (x2), `722` (x4), `723` (x4), `1092` (x1), `1121` (x2), `1145` (x2), `1163` (x2), `1219` (x4), `1227` (x4), `1262` (x2)
  - `3` (Basic Energy x33)
- **Constraint**: Decks MUST have exactly 60 valid card IDs.

---

## 5. Submission Requirements & Rules
- **Submission File**: `submission.tar.gz`
- **Root Files Required**:
  - `main.py` (Must expose `def agent(obs, config=None):` or `def agent(obs):`)
  - `deck.csv` (60 card IDs)
- **Submission Size Limit**: <= 197.7 MiB
- **Resource Constraints**: ~12.2 GiB RAM, 2 vCPUs
- **Time Limits**: `remainingOverageTime` = 600s (10 min per player total overage budget).
- **Rule Violations**: Any invalid index, exception, or timeout results in immediate forfeit (Reward = -1). Robust fallback mechanism is mandatory.

---

## 6. Evaluation & Local Testing Strategy
- **Self-Play Simulator**: Run local multi-game series using `kaggle_environments`.
- **Metric**: Win Rate / Elo rating across randomized deck/player orders (to eliminate first-player bias).
