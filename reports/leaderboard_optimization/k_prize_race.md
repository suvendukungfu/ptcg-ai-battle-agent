# Candidate K Expected Prize Race & Energy Policy

Generated at: 2026-08-16 10:06:30 UTC

---

## 1. Formal Expected Prize Race Formula

$$\text{Prize Race Margin} = \left( \frac{\text{Opponent Prizes}}{\text{Our Attacks to KO Opponent Active/Bench}} \right) - \left( \frac{\text{Our Prizes}}{\text{Opponent Attacks to KO Our Active}} \right)$$

When Margin $> 0$, the AI presses the aggressive line of play; when Margin $\le 0$, the AI prioritizes bench reinforcement.

---

## 2. Energy Attachment Lookahead

1. If active Crustle requires 1 energy for lethal attack this turn $\rightarrow$ Attach to Active.
2. If active already has 2 Grass Energy $\rightarrow$ Attach to benched Dwebble/Crustle (0 energy wasted).
3. If active is facing lethal damage next turn $\rightarrow$ Preserve energy by powering benched replacement.
