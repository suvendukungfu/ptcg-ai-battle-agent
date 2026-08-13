# Pokémon TCG AI Battle Challenge — Official Submission Format & Contract

This document details the exact packaging format and runtime contracts required for submissions on Kaggle.

---

## 1. Archive Structure (`submission.tar.gz`)

The submission file must be a standard `.tar.gz` archive ($< 197.7\text{ MiB}$) with `main.py` and `deck.csv` at the **root** of the archive:

```text
submission.tar.gz
├── main.py                     # Entry point exposing agent(obs, config=None)
├── deck.csv                    # Exactly 60 valid integer card IDs (1 per line)
├── agent/                      # Bayesian / count-based opponent model
├── cg/                         # Ctypes engine shared libraries & interfaces
└── src/                        # Policy, search, and state evaluation modules
```

---

## 2. Agent Function Signature & Protocol Contract

The agent entry point in `main.py` must match the Kaggle Environments standard signature:

```python
def agent(obs: dict, config: dict = None) -> list[int]:
    """
    Kaggle PTCG Agent Decision Function.
    
    Turn 0 (Deck Submission):
      - obs["select"] is None
      - Return: list[int] of exactly 60 valid card IDs.
      
    Turn N (Gameplay Decision):
      - obs["select"] is a dict containing options, minCount, and maxCount.
      - Return: list[int] of chosen option indices within [0, len(options)-1].
    """
```

### Turn 0: Deck Selection
- When `obs.get("select") is None`, the engine expects the agent to submit its 60-card deck list.
- Return format: `list[int]` of length exactly 60.

### Turn N: In-Game Action Selection
- When `obs.get("select")` is present:
  - `minCount = obs["select"].get("minCount", 1)`
  - `maxCount = obs["select"].get("maxCount", 1)`
  - `options = obs["select"].get("option", [])`
- Return format: `list[int]` containing between `minCount` and `maxCount` distinct option indices.

---

## 3. `deck.csv` Format Specification

- Must contain exactly 60 non-empty lines.
- Each line contains a single integer Card ID from the official 1,267 card database.
- Maximum 4 copies of any card sharing the same base name (excluding Basic Energy).

---

## 4. Local Execution & Self-Play Simulation

To test an agent locally using `kaggle-environments`:

```python
from kaggle_environments import make
from kaggle_environments.envs.cabt import cabt
import main

# Initialize environment
env = make("cabt", debug=True)

# Run full battle
env.run([main.agent, cabt.random_agent])

# Inspect winner
final_step = env.steps[-1]
p0_reward = final_step[0].reward  # 1 = Win, -1 = Loss, 0 = Draw
print("Result:", "WIN" if p0_reward == 1 else "LOSS")
```

---

## 5. Automated Submission Packaging

Generate the certified submission archive using the automated build script:

```bash
bash tools/build_submission.sh
```
