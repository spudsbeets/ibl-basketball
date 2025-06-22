from lists_and_dicts import *
from Team import *
from helper_functions import *

def generate_team():
    region = regions[generate_random_int(0, 9)]
    city = cities[region][generate_random_int(0, 4)]
    nickname = nicknames[generate_random_int(0, len(nicknames))]
    logo = nickname
    colors = color_schemes[generate_random_int(0, len(color_schemes))]

    return Team(nickname, city, region, logo, colors)


# TESTING
temp_team_pool = []

for _ in range(15):
    temp_team_pool.append(generate_team())

for team in temp_team_pool:
    print({
        'name': team.nickname,
        'city': team.city,
        'region': team.region,
        'logo': team.logo,
        'colors': team.colors
    })