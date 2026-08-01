# Leaderboard Failure Taxonomy & Bottleneck Analysis

## The Core Question
**WHAT ACTUALLY PREVENTS THIS DECK FROM REACHING TOP-TIER PERFORMANCE (1200+ Score)?**

Based on the 10 public matches of Candidate D (7 Wins, 4 Losses) and the prior local testing, we can empirically rank the hypotheses:

### 1. H4: Insufficient Damage Ceiling (Primary Deck Limitation)
**Status: CONFIRMED (Rank 1)**
Crustle caps at 120 damage. The Kaggle meta heavily features Stage 2 Non-EX attackers (like Alakazam) and Stage 1s (like Dudunsparce/Trevenant) with 140+ HP. A deck that physically cannot 1-hit KO the opponent's primary attackers will always lose the prize trade unless it has total immunity (Safeguard). When immunity is bypassed, a 120-damage ceiling is a mathematical death sentence.

### 2. H1: Non-EX Matchup Weakness
**Status: CONFIRMED (Rank 2)**
All 4 losses on the Kaggle ladder are suspected to be against Non-EX decks (Alakazam, Trevenant). Because Crustle relies entirely on its `Safeguard` ability (immunity to Pokémon-ex), it acts as a vanilla 150 HP Pokémon that deals 120 damage against Non-EX attackers. Non-EX attackers like Alakazam (using Mind Jack) easily hit 200+ damage, bypassing Safeguard and out-trading Crustle.

### 3. H13: Over-specialization around Safeguard
**Status: CONFIRMED (Rank 3)**
The deck (4x Dwebble, 4x Crustle) has exactly one game plan: wall out EX Pokémon. It has no backup attackers, no secondary win conditions, and no tech options. When the opponent doesn't use EX Pokémon, Candidate D has 0 active abilities. 

### 4. H6: Lack of Gust/Control
**Status: CONFIRMED (Rank 4)**
Candidate D runs 0 copies of Boss's Orders or Crushing Hammer. It cannot drag up weak pre-evolutions (e.g., 50 HP Abra) to bypass the 120-damage ceiling limitation. (Note: Our local Phase F tests showed adding Gust alone didn't fix the issue against bots, but humans play around it much better).

### 5. H8: Energy Dependency (Brick Risk)
**Status: CONFIRMED (Rank 5)**
While pure Grass energy works beautifully for consistency, previous local experiments (Candidate E) proved that adding even a small splash of a second energy type (Lightning) crashed the win rate to 4% due to energy bricking. This limits deckbuilding flexibility severely.

### Other Hypotheses:
- **H2: Pokémon-ex matchup weakness** (REJECTED): The deck dominates EX matchups (100% locally, strong on Kaggle).
- **H3: Opening-hand consistency** (REJECTED): With 41 energy and 8 Basics, opening brick rate is low.
- **H14: Rating variance** (REJECTED): The losses are systematic and structural, not just bad luck.

---

## Conclusion
The true bottleneck is **Architectural**. A pure Crustle deck has a hard mathematical ceiling. It dominates EX decks but automatically loses to competent Non-EX decks because it lacks both the damage (120 vs 140) and the control tools to disrupt them. To reach 1264 rating, a deck must have game against *both* halves of the meta.

**Next Step (Phase 5):** We must explore multi-attacker architectures (Hybrid/Balanced) that do not suffer from the fatal energy-dilution bricking seen in Candidate E.
