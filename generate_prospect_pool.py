from generate_player import *
from pools import *

def generate_entry_draft_class():
    for _ in range(250):
        player = generate_entry_draft_player()
        prospect_pool.append(player)

def generate_normal_draft_class():
    for _ in range(50):
        player = generate_normal_draft_player()
        prospect_pool.append(player)