# Candidate K Endgame Planning Engine

Generated at: 2026-08-16 10:07:00 UTC

---

## 1. Endgame Evaluator (Prizes $\le 3$)

When either player reaches $\le 3$ prize cards:
1. **Lethal Search**: Check if active attack or gust attack takes remaining prizes immediately.
2. **Safeguard Stall Verification**: If opponent's remaining attackers are all Pokémon ex, board state is mathematically unwinnable for opponent regardless of prize counts.
3. **Bench Exhaustion Check**: If opponent has 0 bench Pokémon, all resources focus on KOing active for an immediate bench-out victory.
