from Rating import Rating
from initial_templates import (initial_stats_block, initial_amateur_stats)
from rating_weights import *

class Player:

    def __init__(self,
                 name, height, weight, position, region, mercuriality, salary, age,
                 o_reb, finishing, open_mid, open_3, contest_mid, contest_3, playmaking, ft_shoot,
                 d_reb, block, steal, stickiness,
                 awareness, endurance, confidence,
                 contentment, character):

        # Static Values
        self.name = name
        self.height = height
        self.weight = weight
        self.position = position
        self.region = region
        self.mercuriality = mercuriality
        self.salary = salary
        self.age = age

        # Ratings Class Values
        # Offensive Ratings
        self.o_reb = o_reb
        self.finishing = finishing
        self.open_mid = open_mid
        self.open_3 = open_3
        self.contest_mid = contest_mid
        self.contest_3 = contest_3
        self.playmaking = playmaking
        self.ft_shoot = ft_shoot
        # Defensive Ratings
        self.d_reb = d_reb
        self.block = block
        self.steal = steal
        self.stickiness = stickiness
        # Intangible Ratings On-Court (generally)
        self.awareness = awareness
        self.endurance = endurance
        self.confidence = confidence
        # Intangibles Ratings Off-Court
        self.contentment = contentment
        self.character = character

        # Calculations within class for Overall ratings
        self.o_ovr = self._calculate_o_overall()
        self.d_ovr = self._calculate_d_overall()
        self.intangibles_ovr = self._calculate_intangibles_overall()
        self.overall = self._calculate_overall()

        # Prospect Stats in Amateur Leagues
        self.amateur_stats = self._calculate_amateur_stats()

        # Stats Tracker
        self.stat_block = initial_stats_block

        # Initializes stamina meter to be changed mid-game
        self.stamina = 99

    # Private Methods
    def _calculate_o_overall(self):
        if self._position == 'PG':
            weight = pg_weight_offense
        elif self._position == 'SG':
            weight = sg_weight_offense
        elif self._position == 'SF':
            weight = sf_weight_offense
        elif self._position == 'PF':
            weight = pf_weight_offense
        else:
            weight = c_weight_offense

        return round((self.o_reb * weight['o_reb']) + (self.finishing * weight['finishing']) + \
            (self.open_mid * weight['open_mid']) + (self.open_3 * weight['open_3']) + \
            (self.contest_mid * weight['contest_mid']) + (self.contest_3 * weight['contest_3']) + \
            (self.playmaking * weight['playmaking']) + (self.ft_shoot * weight['ft_shoot']))

    def _calculate_d_overall(self):
        if self.position == 'PG' or self.position == 'SG':
            weight = g_weight_defense
        elif self.position == 'SF' or self.position == 'PF':
            weight = f_weight_defense
        else:
            weight = c_weight_defense

        return round((self.d_reb * weight['d_reb']) + (self.block * weight['block']) + \
            (self.steal * weight['steal']) + (self.stickiness * weight['stickiness']))

    def _calculate_intangibles_overall(self):
        return round((self.awareness * intangibles_weight['awareness']) + \
            (self.endurance * intangibles_weight['endurance']) + (self.confidence * intangibles_weight['confidence']))

    def _calculate_overall(self):
        return round((self.o_ovr * .45) + (self.d_ovr * .45) + (self.intangibles_ovr * .1))

    def _calculate_amateur_stats(self):
        amateur_stats = initial_amateur_stats
        return amateur_stats

    # Public Methods
    def set_rating(self, new_num, kind):
        self.rating.kind = new_num

    def set_salary(self, new_num):
        self.salary = new_num

    def increment_age(self):
        self.age += 1

