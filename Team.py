from helper_functions import generate_random_int
from initial_templates import *
from get_sorted_pools import *

class Team:

    def __init__(self, nickname, city, region, logo, colors,
                 coach=None, roster=None, starters=None, bench=None, scouts=None,
                 accolades=None):
        # General team info
        self.nickname = nickname
        self.city = city
        self.region = region
        self.logo = logo
        self.colors = colors
        # Coaches, Scouts, Players
        self.coach = coach
        self.roster = roster if roster is not None else []
        self.starters = starters if starters is not None else {}
        self.bench = bench if bench is not None else []
        self.scouts = scouts if scouts is not None else []
        # In game trackers
        self.timeouts = 5
        self.points = 0
        self.fouls_in_q = 0
        # Stats and Accolades
        self.accolades = accolades if accolades is not None else {'2030': None}
        self.wins = 0,
        self.losses = 0,
        self.total_stats = team_totals
        self.average_stats = self._calculate_average_stats()
        self.individual_stats_season = {}
        self.individual_stats_career = {}
        self.stats_archive = {}
        # Year Tracker
        self.curr_year = 2030

    # Private Methods
    def _calculate_average_stats(self):
        # Ensure not dividing by 0

        if self.total_stats['games_played'] == 0:
            return {
                'ppg': 0,
                'fg%': 0,
                '3pt%': 0,
                'ft%': 0,
                'rebounds': 0,
                'offensive_rebounds': 0,
                'defensive_rebounds': 0,
                'assists': 0,
                'steals': 0,
                'blocks': 0,
                'turnovers': 0,
                'fouls': 0
            }
        else:
            if self.total_stats['2fg_taken'] == 0:
                fg2_perc = 0
            else:
                fg2_perc = round(self.total_stats['2fg_made'] / self.total_stats['2fg_taken'], 3)

            if self.total_stats['3fg_taken'] == 0:
                fg3_perc = 0
            else:
                fg3_perc = round(self.total_stats['3fg_made'] / self.total_stats['3fg_taken'], 3)

            if self.total_stats['ft_taken'] == 0:
                ft_perc = 0
            else:
                ft_perc = round(self.total_stats['ft_made'] / self.total_stats['ft_taken'], 3)

            return {
            'ppg': round(self.total_stats['points'] / self.total_stats['games_played'], 1),
            'fg%': fg2_perc,
            '3pt%': fg3_perc,
            'ft%': ft_perc,
            'rebounds_pg': round(self.total_stats['rebounds'] / self.total_stats['games_played'], 1),
            'offensive_rebounds_pg': round(self.total_stats['offensive_rebounds'] / self.total_stats['games_played'], 1),
            'defensive_rebounds_pg': round(self.total_stats['defensive_rebounds'] / self.total_stats['games_played'], 1),
            'assists_pg': round(self.total_stats['assists'] / self.total_stats['games_played'], 1),
            'steals_pg': round(self.total_stats['steals'] / self.total_stats['games_played'], 1),
            'blocks_pg': round(self.total_stats['blocks'] / self.total_stats['games_played'], 1),
            'turnovers_pg': round(self.total_stats['turnovers'] / self.total_stats['games_played'], 1),
            'fouls_pg': round(self.total_stats['fouls'] / self.total_stats['games_played'], 1)
        }

    # Public Methods
    def add_player(self, player):
        self.roster.append(player)

    def change_coach(self, coach):
        self.coach = coach

    def add_scout(self, scout):
        self.scouts.append(scout)

    def set_starters(self):
        used_positions = set()
        for player in get_sorted_players(self.roster):
            if player.position not in used_positions:
                self.starters[player.position] = player
                used_positions.add(player.position)
            else:
                self.bench.append(player)

    def update_individual_stats(self):
        for player in self.roster:
            self.individual_stats_season[player.name] = player.season_stats
            self.individual_stats_career[player.name] = player.career_stats

    def update_season_stats(self, game_stat_block, location, result):
        if result == 'loss':
            self.losses += 1
        else:
            self.wins += 1

        if location == 'home':
            team = 'home_team'
        else:
            team = 'away_team'

        # Update Total Stats
        self.total_stats['games_played'] += 1
        self.total_stats['points'] += game_stat_block[team]['points']
        self.total_stats['2fg_taken'] += game_stat_block[team]['2fg_taken']
        self.total_stats['2fg_made'] += game_stat_block[team]['2fg_made']
        self.total_stats['3fg_taken'] += game_stat_block[team]['3fg_taken']
        self.total_stats['3fg_made'] += game_stat_block[team]['3fg_made']
        self.total_stats['ft_taken'] += game_stat_block[team]['ft_taken']
        self.total_stats['ft_made'] += game_stat_block[team]['ft_made']
        self.total_stats['rebounds'] += game_stat_block[team]['rebounds']
        self.total_stats['offensive_rebounds'] += game_stat_block[team]['offensive_rebounds']
        self.total_stats['defensive_rebounds'] += game_stat_block[team]['defensive_rebounds']
        self.total_stats['assists'] += game_stat_block[team]['assists']
        self.total_stats['steals'] += game_stat_block[team]['steals']
        self.total_stats['blocks'] += game_stat_block[team]['blocks']
        self.total_stats['turnovers'] += game_stat_block[team]['turnovers']
        self.total_stats['fouls'] += game_stat_block[team]['fouls']

        # Update Individual Stats
        for player in self.roster:
            player.update_total_stats()

        self.update_individual_stats

    # Broad effect of a coach on player ratings
    def alter_offensive_player_ratings_by_coach(self):
        if self.coach is None:
            return
        else:
            for player in self.roster:
                # Alter offensive ratings
                if self.coach.coach_offense.rating > 0 and self.coach.coach_offense.rating <= 40:
                    player.o_reb.curr_rating = max(0, player.o_reb.curr_rating - generate_random_int(0, 5))
                    player.finishing.curr_rating = max(0, player.finishing.curr_rating - generate_random_int(0, 5))
                    player.open_mid.curr_rating = max(0, player.open_mid.curr_rating - generate_random_int(0, 5))
                    player.open_3.curr_rating = max(0, player.open_3.curr_rating - generate_random_int(0, 5))
                    player.contest_mid.curr_rating = max(0, player.contest_mid.curr_rating - generate_random_int(0, 5))
                    player.playmaking.curr_rating = max(0, player.playmaking.curr_rating - generate_random_int(0, 5))
                    player.ft_shoot.curr_rating = max(0, player.ft_shoot.curr_rating - generate_random_int(0, 5))
                elif self.coach.coach_offense.rating > 40 and self.coach.coach_offense.rating <= 70:
                    o_reb_change = generate_random_int(-2, 2)
                    player.o_reb.curr_rating = max(0, min(99, player.o_reb.curr_rating + o_reb_change))
                    finishing_change = generate_random_int(-2, 2)
                    player.finishing.curr_rating = max(0, min(99, player.finishing.curr_rating + finishing_change))
                    open_mid_change = generate_random_int(-2, 2)
                    player.open_mid.curr_rating = max(0, min(99, player.open_mid.curr_rating + open_mid_change))
                    open_3_change = generate_random_int(-2, 2)
                    player.open_3.curr_rating = max(0, min(99, player.open_3.curr_rating + open_3_change))
                    contest_mid_change = generate_random_int(-2, 2)
                    player.contest_mid.curr_rating = max(0, min(99, player.contest_mid.curr_rating + contest_mid_change))
                    playmaking_change = generate_random_int(-2, 2)
                    player.playmaking.curr_rating = max(0, min(99, player.playmaking.curr_rating + playmaking_change))
                    ft_shoot_change = generate_random_int(-2, 2)
                    player.ft_shoot.curr_rating = max(0, min(99, player.ft_shoot.curr_rating + ft_shoot_change))
                else:
                    player.o_reb.curr_rating = min(99, player.o_reb.curr_rating + generate_random_int(0, 5))
                    player.finishing.curr_rating = min(99, player.finishing.curr_rating + generate_random_int(0, 5))
                    player.open_mid.curr_rating = min(99, player.open_mid.curr_rating + generate_random_int(0, 5))
                    player.open_3.curr_rating = min(99, player.open_3.curr_rating + generate_random_int(0, 5))
                    player.contest_mid.curr_rating = min(99, player.contest_mid.curr_rating + generate_random_int(0, 5))
                    player.playmaking.curr_rating = min(99, player.playmaking.curr_rating + generate_random_int(0, 5))
                    player.ft_shoot.curr_rating = min(99, player.ft_shoot.curr_rating + generate_random_int(0, 5))

    def alter_defensive_player_ratings_by_coach(self):
        if self.coach is None:
            return
        else:
            for player in self.roster:
                # Alter offensive ratings
                if self.coach.coach_defense.rating > 0 and self.coach.coach_defense.rating <= 40:
                    player.d_reb.curr_rating = max(0, player.d_reb.curr_rating - generate_random_int(0, 5))
                    player.block.curr_rating = max(0, player.block.curr_rating - generate_random_int(0, 5))
                    player.steal.curr_rating = max(0, player.steal.curr_rating - generate_random_int(0, 5))
                    player.stickiness.curr_rating = max(0, player.stickiness.curr_rating - generate_random_int(0, 5))
                elif self.coach.coach_defense.rating > 40 and self.coach.coach_defense.rating <= 70:
                    d_reb_change = generate_random_int(-2, 2)
                    player.d_reb.curr_rating = max(0, min(99, player.d_reb.curr_rating + d_reb_change))
                    block_change = generate_random_int(-2, 2)
                    player.block.curr_rating = max(0, min(99, player.block.curr_rating + block_change))
                    steal_change = generate_random_int(-2, 2)
                    player.steal.curr_rating = max(0, min(99, player.steal.curr_rating + steal_change))
                    stickiness_change = generate_random_int(-2, 2)
                    player.stickiness.curr_rating = max(0, min(99, player.stickiness.curr_rating + stickiness_change))
                else:
                    player.d_reb.curr_rating = min(99, player.d_reb.curr_rating + generate_random_int(0, 5))
                    player.block.curr_rating = min(99, player.block.curr_rating + generate_random_int(0, 5))
                    player.steal.curr_rating = min(99, player.steal.curr_rating + generate_random_int(0, 5))
                    player.stickiness.curr_rating = min(99, player.stickiness.curr_rating + generate_random_int(0, 5))

    def alter_intangible_player_ratings_by_coach(self):
        if self.coach is None:
            return
        else:
            for player in self.roster:
                # Alter offensive ratings
                if self.coach.coach_intangibles.rating > 0 and self.coach.coach_intangibles.rating <= 40:
                    player.awareness.curr_rating = max(0, player.awareness.curr_rating - generate_random_int(0, 5))
                    player.endurance.curr_rating = max(0, player.endurance.curr_rating - generate_random_int(0, 5))
                    player.confidence.curr_rating = max(0, player.confidence.curr_rating - generate_random_int(0, 5))
                elif self.coach.coach_intangibles.rating > 40 and self.coach.coach_intangibles.rating <= 70:
                    awareness_change = generate_random_int(-2, 2)
                    player.awareness.curr_rating = max(0, min(99, player.awareness.curr_rating + awareness_change))
                    endurance_change = generate_random_int(-2, 2)
                    player.endurance.curr_rating = max(0, min(99, player.endurance.curr_rating + endurance_change))
                    confidence_change = generate_random_int(-2, 2)
                    player.confidence.curr_rating = max(0, min(99, player.confidence.curr_rating + confidence_change))
                else:
                    player.awareness.curr_rating = min(99, player.awareness.curr_rating + generate_random_int(0, 5))
                    player.endurance.curr_rating = min(99, player.endurance.curr_rating + generate_random_int(0, 5))
                    player.confidence.curr_rating = min(99, player.confidence.curr_rating + generate_random_int(0, 5))

    def goto_next_season(self):
        # Log stats into archive
        self.stats_archive[str(self.curr_year)] = {
            'wins': self.wins,
            'losses': self.losses,
            'total_stats': self.total_stats,
            'average_stats': self.average_stats,
            'individual_stats': self.individual_stats_season,
            'accolades': self.accolades[str(self.curr_year)]
        }
        # Clear stats, move to next season
        self.total_stats = team_totals
        self.individual_stats_season = {}
        for player in self.roster:
            player.next_season()
        self.curr_year += 1



