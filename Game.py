from get_sorted_pools import *
from initial_templates import *
from helper_functions import *
import math

class Game():
    def __init__(self, home_team, away_team,
                 home_onCourt=None, away_onCourt=None, home_onBench=None, away_onBench=None):
        # Teams participating
        self.home_team = home_team
        self.away_team = away_team
        # Players currently on the court
        self.home_onCourt = home_onCourt if home_onCourt is not None else []
        self.away_onCourt = away_onCourt if away_onCourt is not None else []
        # Players currently on the bench
        self.home_onBench = home_onBench or self.home_team.bench
        self.away_onBench = away_onBench or self.away_team.bench
        # Randomized play count by quarter
        self.curr_quarter = 1
        self.q1_plays = generate_random_int(40, 60)
        self.q2_plays = generate_random_int(40, 60)
        self.q3_plays = generate_random_int(40, 60)
        self.q4_plays = generate_random_int(40, 60)
        self.OT_plays_current = 0
        self.total_plays = self.q1_plays + self.q2_plays + self.q3_plays + self.q4_plays
        # Initialize empty game state block
        self.game_stat_block = full_game_stat_block
        # Initialize empty possession tracker, always either 'home_team' or 'away_team'
        self.curr_poss = ''

    # Private Methods
    # SETTING UP GAME SIM
    def _set_onCourt(self):
        """
        Sets the initial on court lineup for each team, based on the starters in the Team class.
        """
        # Reset the onCourt and onBench lists completely
        self.home_onCourt = list(self.home_team.starters.values())
        self.away_onCourt = list(self.away_team.starters.values())

        # Everyone else goes to the bench. Use the full roster to ensure no overlap.
        self.home_onBench = [p for p in self.home_team.roster if p not in self.home_onCourt]
        self.away_onBench = [p for p in self.away_team.roster if p not in self.away_onCourt]

    def _determine_tipoff(self):
        """
        Randomly determines the winner of the tipoff based on C height.
        """
        randomNum = generate_random_int(0, 100)
        if self.home_team.starters['C'].height - self.away_team.starters['C'].height > 4:
            if randomNum > 70:
                self.curr_poss = 'away_team'
            else:
                self.curr_poss = 'home_team'
        elif self.away_team.starters['C'].height - self.home_team.starters['C'].height > 4:
            if randomNum > 70:
                self.curr_poss = 'home_team'
            else:
                self.curr_poss = 'away_team'
        else:
            if randomNum >= 50:
                self.curr_poss = 'home_team'
            else:
                self.curr_poss = 'away_team'

    # STAMINA METHODS
    def _increase_stamina_all(self, stoppage_type):
        """
        Stamina increase whenever there is a stoppage in play.
        """
        stamina_dict = {
            'timeout': {'lo': 14, 'hi': 22},
            'OB': {'lo': 3, 'hi': 6},
            'fts': {'lo': 4, 'hi': 7}
        }
        if stoppage_type in stamina_dict:
            for player in self.home_team.roster + self.away_team.roster:
                base_increase = generate_random_int(stamina_dict[stoppage_type]['lo'], stamina_dict[stoppage_type]['hi'])
                # Endurance modifier
                modifier = (player.endurance.curr_rating - 50) / 50  # -1.0 .. +1.0
                adjustment = int(base_increase * (modifier * 0.2))  # up to ±20%
                player.stamina = min(99, player.stamina + base_increase + adjustment)
        else:
            print('Error! Unknown stoppage type.')

    def _increase_stamina_bench(self, home_bench, away_bench):
        """
        Stamina increase for bench whenever a normal play occurs.
        """
        for player in home_bench + away_bench:
            base_increase = generate_random_int(3, 6)
            modifier = (player.endurance.curr_rating - 50) / 50
            adjustment = int(base_increase * (modifier * 0.2))
            player.stamina = min(99, player.stamina + base_increase + adjustment)

    def _decrease_stamina_onCourt(self, primary_playmaker, primary_defender, secondary_playmaker, secondary_defender,
                                  offense_on_court, defense_on_court, primary_o_reb, primary_d_reb):
        """
        Stamina decrease for whoever is on the court, with bigger decreases for active playmakers.
        """
        teams_on_court = [offense_on_court, defense_on_court]
        for team in teams_on_court:
            for player in team:
                if player == primary_playmaker or player == primary_defender:
                    base_decrease = generate_random_int(4, 7)
                elif player == secondary_playmaker or player == secondary_defender or player == primary_o_reb or player == primary_d_reb:
                    base_decrease = generate_random_int(3, 6)
                else:
                    base_decrease = generate_random_int(1, 4)

                modifier = (player.endurance.curr_rating - 50) / 50
                adjustment = int(base_decrease * (modifier * -0.2))  # high endurance = smaller decrease
                player.stamina -= base_decrease + adjustment

    def _reset_stamina(self):
        """
        Resets stamina for every player for halftime and after game is over.
        """
        for player in self.home_team.roster:
            player.stamina = 99
        for player in self.away_team.roster:
            player.stamina = 99

    # STAT UPDATES
    def _update_play_counts(self):
        """
        Updates play count for on court players.
        """
        for player in self.home_onCourt:
            player.game_stats['plays'] += 1
        for player in self.away_onCourt:
            player.game_stats['plays'] += 1

    def _update_plus_minus(self, offense_on_court, defense_on_court, points_scored):
        """
        Updates +/- for on court players.
        """
        for player in offense_on_court:
            player.game_stats['+/-'] += points_scored
        for player in defense_on_court:
            player.game_stats['+/-'] -= points_scored

    def _log_fouls_and_points_by_q(self, home_team, away_team, stat_block, curr_quarter):
        """
        Updates fouls and points stats and trackers at the end of every quarter.
        """
        stat_block[curr_quarter]['home_team']['fouls'] += home_team.fouls_in_q
        stat_block[curr_quarter]['away_team']['fouls'] += away_team.fouls_in_q
        stat_block['Full Game']['home_team']['fouls'] += home_team.fouls_in_q
        stat_block['Full Game']['away_team']['fouls'] += away_team.fouls_in_q
        stat_block[curr_quarter]['home_team']['points'] += home_team.points_in_q
        stat_block[curr_quarter]['away_team']['points'] += away_team.points_in_q
        stat_block['Full Game']['home_team']['points'] += home_team.points_in_q
        stat_block['Full Game']['away_team']['points'] += away_team.points_in_q
        self.home_team.points_total += home_team.points_in_q
        self.away_team.points_total += away_team.points_in_q
        home_team.fouls_in_q = 0
        away_team.fouls_in_q = 0
        home_team.points_in_q = 0
        away_team.points_in_q = 0

    def _update_minutes(self, total_plays, ot_count):
        for player in self.home_team.roster + self.away_team.roster:
            plays = player.game_stats['plays']
            game_minutes = 48 + ((ot_count * 5) - 5)
            minutes = (plays / total_plays) * game_minutes
            player.game_stats['minutes'] = round(minutes, 1)

    def _print_end_of_game_stats(self, ot_count):
        """
        Prints end of game stats.
        """
        print("")
        print('FINAL SCORE')
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Show Box Score
        print("")
        print(f"{self.home_team.nickname} TEAM STATS:")
        print(f"Q1: {self.game_stat_block[1]['home_team']}")
        print(f"Q2: {self.game_stat_block[2]['home_team']}")
        print(f"Q3: {self.game_stat_block[3]['home_team']}")
        print(f"Q4: {self.game_stat_block[4]['home_team']}")
        if ot_count > 1:
            print(f"OT: {self.game_stat_block['OT']['home_team']}")
        print(f"FULL GAME: {self.game_stat_block['Full Game']['home_team']}")
        print("")
        print(f"{self.away_team.nickname} TEAM STATS:")
        print(f"Q1: {self.game_stat_block[1]['away_team']}")
        print(f"Q2: {self.game_stat_block[2]['away_team']}")
        print(f"Q3: {self.game_stat_block[3]['away_team']}")
        print(f"Q4: {self.game_stat_block[4]['away_team']}")
        if ot_count > 1:
            print(f"OT: {self.game_stat_block['OT']['away_team']}")
        print(f"FULL GAME: {self.game_stat_block['Full Game']['away_team']}")
        print("")
        print(f"PLAYER STATS {self.home_team.nickname}:")
        for player in self.home_team.roster:
            if player.game_stats['plays'] != 0:
                print(f"NAME: {player.name}")
                print(f"MINUTES: {player.game_stats['minutes']} POINTS: {player.game_stats['points']}, PLAYS: {player.game_stats['plays']}, FG ATTEMPTS: {player.game_stats['2fg_taken']}, FG MADE: {player.game_stats['2fg_made']}, 2FG%: {round(player.game_stats['2fg_made'] / player.game_stats['2fg_taken'] * 100) if player.game_stats['2fg_taken'] > 0 else 0}%, 3PT ATTEMPTS: {player.game_stats['3fg_taken']}, 3PT MADE: {player.game_stats['3fg_made']}, 3PT%: {round(player.game_stats['3fg_made'] / player.game_stats['3fg_taken'] * 100) if player.game_stats['3fg_taken'] > 0 else 0}%, FT ATTEMPTS: {player.game_stats['ft_taken']}, FT MADE: {player.game_stats['ft_made']}, FT%: {round(player.game_stats['ft_made'] / player.game_stats['ft_taken'] * 100) if player.game_stats['ft_taken'] > 0 else 0}%, REBOUNDS: {player.game_stats['rebounds']}, OFFENSIVE REBOUNDS: {player.game_stats['offensive_rebounds']}, DEFENSIVE REBOUNDS: {player.game_stats['defensive_rebounds']}, ASSISTS: {player.game_stats['assists']}, STEALS: {player.game_stats['steals']}, BLOCKS: {player.game_stats['blocks']}, TURNOVERS: {player.game_stats['turnovers']}, FOULS: {player.game_stats['fouls']}, +/-: {player.game_stats['+/-']}")
        print("")
        print(f"PLAYER STATS {self.away_team.nickname}:")
        for player in self.away_team.roster:
            if player.game_stats['plays'] != 0:
                print(f"NAME: {player.name}")
                print(f"MINUTES: {player.game_stats['minutes']} POINTS: {player.game_stats['points']}, PLAYS: {player.game_stats['plays']}, FG ATTEMPTS: {player.game_stats['2fg_taken']}, FG MADE: {player.game_stats['2fg_made']}, 2FG%: {round(player.game_stats['2fg_made'] / player.game_stats['2fg_taken'] * 100) if player.game_stats['2fg_taken'] > 0 else 0}%, 3PT ATTEMPTS: {player.game_stats['3fg_taken']}, 3PT MADE: {player.game_stats['3fg_made']}, 3PT%: {round(player.game_stats['3fg_made'] / player.game_stats['3fg_taken'] * 100) if player.game_stats['3fg_taken'] > 0 else 0}%, FT ATTEMPTS: {player.game_stats['ft_taken']}, FT MADE: {player.game_stats['ft_made']}, FT%: {round(player.game_stats['ft_made'] / player.game_stats['ft_taken'] * 100) if player.game_stats['ft_taken'] > 0 else 0}%, REBOUNDS: {player.game_stats['rebounds']}, OFFENSIVE REBOUNDS: {player.game_stats['offensive_rebounds']}, DEFENSIVE REBOUNDS: {player.game_stats['defensive_rebounds']}, ASSISTS: {player.game_stats['assists']}, STEALS: {player.game_stats['steals']}, BLOCKS: {player.game_stats['blocks']}, TURNOVERS: {player.game_stats['turnovers']}, FOULS: {player.game_stats['fouls']}, +/-: {player.game_stats['+/-']}")

    # THRESHOLD ADJUSTERS
    def _non_binary_adjust_thresholds(self, rating, threshold_dict, max_change, d_or_o):
        """
        Pseudo-randomly manipulates a dictionary that determines thresholds for the occurrences of certain events.
        Intended for events with 3 possible outcomes.
        """
        distance = abs(rating - 50) / 50
        raw_adjust = random.uniform(1, max_change) * distance
        adjustment = math.ceil(raw_adjust)
        rating_thresh = generate_random_int(40, 60)

        if rating < rating_thresh:
            if d_or_o == 'defense':
                threshold_dict['lo'] += adjustment
                threshold_dict['hi'] += adjustment
            else:
                threshold_dict['lo'] -= adjustment
                threshold_dict['hi'] -= adjustment
        elif rating > rating_thresh:
            if d_or_o == 'defense':
                threshold_dict['lo'] -= adjustment
                threshold_dict['hi'] -= adjustment
            else:
                threshold_dict['lo'] += adjustment
                threshold_dict['hi'] += adjustment

        # Clamp to [0, 99]
        threshold_dict['lo'] = max(0, min(99, threshold_dict['lo']))
        threshold_dict['hi'] = max(0, min(99, threshold_dict['hi']))

        # Ensure lo never exceeds hi
        if threshold_dict['lo'] > threshold_dict['hi']:
            threshold_dict['lo'] = threshold_dict['hi']

    def _binary_adjust_threshold(self, rating, threshold, max_change, d_or_o):
        """
        Pseudo-randomly manipulates a threshold value that determines the occurrences of certain events.
        Intended for events with only 2 outcomes.
        """
        distance = abs(rating - 50) / 50
        raw_adjust = random.uniform(1, max_change) * distance
        adjustment = math.ceil(raw_adjust)
        rating_thresh = random.randint(40, 60)

        if rating < rating_thresh:
            if d_or_o == 'defense':
                threshold += adjustment
            else:
                threshold -= adjustment
        elif rating > rating_thresh:
            if d_or_o == 'defense':
                threshold -= adjustment
            else:
                threshold += adjustment

        threshold = max(0, min(99, threshold))
        return threshold

    def _handle_subs(self, on_court, on_bench, starters, team_name):
        # This list will hold tuples of (player_out, player_in)
        subs_to_make = []

        # Create working copies of the lists to modify
        players_to_sub_out = set()

        # Identify players that should be subbed out
        for player in on_court:
            if player in starters.values() and player.stamina < 10:
                players_to_sub_out.add(player)
            elif player not in starters.values() and player.stamina < 40:
                players_to_sub_out.add(player)

        available_bench_players = set(get_sorted_players(on_bench))

        # Now, find appropriate replacements and build the substitution list
        for player_out in players_to_sub_out:
            position_out = 'guard' if player_out.position in ('PG', 'SG') else 'forward'
            sub_found = False

            # Priority 1: Sub in a rested starter
            rested_starters = [
                p for p in available_bench_players
                if p in starters.values()
                   and p.stamina > 60
                   and ((p.position in ('PG', 'SG') and position_out == 'guard') or
                        (p.position in ('SF', 'PF', 'C') and position_out == 'forward'))
            ]

            if rested_starters:
                best_choice = get_sorted_players(rested_starters)[0]
                subs_to_make.append((player_out, best_choice))
                available_bench_players.remove(best_choice)
                sub_found = True

            # Priority 2: Sub in a high-stamina bench player
            if not sub_found:
                for player_in in available_bench_players:
                    if player_in.stamina > 75 and \
                            ((player_in.position in ('PG', 'SG') and position_out == 'guard') or
                             (player_in.position in ('SF', 'PF', 'C') and position_out == 'forward')):
                        subs_to_make.append((player_out, player_in))
                        available_bench_players.remove(player_in)
                        sub_found = True
                        break

        # Commit substitutions
        for out_p, in_p in subs_to_make:
            if out_p in on_court and in_p in on_bench:
                on_court.remove(out_p)
                on_court.append(in_p)
                on_bench.remove(in_p)
                on_bench.append(out_p)
                print(f"{out_p.name} ({out_p.position}) subs out for {in_p.name} ({in_p.position})")

        # Final check
        assert len(on_court) == 5, f"{team_name}: Invalid onCourt size {len(on_court)}"
        assert len(set(on_court)) == 5, f"{team_name}: Duplicate player detected on court!"

    # CHECKS FOR TIMEOUTS AND SUBS
    def _check_for_subs(self):
        """
        Runs the handle_subs() method for each team to determine if a team wants to substitute any of the
        players on court for those on the bench.
        """
        # Reset subbed_out boolean
        for player in self.home_team.roster + self.away_team.roster:
            player.subbed_out_this_play = False

        # Run for both teams
        self._handle_subs(self.home_onCourt, self.home_onBench, self.home_team.starters, self.home_team.nickname)
        self._handle_subs(self.away_onCourt, self.away_onBench, self.away_team.starters, self.away_team.nickname)

        if len(self.home_onCourt) != 5 or len(self.away_onCourt) != 5:
            print(f"RED ALERT. WRONG NUMBER OF PLAYERS {len(self.home_onCourt)} {len(self.away_onCourt)})")

        print(f"{self.home_team.nickname} CURRENTLY ON COURT:")
        for player in self.home_onCourt:
            print(player.name)
        print(f"{self.away_team.nickname} CURRENTLY ON COURT:")
        for player in self.away_onCourt:
            print(player.name)

    def _check_for_timeout(self, offense_on_court, offense_team, defense_team):
        """
        Checks whether a team is in a situation where a timeout is a good decision.
        """
        # Check to see if majority of on court players are gassed
        low_stamina_count = sum(1 for p in offense_on_court if p.stamina <= 25)

        # Dictionary for determining logical timeout usage
        timeout_rules = {
            1: {'min_timeouts': 5, 'min_deficit': 6},
            2: {'min_timeouts': 4, 'min_deficit': 6},
            3: {'min_timeouts': 2, 'min_deficit': 6},
            4: {'min_timeouts': 1, 'min_deficit': 3},
            'OT': {'min_timeouts': 1, 'min_deficit': 3},
        }

        # If players are tired and game situation dictates it, take timeout
        if low_stamina_count >= 3:
            rules = timeout_rules.get(self.curr_quarter)
            if offense_team.timeouts >= rules['min_timeouts'] and \
                    ((defense_team.points_total + defense_team.points_in_q) -
                     (offense_team.points_total + offense_team.points_in_q)) >= rules['min_deficit']:
                print("")
                print(f"Timeout taken by {offense_team.nickname}")
                self._update_play_counts()
                offense_team.timeouts -= 1
                self._check_for_subs()
                self._increase_stamina_all('timeout')
                return True

        return False

    # DETERMINES PLAYS/PLAYMAKERS
    def _determine_play_type(self, primary_playmaker, primary_defender):
        """
        Based off primary playmaker and defender strengths and weaknesses, determines with a degree of
        randomness what kind of basketball play will be attempted.
        """
        # Returns a string from these OPTIONS:
        # 'create_3'
        # 'create_mid'
        # 'iso_drive'
        # 'post_up'
        # 'pick_n_roll' --> secondary POTENTIALLY needed
        # 'drive_n_pass' --> secondary needed
        # 'find_cutter' --> secondary needed

        # Determine decision tree based off offensive archetype
        if primary_playmaker.offensive_archetype == 'offensive_beast' or primary_playmaker.offensive_archetype == 'offensive_dud':
            probabilities = {
                'create_3': 15, # 15% chance
                'create_mid': 30, # 15% chance
                'iso_drive': 45, # 15% chance
                'post_up': 55, # 10% chance
                'pick_n_roll': 70, # 15% chance
                'drive_n_pass': 85, # 15% chance
                'find_cutter': 100 # 15% chance
            }
        elif primary_playmaker.offensive_archetype == 'creates_jumpers':
            probabilities = {
                'create_3': 25, # 25% chance
                'create_mid': 50, # 25% chance
                'iso_drive': 65, # 15% chance
                'post_up': 70, #5% chance
                'pick_n_roll': 80, # 10% chance
                'drive_n_pass': 90, # 10% chance
                'find_cutter': 100 # 10% chance
            }
        elif primary_playmaker.offensive_archetype == 'create_drives':
            probabilities = {
                'create_3': 10, # 10% chance
                'create_mid': 20, # 10% chance
                'iso_drive': 45, # 25% chance
                'post_up': 60, #10% chance
                'pick_n_roll': 70, # 15% chance
                'drive_n_pass': 85, # 15% chance
                'find_cutter': 100 # 15% chance
            }
        elif primary_playmaker.offensive_archetype == 'post_merchant':
            probabilities = {
                'create_3': 5, # 5% chance
                'create_mid': 15, # 10% chance
                'iso_drive': 30, # 15% chance
                'post_up': 60, #30% chance
                'pick_n_roll': 70, # 10% chance
                'drive_n_pass': 85, # 15% chance
                'find_cutter': 100 # 15% chance
            }
        # 'creates_for_teammates'
        else:
            probabilities = {
                'create_3': 10, # 10% chance
                'create_mid': 20, # 10% chance
                'iso_drive': 30, # 10% chance
                'post_up': 40, # 10% chance
                'pick_n_roll': 60, # 20% chance
                'drive_n_pass': 80, # 20% chance
                'find_cutter': 100 # 20% chance
            }

        # Prioritize getting ball out of hands if defender is awesome
        if primary_defender.d_ovr > 75:
            probabilities['create_3'] -= 5
            probabilities['create_mid'] -= 10
            probabilities['iso_drive'] -= 15
            probabilities['post_up'] -= 15
            probabilities['pick_n_roll'] -= 10
            probabilities['drive_n_pass'] -= 5

        randomNum = generate_random_int(0, 100)

        if randomNum <= probabilities['create_3']:
            return 'create_3'
        elif randomNum <= probabilities['create_mid']:
            return 'create_mid'
        elif randomNum <= probabilities['iso_drive']:
            return 'iso_drive'
        elif randomNum <= probabilities['post_up']:
            return 'post_up'
        elif randomNum <= probabilities['pick_n_roll']:
            return 'pick_n_roll'
        elif randomNum <= probabilities['drive_n_pass']:
            return 'drive_n_pass'
        else:
            return 'find_cutter'

    def _determine_primary_playmaker(self, offense_on_court):
        """
        Determines who the primary playmaker for the offense will be on a given play.
        """
        # Randomize whether high IQ or high playmaker gets the priority for the ball
        firstRandomNum = generate_random_int(0, 100)
        if firstRandomNum >= 40:
            sorted_offense = get_sorted_roster_by_o_overall(offense_on_court)
        elif firstRandomNum >= 70:
            sorted_offense = get_sorted_roster_by_awareness(offense_on_court)
        else:
            sorted_offense = get_sorted_roster_by_playmaking(offense_on_court)

        # Pseudo-randomly select primary playmaker
        secondRandomNum = generate_random_int(0, 100)

        if secondRandomNum < 40:
            return sorted_offense[0]
        elif secondRandomNum < 70:
            return sorted_offense[1]
        elif secondRandomNum < 90:
            return sorted_offense[2]
        elif secondRandomNum < 95:
            return sorted_offense[3]
        else:
            return sorted_offense[4]

    def _determine_secondary_playmaker(self, primary_playmaker, offense_on_court):
        """
        Determines the secondary playmaker on a non-iso play.
        """
        available_offense = [p for p in offense_on_court if p != primary_playmaker]

        firstRandomNum = generate_random_int(0, 100)

        if firstRandomNum >= 20:
            sorted_offense = get_sorted_roster_by_o_overall(available_offense)
        elif firstRandomNum >= 40:
            sorted_offense = get_sorted_roster_by_awareness(available_offense)
        elif firstRandomNum >= 60:
            sorted_offense = get_sorted_roster_by_playmaking(available_offense)
        elif firstRandomNum >= 85:
            sorted_offense = get_sorted_roster_by_open_3(available_offense)
        else:
            sorted_offense = get_sorted_roster_by_open_mid(available_offense)

        secondRandomNum = generate_random_int(0, 100)

        if secondRandomNum < 40:
            return sorted_offense[0]
        elif secondRandomNum < 70:
            return sorted_offense[1]
        elif secondRandomNum < 90:
            return sorted_offense[2]
        else:
            return sorted_offense[3]

    def _determine_primary_offense_rebounder(self, offense_on_court):
        """
        Determines which offensive player is gunning for an offensive rebound on a given play.
        """
        sorted_offense = get_sorted_roster_by_o_reb(offense_on_court)

        offense_random_num = generate_random_int(0, 100)

        if offense_random_num < 40:
            return sorted_offense[0]
        elif offense_random_num < 70:
            return sorted_offense[1]
        elif offense_random_num < 90:
            return sorted_offense[2]
        elif offense_random_num < 95:
            return sorted_offense[3]
        else:
            return sorted_offense[4]

    def _determine_primary_defense_rebounder(self, defense_on_court):
        """
        Determines which defensive player is gunning for a defensive rebound on a given play.
        """
        sorted_defense = get_sorted_roster_by_d_reb(defense_on_court)

        defense_random_num = generate_random_int(0, 100)

        if defense_random_num < 40:
            return sorted_defense[0]
        elif defense_random_num < 70:
            return sorted_defense[1]
        elif defense_random_num < 90:
            return sorted_defense[2]
        elif defense_random_num < 95:
            return sorted_defense[3]
        else:
            return sorted_defense[4]

    def _determine_matchups(self, offense_on_court, defense_on_court, defensive_scheme='MAN'):
        """
        Returns a dictionary that matches each player up to their most sensible defensive counterpart.
        """

        assignments = {}
        assigned_defenders = set()  # track who is already assigned
        sorted_offense = get_sorted_roster_by_o_overall(offense_on_court)
        sorted_defense = get_sorted_roster_by_d_overall(defense_on_court)

        if defensive_scheme == 'MAN':
            for player in sorted_offense:
                off_pos = player.position

                # Determine which defender positions can guard this offensive player
                if off_pos in ('PG', 'SG'):
                    guardable_positions = ('PG', 'SG', 'SF')
                elif off_pos == 'SF':
                    guardable_positions = None  # anyone can guard
                else:  # PF/C
                    guardable_positions = ('SF', 'PF', 'C')

                # Find the best unassigned defender who can guard this offensive player
                for defender in sorted_defense:
                    if defender in assigned_defenders:
                        continue
                    if guardable_positions is None or defender.position in guardable_positions:
                        assignments[player.name] = defender
                        assigned_defenders.add(defender)
                        break
                else:
                    # fallback if no match: assign the best remaining defender
                    for defender in sorted_defense:
                        if defender not in assigned_defenders:
                            assignments[player.name] = defender
                            assigned_defenders.add(defender)
                            break
        else:
            print('we aint worried bout this yet')

        return assignments

    # HELPERS FOR SPECIFIC PLAYS
    def _shoot_fts(self, primary_playmaker, attempts, offense, offense_team, offense_on_court, defense_on_court):
        """
        Simulates shooting free throws and updates stats accordingly. Returns 'fts' for stoppage purposes.
        """
        # Low Result = Make, High result = Miss
        initial_ft_threshold = generate_random_int(55, 80)
        # MODIFIERS
        ft_threshold = self._binary_adjust_threshold(primary_playmaker.ft_shoot.curr_rating, initial_ft_threshold, 25, 'offense')
        made_count = 0
        for _ in range(attempts):
            ft_success = generate_random_int(0, 100)
            if ft_success < ft_threshold:
                made_count += 1
        primary_playmaker.game_stats['ft_taken'] += 2
        primary_playmaker.game_stats['ft_made'] += made_count
        primary_playmaker.game_stats['points'] += made_count
        self.game_stat_block[self.curr_quarter][offense]['ft_taken'] += 2
        self.game_stat_block[self.curr_quarter][offense]['ft_made'] += made_count
        self.game_stat_block['Full Game'][offense]['ft_taken'] += 2
        self.game_stat_block['Full Game'][offense]['ft_made'] += made_count
        self._update_plus_minus(offense_on_court, defense_on_court, made_count)
        offense_team.points_in_q += made_count
        print(f"Free throws awarded to {primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}). {primary_playmaker.name} makes {made_count} / {attempts} fts.")
        return 'fts'

    def _rebound_ball(self, offense_on_court, defense_on_court, offense, defense):
        """
        Simulates rebounding a ball and updates stats accordingly. Returns a tuple for poss_change
        and stamina purposes.
        """
        # Add in put-back possibility later...

        # Low result = Offensive rebound, High result = Defensive Rebound
        initial_rebound_threshold = generate_random_int(25, 35)
        primary_o_reb = self._determine_primary_offense_rebounder(offense_on_court)
        primary_d_reb = self._determine_primary_defense_rebounder(defense_on_court)
        # MODIFIERS
        offense_mod_rebound_threshold = self._binary_adjust_threshold(
            primary_o_reb.o_reb.curr_rating, initial_rebound_threshold, 11, 'offense')
        rebound_threshold = self._binary_adjust_threshold(primary_d_reb.d_reb.curr_rating,
                                                          offense_mod_rebound_threshold, 11,
                                                          'defense')
        # Success Roll
        rebound_success = generate_random_int(0, 100)
        if rebound_success < rebound_threshold:
            primary_o_reb.game_stats['rebounds'] += 1
            primary_o_reb.game_stats['offensive_rebounds'] += 1
            self.game_stat_block[self.curr_quarter][offense]['rebounds'] += 1
            self.game_stat_block[self.curr_quarter][offense]['offensive_rebounds'] += 1
            self.game_stat_block['Full Game'][offense]['rebounds'] += 1
            self.game_stat_block['Full Game'][offense]['offensive_rebounds'] += 1
            poss_change = False
            print(f"Offensive rebound secured by {primary_o_reb.name}({primary_o_reb.position}).")
        else:
            primary_d_reb.game_stats['rebounds'] += 1
            primary_d_reb.game_stats['defensive_rebounds'] += 1
            self.game_stat_block[self.curr_quarter][defense]['rebounds'] += 1
            self.game_stat_block[self.curr_quarter][defense]['defensive_rebounds'] += 1
            self.game_stat_block['Full Game'][defense]['rebounds'] += 1
            self.game_stat_block['Full Game'][defense]['defensive_rebounds'] += 1
            poss_change = True
            print(f"Defensive rebound secured by {primary_d_reb.name} ({primary_d_reb.position}).")
        return (poss_change, primary_o_reb, primary_d_reb)

    def _make_a_three(self, primary_playmaker, offense, offense_team, offense_on_court, defense_on_court):
        """
        Record stats for a made 3. Return True for possession change purposes.
        """
        primary_playmaker.game_stats['3fg_taken'] += 1
        primary_playmaker.game_stats['3fg_made'] += 1
        primary_playmaker.game_stats['points'] += 3
        self.game_stat_block[self.curr_quarter][offense]['3fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['3fg_made'] += 1
        self.game_stat_block['Full Game'][offense]['3fg_taken'] += 1
        self.game_stat_block['Full Game'][offense]['3fg_made'] += 1
        offense_team.points_in_q += 3
        self._update_plus_minus(offense_on_court, defense_on_court, 3)
        print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) made open 3 point basket.")
        return True

    def _make_a_mid_range(self, primary_playmaker, offense, offense_team, offense_on_court, defense_on_court):
        """
        Record stats for a made mid-range. Return True for possession change purposes.
        """
        primary_playmaker.game_stats['2fg_taken'] += 1
        primary_playmaker.game_stats['2fg_made'] += 1
        primary_playmaker.game_stats['points'] += 2
        self.game_stat_block[self.curr_quarter][offense]['2fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['2fg_made'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_taken'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_made'] += 1
        offense_team.points_in_q += 2
        self._update_plus_minus(offense_on_court, defense_on_court, 2)
        print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) made open mid-range basket.")
        return True

    def _make_a_layup(self, primary_playmaker, offense, offense_team, offense_on_court, defense_on_court):
        """
        Record stats for a made layup. Return True for possession change purposes.
         """
        primary_playmaker.game_stats['2fg_taken'] += 1
        primary_playmaker.game_stats['2fg_made'] += 1
        primary_playmaker.game_stats['points'] += 2
        self.game_stat_block[self.curr_quarter][offense]['2fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['2fg_made'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_taken'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_made'] += 1
        offense_team.points_in_q += 2
        self._update_plus_minus(offense_on_court, defense_on_court, 2)
        print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) made open layup.")
        return True

    def _make_a_dunk(self, primary_playmaker, offense, offense_team, offense_on_court, defense_on_court):
        """
        Record stats for a made mid-range. Return True for possession change purposes.
        """
        primary_playmaker.game_stats['2fg_taken'] += 1
        primary_playmaker.game_stats['2fg_made'] += 1
        primary_playmaker.game_stats['points'] += 2
        self.game_stat_block[self.curr_quarter][offense]['2fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['2fg_made'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_taken'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_made'] += 1
        offense_team.points_in_q += 2
        self._update_plus_minus(offense_on_court, defense_on_court, 2)
        print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) made a dunk!")
        return True

    def _miss_a_three(self, primary_playmaker, offense_team, offense, shot_type):
        """
        Records stats for a missed 3 pointer.
        """
        primary_playmaker.game_stats['3fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['3fg_taken'] += 1
        self.game_stat_block['Full Game'][offense]['3fg_taken'] += 1
        if shot_type == 'open':
            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed an open 3 point basket.")
        # shot_type == 'contested'
        else:
            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a contested 3 point basket.")

    def _miss_a_two(self, primary_playmaker, offense_team, offense, shot_type):
        """
        Records stats for a missed 2 pointer.
        """
        primary_playmaker.game_stats['2fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['2fg_taken'] += 1
        self.game_stat_block['Full Game'][offense]['2fg_taken'] += 1
        if shot_type == 'layup':
            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a layup.")
        elif shot_type == 'mid-range-open':
            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed an open mid-range basket.")
        elif shot_type == 'post-up':
            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a post-up attempt.")
        # shot_type == 'mid-range-contested'
        else:
            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a contested mid-range basket.")

    def _record_a_steal(self, primary_defender, primary_playmaker, defense, offense):
        """
        Record stats for a successful steal. Returns True for poss_change purposes.
        """
        primary_defender.game_stats['steals'] += 1
        primary_playmaker.game_stats['turnovers'] += 1
        self.game_stat_block[self.curr_quarter][defense]['steals'] += 1
        self.game_stat_block[self.curr_quarter][offense]['turnovers'] += 1
        self.game_stat_block['Full Game'][defense]['steals'] += 1
        self.game_stat_block['Full Game'][offense]['turnovers'] += 1
        print(f"Ball stolen from {primary_playmaker.name} by {primary_defender.name}({primary_defender.position}).")
        return True

    def _record_a_block(self, primary_defender, defense, defense_team, offense_team):
        """
        Records stats for a block, returns a tuple to determine (stoppage, stoppage_type, poss_change)
        """
        stoppage = False
        stoppage_type = None
        poss_change = False

        primary_defender.game_stats['blocks'] += 1
        self.game_stat_block[self.curr_quarter][defense]['blocks'] += 1
        self.game_stat_block['Full Game'][defense]['blocks'] += 1
        print(f"Shot blocked by {primary_defender.name}({primary_defender.position}, {defense_team.nickname}).")
        # Low result = Offense gets ball back (OB or no), High result = Defense gets ball back
        possession_acquired_threshold = generate_random_int(35, 46)
        # NO MODIFIERS (random result)
        # Success Roll
        possession_acquired_success = generate_random_int(0, 100)
        if possession_acquired_success < possession_acquired_threshold:
            # Low result = Ball OB off defense, High result = Ball returns to offense off 'rebound'
            knock_OB_threshold = generate_random_int(26, 38)
            # NO MODIFIERS (random result)
            # Success Roll
            knock_OB_success = generate_random_int(0, 100)
            if knock_OB_success < knock_OB_threshold:
                stoppage = True
                stoppage_type = 'OB'
                print(f"Ball knocked out of bounds by {primary_defender.name}.")
            else:
                print(f"Ball recovered by {offense_team.nickname} off block.")
        else:
            poss_change = True
            print(f"Ball recovered by {defense_team.nickname} off block.")
        return (stoppage, stoppage_type, poss_change)

    def _record_an_assist(self, off_ball, offense):
        """
        Records stats for an assist.
        """
        self.game_stat_block[self.curr_quarter][offense]['assists'] += 1
        self.game_stat_block['Full Game'][offense]['assists'] += 1
        off_ball.game_stats['assists'] += 1

    def _record_offensive_foul(self, primary_playmaker, primary_defender, offense, offense_team, defense_team):
        """
        Records stats for an offensive foul.
        """
        primary_playmaker.game_stats['fouls'] += 1
        primary_playmaker.game_stats['turnovers'] += 1
        self.game_stat_block[self.curr_quarter][offense]['turnovers'] += 1
        self.game_stat_block['Full Game'][offense]['turnovers'] += 1
        offense_team.fouls_in_q += 1
        print(f"Offensive foul committed by {primary_playmaker.name}({offense_team.nickname}) on {primary_defender.name}({defense_team.nickname}).")
        return (True, True, 'OB')

    def _determine_play_outcome(self, primary_playmaker, primary_defender, play_type,
                                offense_team, defense_team, offense_on_court, defense_on_court,
                                offense_on_bench, defense_on_bench):
        """
        Determines the outcome(s) of a play and updates stats and trackers accordingly.
        """
        # GREATER VALUES --> Good for defense
        # LESSER VALUES --> Good for offense

        # Add Potential for fast break bucket (off turnover, low chance off d-reb) later...
        # Add injury possibility later...
        # Add foul out logic later...

        # SETUP
        if self.curr_poss == 'home_team':
            offense = 'home_team'
            defense = 'away_team'
        else:
            offense = 'away_team'
            defense = 'home_team'

        stoppage = False
        stoppage_type = None
        poss_change = False

        secondary_playmaker = None
        secondary_defender = None

        primary_d_reb = None
        primary_o_reb = None

        # OFFENSIVE RATINGS AT PLAY:
        # PRIMARY --> playmaking (ability to get open for open_3/mid or contest_3/mid)
        #             open_3/open_mid (for open shots)
        #             constest_3/contest_mid/finishing/post_up (for contested shots)
        #             awareness (ability to make good decision)
        #             ft_shoot (when fts are awarded)
        # PRIMARY_O_REB --> o_reb (off miss)
        # DEFENSIVE RATINGS AT PLAY:
        # PRIMARY --> stickiness (ability to prevent getting open)
        #             steal (poke the ball out)
        #             block (if shot gets off)
        #             awareness (good decision making)
        # PRIMARY_D_REB --> d_reb (off miss)
        # POSSIBILITY TREE --> 1) Determine Steal or reach-in foul,
        # 2) Determine Open or Contested (create_3 and create_mid only),
        # 3) Determine Block, Shooting Foul, Make, or Miss (contested only for block/foul),
        # 4) Off miss, determine Offensive Rebound, Defensive Rebound, Off-ball foul, or Swat OB,
        # 5) Update stats, points, possession, stamina, substitutes where necessary
        if play_type in ('create_3', 'create_mid', 'iso_drive', 'post_up'):
            print("")
            if play_type == 'create_3':
                print('PLAY TYPE: Create 3')
            elif play_type == 'iso_drive':
                print('PLAY TYPE: Iso Drive')
            elif play_type == 'create_mid':
                print('PLAY TYPE: Create Mid Range')
            else:
                print('PLAY TYPE: Post Up')
            # Determine (1)
            # Low result = reach-in foul, High result = steal
            if play_type == 'create_3' or play_type == 'post_up':
                steal_threshold = {'lo': generate_random_int(5, 8), 'hi': generate_random_int(91, 95)}
            elif play_type == 'create_mid':
                steal_threshold = {'lo': generate_random_int(7, 11), 'hi': generate_random_int(88, 92)}
            else:
                steal_threshold = {'lo': generate_random_int(9, 13), 'hi': generate_random_int(85, 90)}
            # MODIFIERS
            self._non_binary_adjust_thresholds(primary_defender.steal.curr_rating, steal_threshold, 6, 'defense')
            self._non_binary_adjust_thresholds(primary_playmaker.awareness.curr_rating, steal_threshold, 6, 'offense')
            # Success Roll
            steal_success = generate_random_int(0, 100)
            if steal_success > steal_threshold['hi']:
                steal_OB = generate_random_int(0, 100)
                # Base 30% chance steal attempt goes OB
                if steal_OB > 30:
                    poss_change = self._record_a_steal(primary_defender, primary_playmaker, defense, offense)
                else:
                    stoppage = True
                    stoppage_type = 'OB'
                    print(f"Ball knocked out of bounds by {primary_defender.name}({defense_team.nickname}) from {primary_playmaker.name}({offense_team.nickname}).")

            elif steal_success < steal_threshold['lo']:
                stoppage = True
                primary_defender.game_stats['fouls'] += 1
                defense_team.fouls_in_q += 1
                print(f"Reach-in foul committed by {primary_defender.name}({defense_team.nickname}) on {primary_playmaker.name}({offense_team.nickname}).")
                # If offense is in the bonus take FTS
                if defense_team.fouls_in_q > 4 or (defense_team.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                    stoppage_type = self._shoot_fts(primary_playmaker, 2, offense, offense_team, offense_on_court, defense_on_court)
                    poss_change = True
                else:
                    stoppage_type = 'OB'
                    print(f"Ball taken out of bounds by {offense_team.nickname}.")

            # Determine (2)
            # Low result = Gets open, High result = Contested shot
            elif play_type in ('create_3', 'create_mid'):
                if play_type == 'create_3':
                    initial_open_threshold = generate_random_int(35, 51)
                else:
                    initial_open_threshold = generate_random_int(38, 56)
                # MODIFIERS
                offense_mod_open_threshold = self._binary_adjust_threshold(primary_playmaker.playmaking.curr_rating, initial_open_threshold, 8, 'offense')
                open_threshold = self._binary_adjust_threshold(primary_defender.stickiness.curr_rating, offense_mod_open_threshold, 8, 'defense')
                # Success roll
                open_success = generate_random_int(0, 100)
                if open_success < open_threshold:
                    # Determine (3)
                    # Low result = Make, High result = Miss
                    if play_type == 'create_3':
                        initial_open_threshold = generate_random_int(32, 44)
                        open_threshold = self._binary_adjust_threshold(primary_playmaker.open_3.curr_rating, initial_open_threshold, 12, 'offense')
                    else:
                        initial_open_threshold = generate_random_int(40, 58)
                        open_threshold = self._binary_adjust_threshold(primary_playmaker.open_mid.curr_rating, initial_open_threshold, 12, 'offense')
                    # MODIFIERS
                    # Success roll
                    open_success = generate_random_int(0, 100)
                    # If made
                    if open_success < open_threshold:
                        if play_type == 'create_3':
                            poss_change = self._make_a_three(primary_playmaker, offense, offense_team, offense_on_court, defense_on_court)
                        else:
                            poss_change = self._make_a_mid_range(primary_playmaker, offense, offense_team, offense_on_court, defense_on_court)
                    # If missed
                    # Determine (4)
                    else:
                        if play_type == 'create_3':
                            self._miss_a_three(primary_playmaker, offense_team, offense, 'open')
                        else:
                            self._miss_a_two(primary_playmaker, offense_team, offense, 'mid-range-open')
                        # Low result = Swat OB (determine off whom), High result = Foul (determine on whom)
                        swatOB_or_foul_threshold = {'lo': generate_random_int(6, 9), 'hi': generate_random_int(93, 96)}
                        # NO MODIFIERS (random result)
                        # Success Roll
                        swatOB_or_foul_success = generate_random_int(0, 100)
                        if swatOB_or_foul_success < swatOB_or_foul_threshold['lo']:
                            team_OB_success = generate_random_int(0, 100)
                            if team_OB_success < 50:
                                team_OB = offense_team
                                OB_player = offense_on_court[generate_random_int(0, 4)]
                                poss_change = True
                            else:
                                team_OB = defense_team
                                OB_player = defense_on_court[generate_random_int(0, 4)]
                            stoppage_type = 'OB'
                            stoppage = True
                            print(f"Ball swatted out of bounds off {OB_player.name} by {team_OB.nickname}.")
                        elif swatOB_or_foul_success > swatOB_or_foul_threshold['hi']:
                            stoppage = True
                            team_foul_success = generate_random_int(0, 100)
                            if team_foul_success < 50:
                                team_foul = offense_team
                                fouled_team = defense_team
                                fouled_team_stats = defense
                                foul_player = offense_on_court[generate_random_int(0, 4)]
                                fouled_player = defense_on_court[generate_random_int(0, 4)]
                                poss_change = True
                            else:
                                team_foul = defense_team
                                fouled_team = offense_team
                                fouled_team_stats = offense
                                foul_player = defense_on_court[generate_random_int(0, 4)]
                                fouled_player = offense_on_court[generate_random_int(0, 4)]
                            team_foul.fouls_in_q += 1
                            foul_player.game_stats['fouls'] += 1
                            print(f"Off ball foul committed by {foul_player.name} on {fouled_player.name}.")
                            # Check to see if team is in the bonus
                            if team_foul.fouls_in_q > 4 or (team_foul.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                                poss_change = True
                                stoppage_type = self._shoot_fts(fouled_player, 2, fouled_team_stats, fouled_team, offense_on_court, defense_on_court)
                            else:
                                stoppage_type = 'OB'
                        # Determine Rebound
                        else:
                            (poss_change, primary_o_reb, primary_d_reb) = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)
                # Contested 3
                # Determine (3)
                else:
                    # Low result = Shooting Foul, High result = Block
                    if play_type == 'create_3':
                        block_or_shooting_foul_threshold = {'lo': generate_random_int(2, 5), 'hi': generate_random_int(93, 96)}
                    else:
                        block_or_shooting_foul_threshold = {'lo': generate_random_int(8, 13), 'hi': generate_random_int(83, 90)}
                    # MODIFIERS
                    self._non_binary_adjust_thresholds(primary_defender.block.curr_rating, block_or_shooting_foul_threshold, 6, 'defense')
                    self._non_binary_adjust_thresholds(primary_defender.awareness.curr_rating, block_or_shooting_foul_threshold,6, 'defense')
                    # Success Roll
                    block_or_shooting_foul_success = generate_random_int(0, 100)
                    if block_or_shooting_foul_success < block_or_shooting_foul_threshold['lo']:
                        stoppage = True
                        poss_change = True
                        primary_defender.game_stats['fouls'] += 1
                        defense_team.fouls_in_q += 1
                        print(f"Shooting foul committed by {primary_defender.name}({primary_defender.position}) on {primary_playmaker.name}({primary_playmaker.position}).")
                        if play_type == 'create_3':
                            stoppage_type = self._shoot_fts(primary_playmaker, 3, offense, offense_team, offense_on_court, defense_on_court)
                        else:
                            stoppage_type = self._shoot_fts(primary_playmaker, 2, offense, offense_team, offense_on_court, defense_on_court)
                    elif block_or_shooting_foul_success > block_or_shooting_foul_threshold['hi']:
                        (stoppage, stoppage_type, poss_change) = self._record_a_block(primary_defender, defense, defense_team, offense_team)
                    else:
                        if play_type == 'create_3':
                            initial_contest_threshold = generate_random_int(20, 33)
                            contest_threshold = self._binary_adjust_threshold(primary_playmaker.contest_3.curr_rating, initial_contest_threshold, 12, 'offense')
                        else:
                            initial_contest_threshold = generate_random_int(30, 46)
                            contest_threshold = self._binary_adjust_threshold(primary_playmaker.contest_mid.curr_rating, initial_contest_threshold, 12, 'offense')
                        # MODIFIERS
                        # Success roll
                        contest_success = generate_random_int(0, 100)
                        # If made
                        if contest_success < contest_threshold:
                            if play_type == 'create_3':
                                poss_change = self._make_a_three(primary_playmaker, offense, offense_team, offense_on_court, defense_on_court)
                            else:
                                poss_change = self._make_a_mid_range(primary_playmaker, offense, offense_team, offense_on_court, defense_on_court)
                        # If missed
                        # Determine (4)
                        else:
                            if play_type == 'create_3':
                                self._miss_a_three(primary_playmaker, offense_team, offense, 'contested')
                            else:
                                self._miss_a_two(primary_playmaker, offense_team, offense, 'mid-range-contested')
                            # Low result = Swat OB (determine off whom), High result = Foul (determine on whom)
                            swatOB_or_foul_threshold = {'lo': generate_random_int(6, 9), 'hi': generate_random_int(93, 96)}
                            # NO MODIFIERS (random result)
                            # Success Roll
                            swatOB_or_foul_success = generate_random_int(0, 100)
                            if swatOB_or_foul_success < swatOB_or_foul_threshold['lo']:
                                team_OB_success = generate_random_int(0, 100)
                                if team_OB_success < 50:
                                    team_OB = offense_team
                                    OB_player = offense_on_court[generate_random_int(0, 4)]
                                    poss_change = True
                                else:
                                    team_OB = defense_team
                                    OB_player = defense_on_court[generate_random_int(0, 4)]
                                stoppage_type = 'OB'
                                stoppage = True
                                print(f"Ball swatted out of bounds off {OB_player.name} by {team_OB.nickname}.")
                            elif swatOB_or_foul_success > swatOB_or_foul_threshold['hi']:
                                stoppage = True
                                team_foul_success = generate_random_int(0, 100)
                                if team_foul_success < 50:
                                    team_foul = offense_team
                                    fouled_team = defense_team
                                    fouled_team_stats = defense
                                    foul_player = offense_on_court[generate_random_int(0, 4)]
                                    fouled_player = defense_on_court[generate_random_int(0, 4)]
                                    poss_change = True
                                else:
                                    team_foul = defense_team
                                    fouled_team = offense_team
                                    fouled_team_stats = offense
                                    foul_player = defense_on_court[generate_random_int(0, 4)]
                                    fouled_player = offense_on_court[generate_random_int(0, 4)]
                                team_foul.fouls_in_q += 1
                                foul_player.game_stats['fouls'] += 1
                                print(f"Off ball foul committed by {foul_player.name}({team_foul.nickname}) on {fouled_player.name}({fouled_team.nickname}).")
                                # Check to see if team is in the bonus
                                if team_foul.fouls_in_q > 4 or (team_foul.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                                    poss_change = True
                                    stoppage_type = self._shoot_fts(fouled_player, 2, fouled_team_stats, fouled_team, offense_on_court, defense_on_court)
                                else:
                                    stoppage_type = 'OB'
                            # Determine Rebound
                            else:
                                (poss_change, primary_o_reb, primary_d_reb) = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)
            # Post ups and Iso Drives
            else:
                # Low result = No foul, High result = Offensive foul
                initial_offensive_foul_threshold = generate_random_int(92, 95)
                # MODIFIERS
                offense_mod_offensive_foul_threshold = self._binary_adjust_threshold(primary_playmaker.awareness.curr_rating, initial_offensive_foul_threshold, 10, 'offense')
                offensive_foul_threshold = self._binary_adjust_threshold(primary_defender.awareness.curr_rating, offense_mod_offensive_foul_threshold, 10, 'defense')
                # Success Roll
                offensive_foul_success = generate_random_int(0, 100)
                if offensive_foul_success > offensive_foul_threshold:
                    (stoppage, poss_change, stoppage_type) = self._record_offensive_foul(primary_playmaker, primary_defender, offense, offense_team, defense_team)
                if not poss_change:
                    # Low result = Shooting Foul, High result = Block
                    block_or_shooting_foul_threshold = {'lo': generate_random_int(10, 15), 'hi': generate_random_int(80, 85)}
                    # MODIFIERS
                    self._non_binary_adjust_thresholds(primary_defender.block.curr_rating, block_or_shooting_foul_threshold,6, 'defense')
                    self._non_binary_adjust_thresholds(primary_defender.awareness.curr_rating, block_or_shooting_foul_threshold, 6, 'defense')
                    # Success Roll
                    block_or_shooting_foul_success = generate_random_int(0, 100)
                    if block_or_shooting_foul_success < block_or_shooting_foul_threshold['lo']:
                        stoppage = True
                        poss_change = True
                        primary_defender.game_stats['fouls'] += 1
                        defense_team.fouls_in_q += 1
                        print(f"Shooting foul committed by {primary_defender.name}({defense_team.nickname}) on {primary_playmaker.name}({offense_team.nickname}).")
                        stoppage_type = self._shoot_fts(primary_playmaker, 2, offense, offense_team, offense_on_court, defense_on_court)
                    elif block_or_shooting_foul_success > block_or_shooting_foul_threshold['hi']:
                        (stoppage, stoppage_type, poss_change) = self._record_a_block(primary_defender, defense, defense_team, offense_team)
                    else:
                        if play_type == 'iso_drive':
                            initial_shot_threshold = generate_random_int(45, 55)
                            shot_threshold = self._binary_adjust_threshold(primary_playmaker.finishing.curr_rating, initial_shot_threshold, 12, 'offense')
                        else:
                            initial_shot_threshold = generate_random_int(47, 57)
                            shot_threshold = self._binary_adjust_threshold(primary_playmaker.post_up.curr_rating, initial_shot_threshold, 12, 'offense')
                        # MODIFIERS
                        # Success roll
                        shot_success = generate_random_int(0, 100)
                        # If made
                        if shot_success < shot_threshold:
                            dunk_or_layup = generate_random_int(0, 100)
                            if dunk_or_layup < 25:
                                poss_change = self._make_a_dunk(primary_playmaker, offense, offense_team, offense_on_court, defense_on_court)
                            else:
                                poss_change = self._make_a_layup(primary_playmaker, offense, offense_team, offense_on_court, defense_on_court)
                        # If missed
                        # Determine (4)
                        else:
                            if play_type == 'iso_drive':
                                self._miss_a_two(primary_playmaker, offense_team, offense, 'layup')
                            else:
                                self._miss_a_two(primary_playmaker, offense_team, offense, 'post-up')
                            # Low result = Swat OB (determine off whom), High result = Foul (determine on whom)
                            swatOB_or_foul_threshold = {'lo': generate_random_int(6, 9), 'hi': generate_random_int(93, 96)}
                            # NO MODIFIERS (random result)
                            # Success Roll
                            swatOB_or_foul_success = generate_random_int(0, 100)
                            if swatOB_or_foul_success < swatOB_or_foul_threshold['lo']:
                                team_OB_success = generate_random_int(0, 100)
                                if team_OB_success < 50:
                                    team_OB = offense_team
                                    OB_player = offense_on_court[generate_random_int(0, 4)]
                                    poss_change = True
                                else:
                                    team_OB = defense_team
                                    OB_player = defense_on_court[generate_random_int(0, 4)]
                                stoppage_type = 'OB'
                                stoppage = True
                                print(f"Ball swatted out of bounds off {OB_player.name} by {team_OB.nickname}.")
                            elif swatOB_or_foul_success > swatOB_or_foul_threshold['hi']:
                                stoppage = True
                                team_foul_success = generate_random_int(0, 100)
                                if team_foul_success < 50:
                                    team_foul = offense_team
                                    fouled_team = defense_team
                                    fouled_team_stats = defense
                                    foul_player = offense_on_court[generate_random_int(0, 4)]
                                    fouled_player = defense_on_court[generate_random_int(0, 4)]
                                    poss_change = True
                                else:
                                    team_foul = defense_team
                                    fouled_team = offense_team
                                    fouled_team_stats = offense
                                    foul_player = defense_on_court[generate_random_int(0, 4)]
                                    fouled_player = offense_on_court[generate_random_int(0, 4)]
                                team_foul.fouls_in_q += 1
                                foul_player.game_stats['fouls'] += 1
                                print(f"Off ball foul committed by {foul_player.name}({team_foul.nickname}) on {fouled_player.name}({fouled_team.nickname}).")
                                # Check to see if team is in the bonus
                                if team_foul.fouls_in_q > 4 or (team_foul.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                                    poss_change = True
                                    stoppage_type = self._shoot_fts(fouled_player, 2, fouled_team_stats, fouled_team, offense_on_court, defense_on_court)
                                else:
                                    stoppage_type = 'OB'
                            # Determine Rebound
                            else:
                                (poss_change, primary_o_reb, primary_d_reb) = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)
        # play_type == pick_n_roll, drive_n_pass, find_cutter
        #
        # OFFENSIVE RATINGS AT PLAY:
        # PRIMARY --> playmaking (ability to make good pass)
        #             awareness (ability to make good decision)
        #             open_3/open_mid (for open shots)
        #             constest_3/contest_mid/finishing/post_up (for contested shots)
        #             ft_shoot (when fts are awarded)
        # SECONDARY --> playmaking (ability to make good pass --> pick_n_roll only)
        #               awareness (ability to make good decision --> pick_n_roll only)
        #               open_3/open_mid (for open shots)
        #               constest_3/contest_mid/finishing/post_up (for contested shots)
        #               ft_shoot (when fts are awarded)
        # PRIMARY_O_REB --> o_reb (off miss)
        # DEFENSIVE RATINGS AT PLAY:
        # PRIMARY --> stickiness (ability to prevent getting open)
        #             steal (poke the ball out)
        #             block (if shot gets off)
        #             awareness (good decision making)
        # SECONDARY --> stickiness (ability to prevent getting open)
        #               steal (poke the ball out)
        #               block (if shot gets off)
        #               awareness (good decision making)
        # PRIMARY_D_REB --> d_reb (off miss)
        # POSSIBILITY TREE --> 1) Determine Steal or reach-in foul,
        # 2) Determine Successful pass(es) or turnover (pick_n_roll --> 0, 1, or 2 passes, all others exactly 1)
        # 3) Determine secondary playmaker and defender,
        # 4) Determine shot type (and shot taker for pick_n_roll)
        # 5) Determine Block, Shooting Foul, Make, or Miss (contested only for block/foul),
        # 6) Off miss, determine Offensive Rebound, Defensive Rebound, Off-ball foul, or Swat OB,
        # 7) Update stats, points, possession, stamina, substitutes where necessary
        else:
            print("")
            if play_type == 'pick_n_roll':
                print('PLAY TYPE: Pick & Roll')
            elif play_type == 'iso_drive':
                print('PLAY TYPE: Drive & Pass')
            else:
                print('PLAY TYPE: Find Cutter')
            # Determine (1)
            # Low result = reach-in foul, High result = steal
            steal_threshold = {'lo': generate_random_int(5, 8), 'hi': generate_random_int(91, 95)}
            # MODIFIERS
            self._non_binary_adjust_thresholds(primary_defender.steal.curr_rating, steal_threshold, 6, 'defense')
            self._non_binary_adjust_thresholds(primary_playmaker.awareness.curr_rating, steal_threshold, 6, 'offense')
            # Success Roll
            steal_success = generate_random_int(0, 100)
            if steal_success > steal_threshold['hi']:
                steal_OB = generate_random_int(0, 100)
                # Base 30% chance steal attempt goes OB
                if steal_OB > 30:
                    poss_change = self._record_a_steal(primary_defender, primary_playmaker, defense, offense)
                else:
                    stoppage = True
                    stoppage_type = 'OB'
                    print(f"Ball knocked out of bounds by {primary_defender.name}({defense_team.nickname}) from {primary_playmaker.name}({offense_team.nickname}).")

            elif steal_success < steal_threshold['lo']:
                stoppage = True
                primary_defender.game_stats['fouls'] += 1
                defense_team.fouls_in_q += 1
                print(f"Reach-in foul committed by {primary_defender.name}({defense_team.nickname}) on {primary_playmaker.name}({offense_team.nickname}).")
                # If offense is in the bonus take FTS
                if defense_team.fouls_in_q > 4 or (defense_team.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                    stoppage_type = self._shoot_fts(primary_playmaker, 2, offense, offense_team, offense_on_court, defense_on_court)
                    poss_change = True
                else:
                    stoppage_type = 'OB'
                    print(f"Ball taken out of bounds by {offense_team.nickname}.")
            else:
                # Determine (2)
                # Determine number of passes for pick_n_rolls
                pass_count = 1
                if play_type == 'pick_n_roll':
                    zero_or_mult_pass_threshold = generate_random_int(65, 80)
                    zero_or_mult_pass_success = generate_random_int(0, 100)
                    if zero_or_mult_pass_success > zero_or_mult_pass_threshold:
                        zero_or_two_roll = generate_random_int(0, 100)
                        if zero_or_two_roll > 50:
                            pass_count = 0
                        else:
                            pass_count = 2
                # If passes occur, determine (3)
                on_ball = primary_playmaker
                on_ball_defense = primary_defender
                if pass_count > 0:
                    secondary_playmaker = self._determine_secondary_playmaker(primary_playmaker, offense_on_court)
                    matchup_dict = self._determine_matchups(offense_on_court, defense_on_court)
                    secondary_defender = matchup_dict[primary_playmaker.name]
                    off_ball = secondary_playmaker
                    off_ball_defense = secondary_defender
                # Determine is pass(es) are successful
                for _ in range(pass_count):
                    # Low result = Successful pass, High result = Steal
                    initial_pass_threshold = generate_random_int(92, 100)
                    # MODIFIERS
                    offense_mod_pass_threshold = self._binary_adjust_threshold(on_ball.playmaking.curr_rating, initial_pass_threshold, 12, 'offense')
                    defense_mod_pass_threshold = self._binary_adjust_threshold(on_ball_defense.stickiness.curr_rating, offense_mod_pass_threshold, 9, 'defense')
                    final_mod_pass_threshold = self._binary_adjust_threshold(off_ball.awareness.curr_rating, defense_mod_pass_threshold, 7, 'offense')
                    pass_threshold = self._binary_adjust_threshold(off_ball_defense.steal.curr_rating, final_mod_pass_threshold, 10, 'defense')
                    # Success Roll
                    pass_success = generate_random_int(0, 100)
                    if pass_success > pass_threshold:
                        steal_OB = generate_random_int(0, 100)
                        # 30% chance steal attempt goes OB
                        if steal_OB > 30:
                            poss_change = self._record_a_steal(off_ball_defense, on_ball, defense, offense)
                        else:
                            stoppage = True
                            stoppage_type = 'OB'
                            print(f"Ball knocked out of bounds by {off_ball_defense.name}({defense_team.nickname}) from {on_ball.name}({offense_team.nickname}).")
                    else:
                        (on_ball, off_ball, on_ball_defense, off_ball_defense) = (off_ball, on_ball, off_ball_defense, on_ball_defense)
                # Determine (4)
                # Low result = Finish at basket, Mid result = Mid range, High result = 3 pointer
                if play_type == 'drive_n_pass' or pass_count == 1:
                    shot_type_threshold = {'lo': generate_random_int(10, 12), 'hi': generate_random_int(50, 56)}
                # 'find_cutter', pass_count == 0 or 2
                else:
                    shot_type_threshold = {'lo': generate_random_int(61, 73), 'hi': generate_random_int(90, 92)}
                shot_type_determiner = generate_random_int(0, 100)
                if shot_type_determiner < shot_type_threshold['lo']:
                    shot_type = 'finish_at_basket'
                elif shot_type_determiner <= shot_type_threshold['hi']:
                    shot_type = 'mid_range'
                else:
                    shot_type = 'three_pointer'
                # Determine (5)
                # Determine if shot is open or contested if it is not a finish at bucket
                shot_contest = 'contested'
                if shot_type != 'finish_at_basket':
                    # Low result = Open shot, High result = Contested Shot
                    if shot_type == 'three_pointer':
                        initial_open_threshold = generate_random_int(42, 61)
                    else:
                        initial_open_threshold = generate_random_int(48, 70)
                    # MODIFIERS
                    if pass_count == 1:
                        initial_open_threshold += generate_random_int(0, 5)
                    elif pass_count == 2:
                        initial_open_threshold += generate_random_int(5, 10)
                    offense_mod_open_threshold = self._binary_adjust_threshold(on_ball.playmaking.curr_rating, initial_open_threshold, 8, 'offense')
                    open_threshold = self._binary_adjust_threshold(on_ball_defense.stickiness.curr_rating, offense_mod_open_threshold, 8, 'defense')
                    # Success roll
                    open_success = generate_random_int(0, 100)
                    if open_success < open_threshold:
                        shot_contest = 'open'
                if shot_contest == 'open':
                    if shot_type == 'three_pointer':
                        initial_open_threshold = generate_random_int(32, 44)
                        open_threshold = self._binary_adjust_threshold(on_ball.open_3.curr_rating, initial_open_threshold, 12, 'offense')
                    else:
                        initial_open_threshold = generate_random_int(40, 58)
                        open_threshold = self._binary_adjust_threshold(on_ball.open_mid.curr_rating, initial_open_threshold, 12, 'offense')
                    # MODIFIERS
                    # Success roll
                    open_success = generate_random_int(0, 100)
                    # If made
                    if open_success < open_threshold:
                        if pass_count > 0:
                            self._record_an_assist(off_ball, offense)
                        if shot_type == 'three_pointer':
                            poss_change = self._make_a_three(on_ball, offense, offense_team, offense_on_court, defense_on_court)
                        else:
                            poss_change = self._make_a_mid_range(on_ball, offense, offense_team, offense_on_court, defense_on_court)
                    # If missed
                    # Determine (6)
                    else:
                        if shot_type == 'three_pointer':
                            self._miss_a_three(on_ball, offense_team, offense, 'open')
                        else:
                            self._miss_a_two(on_ball, offense_team, offense, 'mid-range-open')
                        # Low result = Swat OB (determine off whom), High result = Foul (determine on whom)
                        swatOB_or_foul_threshold = {'lo': generate_random_int(6, 9), 'hi': generate_random_int(93, 96)}
                        # NO MODIFIERS (random result)
                        # Success Roll
                        swatOB_or_foul_success = generate_random_int(0, 100)
                        if swatOB_or_foul_success < swatOB_or_foul_threshold['lo']:
                            team_OB_success = generate_random_int(0, 100)
                            if team_OB_success < 50:
                                team_OB = offense_team
                                OB_player = offense_on_court[generate_random_int(0, 4)]
                                poss_change = True
                            else:
                                team_OB = defense_team
                                OB_player = defense_on_court[generate_random_int(0, 4)]
                            stoppage_type = 'OB'
                            stoppage = True
                            print(f"Ball swatted out of bounds off {OB_player.name} by {team_OB.nickname}.")
                        elif swatOB_or_foul_success > swatOB_or_foul_threshold['hi']:
                            stoppage = True
                            team_foul_success = generate_random_int(0, 100)
                            if team_foul_success < 50:
                                team_foul = offense_team
                                fouled_team = defense_team
                                fouled_team_stats = defense
                                foul_player = offense_on_court[generate_random_int(0, 4)]
                                fouled_player = defense_on_court[generate_random_int(0, 4)]
                                poss_change = True
                            else:
                                team_foul = defense_team
                                fouled_team = offense_team
                                fouled_team_stats = offense
                                foul_player = defense_on_court[generate_random_int(0, 4)]
                                fouled_player = offense_on_court[generate_random_int(0, 4)]
                            team_foul.fouls_in_q += 1
                            foul_player.game_stats['fouls'] += 1
                            print(f"Off ball foul committed by {foul_player.name} on {fouled_player.name}.")
                            # Check to see if team is in the bonus
                            if team_foul.fouls_in_q > 4 or (team_foul.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                                poss_change = True
                                stoppage_type = self._shoot_fts(fouled_player, 2, fouled_team_stats, fouled_team, offense_on_court, defense_on_court)
                            else:
                                stoppage_type = 'OB'
                        # Determine Rebound
                        else:
                            (poss_change, primary_o_reb, primary_d_reb) = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)
                else:
                    if shot_type == 'finish_at_basket':
                        # Low result = No foul, High result = Offensive foul
                        initial_offensive_foul_threshold = generate_random_int(92, 95)
                        # MODIFIERS
                        offense_mod_offensive_foul_threshold = self._binary_adjust_threshold(on_ball.awareness.curr_rating, initial_offensive_foul_threshold, 10, 'offense')
                        offensive_foul_threshold = self._binary_adjust_threshold(on_ball_defense.awareness.curr_rating, offense_mod_offensive_foul_threshold, 10, 'defense')
                        # Success Roll
                        offensive_foul_success = generate_random_int(0, 100)
                        if offensive_foul_success > offensive_foul_threshold:
                            (stoppage, poss_change, stoppage_type) = self._record_offensive_foul(on_ball, on_ball_defense, offense, offense_team, defense_team)
                    if not poss_change:
                        # Low result = Shooting Foul, High result = Block
                        if shot_type == 'finish_at_basket':
                            block_or_shooting_foul_threshold = {'lo': generate_random_int(10, 15), 'hi': generate_random_int(84, 88)}
                        elif shot_type == 'three_pointer':
                            block_or_shooting_foul_threshold = {'lo': generate_random_int(2, 5), 'hi': generate_random_int(95, 97)}
                        else:
                            block_or_shooting_foul_threshold = {'lo': generate_random_int(8, 13), 'hi': generate_random_int(87, 93)}
                        # MODIFIERS
                        self._non_binary_adjust_thresholds(on_ball_defense.block.curr_rating, block_or_shooting_foul_threshold, 6, 'defense')
                        self._non_binary_adjust_thresholds(on_ball_defense.awareness.curr_rating, block_or_shooting_foul_threshold, 6, 'defense')
                        # Success Roll
                        block_or_shooting_foul_success = generate_random_int(0, 100)
                        if block_or_shooting_foul_success < block_or_shooting_foul_threshold['lo']:
                            stoppage = True
                            poss_change = True
                            primary_defender.game_stats['fouls'] += 1
                            defense_team.fouls_in_q += 1
                            print(f"Shooting foul committed by {on_ball_defense.name}({defense_team.nickname}) on {on_ball.name}({offense_team.nickname}).")
                            stoppage_type = self._shoot_fts(on_ball, 2, offense, offense_team, offense_on_court, defense_on_court)
                        elif block_or_shooting_foul_success > block_or_shooting_foul_threshold['hi']:
                            (stoppage, stoppage_type, poss_change) = self._record_a_block(on_ball_defense, defense, defense_team, offense_team)
                        else:
                            if shot_type == 'finish_at_basket':
                                initial_shot_threshold = generate_random_int(47, 56)
                                shot_threshold = self._binary_adjust_threshold(on_ball.finishing.curr_rating, initial_shot_threshold, 12, 'offense')
                            elif shot_type == 'three_pointer':
                                initial_contest_threshold = generate_random_int(23, 35)
                                shot_threshold = self._binary_adjust_threshold(on_ball.contest_3.curr_rating, initial_contest_threshold, 12,'offense')
                            else:
                                initial_contest_threshold = generate_random_int(33, 49)
                                shot_threshold = self._binary_adjust_threshold(on_ball.contest_mid.curr_rating, initial_contest_threshold, 12,'offense')
                            # Success roll
                            shot_success = generate_random_int(0, 100)
                            # If made
                            if shot_success < shot_threshold:
                                if pass_count > 0:
                                    self._record_an_assist(off_ball, offense)
                                if shot_type == 'finish_at_basket':
                                    dunk_or_layup = generate_random_int(0, 100)
                                    if dunk_or_layup < 25:
                                        poss_change = self._make_a_dunk(on_ball, offense, offense_team, offense_on_court, defense_on_court)
                                    else:
                                        poss_change = self._make_a_layup(on_ball, offense, offense_team, offense_on_court, defense_on_court)
                                elif shot_type == 'three_pointer':
                                    poss_change = self._make_a_three(on_ball, offense, offense_team, offense_on_court, defense_on_court)
                                else:
                                    poss_change = self._make_a_mid_range(on_ball, offense, offense_team, offense_on_court, defense_on_court)
                            # If missed
                            # Determine (6)
                            else:
                                if shot_type == 'finish_at_basket':
                                    self._miss_a_two(on_ball, offense_team, offense, 'layup')
                                elif shot_type == 'three_pointer':
                                    self._miss_a_three(on_ball, offense_team, offense, 'contested')
                                else:
                                    self._miss_a_two(on_ball, offense_team, offense, 'mid-range-contested')
                                # Low result = Swat OB (determine off whom), High result = Foul (determine on whom)
                                swatOB_or_foul_threshold = {'lo': generate_random_int(6, 9), 'hi': generate_random_int(93, 96)}
                                # NO MODIFIERS (random result)
                                # Success Roll
                                swatOB_or_foul_success = generate_random_int(0, 100)
                                if swatOB_or_foul_success < swatOB_or_foul_threshold['lo']:
                                    team_OB_success = generate_random_int(0, 100)
                                    if team_OB_success < 50:
                                        team_OB = offense_team
                                        OB_player = offense_on_court[generate_random_int(0, 4)]
                                        poss_change = True
                                    else:
                                        team_OB = defense_team
                                        OB_player = defense_on_court[generate_random_int(0, 4)]
                                    stoppage_type = 'OB'
                                    stoppage = True
                                    print(f"Ball swatted out of bounds off {OB_player.name} by {team_OB.nickname}.")
                                elif swatOB_or_foul_success > swatOB_or_foul_threshold['hi']:
                                    stoppage = True
                                    team_foul_success = generate_random_int(0, 100)
                                    if team_foul_success < 50:
                                        team_foul = offense_team
                                        fouled_team = defense_team
                                        fouled_team_stats = defense
                                        foul_player = offense_on_court[generate_random_int(0, 4)]
                                        fouled_player = defense_on_court[generate_random_int(0, 4)]
                                        poss_change = True
                                    else:
                                        team_foul = defense_team
                                        fouled_team = offense_team
                                        fouled_team_stats = offense
                                        foul_player = defense_on_court[generate_random_int(0, 4)]
                                        fouled_player = offense_on_court[generate_random_int(0, 4)]
                                    team_foul.fouls_in_q += 1
                                    foul_player.game_stats['fouls'] += 1
                                    print(f"Off ball foul committed by {foul_player.name}({team_foul.nickname}) on {fouled_player.name}({fouled_team.nickname}).")
                                    # Check to see if team is in the bonus
                                    if team_foul.fouls_in_q > 4 or (team_foul.fouls_in_q > 1 and self.curr_quarter == 'OT'):
                                        poss_change = True
                                        stoppage_type = self._shoot_fts(fouled_player, 2, fouled_team_stats, fouled_team, offense_on_court, defense_on_court)
                                    else:
                                        stoppage_type = 'OB'
                                # Determine Rebound
                                else:
                                    (poss_change, primary_o_reb, primary_d_reb) = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)


        # Happens after any result
        self._decrease_stamina_onCourt(primary_playmaker, primary_defender, secondary_playmaker, secondary_defender,
                                       offense_on_court, defense_on_court, primary_o_reb, primary_d_reb)
        self._update_play_counts()
        if poss_change:
            self.curr_poss = defense
        if not stoppage:
            self._increase_stamina_bench(offense_on_bench, defense_on_bench)
        else:
            self._increase_stamina_all(stoppage_type)
            self._check_for_subs()

    def _simulate_play(self):
        """
        Simulates a play.
        """
        # SETUP

        if self.curr_poss == 'home_team':
            offense_team = self.home_team
            defense_team = self.away_team
            offense_on_court = self.home_onCourt
            defense_on_court = self.away_onCourt
            offense_on_bench = self.home_onBench
            defense_on_bench = self.away_onBench
        else:
            offense_team = self.away_team
            defense_team = self.home_team
            offense_on_court = self.away_onCourt
            defense_on_court = self.home_onCourt
            offense_on_bench = self.away_onBench
            defense_on_bench = self.home_onBench

        # Team can choose to take timeout
        if self._check_for_timeout(offense_on_court, offense_team, defense_team):
            return

        # Determine playmaker
        primary_playmaker = self._determine_primary_playmaker(offense_on_court)

        # Determine primary defender (or Zone --> composite of a few nearby players)
        matchup_dict = self._determine_matchups(offense_on_court, defense_on_court)
        primary_defender = matchup_dict[primary_playmaker.name]

        # Determine attempted play
        play_type = self._determine_play_type(primary_playmaker, primary_defender)

        # Determine outcome, update possession (if necessary), update stamina, on stoppage --> allow subs,
        # update stats and points (if necessary)
        self._determine_play_outcome(primary_playmaker, primary_defender, play_type, offense_team, defense_team,
                                     offense_on_court, defense_on_court, offense_on_bench, defense_on_bench)

    # Public Methods
    def simulate_game(self):
        """
        Simulate a full game.
        """
        # Get game setup
        self._determine_tipoff()
        self._set_onCourt()
        # Print out rosters with basic ratings
        print({'TEAM STARTERS': self.home_team.nickname})
        for player in self.home_onCourt:
            print({
                'name': player.name,
                'position': player.position,
                'overall': player.overall,
                'o_ovr': player.o_ovr,
                'd_ovr': player.d_ovr
            })
        print({'TEAM BENCH': self.home_team.nickname})
        for player in self.home_onBench:
            print({
                'name': player.name,
                'position': player.position,
                'overall': player.overall,
                'o_ovr': player.o_ovr,
                'd_ovr': player.d_ovr
            })
        print({'TEAM STARTERS': self.away_team.nickname})
        for player in self.away_onCourt:
            print({
                'name': player.name,
                'position': player.position,
                'overall': player.overall,
                'o_ovr': player.o_ovr,
                'd_ovr': player.d_ovr
            })
        print({'TEAM BENCH': self.away_team.nickname})
        for player in self.away_onBench:
            print({
                'name': player.name,
                'position': player.position,
                'overall': player.overall,
                'o_ovr': player.o_ovr,
                'd_ovr': player.d_ovr
            })
        # Simulate Q1
        for _ in range(self.q1_plays):
            self._simulate_play()
        print("")
        print('END Q1')
        # Log stats, reset trackers
        self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Simulate Q2
        self.curr_quarter = 2
        for _ in range(self.q2_plays):
            self._simulate_play()
        print("")
        print('END Q2')
        # Re-insert starters, reset stamina
        self._reset_stamina()
        self._set_onCourt()
        # Log stats, reset trackers
        self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Simulate Q3
        self.curr_quarter = 3
        for _ in range(self.q3_plays):
            self._simulate_play()
        print("")
        print('END Q3')
        # Log stats, reset trackers
        self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Simulate Q4
        self.curr_quarter = 4
        for _ in range(self.q4_plays):
            self._simulate_play()
        print("")
        print('END Q4')
        # Log stats, reset trackers
        self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Simulate OT if needed
        # Two timeouts awarded to each team for OT periods
        self.home_team.timeouts = 2
        self.away_team.timeouts = 2
        self.curr_quarter = 'OT'
        # Count the number of OTs
        ot_count = 1
        while self.home_team.points_total == self.away_team.points_total:
            self.OT_plays_current += generate_random_int(13, 20)
            self.total_plays += self.OT_plays_current
            for _ in range (self.OT_plays_current):
                self._simulate_play()
            print("")
            print(f"END OT{ot_count}")
            self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
            print(f"{self.home_team.nickname}: {self.home_team.points_total}")
            print(f"{self.away_team.nickname}: {self.away_team.points_total}")
            self.OT_plays_current = 0
            ot_count += 1
        print("")
        print('END GAME')
        # Update minutes for all players
        self._update_minutes(self.total_plays, ot_count)
        # Print End of game stats
        self._print_end_of_game_stats(ot_count)
        # Log player stats and game stats
        if self.home_team.points_total > self.away_team.points_total:
            self.home_team.update_season_stats(self.game_stat_block, 'home', 'win')
            self.away_team.update_season_stats(self.game_stat_block, 'away', 'loss')
        else:
            self.home_team.update_season_stats(self.game_stat_block, 'home', 'loss')
            self.away_team.update_season_stats(self.game_stat_block, 'away', 'win')
        # Optional print statements to see logged and updated stats
        # print(f"{self.home_team.nickname} WINS-LOSSES: {self.home_team.wins} - {self.home_team.losses}")
        # print(f"{self.away_team.nickname} WINS-LOSSES: {self.away_team.wins} - {self.away_team.losses}")
        # print(self.home_team.total_stats)
        # print(self.home_team.average_stats)
        # print(self.away_team.total_stats)
        # print(self.away_team.average_stats)
        # print(self.home_team.roster[0].season_stats)
        # print(self.home_team.roster[0].career_stats)
        # print(self.away_team.roster[0].season_stats)
        # print(self.away_team.roster[0].career_stats)
        # Reset starters, stamina, and trackers for next game
        self._reset_stamina()
        self._set_onCourt()
        self.home_team.points_total = 0
        self.away_team.points_total = 0
        self.home_team.timeouts = 5
        self.away_team.timeouts = 5