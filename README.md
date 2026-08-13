# Pokémon TCG AI Battle Challenge — Baseline Agent (V0)

V0 is a completely reliable, crash-proof baseline agent for **The Pokémon Company – PTCG AI Battle Challenge Simulation** on Kaggle.

---

## Key Features & Architecture

- **Zero-Crash Design**: Wrapped in outer defensive exception boundaries with deterministic legal fallback handling.
- **Dynamic Path Resolution**: Resolves `deck.csv` relative to `main.py` directory and supports `/kaggle_simulations/agent/deck.csv` regardless of working directory (`Cwd`).
- **Deck Validation**: Ensures exactly 60 valid card IDs are loaded and cached.
- **Action Preference Engine**:
  - Turn 0: Submits valid 60-card deck.
  - In-Game Turns: Prioritizes Attacks (Type 7) > Energy Attachment (Type 8) > Playing Cards (Type 0-6) > Other > End Turn (Type 14).
- **Diagnostic Telemetry**: Tracks decisions, policy selections, fallbacks, exceptions, option types, and attack frequency.

---

## Directory Structure

```
.
├── ARCHITECTURE.md     # Engine specs & observation/action schema documentation
├── README.md           # Instructions & setup documentation
├── deck.csv            # 60-card starter deck specification
├── main.py             # Entrypoint agent(obs) implementation
├── requirements.txt    # Dependencies for local development
├── tests/              # Unit test suite
│   └── test_agent.py
└── tools/              # Evaluation & diagnostic tools
    └── self_play.py
```

---

## Setup & Local Testing

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Unit Test Suite

```bash
pytest tests/
```

### 3. Run Self-Play Evaluation Series

Run 10 games of self-play (`agent` vs `agent`) with seat swapping:

```bash
python tools/self_play.py --games 10 --opponent self
```

Run 10 games against `random_agent`:

```bash
python tools/self_play.py --games 10 --opponent random
```

---

## Creating Kaggle Submission Package

```bash
tar -czvf submission.tar.gz main.py deck.csv
```

Verify contents:

```bash
tar -tzvf submission.tar.gz
```
