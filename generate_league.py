from generate_team import *
from pools import *

def generate_league():
    for _ in range(15):
        team = generate_team()
        teams.append(team)
