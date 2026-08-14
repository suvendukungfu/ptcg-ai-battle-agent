from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class GameState:
    """Normalized internal representation of the PTCG game state."""
    raw_obs: Dict[str, Any] = field(default_factory=dict)
    your_index: int = 0
    turn: int = 1
    step: int = 0
    
    # Action context
    select_type: int = -1
    select_context: int = 0
    min_count: int = 1
    max_count: int = 1
    options: List[Dict[str, Any]] = field(default_factory=list)
    
    # Active Turn Flags
    stadium_played: bool = False
    supporter_played: bool = False
    energy_attached: bool = False
    retreated: bool = False
    
    # Own Board State
    your_active: Optional[Dict[str, Any]] = None
    your_bench: List[Dict[str, Any]] = field(default_factory=list)
    your_hand: List[Dict[str, Any]] = field(default_factory=list)
    your_discard: List[Dict[str, Any]] = field(default_factory=list)
    your_prizes: int = 6
    your_deck_count: int = 60
    
    # Opponent Board State (Observable Only)
    opp_active: Optional[Dict[str, Any]] = None
    opp_bench: List[Dict[str, Any]] = field(default_factory=list)
    opp_hand_count: int = 0
    opp_discard: List[Dict[str, Any]] = field(default_factory=list)
    opp_prizes: int = 6
    opp_deck_count: int = 60
    
    # Status Effects
    your_status: Dict[str, bool] = field(default_factory=dict)
    opp_status: Dict[str, bool] = field(default_factory=dict)

    @property
    def total_your_energies(self) -> int:
        count = 0
        if self.your_active:
            energies = self.your_active.get("energies", [])
            count += len(energies) if isinstance(energies, list) else 0
        for b in self.your_bench:
            if b:
                energies = b.get("energies", [])
                count += len(energies) if isinstance(energies, list) else 0
        return count

    @property
    def total_opp_energies(self) -> int:
        count = 0
        if self.opp_active:
            energies = self.opp_active.get("energies", [])
            count += len(energies) if isinstance(energies, list) else 0
        for b in self.opp_bench:
            if b:
                energies = b.get("energies", [])
                count += len(energies) if isinstance(energies, list) else 0
        return count


def parse_game_state(obs: Dict[str, Any]) -> GameState:
    """Parse raw Kaggle observation dictionary into normalized GameState dataclass."""
    state = GameState(raw_obs=obs)
    if not isinstance(obs, dict):
        return state

    state.step = obs.get("step", 0)

    # 1. Parse 'select' context
    select = obs.get("select")
    if isinstance(select, dict):
        state.select_type = select.get("type", -1)
        state.select_context = select.get("context", 0)
        state.min_count = select.get("minCount", 1)
        state.max_count = select.get("maxCount", 1)
        options = select.get("option", [])
        state.options = options if isinstance(options, list) else []

    # 2. Parse 'current' game board state
    current = obs.get("current")
    if not isinstance(current, dict):
        return state

    state.your_index = current.get("yourIndex", 0)
    state.turn = current.get("turn", 1)
    state.stadium_played = current.get("stadiumPlayed", False)
    state.supporter_played = current.get("supporterPlayed", False)
    state.energy_attached = current.get("energyAttached", False)
    state.retreated = current.get("retreated", False)

    players = current.get("players", [])
    if isinstance(players, list) and len(players) > state.your_index:
        yp = players[state.your_index]
        if isinstance(yp, dict):
            active_list = yp.get("active") or []
            state.your_active = active_list[0] if (isinstance(active_list, list) and len(active_list) > 0) else None
            bench_list = yp.get("bench") or []
            state.your_bench = bench_list if isinstance(bench_list, list) else []
            hand_list = yp.get("hand") or []
            state.your_hand = hand_list if isinstance(hand_list, list) else []
            discard_list = yp.get("discard") or []
            state.your_discard = discard_list if isinstance(discard_list, list) else []
            prizes = yp.get("prize") or []
            state.your_prizes = len(prizes) if isinstance(prizes, list) else int(prizes or 0)
            state.your_deck_count = yp.get("deckCount", 60)
            state.your_status = {
                "poisoned": yp.get("poisoned", False),
                "burned": yp.get("burned", False),
                "asleep": yp.get("asleep", False),
                "paralyzed": yp.get("paralyzed", False),
                "confused": yp.get("confused", False),
            }

    opp_index = 1 - state.your_index
    if isinstance(players, list) and len(players) > opp_index:
        op = players[opp_index]
        if isinstance(op, dict):
            opp_active_list = op.get("active") or []
            state.opp_active = opp_active_list[0] if (isinstance(opp_active_list, list) and len(opp_active_list) > 0) else None
            opp_bench_list = op.get("bench") or []
            state.opp_bench = opp_bench_list if isinstance(opp_bench_list, list) else []
            
            # Opponent hand is hidden, handCount is an integer
            hc = op.get("handCount")
            if hc is not None and isinstance(hc, int):
                state.opp_hand_count = hc
            else:
                h_list = op.get("hand")
                state.opp_hand_count = len(h_list) if isinstance(h_list, list) else 0

            opp_discard_list = op.get("discard") or []
            state.opp_discard = opp_discard_list if isinstance(opp_discard_list, list) else []
            opp_prizes = op.get("prize") or []
            state.opp_prizes = len(opp_prizes) if isinstance(opp_prizes, list) else int(opp_prizes or 0)
            state.opp_deck_count = op.get("deckCount", 60)
            state.opp_status = {
                "poisoned": op.get("poisoned", False),
                "burned": op.get("burned", False),
                "asleep": op.get("asleep", False),
                "paralyzed": op.get("paralyzed", False),
                "confused": op.get("confused", False),
            }

    return state
