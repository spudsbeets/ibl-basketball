from numpy.random import normal

from Player import *
from Rating import *
from helper_functions import generate_random_int, calculate_midpoint
from lists_and_dicts import *
from randomized_ratings_spans import entry_draft_rating_spans, normal_draft_rating_spans


def generate_entry_draft_player():
    region = regions[generate_random_int(0, len(regions) - 1)]
    position = positions[generate_random_int(0, len(positions) - 1)]

    if region not in names:
        first_name = names['America']['First'][generate_random_int(0, 99)]
        last_name = names['America']['Last'][generate_random_int(0, 99)]
    else:
        first_name = names[region]['First'][generate_random_int(0, 59)]
        last_name = names[region]['Last'][generate_random_int(0, 59)]

    player_name = first_name + " " + last_name

    height = generate_random_int(heights[position]['low'], heights[position]['high'])
    weight = generate_random_int(weights[position]['low'], weights[position]['high'])

    mercuriality = intangibles[generate_random_int(0, 4)]
    character = intangibles[generate_random_int(0, 4)]

    # Determine Build by height/weight
    height_mid = calculate_midpoint(heights[position]['low'], heights[position]['high'])
    weight_mid = calculate_midpoint(weights[position]['low'], weights[position]['high'])

    if height <= height_mid and weight <= weight_mid:
        build = 'short/slight'
    elif height <= height_mid and weight > weight_mid:
        build = 'short/thick'
    elif height > height_mid and weight <= weight_mid:
        build = 'tall/slight'
    else:
        build = 'tall/thick'

    age = generate_random_int(19, 35)

    # Younger players have more room to grow
    if age < 24:
        span = normal_draft_rating_spans
    else:
        span = entry_draft_rating_spans

    # Older players are slightly lacking athletically
    if age > 31:
        strength = Rating('strength', generate_random_int(span[position][build]['strength']['low'],
                                                          round(span[position][build]['strength']['high'] * .85)), 0, 99)
        speed = Rating('speed', generate_random_int(span[position][build]['speed']['low'],
                                                          round(span[position][build]['speed']['high'] * .85)), 0, 99)
    else:
        strength = Rating('strength', generate_random_int(span[position][build]['strength']['low'],
                                                          span[position][build]['strength']['high']), 0, 99)
        speed = Rating('speed', generate_random_int(span[position][build]['speed']['low'],
                                                    span[position][build]['speed']['high']), 0, 99)

    # If player is strong, boost rebounding and finishing stats
    if strength.curr_rating > round(span[position][build]['strength']['high'] * .65):
        o_reb = Rating('o_reb', generate_random_int(round(span[position][build]['o_reb']['high'] * .6),
                                                    span[position][build]['o_reb']['high']), 0, 99)
        d_reb = Rating('d_reb', generate_random_int(round(span[position][build]['d_reb']['high'] * .6),
                                                    span[position][build]['d_reb']['high']), 0, 99)
        finishing = Rating('finishing', generate_random_int(round(span[position][build]['finishing']['high'] * .6),
                                                    span[position][build]['finishing']['high']), 0, 99)
    else:
        o_reb = Rating('o_reb', generate_random_int(span[position][build]['o_reb']['low'],
                                                    round(span[position][build]['o_reb']['high'] * .75)), 0, 99)
        d_reb = Rating('d_reb', generate_random_int(span[position][build]['d_reb']['low'],
                                                    round(span[position][build]['d_reb']['high'] * .75)), 0, 99)
        finishing = Rating('finishing', generate_random_int(span[position][build]['finishing']['low'],
                                                    round(span[position][build]['finishing']['high'] * .75)), 0, 99)

    open_mid = Rating('open_mid', generate_random_int(span[position][build]['finishing']['low'],
                                                      span[position][build]['open_mid']['high']), 0, 99)

    # If player is generally good shooter, boost shooting stats
    if open_mid.curr_rating > round(span[position][build]['open_mid']['high'] * .75):
        open_3 = Rating('open_3', generate_random_int(round(span[position][build]['open_3']['high'] * .6),
                                                      span[position][build]['open_3']['high']), 0, 99)
        contest_mid = Rating('contest_mid', generate_random_int(round(span[position][build]['contest_mid']['high'] * .6),
                                                 span[position][build]['contest_mid']['high']), 0, 99)
        contest_3 = Rating('contest_3', generate_random_int(round(span[position][build]['contest_3']['high'] * .6),
                                                            span[position][build]['contest_3']['high']), 0, 99)
        ft_shoot = Rating('ft_shoot', generate_random_int(round(span[position][build]['ft_shoot']['high'] * .6),
                                                            span[position][build]['ft_shoot']['high']), 0, 99)
    else:
        open_3 = Rating('open_3', generate_random_int(span[position][build]['open_3']['low'],
                                                      round(span[position][build]['open_3']['high'] * .75)), 0, 99)
        contest_mid = Rating('contest_mid', generate_random_int(span[position][build]['contest_mid']['low'],
                                                                round(span[position][build]['contest_mid'][
                                                                          'high'] * .75)), 0, 99)
        contest_3 = Rating('contest_3', generate_random_int(span[position][build]['contest_3']['low'],
                                                            round(span[position][build]['contest_3']['high'] * .75)), 0,99)
        ft_shoot = Rating('ft_shoot', generate_random_int(span[position][build]['ft_shoot']['low'],
                                                            round(span[position][build]['ft_shoot']['high'] * .75)), 0,99)

    # If player is fast, boost stickiness and endurance
    if speed.curr_rating > round(span[position][build]['speed']['high'] * .65):
        stickiness = Rating('stickiness', generate_random_int(round(span[position][build]['stickiness']['high'] * .6),
                                                      span[position][build]['stickiness']['high']), 0, 99)
        endurance = Rating('endurance', generate_random_int(round(span[position][build]['endurance']['high'] * .6),
                                                      span[position][build]['endurance']['high']), 0, 99)
    else:
        stickiness = Rating('stickiness', generate_random_int(span[position][build]['stickiness']['low'],
                                                            round(span[position][build]['stickiness']['high'] * .75)), 0,99)
        endurance = Rating('endurance', generate_random_int(span[position][build]['endurance']['low'],
                                                            round(span[position][build]['endurance']['high'] * .75)), 0,99)

    awareness = Rating('awareness', generate_random_int(span[position][build]['awareness']['low'],
                                                        span[position][build]['awareness']['high']), 0, 99)

    # If player is really smart, boost playmaking, block, and steal
    if awareness.curr_rating > round(span[position][build]['awareness']['high'] * .65):
        playmaking = Rating('playmaking', generate_random_int(round(span[position][build]['playmaking']['high'] * .6),
                                                              span[position][build]['playmaking']['high']), 0, 99)
        block = Rating('block', generate_random_int(round(span[position][build]['block']['high'] * .6),
                                                              span[position][build]['block']['high']), 0, 99)
        steal = Rating('steal', generate_random_int(round(span[position][build]['steal']['high'] * .6),
                                                              span[position][build]['steal']['high']), 0, 99)
    else:
        playmaking = Rating('playmaking', generate_random_int(span[position][build]['playmaking']['low'],
                                                            round(span[position][build]['playmaking']['high'] * .75)), 0,99)
        block = Rating('block', generate_random_int(span[position][build]['block']['low'],
                                                            round(span[position][build]['block']['high'] * .75)), 0,99)
        steal = Rating('steal', generate_random_int(span[position][build]['steal']['low'],
                                                            round(span[position][build]['steal']['high'] * .75)), 0,99)

    # If player is a super-athlete, boost confidence
    if speed.curr_rating > round(span[position][build]['speed']['high'] * .75) and \
            strength.curr_rating > round(span[position][build]['strength']['high'] * .75):
        confidence = Rating('confidence', generate_random_int(round(span[position][build]['confidence']['high'] * .7),
                                                          span[position][build]['confidence']['high']), 0, 99)
    else:
        confidence = Rating('confidence', generate_random_int(span[position][build]['confidence']['low'],
                                                              span[position][build]['confidence']['high']), 0, 99)


    return Player(player_name, height, weight, position, region, 0, age,
                  mercuriality, 'Neutral', character, o_reb, finishing, open_mid, open_3, contest_mid, contest_3,
                  playmaking, ft_shoot, d_reb, block, steal, stickiness, awareness, endurance, confidence, speed, strength)

def generate_normal_draft_player():
    region = regions[generate_random_int(0, len(regions) - 1)]
    position = positions[generate_random_int(0, len(positions) - 1)]

    if region not in names:
        first_name = names['America']['First'][generate_random_int(0, 99)]
        last_name = names['America']['Last'][generate_random_int(0, 99)]
    else:
        first_name = names[region]['First'][generate_random_int(0, 59)]
        last_name = names[region]['Last'][generate_random_int(0, 59)]

    player_name = first_name + " " + last_name

    height = generate_random_int(heights[position]['low'], heights[position]['high'])
    weight = generate_random_int(weights[position]['low'], weights[position]['high'])

    mercuriality = intangibles[generate_random_int(0, 4)]
    character = intangibles[generate_random_int(0, 4)]

    # Determine Build by height/weight
    height_mid = calculate_midpoint(heights[position]['low'], heights[position]['high'])
    weight_mid = calculate_midpoint(weights[position]['low'], weights[position]['high'])

    if height <= height_mid and weight <= weight_mid:
        build = 'short/slight'
    elif height <= height_mid and weight > weight_mid:
        build = 'short/thick'
    elif height > height_mid and weight <= weight_mid:
        build = 'tall/slight'
    else:
        build = 'tall/thick'

    age = generate_random_int(19, 23)

    # space for potential 'generational' prospect
    if generate_random_int(0, 99) > 90:
        span = entry_draft_rating_spans
    else:
        span = normal_draft_rating_spans

    strength = Rating('strength', generate_random_int(span[position][build]['strength']['low'],
                                                span[position][build]['strength']['high']), 0, 99)

    # If player is strong, boost rebounding and finishing stats
    if strength.curr_rating > round(span[position][build]['strength']['high'] * .65):
        o_reb = Rating('o_reb', generate_random_int(round(span[position][build]['o_reb']['high'] * .6),
                                                    span[position][build]['o_reb']['high']), 0, 99)
        d_reb = Rating('d_reb', generate_random_int(round(span[position][build]['d_reb']['high'] * .6),
                                                    span[position][build]['d_reb']['high']), 0, 99)
        finishing = Rating('finishing', generate_random_int(round(span[position][build]['finishing']['high'] * .6),
                                                    span[position][build]['finishing']['high']), 0, 99)
    else:
        o_reb = Rating('o_reb', generate_random_int(span[position][build]['o_reb']['low'],
                                                    round(span[position][build]['o_reb']['high'] * .75)), 0, 99)
        d_reb = Rating('d_reb', generate_random_int(span[position][build]['d_reb']['low'],
                                                    round(span[position][build]['d_reb']['high'] * .75)), 0, 99)
        finishing = Rating('finishing', generate_random_int(span[position][build]['finishing']['low'],
                                                    round(span[position][build]['finishing']['high'] * .75)), 0, 99)

    open_mid = Rating('open_mid', generate_random_int(span[position][build]['finishing']['low'],
                                                      span[position][build]['open_mid']['high']), 0, 99)

    # If player is generally good shooter, boost shooting stats
    if open_mid.curr_rating > round(span[position][build]['open_mid']['high'] * .75):
        open_3 = Rating('open_3', generate_random_int(round(span[position][build]['open_3']['high'] * .6),
                                                      span[position][build]['open_3']['high']), 0, 99)
        contest_mid = Rating('contest_mid', generate_random_int(round(span[position][build]['contest_mid']['high'] * .6),
                                                 span[position][build]['contest_mid']['high']), 0, 99)
        contest_3 = Rating('contest_3', generate_random_int(round(span[position][build]['contest_3']['high'] * .6),
                                                            span[position][build]['contest_3']['high']), 0, 99)
        ft_shoot = Rating('ft_shoot', generate_random_int(round(span[position][build]['ft_shoot']['high'] * .6),
                                                            span[position][build]['ft_shoot']['high']), 0, 99)
    else:
        open_3 = Rating('open_3', generate_random_int(span[position][build]['open_3']['low'],
                                                      round(span[position][build]['open_3']['high'] * .75)), 0, 99)
        contest_mid = Rating('contest_mid', generate_random_int(span[position][build]['contest_mid']['low'],
                                                                round(span[position][build]['contest_mid'][
                                                                          'high'] * .75)), 0, 99)
        contest_3 = Rating('contest_3', generate_random_int(span[position][build]['contest_3']['low'],
                                                            round(span[position][build]['contest_3']['high'] * .75)), 0,99)
        ft_shoot = Rating('ft_shoot', generate_random_int(span[position][build]['ft_shoot']['low'],
                                                            round(span[position][build]['ft_shoot']['high'] * .75)), 0,99)

    speed = Rating('speed', generate_random_int(span[position][build]['speed']['low'],
                                                span[position][build]['speed']['high']), 0, 99)

    # If player is fast, boost stickiness and endurance
    if speed.curr_rating > round(span[position][build]['speed']['high'] * .65):
        stickiness = Rating('stickiness', generate_random_int(round(span[position][build]['stickiness']['high'] * .6),
                                                      span[position][build]['stickiness']['high']), 0, 99)
        endurance = Rating('endurance', generate_random_int(round(span[position][build]['endurance']['high'] * .6),
                                                      span[position][build]['endurance']['high']), 0, 99)
    else:
        stickiness = Rating('stickiness', generate_random_int(span[position][build]['stickiness']['low'],
                                                            round(span[position][build]['stickiness']['high'] * .75)), 0,99)
        endurance = Rating('endurance', generate_random_int(span[position][build]['endurance']['low'],
                                                            round(span[position][build]['endurance']['high'] * .75)), 0,99)

    awareness = Rating('awareness', generate_random_int(span[position][build]['awareness']['low'],
                                                        span[position][build]['awareness']['high']), 0, 99)

    # If player is really smart, boost playmaking, block, and steal
    if awareness.curr_rating > round(span[position][build]['awareness']['high'] * .65):
        playmaking = Rating('playmaking', generate_random_int(round(span[position][build]['playmaking']['high'] * .6),
                                                              span[position][build]['playmaking']['high']), 0, 99)
        block = Rating('block', generate_random_int(round(span[position][build]['block']['high'] * .6),
                                                              span[position][build]['block']['high']), 0, 99)
        steal = Rating('steal', generate_random_int(round(span[position][build]['steal']['high'] * .6),
                                                              span[position][build]['steal']['high']), 0, 99)
    else:
        playmaking = Rating('playmaking', generate_random_int(span[position][build]['playmaking']['low'],
                                                            round(span[position][build]['playmaking']['high'] * .75)), 0,99)
        block = Rating('block', generate_random_int(span[position][build]['block']['low'],
                                                            round(span[position][build]['block']['high'] * .75)), 0,99)
        steal = Rating('steal', generate_random_int(span[position][build]['steal']['low'],
                                                            round(span[position][build]['steal']['high'] * .75)), 0,99)

    # If player is a super-athlete, boost confidence
    if speed.curr_rating > round(span[position][build]['speed']['high'] * .75) and \
            strength.curr_rating > round(span[position][build]['strength']['high'] * .75):
        confidence = Rating('confidence', generate_random_int(round(span[position][build]['confidence']['high'] * .7),
                                                          span[position][build]['confidence']['high']), 0, 99)
    else:
        confidence = Rating('confidence', generate_random_int(span[position][build]['confidence']['low'],
                                                              span[position][build]['confidence']['high']), 0, 99)


    return Player(player_name, height, weight, position, region, 0, age,
                  mercuriality, 'Neutral', character, o_reb, finishing, open_mid, open_3, contest_mid, contest_3,
                  playmaking, ft_shoot, d_reb, block, steal, stickiness, awareness, endurance, confidence, speed, strength)


# TESTING
temp_player_pool = []

for _ in range(50):
    player = generate_normal_draft_player()
    temp_player_pool.append(player)

sorted_pool = sorted(temp_player_pool, key=lambda x: x.overall)

for player in sorted_pool:
    print({
        'name': player.name,
        'age': player.age,
        'position': player.position,
        'o_reb': player.o_reb.curr_rating,
        'finishing': player.finishing.curr_rating,
        'open_mid': player.open_mid.curr_rating,
        'open_3': player.open_3.curr_rating,
        'contest_mid': player.contest_mid.curr_rating,
        'contest_3': player.contest_3.curr_rating,
        'playmaking': player.playmaking.curr_rating,
        'ft_shoot': player.ft_shoot.curr_rating,
        'd_reb': player.d_reb.curr_rating,
        'block': player.block.curr_rating,
        'steal': player.steal.curr_rating,
        'stickiness': player.stickiness.curr_rating,
        'awareness': player.awareness.curr_rating,
        'endurance': player.endurance.curr_rating,
        'confidence': player.confidence.curr_rating,
        'speed': player.speed.curr_rating,
        'strength': player.strength.curr_rating,
        'overall': player.overall,
        'o_ovr': player.o_ovr,
        'd_ovr': player.d_ovr
    })
