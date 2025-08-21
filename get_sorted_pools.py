from pools import *

def get_sorted_coaches():
    return sorted(available_coaches, key=lambda c: c.coach_overall, reverse=True)

def get_sorted_players():
    return sorted(prospect_pool, key=lambda p: p.overall, reverse=True)

def get_sorted_team_roster(roster):
    return sorted(roster, key=lambda p: p.overall, reverse=True)