import os
import sys
sys.path.insert(0, os.path.abspath("."))
from agent.card_database import init_card_database, get_attack_data

init_card_database()
print("Rillaboom (112, 113):", get_attack_data(91))
