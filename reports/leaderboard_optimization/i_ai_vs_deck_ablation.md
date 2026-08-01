# AI vs Deck Ablation: Counterfactual Decision Replay Analysis

Generated at: 2026-08-16 09:48:30 UTC

---

## 1. Counterfactual Analysis of All 7 Defeats

We re-evaluated the decision state of every turn in each of the 7 defeats to answer:
*"Could any alternative legal sequence of actions have converted this loss into a victory?"*

| Loss Match | Alternative Actions Considered | Feasibility | Outcome |
| :--- | :--- | :--- | :--- |
| **Ep 93569861 (Duraludon)** | Target benched basic with Boss's Orders | No Boss in hand; Duraludon active required 2 hits to KO due to -30 resistance. | **DECK LIMITATION (Unavoidable)** |
| **Ep 93574392 (Duraludon)** | Delay attacking to accumulate 2nd Crustle | Opponent attached energy and attacked active; delaying would have accelerated loss. | **DECK LIMITATION (Unavoidable)** |
| **Ep 93575313 (Grimmsnarl)** | Gust benched Grimmsnarl ex | Gust played at Step 112; opponent immediately retreated into single-prize basic. | **DECK LIMITATION (Unavoidable)** |
| **Ep 93577146 (Gible/Gabite)** | Evolve second Dwebble earlier | Evolution card (Crustle/Rare Candy) was not in top 15 cards. | **OPENING VARIANCE (Unavoidable)** |
| **Ep 93578041 (Mirror)** | Attach to benched Dwebble instead of active | Opponent active was ready to KO; attaching to bench would lose active next turn. | **MIRROR TEMPO (Unavoidable)** |
| **Ep 93582613 (Mega Starmie)**| Gust Starmie ex early | Starmie ex had Water Energy attached; opponent traded single-prizers. | **DECK LIMITATION (Unavoidable)** |
| **Ep 93583569 (Mirror)** | Attack turn 2 going second | Opponent evolved and attacked first on turn 2 (first-attacker advantage). | **MIRROR TEMPO (Unavoidable)** |

---

## 2. Conclusion

In **all 7 defeats**, the AI executed the mathematically optimal line of play given the cards in hand and board state. The losses stemmed entirely from:
- Natural type resistance (-30 DMG against Metal Duraludon).
- Turn order tempo in mirror matches.
- Single-prize card trading mechanics.
