# Meta Strategic Hypotheses & Competitive Research Matrix

**Competition**: Kaggle Pokémon TCG AI Battle Challenge Simulation  
**Platform Rules**: Standard 60-card format, 6 Prize cards, CABT engine rules.  
**Deadline**: August 16, 2026

---

## Strategic Hypothesis Registry

### Hypothesis H1: Safeguard Wall (Crustle) Control Domination
- **Hypothesis**: Decks relying on Crustle's *Mysterious Rock Inn* ability (prevent all damage from Pokémon ex) achieve high win rates against pure ex-heavy decks by creating an insurmountable damage wall.
- **Source**: CABT environment analysis (`data/EN Card Data.csv` card #345) & competitive TCG archetypes.
- **Why It May Work**: If the opponent relies exclusively on Pokémon ex (e.g. Bellibolt ex), their attacks deal $0$ damage, forcing a deck-out or slow prize loss.
- **How We Test It**: Simulate Bellibolt ex against Crustle Safeguard control decks. Measure win rate and investigate whether hybrid non-ex attackers (`722` Bellibolt) and Boss's Orders (`1262`) gusting circumvent the wall.
- **Result**: [Pending Phase 5 Tournament]
- **Decision**: [Pending Phase 5 Forensics]

---

### Hypothesis H2: Basic-to-Evolution Consistency Ratio
- **Hypothesis**: Increasing the basic Tadbulb count from $2 \to 4$ will significantly reduce dead hands, prize-locking, and early knockouts, increasing overall matchup win rate across all opponents.
- **Source**: Hypergeometric probability distribution of opening hands and 6-prize distribution ($P(\text{prized}) = \frac{6}{60} = 10\%$).
- **Why It May Work**: With 2 basics, the probability of at least one being prized is $1 - \frac{\binom{58}{6}}{\binom{60}{6}} \approx 19.0\%$. With 4 basics, having all 4 prized is $< 0.001\%$, and opening hand Basic probability jumps from $22.4\% \to 40.0\%$.
- **How We Test It**: Build candidate decks with varying Basic:Evolution ratios ($2:8$ vs $4:6$ vs $4:4$) and run 50-game CABT simulations against benchmark opponents.
- **Result**: [Pending Phase 4 Benchmark]
- **Decision**: [Pending Phase 4 Evaluation]

---

### Hypothesis H3: Electric Generator Bench Acceleration
- **Hypothesis**: High Basic Lightning Energy density ($25\text{--}33$ cards) paired with 4 $\times$ Electric Generator allows Turn 2 Bellibolt ex 160 DMG attacks with $> 85\%$ consistency, creating an unrecoverable prize tempo advantage.
- **Source**: Bellibolt Ramp engine mechanics.
- **Why It May Work**: Electric Generator checks top 5 cards. With 30 energies in a 50-card deck ($60\%$), $E[\text{Energy drawn}] = 5 \times 0.6 = 3.0$ energies. It reliably hits the 2 energy attachments needed for Electro Bullet in a single item play.
- **How We Test It**: Simulate turn-2 attack success rates across varying energy counts ($20, 25, 30, 33$).
- **Result**: [Pending Phase 4 Benchmark]
- **Decision**: [Pending Phase 4 Evaluation]

---

### Hypothesis H4: Targeted Boss Gusting vs Bench Setup
- **Hypothesis**: Saving Boss's Orders (`1262`) specifically to gust vulnerable benched evolving basics (e.g., Dwebble before it evolves to Crustle, or low-HP 2-prize targets) increases 2-ply lookahead search win rates.
- **Source**: CABT tactical replay analysis.
- **Why It May Work**: Knocking out Dwebble before it evolves prevents Crustle Safeguard from ever entering the active spot.
- **How We Test It**: Compare Heuristic without gust prioritization vs Policy with targeted gusting on evolvable basics.
- **Result**: [Pending Phase 10 Loss Mining]
- **Decision**: [Pending Phase 11 Counterfactual]

---

### Hypothesis H5: Fighting Weakness Exposure
- **Hypothesis**: Bellibolt (Lightning type) is weak to Fighting ($2\times$ damage). Decks utilizing Fighting attackers (e.g. Lucario) can achieve 1-hit KOs on Bellibolt ex for half the normal damage threshold.
- **Source**: Card weakness rules in `EN Card Data.csv` (Weakness: Fighting $\times 2$).
- **Why It May Work**: Lucario doing 80 base damage hits Bellibolt for 160 damage.
- **How We Test It**: Evaluate our agent against Fighting-archetype baselines.
- **Result**: [Pending Phase 4 Tournament]
- **Decision**: [Pending Phase 4 Evaluation]
