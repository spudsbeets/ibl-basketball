pg_weight_offense = {
    'o_reb': .05,
    'finishing': .15,
    'post_up': .03,
    'open_mid': .1,
    'open_3': .1,
    'contest_mid': .1,
    'contest_3': .1,
    'playmaking': .27,
    'ft_shoot': .1
}

sg_weight_offense = {
    'o_reb': .05,
    'finishing': .12,
    'post_up': .03,
    'open_mid': .15,
    'open_3': .15,
    'contest_mid': .14,
    'contest_3': .14,
    'playmaking': .12,
    'ft_shoot': .1
}

sf_weight_offense = {
    'o_reb': .1,
    'finishing': .16,
    'post_up': .06,
    'open_mid': .13,
    'open_3': .11,
    'contest_mid': .13,
    'contest_3': .11,
    'playmaking': .1,
    'ft_shoot': .1
}

pf_weight_offense = {
    'o_reb': .14,
    'finishing': .18,
    'post_up': .11,
    'open_mid': .12,
    'open_3': .09,
    'contest_mid': .12,
    'contest_3': .08,
    'playmaking': .06,
    'ft_shoot': .1
}

c_weight_offense = {
    'o_reb': .16,
    'finishing': .22,
    'post_up': .2,
    'open_mid': .09,
    'open_3': .07,
    'contest_mid': .09,
    'contest_3': .07,
    'playmaking': .03,
    'ft_shoot': .07
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