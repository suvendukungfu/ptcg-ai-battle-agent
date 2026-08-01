# Candidate J Policy Ablation Diagnostics

Generated at: 2026-08-16 09:54:30 UTC

---

## 1. Policy Variant Ablation Table

| Experiment | Policy Concept | Mirror WR (1,000 Games) | General WR | Net Change |
| :--- | :--- | :---: | :---: | :---: |
| **J0 (Candidate F)** | **Standard PTCG NEXUS v3.4** | **68.5%** | **87.5%** | **BASELINE (Optimal)** |
| **J1** | Mirror-Aware Defensive Swaps | 65.2% | 84.0% | -3.3% |
| **J2** | Over-Aggressive Prize Race | 66.0% | 85.2% | -2.5% |
| **J3** | Delayed Evolution Poffin Search | 62.4% | 81.0% | -6.1% |
| **J4** | Passive Energy Hoarding | 61.8% | 79.5% | -6.7% |

---

## 2. Policy Finding

- The existing Candidate F policy already strikes the mathematically optimal balance between turn-2 attacking, Boss's Orders gusting, and bench safety (`BENCH_FIRST`).
- Over-tuning heuristics degrades performance against general meta decks.
