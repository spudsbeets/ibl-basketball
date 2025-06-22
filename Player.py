from Rating import Rating
from initial_templates import *
from rating_weights import *

class Player:

    def __init__(self,
                 name, height, weight, position, region, salary, age, mercuriality, contentment, character,
                 o_reb, finishing, open_mid, open_3, contest_mid, contest_3, playmaking, ft_shoot,
                 d_reb, block, steal, stickiness,
                 awareness, endurance, confidence,
                 speed, strength):

        # Static Values
        self.name = name
        self.height = height
        self.weight = weight
        self.position = position
        self.region = region
        self.salary = salary
        self.age = age

        # Intangibles Ratings Off-Court
        self.mercuriality = mercuriality
        self.contentment = contentment
        self.character = character

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
        # Raw athleticism ratings
        self.speed = speed
        self.strength = strength

        # Calculations within class for Overall ratings
        self.o_ovr = self._calculate_o_overall()
        self.d_ovr = self._calculate_d_overall()
        self.intangibles_ovr = self._calculate_intangibles_overall()
        self.overall = self._calculate_overall()

        # Prospect Stats in Amateur Leagues
        self.amateur_stats = self._calculate_amateur_stats()

        # Stats Tracker
        self.game_stats = individual_stat_block_game
        self.season_stats = individual_stat_block_overalls
        self.career_stats = individual_stat_block_overalls
        self.stats_archive = {}

        # Initializes stamina meter to be changed mid-game
        self.stamina = 99

        # Year Tracker
        self.curr_year = 2030

    # Private Methods
    def _calculate_o_overall(self):
        if self.position == 'PG':
            weight = pg_weight_offense
        elif self.position == 'SG':
            weight = sg_weight_offense
        elif self.position == 'SF':
            weight = sf_weight_offense
        elif self.position == 'PF':
            weight = pf_weight_offense
        else:
            weight = c_weight_offense

        return round((self.o_reb.curr_rating * weight['o_reb']) + (self.finishing.curr_rating * weight['finishing']) + \
            (self.open_mid.curr_rating * weight['open_mid']) + (self.open_3.curr_rating * weight['open_3']) + \
            (self.contest_mid.curr_rating * weight['contest_mid']) + (self.contest_3.curr_rating * weight['contest_3']) + \
            (self.playmaking.curr_rating * weight['playmaking']) + (self.ft_shoot.curr_rating * weight['ft_shoot']))

    def _calculate_d_overall(self):
        if self.position == 'PG' or self.position == 'SG':
            weight = g_weight_defense
        elif self.position == 'SF' or self.position == 'PF':
            weight = f_weight_defense
        else:
            weight = c_weight_defense

        return round((self.d_reb.curr_rating * weight['d_reb']) + (self.block.curr_rating * weight['block']) + \
            (self.steal.curr_rating * weight['steal']) + (self.stickiness.curr_rating * weight['stickiness']))

    def _calculate_intangibles_overall(self):
        return round((self.awareness.curr_rating * intangibles_weight['awareness']) + \
            (self.endurance.curr_rating * intangibles_weight['endurance']) + (self.confidence.curr_rating * intangibles_weight['confidence']))

    def _calculate_overall(self):
        return round((self.o_ovr * .5) + (self.d_ovr * .4) + (self.intangibles_ovr * .1))

    def _calculate_amateur_stats(self):
        amateur_stats = individual_stat_block_overalls
        return amateur_stats

    # Public Methods
    def set_salary(self, new_num):
        self.salary = new_num

    def increment_age(self):
        self.age += 1

    def change_mercuriality(self, new_merc):
        self.mercuriality = new_merc

    def change_contentment(self, new_content):
        self.contentment = new_content

    def change_character(self, new_character):
        self.character = new_character

    def update_total_stats(self):
        if self.game_stats['minutes'] != 0:
            self.season_stats['games_played'] += 1
            self.career_stats['games_played'] += 1

            self.season_stats['minutes']['total'] += self.game_stats['minutes']
            self.career_stats['minutes']['total'] += self.game_stats['minutes']
            self.season_stats['minutes']['average'] = round(self.season_stats['minutes']['total'] / self.season_stats['games_played'], 1)
            self.career_stats['minutes']['average'] = round(self.career_stats['minutes']['total'] / self.career_stats['games_played'], 1)

            self.season_stats['points']['total'] += self.game_stats['points']
            self.career_stats['points']['total'] += self.career_stats['points']
            self.season_stats['points']['average'] = round(self.season_stats['points'] / self.season_stats['games_played'], 1)
            self.career_stats['points']['average'] = round(self.career_stats['points'] / self.career_stats['games_played'], 1)

            self.season_stats['2fg_taken'] += self.game_stats['2fg_taken']
            self.career_stats['2fg_taken'] += self.game_stats['2fg_taken']
            self.season_stats['2fg_made'] += self.game_stats['2fg_made']
            self.career_stats['2fg_made'] += self.game_stats['2fg_made']
            self.season_stats['3fg_taken'] += self.game_stats['3fg_taken']
            self.career_stats['3fg_taken'] += self.game_stats['3fg_taken']
            self.season_stats['3fg_made'] += self.game_stats['3fg_made']
            self.career_stats['3fg_made'] += self.game_stats['3fg_made']
            self.season_stats['ft_taken'] += self.game_stats['ft_taken']
            self.career_stats['ft_taken'] += self.game_stats['ft_taken']
            self.season_stats['ft_made'] += self.game_stats['ft_made']
            self.career_stats['ft_made'] += self.game_stats['ft_made']

            self.season_stats['2fg%'] = round(self.season_stats['2fg_taken'] / self.season_stats['2fg_made'], 3)
            self.season_stats['3fg%'] = round(self.season_stats['3fg_taken'] / self.season_stats['3fg_made'], 3)
            self.season_stats['ft%'] = round(self.season_stats['ft_taken'] / self.season_stats['ft_made'], 3)
            self.career_stats['2fg%'] = round(self.career_stats['2fg_taken'] / self.career_stats['2fg_made'], 3)
            self.career_stats['3fg%'] = round(self.career_stats['3fg_taken'] / self.career_stats['3fg_made'], 3)
            self.career_stats['ft%'] = round(self.career_stats['ft_taken'] / self.career_stats['ft_made'], 3)

            self.season_stats['rebounds']['total'] += self.game_stats['rebounds']
            self.career_stats['rebounds']['total'] += self.career_stats['rebounds']
            self.season_stats['rebounds']['average'] = round(self.season_stats['rebounds'] / self.season_stats['games_played'], 1)
            self.career_stats['rebounds']['average'] = round(self.career_stats['rebounds'] / self.career_stats['games_played'], 1)

            self.season_stats['offensive_rebounds']['total'] += self.game_stats['offensive_rebounds']
            self.career_stats['offensive_rebounds']['total'] += self.career_stats['offensive_rebounds']
            self.season_stats['offensive_rebounds']['average'] = round(self.season_stats['offensive_rebounds'] / self.season_stats['games_played'], 1)
            self.career_stats['offensive_rebounds']['average'] = round(self.career_stats['offensive_rebounds'] / self.career_stats['games_played'], 1)

            self.season_stats['defensive_rebounds']['total'] += self.game_stats['defensive_rebounds']
            self.career_stats['defensive_rebounds']['total'] += self.career_stats['defensive_rebounds']
            self.season_stats['defensive_rebounds']['average'] = round(self.season_stats['defensive_rebounds'] / self.season_stats['games_played'], 1)
            self.career_stats['defensive_rebounds']['average'] = round(self.career_stats['defensive_rebounds'] / self.career_stats['games_played'], 1)

            self.season_stats['assists']['total'] += self.game_stats['assists']
            self.career_stats['assists']['total'] += self.career_stats['assists']
            self.season_stats['assists']['average'] = round(self.season_stats['assists'] / self.season_stats['games_played'], 1)
            self.career_stats['assists']['average'] = round(self.career_stats['assists'] / self.career_stats['games_played'], 1)

            self.season_stats['steals']['total'] += self.game_stats['steals']
            self.career_stats['steals']['total'] += self.career_stats['steals']
            self.season_stats['steals']['average'] = round(self.season_stats['steals'] / self.season_stats['games_played'], 1)
            self.career_stats['steals']['average'] = round(self.career_stats['steals'] / self.career_stats['games_played'], 1)

            self.season_stats['blocks']['total'] += self.game_stats['blocks']
            self.career_stats['blocks']['total'] += self.career_stats['blocks']
            self.season_stats['blocks']['average'] = round(self.season_stats['blocks'] / self.season_stats['games_played'], 1)
            self.career_stats['blocks']['average'] = round(self.career_stats['blocks'] / self.career_stats['games_played'], 1)

            self.season_stats['turnovers']['total'] += self.game_stats['turnovers']
            self.career_stats['turnovers']['total'] += self.career_stats['turnovers']
            self.season_stats['turnovers']['average'] = round(self.season_stats['turnovers'] / self.season_stats['games_played'], 1)
            self.career_stats['turnovers']['average'] = round(self.career_stats['turnovers'] / self.career_stats['games_played'], 1)

            self.season_stats['fouls']['total'] += self.game_stats['fouls']
            self.career_stats['fouls']['total'] += self.career_stats['fouls']
            self.season_stats['fouls']['average'] = round(self.season_stats['fouls'] / self.season_stats['games_played'], 1)
            self.career_stats['fouls']['average'] = round(self.career_stats['fouls'] / self.career_stats['games_played'], 1)

            self.season_stats['+/-']['total'] += self.game_stats['+/-']
            self.career_stats['+/-']['total'] += self.career_stats['+/-']

        self.game_stats = individual_stat_block_game

    def next_season(self):
        self.stats_archive[str(self.curr_year)] = self.season_stats
        self.season_stats = individual_stat_block_overalls
        self.curr_year += 1