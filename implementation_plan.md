# Implementation Plan - Final Kaggle Submission Builder & Certification

Build the automated submission packager (`tools/build_submission.sh`), execute a comprehensive pre-packaging smoke test, assemble the clean `submission.tar.gz` archive containing all necessary engine files (`cg/`, `src/`, `agent/`, `main.py`, `deck.csv`), and generate the final competition certification checklist (`FINAL_SUBMISSION_CHECKLIST.md`).

## Proposed Changes

### Phase 5-7: Heuristic Engine & AI Upgrades
- **Status: COMPLETE**
- Discovered that the heuristic engine evaluates complex attack logic (like Mind Jack) poorly, assuming 0 or 60 damage instead of 210+.
- Fixed `get_pokemon_damage_profile` in `opponent_model.py` to hardcode major meta threats (Alakazam, Bellibolt).
- Fixed `rank_energy_attachment_options` in `policy.py` to correctly prioritize Non-EX attackers when facing a Safeguard opponent (e.g. Crustle).
- Evaluated Bellibolt EX + Non-EX hybrid deck against Crustle with improved AI. Win rate improved from 5% to 30%, but still loses because Crustle is 1 turn faster (2 energy vs 3 energy).

## Phase 8: Candidate F (The Meta Breaker)
### [NEW] Design a Hybrid Deck
- **Goal:** Create a deck that beats both EX Aggro (Bellibolt) and Non-EX Swarm (Alakazam/Crustle).
- **Concept:** Bellibolt EX (for raw power vs EX and Alakazam) + a FAST Non-EX attacker (1-2 energy) to counter Safeguard.
- **Action:** Write a script to find a Lightning or Colorless Basic/Stage 1 Non-EX attacker that deals >= 120 damage for <= 2 energy, or uses a utility attack (e.g., paralyze, spread damage).
- **Alternative:** Return to Candidate B (Bellibolt EX) but add a Gus/Boss's Orders equivalent (e.g. Pokemon Catcher) to drag around Safeguard walls and kill their bench.

### Packaging Script

#### [NEW] [tools/build_submission.sh](file:///Users/suvendusahoo/Downloads/pokemon/tools/build_submission.sh)
- Automated submission build and validation script:
  1. Creates a clean temporary directory (`/tmp/submission_build_...`).
  2. Copies `main.py`, `deck.csv`, `src/`, `agent/`, and `cg/` (without `__pycache__`, `.DS_Store`, or git artifacts).
  3. Validates `deck.csv` line count = exactly 60 card IDs.
  4. Validates import paths and executes a standalone smoke test simulation in isolation.
  5. Packages `submission.tar.gz` with `main.py` and `deck.csv` at the root.
  6. Verifies archive size ($< 197.7$ MiB) and prints the table of contents.

---

### Final Documentation

#### [NEW] [FINAL_SUBMISSION_CHECKLIST.md](file:///Users/suvendusahoo/Downloads/pokemon/FINAL_SUBMISSION_CHECKLIST.md)
- Complete Kaggle submission checklist and verification certification:
  - Archive structure and root requirements.
  - Resource and runtime constraints.
  - Zero-crash & 100% legal fallback guarantees.
  - Step-by-step submission instructions.

---

## Verification Plan

### Automated Execution
- Run `bash tools/build_submission.sh` to build and validate `submission.tar.gz`.
- Verify smoke test passes in isolated directory.
- Verify archive size ($< 10$ MB, far below 197.7 MiB).
- Verify tarball root listing (`tar -tzvf submission.tar.gz`).
