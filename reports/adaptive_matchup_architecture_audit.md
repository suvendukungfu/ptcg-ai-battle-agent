# Architecture Audit: Adaptive Matchup Intelligence & Opponent State Representation

**Project**: `PTCG // NEXUS — Autonomous Game Intelligence`  
**Focus Area**: Generalized Matchup Modeling, Opponent Threat Categorization, and Safeguard Counterplay  
**Baseline Model**: Candidate B (`Submission 55540464`, Version: `v3.2`)  
**Date**: August 16, 2026  
**Status**: **RESEARCH AUDIT COMPLETE**

---

## 1. System-Wide Module Audit

| Module | Current Capability | Missing Capability | Redundant / Fragile Logic | Regression Risk |
| :--- | :--- | :--- | :--- | :---: |
| [`agent/opponent_model.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/opponent_model.py) | • Hypergeometric probability estimation ($P(\text{Energy}), P(\text{Gust}), P(\text{Evolution})$).<br>• Observable card history tracking. | • Multi-threat bench tracking.<br>• Threat readiness stages ($T_0, T_1, T_2, T_3$).<br>• Dynamic attack damage extraction from database. | • Hardcoded card-ID checks (`723, 722, 721`) for attack probabilities. | **MEDIUM** |
| [`agent/evaluator.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/evaluator.py) | • Basic Safeguard ex-immunity multiplier (`0.0` vs `1.0`).<br>• Prize advantage weighting.<br>• Zero-bench fragility penalty ($-150.0$). | • Un-Safeguarded non-ex breaker threat quantification.<br>• Dynamic bench attacker backup valuation. | • `estimate_raw_damage` defaults to `energies * 30` when card ID is not hardcoded. | **LOW** |
| [`agent/search.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/search.py) | • 1-2 ply shallow risk-aware lookahead.<br>• Action state projection (`project_action`).<br>• Bench-depletion fatal counterattack penalty ($2500.0$). | • Benched non-ex threat counterattack projection.<br>• Switch/retreat prediction for powered bench threats. | • Evaluates only active opponent counterattacks. | **LOW** |
| [`agent/goals.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/goals.py) | • Strategic goal transitions (`GOAL_WIN_NOW`, `GOAL_COUNTER_CRUSTLE`, `GOAL_PROTECT_ACTIVE`, `GOAL_ANTI_DECKOUT`, `GOAL_BUILD_BENCH`). | • Opponent win-condition identification.<br>• Non-ex breaker elimination goal. | • Uses static prize thresholds rather than dynamic board momentum. | **LOW** |
| [`agent/risk_model.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/risk_model.py) | • Standing-based risk profiling (`AHEAD_LOCK_IN`, `BEHIND_COMEBACK`, `MATCH_POINT_RUSH`, `ANTI_DECKOUT`). | • Matchup-specific risk adaptation (e.g. high-damage breaker vs pure stall). | • None (clean and robust). | **LOW** |
| [`agent/belief_state.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/belief_state.py) | • Bayesian posterior estimation of hidden opponent hand assets (Gust, Switch, Energy). | • Integration of belief weights into combinatorial search branching. | • Discard counts use static initial deck estimates. | **LOW** |
| [`agent/decomposition.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/decomposition.py) | • Explainable additive score breakdown ($V(a) = V_{\text{win}} + V_{\text{prize}} + V_{\text{board}} + V_{\text{threat}} - V_{\text{risk}}$). | • Explicit Threat Reduction metric $T_{\text{reduction}}(a)$. | • None (clean diagnostic structure). | **LOW** |
| [`agent/policy.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/policy.py) | • Tactical rankings (`rank_attack_options`, `rank_energy_attachment_options`, `rank_card_play_options`, `rank_discard_options`).<br>• `BENCH_FIRST` rule (+350.0).<br>• `PROTECT_BASIC_DISCARD` rule (-5000.0). | • Dynamic Gust target ranking for un-Safeguarded benched non-ex threats.<br>• Dynamic backup bench energy allocation. | • Some residual hardcoded card IDs in trainer checks. | **MEDIUM** |
| [`agent/action_selector.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/action_selector.py) | • Unified pipeline: parse state -> update beliefs -> identify goal -> lookahead search -> heuristic fallback. | • None. | • None (fully functional routing). | **LOW** |
| [`agent/state.py`](file:///Users/suvendusahoo/Downloads/pokemon/agent/state.py) | • Normalized dataclass representing board, zones, options, and status. | • None. | • None. | **LOW** |

---

## 2. Opponent State Representation Model

A generalized adaptive agent requires a structured, incomplete-information representation of the opponent:

```
@dataclass
class OpponentThreat:
    card_id: int
    name: str
    is_ex: bool
    hp: float
    max_hp: float
    energy_attached: int
    attack_cost: int
    raw_damage: float
    effective_damage: float      # 0.0 if our Active is Safeguarded and attacker is EX
    readiness_stage: str         # 'T0_READY', 'T1_NEXT_TURN', 'T2_SETUP', 'T3_DISTANT'
    is_lethal: bool              # effective_damage >= our_active_hp
    is_safeguard_blocked: bool   # True if our active walls this attacker
    categories: List[str]        # ATTACK_THREAT, ENERGY_RAMP, EVOLUTION_THREAT, BENCH_ENGINE
    threat_score: float

@dataclass
class OpponentBoardState:
    active_threat: Optional[OpponentThreat]
    bench_threats: List[OpponentThreat]
    primary_threat: Optional[OpponentThreat]
    total_known_energies: int
    estimated_hand_energy_prob: float
    estimated_hand_gust_prob: float
    opponent_win_condition: str  # 'SAFEGUARD_BREAKER_PIVOT', 'PRIZE_SWEEP', 'BENCH_SNIPE', 'STALL'
```

---

## 3. Threat Classification & Readiness Hierarchy

Opponent Pokémon are dynamically classified across 6 orthogonal dimensions without hardcoding card IDs:

```
                     ┌──────────────────────────────────────────────┐
                     │          OPPONENT POKÉMON DETECTED           │
                     └──────────────────────┬───────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
         [Is Pokémon EX / Tera]                           [Is Non-EX Attacker]
                    │                                               │
           Our Active Safeguarded?                         Our Active Safeguarded?
          ┌─────────┴─────────┐                           ┌─────────┴─────────┐
         YES                 NO                          YES                 NO
          │                   │                           │                   │
    [Effective Dmg = 0] [Full Damage]              [Full Lethal Dmg]   [Full Damage]
    (Wall Neutralized)  (High Threat)              (CRITICAL BREAKER)  (Standard Attacker)
```

### Readiness Staging ($T_0, T_1, T_2, T_3$):
- **$T_0$ (Active & Ready Now)**: $\Delta_E = 0$. Can attack this upcoming turn.
- **$T_1$ (Ready Next Turn)**: $\Delta_E = 1$. Requires 1 energy attachment ($P(\text{Ready}) \approx 0.85 \times P(\text{Energy})$).
- **$T_2$ (Setup Required)**: $\Delta_E = 2$. Requires 2 attachments / 2 turns.
- **$T_3$ (Distant Threat)**: $\Delta_E \ge 3$ or un-evolved Basic without energy.

---

## 4. Win-Condition Alignment

The agent's decision logic dynamically pivots based on the detected opponent win condition:

| Opponent Strategy | Detected Pattern | Our Adapted Win Condition | Tactical Adjustment |
| :--- | :--- | :--- | :--- |
| **Pure EX Aggro** (e.g. Kangaskhan ex) | 0 Non-EX attackers on board/discard | **`SAFEGUARD_LOCK`** | • Maintain Active Crustle.<br>• Concentrate energy on Active.<br>• Sweep prizes with 0 retaliation risk. |
| **Non-EX Breaker Tech** (e.g. Hariyama 210) | Non-EX Stage 1 with $\ge 2$ energies on Bench | **`BREAKER_ELIMINATION`** | • Prioritize Gust / Boss's Orders to drag and KO breaker.<br>• Ramp backup Crustle on Bench to prepare 1-for-1 prize trade. |
| **Fast Basic Rush** (e.g. Cinderace 100) | Aggressive Turn 1 energy attachment | **`BENCH_REDUNDANCY`** | • Enforce `BENCH_FIRST` (2+ Basics on board).<br>• Evolve immediately on Turn 2. |
| **Stall / Anti-Deckout** | Low prize exchange, turn $\ge 8$ | **`DECISIVE_STRIKE`** | • Prohibit draw supporters ($N_{\text{deck}} \le 7$).<br>• Close match with direct attacks. |

---

*Audit Complete. Stored in `reports/adaptive_matchup_architecture_audit.md`.*
