import random
from pools import available_coaches, prospect_pool


def generate_random_int(lo, hi):
    return random.randint(lo, hi)

def calculate_midpoint(lo, hi):
    return (lo + hi) // 2

def get_sorted_coaches():
    return sorted(available_coaches, key=lambda c: c.coach_overall, reverse=True)

def get_sorted_players():
    return sorted(prospect_pool, key=lambda p: p.overall, reverse=True)