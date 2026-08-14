import os
import sys
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.scenarios import run_scenario_tests


def test_tactical_scenarios():
    results = run_scenario_tests()
    assert results.get("lethal_knockout") is True, "Agent must execute lethal knockout when available"
    assert results.get("crustle_immunity_avoidance") is True, "Agent must avoid 0-damage attacks on immune Crustle"
    assert results.get("anti_deckout_preservation") is True, "Agent must avoid deckout suicide when deck count is low"
