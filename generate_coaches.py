from pools import *
from possible_coaches import *

def generate_initial_coaching_pool():
    for _ in range(20):
        index = generate_random_int(0, len(all_coaches) - 1)
        coach = all_coaches.pop(index)
        available_coaches.append(coach)

def generate_new_coaches():
    for _ in range(2):
        index = generate_random_int(0, len(all_coaches) - 1)
        coach = all_coaches.pop(index)
        available_coaches.append(coach)