# AI Capability Matrix: PTCG Platform

**Status**: FORENSIC AUDIT COMPLETE  
**Evaluation Scope**: Autonomous Decision Engine, Game Heuristics, Search, Modeling, and Research Framework.

---

## 1. Comprehensive Feature Status Classification

| Feature Dimension | Status | Primary Implementation File & Function | Capability Description & Verification |
|---|---|---|---|
| **Legal Action Handling** | **IMPLEMENTED** | `agent/fallback.py::make_distinct_choice` | Validates option length, bounds $[minCount, maxCount]$, and returns unique valid indices. |
| **Deterministic Fallback** | **IMPLEMENTED** | `agent/fallback.py::deterministic_fallback` | Zero-crash fallback guarantee handling `None`, missing keys, and unexpected observation structures. |
| **Attack Evaluation** | **IMPLEMENTED** | `agent/policy.py::rank_attack_options` | Damage estimation, prize yield valuation, and lethal knockout detection. |
| **Knockout (KO) Detection** | **IMPLEMENTED** | `agent/evaluator.py::estimate_raw_damage` | Compares damage with opponent active/bench remaining HP to identify match-point and tempo KOs. |
| **Prize Optimization** | **IMPLEMENTED** | `agent/goals.py::GoalPlanner` | Prioritizes multi-prize targets (`ex` Pokémon) and lethal match-point knockout lines. |
| **Target Selection** | **IMPLEMENTED** | `agent/policy.py::rank_target_options` | Bench Pokémon targeting prioritizing damaged tanks or high-threat targets. |
| **Energy Planning** | **IMPLEMENTED** | `agent/policy.py::rank_energy_attachment_options` | Accelerates energy onto active Bellibolt ex (Electric Generator & manual attachments). |
| **Bench Planning** | **IMPLEMENTED** | `agent/policy.py::rank_card_play_options` | Bench expansion via Nest Ball / Ultra Ball ensuring at least 2 benched basics for tempo. |
| **Trainer Selection** | **IMPLEMENTED** | `agent/policy.py::rank_card_play_options` | Evaluates Professor's Research, Boss's Orders, Heavy Baton, and Switch. |
| **Evolution Handling** | **IMPLEMENTED** | `agent/policy.py::rank_card_play_options` | Evolves Tadbulb (#721) into Bellibolt (#722) or Bellibolt ex (#723). |
| **Retreat Management** | **IMPLEMENTED** | `agent/policy.py` & `agent/search.py` | Detects heavy damage (HP $\le 60$) and switches to preserve energy using Switch (#1145) or Heavy Baton (#1163). |
| **Immunity / Safeguard Handling** | **IMPLEMENTED** | `agent/evaluator.py::is_target_immune_to_ex` | Detects Crustle (#558) Safeguard immunity and diverts attack / gusts bench. |
| **Bayesian Belief State** | **IMPLEMENTED** | `agent/belief_state.py::BeliefStateTracker` | Computes posterior $P(\text{Gust}), P(\text{Energy}), P(\text{Switch}), P(\text{Evolution})$ via hypergeometric math. |
| **Opponent Threat Modeling** | **IMPLEMENTED** | `agent/opponent_model.py::estimate_opponent_threat` | Estimates probability and damage of opponent counterattack on subsequent turn. |
| **Dynamic Risk Modulation** | **IMPLEMENTED** | `agent/risk_model.py::determine_risk_profile` | Dynamically selects `AHEAD_LOCK_IN`, `BEHIND_COMEBACK`, `MATCH_POINT_RUSH`, or `ANTI_DECKOUT`. |
| **Goal Decomposition** | **IMPLEMENTED** | `agent/goals.py` & `agent/decomposition.py` | Macro goal assignment and additive score decomposition ($W_{\text{win}}, W_{\text{prize}}, W_{\text{board}}, -W_{\text{retaliation}}$). |
| **1-2 Ply Shallow Search** | **IMPLEMENTED** | `agent/search.py` & `src/shallow_search.py` | Lookahead state projection simulating candidate actions and opponent counter-responses. |
| **Value Function** | **IMPLEMENTED** | `agent/evaluator.py::evaluate_board_value` | Multi-factor evaluation summing active HP, energy pool, prize lead, and bench readiness. |
| **Dynamic Meta Forecasting** | **IMPLEMENTED** | `analytics/meta_predictor.py::MetaPredictor` | Computes Expected Deck Value $E[V(D)]$ and Worst-Case Robustness Index across shifting ladder distributions. |
| **Deck Policy & Turn 0** | **IMPLEMENTED** | `agent/deck_policy.py::load_and_validate_deck` | 60-card deck validator and starter fallback loader for Turn 0 setup. |
| **Experience Replay Memory** | **IMPLEMENTED** | `research/experience_memory.py::ExperienceMemory` | Serializes structured trajectory tuples `(s, a, alternatives, beliefs, reward)` to JSONL. |
| **Automated Mistake Mining** | **IMPLEMENTED** | `analytics/mistake_miner.py::MistakeMiner` | Blunder mining classifying Critical Mistakes, Missed Lethals, and Tactical Oversights. |
| **Deep MCTS Search (3+ Ply)** | **PARTIAL** | `research/ablations/` | Shallow 1-2 ply search is active in production; deep offline MCTS exists in research prototypes. |
| **Dynamic Opponent Hand Tracking** | **PARTIAL** | `agent/belief_state.py` | Tracks probabilities of specific card classes; individual card ID tracking is in research phase. |
| **Neural Network Policy Head** | **UNUSED** | `research/` | Deep RL neural models tested offline; rule/search engine is active in Kaggle production for zero latency. |
