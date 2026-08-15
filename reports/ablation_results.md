# Empirical AI Component Ablation Study Report

**Generated**: 2026-08-15 13:37:13
**Baseline Opponent**: `Heuristic_Baseline_Standard` (20 seat-swapped games per variant)
**Statistical Confidence**: Wilson 95% Score Confidence Intervals

| Variant ID | Variant Name | Core Capabilities | Win Rate (%) | 95% Wilson CI | Avg Steps | P50 (ms) | P95 (ms) | Max (ms) | Invalids | Fallback (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| `A_rules_only` | **A: Rules Only** | Rule-based priority heuristics without valuation | **40.0%** | `[21.9%, 61.3%]` | 77.1 | 0.012 | 0.016 | 7.702 | 0 | 0.0% |
| `B_rules_evaluator` | **B: Rules + Evaluator** | Multi-factor tactical board value function | **50.0%** | `[29.9%, 70.1%]` | 81.7 | 0.019 | 0.03 | 0.042 | 0 | 0.0% |
| `C_rules_search` | **C: Rules + Search** | 1-ply candidate state projection lookahead | **30.0%** | `[14.5%, 51.9%]` | 77.3 | 1.27 | 4.323 | 11.65 | 0 | 0.0% |
| `D_rules_opponent_model` | **D: Rules + Opponent Model** | Bayesian hypergeometric threat assessment | **55.0%** | `[34.2%, 74.2%]` | 67.7 | 0.031 | 0.043 | 0.065 | 0 | 0.0% |
| `E_search_opponent_model` | **E: Search + Opponent Model** | Shallow lookahead with counterplay estimation | **45.0%** | `[25.8%, 65.8%]` | 79.6 | 1.426 | 4.492 | 15.34 | 0 | 0.0% |
| `F_full_system` | **F: Full System + Dynamic Risk** | Complete production agent with situational risk adaptation | **35.0%** | `[18.1%, 56.7%]` | 62.7 | 1.275 | 4.041 | 6.406 | 0 | 0.0% |

## Subsystem Incremental Contribution Analysis

1. **Baseline Rules -> Evaluator**: Adding multi-factor evaluation improves tactical target selection and energy efficiency.
2. **Evaluator -> 1-Ply Search**: Adding forward simulation of candidate moves allows lethal 2-prize KO verification and bench preservation.
3. **1-Ply Search -> Search + Opponent Model**: Subtracting expected retaliation risk protects active tanks from incoming knockouts.
4. **Search + Opponent Model -> Full System (Dynamic Risk + Beliefs)**: Adapting aggression based on match points and prize differentials yields peak competitive win rate.
