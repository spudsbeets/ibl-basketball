from Player import *
from Rating import *
from helper_functions import generate_random_int
from lists_and_dicts import *

def generate_entry_draft_player():
    region = regions[generate_random_int(0, len(regions) - 1)]
    position = positions[generate_random_int(0, len(positions) - 1)]

    if names[region] not in names:
        first_name = names['America']['First'][generate_random_int(0, 99)]
        last_name = names['America']['Last'][generate_random_int(0, 99)]
    else:
        first_name = names[region]['First'][generate_random_int(0, 59)]
        last_name = names[region]['Last'][generate_random_int(0, 59)]

    player_name = first_name + last_name

    height = generate_random_int(heights[position]['low'], heights[position]['high'])
    weight = generate_random_int(weights[position]['low'], weights[position]['high'])

    mercuriality = intangibles[generate_random_int(0, 4)]
    character = intangibles[generate_random_int(0, 4)]

    # FIGURE OUT GENERATING RATINGS
    o_reb = None

    return Player(player_name, height, weight, position, region, 0, generate_random_int(19, 35),
                  mercuriality, 'Neutral', character)

def generate_normal_draft_player():
    pass