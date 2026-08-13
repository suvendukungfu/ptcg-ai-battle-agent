from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class GameState:
    your_index: int = 0
    opp_index: int = 1
    turn: int = 0
    your_prizes: int = 6
    opp_prizes: int = 6
    prize_diff: int = 0
    prize_race: str = "even"  # "match_point", "behind", "ahead", "even"
    your_active: Optional[Dict[str, Any]] = None
    opp_active: Optional[Dict[str, Any]] = None
    your_bench: List[Dict[str, Any]] = field(default_factory=list)
    opp_bench: List[Dict[str, Any]] = field(default_factory=list)
    your_hand: List[Dict[str, Any]] = field(default_factory=list)
    your_discard: List[Dict[str, Any]] = field(default_factory=list)
    your_deck_count: int = 0
    opp_deck_count: int = 0
    stadium: Optional[Dict[str, Any]] = None
    energy_attached: bool = False
    supporter_played: bool = False
    stadium_played: bool = False
    retreated: bool = False
    select_type: int = 0
    select_context: int = 0
    min_count: int = 1
    max_count: int = 1
    options: List[Dict[str, Any]] = field(default_factory=list)


def parse_game_state(obs: Dict[str, Any]) -> GameState:
    """Parse raw observation dict into structured GameState object."""
    if not isinstance(obs, dict):
        return GameState()

    select = obs.get("select") or {}
    current = obs.get("current") or {}
    players = current.get("players") or [{}, {}]

    your_idx = current.get("yourIndex", 0)
    opp_idx = 1 - your_idx

    p_your = players[your_idx] if len(players) > your_idx else {}
    p_opp = players[opp_idx] if len(players) > opp_idx else {}

    # Prize count parsing
    your_prize_cards = p_your.get("prize") or []
    opp_prize_cards = p_opp.get("prize") or []
    
    your_prizes = len(your_prize_cards) if isinstance(your_prize_cards, list) else 6
    opp_prizes = len(opp_prize_cards) if isinstance(opp_prize_cards, list) else 6

    prize_diff = opp_prizes - your_prizes

    if your_prizes == 1:
        prize_race = "match_point"
    elif prize_diff > 0:
        prize_race = "ahead"
    elif prize_diff < 0:
        prize_race = "behind"
    else:
        prize_race = "even"

    # Active & Bench parsing
    your_active_list = p_your.get("active") or []
    opp_active_list = p_opp.get("active") or []

    your_active = your_active_list[0] if (isinstance(your_active_list, list) and len(your_active_list) > 0 and your_active_list[0]) else None
    opp_active = opp_active_list[0] if (isinstance(opp_active_list, list) and len(opp_active_list) > 0 and opp_active_list[0]) else None

    your_bench_list = p_your.get("bench") or []
    opp_bench_list = p_opp.get("bench") or []

    your_bench = [card for card in your_bench_list if card] if isinstance(your_bench_list, list) else []
    opp_bench = [card for card in opp_bench_list if card] if isinstance(opp_bench_list, list) else []

    # Options parsing
    options_list = select.get("option") or []
    options = [opt for opt in options_list if isinstance(opt, dict)] if isinstance(options_list, list) else []

    min_cnt = select.get("minCount", 1)
    max_cnt = select.get("maxCount", 1)

    return GameState(
        your_index=your_idx,
        opp_index=opp_idx,
        turn=current.get("turn", 0),
        your_prizes=your_prizes,
        opp_prizes=opp_prizes,
        prize_diff=prize_diff,
        prize_race=prize_race,
        your_active=your_active,
        opp_active=opp_active,
        your_bench=your_bench,
        opp_bench=opp_bench,
        your_hand=p_your.get("hand") or [],
        your_discard=p_your.get("discard") or [],
        your_deck_count=p_your.get("deckCount", 0),
        opp_deck_count=p_opp.get("deckCount", 0),
        stadium=current.get("stadium"),
        energy_attached=bool(current.get("energyAttached", False)),
        supporter_played=bool(current.get("supporterPlayed", False)),
        stadium_played=bool(current.get("stadiumPlayed", False)),
        retreated=bool(current.get("retreated", False)),
        select_type=select.get("type", 0),
        select_context=select.get("context", 0),
        min_count=min_cnt if isinstance(min_cnt, int) and min_cnt >= 0 else 1,
        max_count=max_cnt if isinstance(max_cnt, int) and max_cnt >= 1 else 1,
        options=options,
    )
