from Rating import Rating
from initial_templates import (initial_stats_block, initial_amateur_stats)

class Player:

    def __init__(self,
                 name, height, weight, position, region, mercuriality, salary, age,
                 o_reb, finishing, open_mid, open_3, contest_mid, contest_3, playmaking, ft_shoot,
                 d_reb, block, steal, stickiness,
                 awareness, endurance,
                 contentment, character, confidence):

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
        # Both Sides Ratings
        self.awareness = awareness
        self.endurance = endurance
        # Intangibles Ratings
        self.contentment = contentment
        self.character = character
        self.confidence = confidence

        # Calculations within class for Overall ratings
        self.overall = self._calculate_overall()
        self.o_ovr = self._calculate_o_overall()
        self.d_ovr = self.calculate_d_overall()

        # Prospect Stats in Amateur Leagues
        self.amateur_stats = self._calculate_amateur_stats()

        # Stats Tracker
        self.stat_block = initial_stats_block

        # Private Methods
        def _calculate_overall(self):
            pass

        def _calculate_o_overall(self):
            pass

        def _calculate_d_overall(self):
            pass

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

