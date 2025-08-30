from pools import *

def get_sorted_coaches():
    return sorted(available_coaches, key=lambda c: c.coach_overall, reverse=True)

def get_sorted_players(roster):
    return sorted(roster, key=lambda p: p.overall, reverse=True)

def get_sorted_roster_by_playmaking(roster):
    return sorted(roster, key=lambda p: p.playmaking.curr_rating, reverse=True)

def get_sorted_roster_by_awareness(roster):
    return sorted(roster, key=lambda p: p.awareness.curr_rating, reverse=True)

def get_sorted_roster_by_o_overall(roster):
    return sorted(roster, key=lambda p: p.o_ovr, reverse=True)

def get_sorted_roster_by_d_overall(roster):
    return sorted(roster, key=lambda p: p.d_ovr, reverse=True)

def get_sorted_roster_by_d_reb(roster):
    return sorted(roster, key=lambda p: p.d_reb.curr_rating, reverse=True)

def get_sorted_roster_by_o_reb(roster):
    return sorted(roster, key=lambda p: p.o_reb.curr_rating, reverse=True)

def get_sorted_roster_by_open_3(roster):
    return sorted(roster, key=lambda p: p.open_3.curr_rating, reverse=True)

def get_sorted_roster_by_open_mid(roster):
    return sorted(roster, key=lambda p: p.open_mid.curr_rating, reverse=True)