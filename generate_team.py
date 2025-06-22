from lists_and_dicts import *
from Team import *
from helper_functions import *

def generate_team():
    region = regions[generate_random_int(0, len(regions) - 1)]
    city = cities[region][generate_random_int(0, 4)]
    nickname = nicknames[generate_random_int(0, len(nicknames) - 1)]
    logo = nickname
    colors = color_schemes[generate_random_int(0, len(color_schemes) - 1)]

    return Team(nickname, city, region, logo, colors)