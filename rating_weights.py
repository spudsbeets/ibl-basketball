pg_weight_offense = {
    'o_reb': .05,
    'finishing': .15,
    'open_mid': .11,
    'open_3': .11,
    'contest_mid': .1,
    'contest_3': .1,
    'playmaking': .28,
    'ft_shoot': .1
}

sg_weight_offense = {
    'o_reb': .05,
    'finishing': .12,
    'open_mid': .16,
    'open_3': .16,
    'contest_mid': .14,
    'contest_3': .14,
    'playmaking': .13,
    'ft_shoot': .1
}

sf_weight_offense = {
    'o_reb': .1,
    'finishing': .18,
    'open_mid': .14,
    'open_3': .12,
    'contest_mid': .14,
    'contest_3': .12,
    'playmaking': .1,
    'ft_shoot': .1
}

pf_weight_offense = {
    'o_reb': .15,
    'finishing': .21,
    'open_mid': .13,
    'open_3': .1,
    'contest_mid': .13,
    'contest_3': .1,
    'playmaking': .08,
    'ft_shoot': .1
}

c_weight_offense = {
    'o_reb': .2,
    'finishing': .25,
    'open_mid': .11,
    'open_3': .09,
    'contest_mid': .11,
    'contest_3': .09,
    'playmaking': .05,
    'ft_shoot': .1
}

g_weight_defense = {
    'd_reb': .15,
    'block': .15,
    'steal': .3,
    'stickiness': .4
}

f_weight_defense = {
    'd_reb': .25,
    'block': .25,
    'steal': .2,
    'stickiness': .3
}

c_weight_defense = {
    'd_reb': .35,
    'block': .35,
    'steal': .15,
    'stickiness': .15
}

intangibles_weight = {
    'awareness': .34,
    'endurance': .33,
    'confidence': .33,
}

# testing
def does_equal_1(obj):
    count = 0
    for i in obj:
        count += obj[i]
    if count == 1:
        return True
    else:
        return count