"""
Scripted Adversarial Research Opponent: Alakazam Non-EX.
Aggressively sets up Abra -> Kadabra -> Alakazam, executes draw abilities,
attaches Psychic energy, and launches high-damage Mind Jack attacks.
"""

from typing import Dict, Any, List, Optional
import json
from agent.state import GameState, parse_game_state


def scripted_alakazam_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
    """
    Expert scripted pilot for Alakazam Stage 2 Non-EX deck.
    """
    raw_current = obs.get("current", "{}")
    if isinstance(raw_current, str):
        try:
            cur_dict = json.loads(raw_current)
        except Exception:
            cur_dict = {}
    else:
        cur_dict = raw_current

    state = parse_game_state(cur_dict)
    options = state.options
    n_opts = len(options)
    if n_opts == 0:
        return [0]

    min_cnt = max(1, state.min_count)
    max_cnt = min(n_opts, max(1, state.max_count))
    select_type = state.select_type

    # Case A: Main Turn Decision (select_type == 0)
    if select_type == 0:
        # 1. Attack if ready and lethal/advantageous
        for idx, opt in enumerate(options):
            if isinstance(opt, dict) and opt.get("type") in (9, 10) or "attack" in str(opt).lower():
                return [idx]

        # 2. Abilities: Kadabra/Alakazam Psychic Draw, Dudunsparce Run Away Draw
        for idx, opt in enumerate(options):
            if isinstance(opt, dict) and opt.get("type") == 7:  # Ability
                return [idx]

        # 3. Evolution: Evolve into Alakazam (743) or Kadabra (742) or Dudunsparce (66)
        for idx, opt in enumerate(options):
            if isinstance(opt, dict):
                cid = opt.get("id", 0)
                opt_type = opt.get("type", -1)
                if cid in (743, 742, 66) or opt_type in (3, 4):
                    return [idx]

        # 4. Search / Setup Items: Buddy-Buddy Poffin, Rare Candy, Ultra Ball, Nest Ball, Research
        for idx, opt in enumerate(options):
            if isinstance(opt, dict):
                cid = opt.get("id", 0)
                if cid in (1182, 1227, 1121, 1092, 1262):
                    return [idx]

        # 5. Play Basic to Bench: Abra (741), Dunsparce (65)
        for idx, opt in enumerate(options):
            if isinstance(opt, dict):
                cid = opt.get("id", 0)
                if cid in (741, 65) or opt.get("type") in (0, 1, 2):
                    return [idx]

        # 6. Energy Attachment: Attach to Active or Benched Alakazam/Kadabra/Abra
        for idx, opt in enumerate(options):
            if isinstance(opt, dict) and opt.get("type") == 8:  # Energy attachment
                return [idx]

        # 7. Pass / End Turn (Option 0)
        return [0]

    # Case B: Selection / Search Prompt (select_type != 0)
    # Prioritize key pieces: Alakazam (743), Kadabra (742), Abra (741), Rare Candy (1227), Dunsparce (65), Energy
    scored_indices = []
    for idx, opt in enumerate(options):
        score = 0.0
        if isinstance(opt, dict):
            cid = opt.get("id", 0)
            if cid == 743:
                score = 100.0
            elif cid == 742:
                score = 80.0
            elif cid == 741:
                score = 70.0
            elif cid == 1227:  # Rare candy
                score = 90.0
            elif cid == 65:  # Dunsparce
                score = 60.0
            elif cid in (1, 2, 3, 4, 5, 6, 7, 8):  # Energy
                score = 50.0
            else:
                score = 20.0
        else:
            score = 10.0
        scored_indices.append((idx, score))

    scored_indices.sort(key=lambda x: x[1], reverse=True)
    selected = [idx for idx, _ in scored_indices[:min_cnt]]
    return selected if selected else [0]
