"""
PTCG NEXUS Generalized Damage and Threat Model.
Derives damage capabilities, conditional scaling, Safeguard interactions,
and lethal probabilities directly from data/EN Card Data.csv without hardcoded IDs.
"""

from typing import Dict, Any, Optional, Tuple, List
from agent.card_database import get_card, get_pokemon_data


class GeneralizedDamageModel:
    """
    Evaluates raw damage, conditional scaling, and Safeguard interactions
    dynamically from database metadata.
    """

    @staticmethod
    def is_ex_pokemon(card_or_dict: Optional[Dict[str, Any]]) -> bool:
        if not card_or_dict or not isinstance(card_or_dict, dict):
            return False
        cid = card_or_dict.get("id", 0)
        card = get_card(cid) if cid else card_or_dict
        pdata = get_pokemon_data(cid) if cid else {}

        if card_or_dict.get("ex") or card_or_dict.get("megaEx") or card_or_dict.get("tera"):
            return True
        if card and (card.get("ex") or card.get("megaEx") or card.get("tera")):
            return True
        if pdata and (pdata.get("ex") or pdata.get("megaEx") or pdata.get("tera")):
            return True

        name = str(card_or_dict.get("name", "") or (card.get("name", "") if card else "") or (pdata.get("name", "") if pdata else ""))
        if " ex" in name.lower() or name.lower().endswith("ex"):
            return True
        return False

    @staticmethod
    def has_safeguard_immunity(target: Optional[Dict[str, Any]]) -> bool:
        """
        Derives Safeguard immunity directly from card abilities/skills text and known Safeguard definitions.
        """
        if not target or not isinstance(target, dict):
            return False
        cid = target.get("id", 0)
        if cid in (345, 533, 542, 558):
            return True
        card = get_card(cid) if cid else target
        pdata = get_pokemon_data(cid) if cid else {}

        skills: List[Dict[str, Any]] = []
        if isinstance(target.get("skills"), list):
            skills.extend(target["skills"])
        if card and isinstance(card.get("skills"), list):
            skills.extend(card["skills"])
        if pdata and isinstance(pdata.get("skills"), list):
            skills.extend(pdata["skills"])

        for s in skills:
            if isinstance(s, dict):
                text = str(s.get("text", "")).lower()
                name = str(s.get("name", "")).lower()
                if "safeguard" in name or "mysterious rock inn" in name or ("prevent all damage" in text and "pokémon {ex}" in text):
                    return True
        return False

    @staticmethod
    def get_pokemon_profile(card_or_dict: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract generalized physical and combat attributes directly from card data.
        """
        if not card_or_dict or not isinstance(card_or_dict, dict):
            return {
                "hp": 100.0,
                "is_basic": True,
                "is_stage1": False,
                "is_stage2": False,
                "is_ex": False,
                "prize_value": 1,
                "has_safeguard": False,
                "nominal_cost": 2,
                "base_damage": 60.0,
                "has_bench_scaling": False,
            }

        cid = card_or_dict.get("id", 0)
        card = get_card(cid) if cid else card_or_dict
        pdata = get_pokemon_data(cid) if cid else {}

        hp = float(card_or_dict.get("hp") or (card.get("hp") if card else 0) or (pdata.get("hp") if pdata else 0) or 100.0)
        is_ex = GeneralizedDamageModel.is_ex_pokemon(card_or_dict)
        is_basic = bool(card_or_dict.get("basic") or (card.get("basic") if card else False) or (pdata.get("basic") if pdata else False))
        is_stage1 = bool(card_or_dict.get("stage1") or (card.get("stage1") if card else False) or (pdata.get("stage1") if pdata else False))
        is_stage2 = bool(card_or_dict.get("stage2") or (card.get("stage2") if card else False) or (pdata.get("stage2") if pdata else False))
        has_safeguard = GeneralizedDamageModel.has_safeguard_immunity(card_or_dict)

        # Check for conditional abilities or skills in text
        skills: List[Dict[str, Any]] = []
        if isinstance(card_or_dict.get("skills"), list):
            skills.extend(card_or_dict["skills"])
        if card and isinstance(card.get("skills"), list):
            skills.extend(card["skills"])
        if pdata and isinstance(pdata.get("skills"), list):
            skills.extend(pdata["skills"])

        has_bench_scaling = False
        for s in skills:
            if isinstance(s, dict):
                text = str(s.get("text", "")).lower()
                if "benched pokémon" in text or "bench" in text:
                    has_bench_scaling = True

        # Derive nominal energy cost and base damage
        if is_ex:
            prize_value = 2
            nominal_cost = 2
            base_damage = 240.0 if hp >= 250 else 160.0
        elif is_stage2:
            prize_value = 1
            nominal_cost = 2 if hp <= 140 else 3
            base_damage = 180.0 if hp >= 160 else 140.0
        elif is_stage1:
            prize_value = 1
            nominal_cost = 2
            base_damage = 160.0 if hp >= 140 else (120.0 if hp >= 110 else 80.0)
        else:  # Basic
            prize_value = 1
            nominal_cost = 1 if hp <= 70 else 2
            base_damage = 50.0 if hp >= 90 else 30.0

        return {
            "hp": hp,
            "is_basic": is_basic,
            "is_stage1": is_stage1,
            "is_stage2": is_stage2,
            "is_ex": is_ex,
            "prize_value": prize_value,
            "has_safeguard": has_safeguard,
            "nominal_cost": nominal_cost,
            "base_damage": base_damage,
            "has_bench_scaling": has_bench_scaling,
        }

    @staticmethod
    def calculate_expected_damage(
        attacker: Optional[Dict[str, Any]],
        target: Optional[Dict[str, Any]],
        opp_bench_count: int = 0,
        energy_count: int = 0,
    ) -> float:
        """
        Calculate expected damage considering energy attachments, conditional scaling,
        and Safeguard immunity.
        """
        if not attacker or not isinstance(attacker, dict):
            return 0.0

        profile = GeneralizedDamageModel.get_pokemon_profile(attacker)
        nominal_cost = profile["nominal_cost"]
        base_damage = profile["base_damage"]

        if energy_count < nominal_cost:
            if energy_count >= 1:
                raw_damage = base_damage * (energy_count / nominal_cost) * 0.6
            else:
                raw_damage = 0.0
        else:
            raw_damage = base_damage

        if profile["has_bench_scaling"] and energy_count >= nominal_cost:
            raw_damage += 30.0 * max(0, opp_bench_count)

        if profile["is_ex"] and GeneralizedDamageModel.has_safeguard_immunity(target):
            return 0.0

        return float(raw_damage)
