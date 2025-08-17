from generate_prospect_pool import *
from generate_league import *
from pools import *
from generate_scouts import *
from generate_coaches import *

generate_entry_draft_class()

generate_league()

generate_initial_coaching_pool()

sorted_pool = sorted(prospect_pool, key=lambda x: x.overall)

team1 = teams[0]
team2 = teams[1]