from dataclasses import dataclass
from typing import Dict, Any
from agent.state import GameState


@dataclass
class RiskProfile:
    """Dynamic risk multipliers adjusted for the current game context."""
    variance_penalty: float = 1.0     # Higher means favor guaranteed/low-variance plays
    retaliation_weight: float = 1.5   # Penalty multiplier for opponent expected counterattack
    aggression_bonus: float = 1.0     # Multiplier for aggressive knockout lines
    deck_conservation: float = 1.0    # Penalty for excessive card drawing when low on cards
    mode: str = "BALANCED"


def determine_risk_profile(state: GameState) -> RiskProfile:
    """
    Evaluate game state relative standings and return tailored RiskProfile:
    - Ahead (e.g. your_prizes <= 2, opp_prizes >= 4): lock in low-variance winning lines.
    - Behind (e.g. your_prizes >= 4, opp_prizes <= 2): accept higher risk for swing/comeback.
    - Match Point (your_prizes <= 1): all-in prize rush to close out the game.
    - Resource Depleted (your_deck_count < 6): prioritize anti-deckout resource preservation.
    """
    # 1. Match Point: 1 prize remaining
    if state.your_prizes <= 1:
        return RiskProfile(
            variance_penalty=0.2,
            retaliation_weight=0.5,
            aggression_bonus=3.0,
            deck_conservation=0.5,
            mode="MATCH_POINT_RUSH",
        )

    # 2. Critical Deck-out Danger
    if state.your_deck_count <= 5:
        return RiskProfile(
            variance_penalty=1.8,
            retaliation_weight=1.2,
            aggression_bonus=1.5,
            deck_conservation=4.0,
            mode="ANTI_DECKOUT",
        )

    # 3. Substantial Prize Lead (Ahead)
    prize_diff = state.opp_prizes - state.your_prizes
    if prize_diff >= 2:
        return RiskProfile(
            variance_penalty=2.0,
            retaliation_weight=2.2,
            aggression_bonus=0.8,
            deck_conservation=1.2,
            mode="AHEAD_LOCK_IN",
        )

    # 4. Substantial Prize Deficit (Behind)
    elif prize_diff <= -2:
        return RiskProfile(
            variance_penalty=0.4,
            retaliation_weight=0.8,
            aggression_bonus=2.0,
            deck_conservation=0.8,
            mode="BEHIND_COMEBACK",
        )

    # 5. Balanced / Standard state
    return RiskProfile(
        variance_penalty=1.0,
        retaliation_weight=1.5,
        aggression_bonus=1.0,
        deck_conservation=1.0,
        mode="BALANCED",
    )
