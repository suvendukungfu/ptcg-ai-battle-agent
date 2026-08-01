import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_card, get_card_name, get_all_cards

init_card_database()
all_cards = get_all_cards()

# Inspect Alakazam line and Dudunsparce
for cid in [741, 742, 743, 65, 66, 305, 1079, 1081, 1086, 1097, 1182, 1197, 1225, 1231, 1247, 19, 5]:
    c = get_card(cid)
    if c:
        print(f"Card {cid:4d}: {c.get('name')} | Type: {c.get('cardType')} | HP: {c.get('hp')} | Attacks: {c.get('attacks')} | Skills: {c.get('skills')}")
