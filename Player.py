from Rating import Rating
from initial_templates import (initial_stats)

class Player:

    def __init__(self,
                 name, height, weight, position, region, mercuriality, salary,
                 o_reb, finishing, open_mid, open_3, contest_mid, contest_3, playmaking, ft_shoot,
                 d_reb, block, steal,
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

        # Ratings Class Values
        self.o_reb = o_reb
        self.finishing = finishing
        self.open_mid = open_mid
        self.open_3 = open_3
        self.contest_mid = contest_mid
        self.contest_3 = contest_3
        self.playmaking = playmaking
        self.ft_shoot = ft_shoot
        self.d_reb = d_reb
        self.block = block
        self.steal = steal
        self.awareness = awareness
        self.endurance = endurance
        self.contentment = contentment
        self.character = character
        self.confidence = confidence

        # Stats Tracker
        self.stat_block = initial_stats

        # Calculations within class for Overall ratings
        self.overall = self._calculate_overall()
        self.o_ovr = self._calculate_o_overall()
        self.d_ovr = self.calculate_d_overall()

        # Private Methods
        def _calculate_overall(self):
            pass

        def _calculate_o_overall(self):
            pass

        def _calculate_d_overall(self):
            pass

        # Public Methods
        def set_rating(self, new_num, type):
            self.rating.type = new_num

        def set_salary(self, new_num):
            self.salary = new_num

