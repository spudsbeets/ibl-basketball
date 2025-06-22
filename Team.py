from initial_templates import *

class Team:

    def __init__(self, nickname, city, region, logo, colors,
                 coach=None, roster=[], starters=[], scouts=[],
                 accolades={'2030': None}):
        # General team info
        self.nickname = nickname
        self.city = city
        self.region = region
        self.logo = logo
        self.colors = colors
        # Coaches, Scouts, Players
        self.coach = coach
        self.roster = roster
        self.starters = starters
        self.scouts = scouts
        # Stats and Accolades
        self.accolades = accolades
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



