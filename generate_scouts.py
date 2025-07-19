from pools import *
from Scout import *
from lists_and_dicts import *
from helper_functions import *

# Generates an established initial scout pool
def generate_initial_scouts():
    for region in regions:
        for i in range(10):
            if region not in names:
                first_name = names['America']['First'][generate_random_int(0, 99)]
                last_name = names['America']['Last'][generate_random_int(0, 99)]
            else:
                first_name = names[region]['First'][generate_random_int(0, 59)]
                last_name = names[region]['Last'][generate_random_int(0, 59)]
            name = first_name + ' ' + last_name

            if i < 4:
                specialty = "Offense"
            elif i >= 4 and i < 7:
                specialty = "Defense"
            else:
                specialty = "Intangibles"

            level = scout_levels[generate_random_int(0, 4)]

            scout = Scout(name, region, specialty, level)

            available_scouts.append(scout)


# Generates random scout to add scouts to the pool every year
def generate_random_scout():
    region = regions[generate_random_int(0, 9)]

    if region not in names:
        first_name = names['America']['First'][generate_random_int(0, 99)]
        last_name = names['America']['Last'][generate_random_int(0, 99)]
    else:
        first_name = names[region]['First'][generate_random_int(0, 59)]
        last_name = names[region]['Last'][generate_random_int(0, 59)]
    name = first_name + ' ' + last_name

    specialty = scout_specialties[generate_random_int(0, 2)]

    level = scout_levels[generate_random_int(0, 4)]

    scout = Scout(name, region, specialty, level)

    available_scouts.append(scout)