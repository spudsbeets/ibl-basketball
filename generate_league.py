from pools import *
from lists_and_dicts import *
from Team import *
from helper_functions import *

def generate_league():
    used_nicknames = set()
    while len(teams) < 16:
        region = regions[generate_random_int(0, len(regions) - 1)]
        city = cities[region][generate_random_int(0, 4)]
        nickname = nicknames[generate_random_int(0, len(nicknames) - 1)]
        if nickname in used_nicknames:
            continue
        logo = nickname
        colors = color_schemes[generate_random_int(0, len(color_schemes) - 1)]

        team = Team(nickname, city, region, logo, colors)
        teams.append(team)
        used_nicknames.add(nickname)
