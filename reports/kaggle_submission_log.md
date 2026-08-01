# Kaggle Submission Log & Competition Tracker

**Competition**: The Pokémon Company — Pokémon TCG AI Battle Challenge (`pokemon-tcg-ai-battle`)  
**Platform**: Kaggle Environments (`cabt`)  
**Current Active Candidate**: Candidate D (`submission_candidate_d.tar.gz`, 60.0 KB)  
**Rollback Baseline**: Candidate B (`submission_candidate_b.tar.gz`, tag: `candidate-b-v3.2`)  
**Date**: August 16, 2026

---

## 1. Submission History & Leaderboard Status

| Submission ID | Candidate Name | Primary Strategy & Features | Public Score | Status | Validation Episode |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **`55542011`** | **Candidate D (v3.3 Production)** | Adaptive Matchup Intelligence, Non-EX Threat Modeling, Safeguard-Aware Counterplay, Bench Safety, Risk-Aware Search | **600.0** (Initial) | **COMPLETE** | `93503735` (WIN, 68 steps, 0 errors) |
| **`55540464`** | **Candidate B (v3.2 Rollback Baseline)** | Bench-first safety, protected Basic discard policy, lethal-state risk control | **614.2** | **COMPLETE** | `93482308` (WIN, 58 steps, 0 errors) |
| **`55540242`** | **Candidate A (v3.1 Production Baseline)** | Initial Risk-Aware Search, Heuristic Goal Planning, Belief-State Tracking | **518.5** | **COMPLETE** | `93477872` (WIN, 51 steps, 0 errors) |
| `55538168` | v3.0 Prototype | Initial Packaging (Failed on runtime import path) | — | ERROR | `93475210` |
| `55538147` | v3.0 Prototype | Initial Packaging (Failed on missing CSV path) | — | ERROR | `93475189` |

---

## 2. Hardening Audit & Verification Record
- **Archive Contents**: `main.py`, `deck.csv` (60 cards), `agent/` (15 Python modules), `data/EN Card Data.csv`.
- **Zero Forbidden Modules**: Verified `src/`, `tests/`, `research/`, `dashboard/` are absent.
- **Kaggle Sandboxed Execution**: Extracted to clean directory and verified with `get_last_callable` and CABT engine: `Result = 1 DONE` (0 illegal actions, 0 unhandled exceptions).
- **Execution Budget**: Decision latencies: Mean $0.485\text{ ms}$, P95 $0.809\text{ ms}$, representing a $96.8\%$ buffer below the $25.0\text{ ms}$ timeout limit.
