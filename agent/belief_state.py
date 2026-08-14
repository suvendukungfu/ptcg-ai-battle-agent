import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from agent.state import GameState
from agent.card_database import get_all_cards, get_pokemon_data


@dataclass
class BeliefDistribution:
    """Estimated probability distribution of opponent possessing key tactical cards in hidden hand."""
    p_boss_gust: float = 0.25
    p_energy: float = 0.65
    p_switch: float = 0.35
    p_evolution: float = 0.45
    p_supporter: float = 0.50
    estimated_deck_energies: int = 15
    estimated_deck_gusts: int = 2
    estimated_deck_switches: int = 2
    total_unseen_cards: int = 40
    hand_size: int = 5


class BeliefStateTracker:
    """
    Bayesian Belief State Model.
    Tracks uncertainty over hidden opponent information (hand and prize cards)
    using observable evidence, turn counts, discard pile history, and hypergeometric counting.
    """

    def __init__(self):
        self.turn_count: int = 0
        self.discard_seen: Dict[int, int] = {}
        self.board_energies_attached: int = 0
        self.history_actions: List[Dict[str, Any]] = []

    def update_beliefs(self, state: GameState) -> BeliefDistribution:
        """
        Compute posterior probabilities of opponent possessing key tactical assets in hand.
        """
        self.turn_count = getattr(state, "turn", 1)
        opp_hand = getattr(state, "opp_hand_count", 0) or getattr(state, "opponent_hand_count", 0)
        hand_size = opp_hand if opp_hand > 0 else 5

        opp_deck = getattr(state, "opp_deck_count", 0) or getattr(state, "opponent_deck_count", 0)
        deck_size = max(1, opp_deck if opp_deck > 0 else 40)
        total_unseen = hand_size + deck_size

        # Count visible discarded cards
        discard_counts: Dict[str, int] = {
            "energy": 0,
            "gust": 0,
            "switch": 0,
            "supporter": 0,
            "evolution": 0
        }

        opp_discard = getattr(state, "opp_discard", []) or getattr(state, "opponent_discard", [])
        for item in opp_discard:
            card_id = item.get("id") if isinstance(item, dict) else item
            if card_id == 3:  # Basic Lightning Energy
                discard_counts["energy"] += 1
            elif card_id == 1262:  # Boss's Orders
                discard_counts["gust"] += 1
            elif card_id == 1145:  # Switch
                discard_counts["switch"] += 1
            elif card_id in (1092, 1262):
                discard_counts["supporter"] += 1

        # Count energies visible on board
        opp_active = getattr(state, "opp_active", None) or getattr(state, "opponent_active", None)
        board_energies = 0
        if opp_active:
            e_list = opp_active.get("energies", []) if isinstance(opp_active, dict) else getattr(opp_active, "energies", [])
            board_energies += len(e_list)

        opp_bench = getattr(state, "opp_bench", []) or getattr(state, "opponent_bench", [])
        for b in opp_bench:
            e_list = b.get("energies", []) if isinstance(b, dict) else getattr(b, "energies", [])
            board_energies += len(e_list)

        # Assumed typical deck composition bounds (Standard archetype priors)
        prior_energies = 18
        prior_gusts = 2
        prior_switches = 2
        prior_evolutions = 6
        prior_supporters = 6

        # Calculate remaining unseen copies in (deck + hand)
        remaining_energies = max(0, prior_energies - discard_counts["energy"] - board_energies)
        remaining_gusts = max(0, prior_gusts - discard_counts["gust"])
        remaining_switches = max(0, prior_switches - discard_counts["switch"])
        remaining_supporters = max(0, prior_supporters - discard_counts["supporter"])

        # Hypergeometric probability: P(at least 1 copy in hand of size k drawn from N unseen)
        p_energy = self._hypergeometric_at_least_one(total_unseen, remaining_energies, hand_size)
        p_gust = self._hypergeometric_at_least_one(total_unseen, remaining_gusts, hand_size)
        p_switch = self._hypergeometric_at_least_one(total_unseen, remaining_switches, hand_size)
        p_supporter = self._hypergeometric_at_least_one(total_unseen, remaining_supporters, hand_size)

        # Evolution belief based on basic pokemons on bench
        unEvolved_basics = 0
        if opp_active:
            cid = opp_active.get("id") if isinstance(opp_active, dict) else getattr(opp_active, "id", 0)
            if cid in (721,):
                unEvolved_basics += 1
        for b in opp_bench:
            cid = b.get("id") if isinstance(b, dict) else getattr(b, "id", 0)
            if cid in (721,):
                unEvolved_basics += 1

        p_evolution = self._hypergeometric_at_least_one(total_unseen, min(remaining_energies, prior_evolutions), hand_size) if unEvolved_basics > 0 else 0.15

        return BeliefDistribution(
            p_boss_gust=round(p_gust, 3),
            p_energy=round(p_energy, 3),
            p_switch=round(p_switch, 3),
            p_evolution=round(p_evolution, 3),
            p_supporter=round(p_supporter, 3),
            estimated_deck_energies=remaining_energies,
            estimated_deck_gusts=remaining_gusts,
            estimated_deck_switches=remaining_switches,
            total_unseen_cards=total_unseen,
            hand_size=hand_size,
        )

    @staticmethod
    def _hypergeometric_at_least_one(N: int, K: int, n: int) -> float:
        """Calculate hypergeometric probability P(X >= 1)."""
        if N <= 0 or K <= 0 or n <= 0:
            return 0.0
        if K >= N or n >= N:
            return 1.0

        try:
            p_zero = math.comb(N - K, n) / math.comb(N, n)
            return max(0.0, min(1.0, 1.0 - p_zero))
        except (ValueError, ZeroDivisionError):
            return 0.5
