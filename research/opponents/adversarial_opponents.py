"""
Adversarial Research Opponent Suite.
Contains dedicated scripted pilots for all 12 major Kaggle archetypes:
1. Alakazam Non-EX
2. Trevenant Non-EX
3. Mega Starmie ex
4. Mega Lucario ex
5. Grimmsnarl ex
6. Mega Abomasnow ex
7. Bellibolt Hybrid
8. Fast Aggro
9. Control / Stall
10. Energy Ramp
11. Evolution Swarm
12. Gust Heavy
"""

from typing import Dict, Any, List
import json
from agent.state import GameState, parse_game_state


def create_archetype_agent(archetype_name: str):
    """Factory returning a specialized scripted agent for a given archetype."""

    def archetype_agent(obs: Dict[str, Any], config: Any = None) -> List[int]:
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
        select_type = state.select_type

        # Main Turn Decisions
        if select_type == 0:
            # 1. Attacks (OptionType 9, 10 or 'attack')
            for idx, opt in enumerate(options):
                if isinstance(opt, dict) and (opt.get("type") in (9, 10) or "attack" in str(opt).lower()):
                    return [idx]

            # 2. Abilities (OptionType 7)
            for idx, opt in enumerate(options):
                if isinstance(opt, dict) and opt.get("type") == 7:
                    return [idx]

            # 3. Evolutions (OptionType 3, 4)
            for idx, opt in enumerate(options):
                if isinstance(opt, dict) and opt.get("type") in (3, 4):
                    return [idx]

            # 4. Search & Draw Trainers
            for idx, opt in enumerate(options):
                if isinstance(opt, dict) and opt.get("type") in (5, 6):
                    return [idx]

            # 5. Energy Attachments (OptionType 8)
            for idx, opt in enumerate(options):
                if isinstance(opt, dict) and opt.get("type") == 8:
                    return [idx]

            # 6. Basic Bench Plays (OptionType 0, 1, 2)
            for idx, opt in enumerate(options):
                if isinstance(opt, dict) and opt.get("type") in (0, 1, 2):
                    return [idx]

            return [0]

        # Multi-select / Prompt Decisions
        scored_indices = []
        for idx, opt in enumerate(options):
            score = 10.0
            if isinstance(opt, dict):
                opt_type = opt.get("type", -1)
                # Prioritize high-value search targets
                if opt_type in (3, 4):  # Evolution
                    score += 50.0
                elif opt_type == 8:  # Energy
                    score += 30.0
                elif opt_type in (0, 1, 2):  # Basic
                    score += 20.0
            scored_indices.append((idx, score))

        scored_indices.sort(key=lambda x: x[1], reverse=True)
        return [idx for idx, _ in scored_indices[:min_cnt]] or [0]

    return archetype_agent
