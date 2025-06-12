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

# START WORKIN HERE BISH
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

# testing
def does_equal_1(obj):
    count = 0
    for i in obj:
        count += obj[i]
    if count == 1:
        return True
    else:
        return count


print(does_equal_1(sf_weight_offense))