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
        self.OT_plays_total = 0
        self.OT_plays_current = 0
        self.total_plays = self.q1_plays + self.q2_plays + self.q3_plays + self.q4_plays + self.OT_plays_total
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

        # Everyone else goes to the bench
        self.home_onBench = [p for p in self.home_team.bench if p not in self.home_onCourt]
        self.away_onBench = [p for p in self.away_team.bench if p not in self.away_onCourt]

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
            'timeout': {'lo': 12, 'hi': 18},
            'OB': {'lo': 2, 'hi': 4},
            'fts': {'lo': 3, 'hi': 6}
        }
        if stoppage_type in stamina_dict:
            for player in self.home_team.roster:
                increase = generate_random_int(stamina_dict[stoppage_type]['lo'],
                                                stamina_dict[stoppage_type]['hi'])
                player.stamina = min(99, player.stamina + increase)
            for player in self.away_team.roster:
                increase = generate_random_int(stamina_dict[stoppage_type]['lo'],
                                                stamina_dict[stoppage_type]['hi'])
                player.stamina = min(99, player.stamina + increase)
        else:
            print('Error! Unknown stoppage type.')

    def _increase_stamina_bench(self, home_bench, away_bench):
        """
        Stamina increase for bench whenever a normal play occurs.
        """
        for player in home_bench:
            player.stamina += min(99, generate_random_int(2, 4))
        for player in away_bench:
            player.stamina += min(99, generate_random_int(2, 4))

    def _decrease_stamina_onCourt(self, primary_playmaker, primary_defender, secondary_playmaker, secondary_defender,
                                  offense_on_court, defense_on_court):
        """
        Stamina decrease for whoever is on the court, with bigger decreases for active playmakers.
        """
        teams_on_court = [offense_on_court, defense_on_court]
        for team in teams_on_court:
            for player in team:
                if player == primary_playmaker or player == primary_defender:
                    player.stamina -= generate_random_int(5, 8)
                elif player == secondary_playmaker or player == secondary_defender:
                    player.stamina -= generate_random_int(4, 7)
                else:
                    player.stamina -= generate_random_int(2, 5)

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

    # CHECKS FOR TIMEOUTS AND SUBS
    def _check_for_subs(self):
        """
        Runs the handle_subs() method for each team to determine if a team wants to substitute any of the
        players on court for those on the bench.
        """
        def handle_subs(on_court, on_bench, starters, team_name):
            # Check to ensure there is no overlap error between on court and on bench players.
            overlap = set(on_court) & set(on_bench)
            if overlap:
                print(f"⚠️ Overlap detected in {team_name}: {[p.name for p in overlap]} "
                      f"found in both court and bench. Auto-fixing.")
                on_bench[:] = [p for p in on_bench if p not in on_court]

            subs_to_make = []
            available_bench = get_sorted_players(on_bench)[:]  # fresh copy

            # Plan substitutions
            for court_player in on_court:
                if court_player.stamina < 30 or court_player not in starters.values():
                    cp_position = 'guard' if court_player.position in ('PG', 'SG') else 'forward'

                    for bench_player in available_bench:
                        if bench_player.stamina <= 75:
                            continue

                        if (bench_player.position in ('PG', 'SG') and cp_position == 'guard') or \
                                (bench_player.position in ('SF', 'PF', 'C') and cp_position == 'forward'):
                            subs_to_make.append((court_player, bench_player))
                            available_bench.remove(bench_player)  # prevent reuse
                            break

            # Commit substitutions
            new_court = list(on_court)
            new_bench = list(on_bench)

            for out_p, in_p in subs_to_make:
                if out_p not in new_court or in_p not in new_bench:
                    print(f"⚠️ Sub inconsistency: {out_p.name} / {in_p.name} not found where expected.")
                    continue

                new_court.remove(out_p)
                new_court.append(in_p)

                new_bench.remove(in_p)
                new_bench.append(out_p)

                print(f"{out_p.name} ({out_p.position}) subs out for {in_p.name} ({in_p.position})")

            # Replace lists in one shot
            on_court[:] = new_court
            on_bench[:] = new_bench

            # Check to ensure length of on_court is precisely 5
            assert len(on_court) == 5, f"{team_name}: Invalid onCourt size {len(on_court)}"
            assert len(set(on_court)) == 5, f"{team_name}: Duplicate player detected on court!"

        # Run for both teams
        handle_subs(self.home_onCourt, self.home_onBench, self.home_team.starters, self.home_team.nickname)
        handle_subs(self.away_onCourt, self.away_onBench, self.away_team.starters, self.away_team.nickname)

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

    def _determine_matchups(self, offense_on_court, defense_on_court, defensive_scheme):
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
        self._update_plus_minus(offense_on_court, defense_on_court, made_count)
        offense_team.points_in_q += made_count
        print(f"Free throws awarded to {primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}). {primary_playmaker.name} makes {made_count} / {attempts} fts.")
        return 'fts'

    def _rebound_ball(self, offense_on_court, defense_on_court, offense, defense):
        """
        Simulates rebounding a ball and updates stats accordingly. Returns for poss_change purposes.
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
            poss_change = False
            print(f"Offensive rebound secured by {primary_o_reb.name}({primary_o_reb.position}).")
        else:
            primary_d_reb.game_stats['rebounds'] += 1
            primary_d_reb.game_stats['defensive_rebounds'] += 1
            self.game_stat_block[self.curr_quarter][defense]['rebounds'] += 1
            self.game_stat_block[self.curr_quarter][defense]['defensive_rebounds'] += 1
            poss_change = True
            print(f"Defensive rebound secured by {primary_d_reb.name} ({primary_d_reb.position}).")
        return poss_change

    def _make_a_three(self, primary_playmaker, offense, offense_team, offense_on_court, defense_on_court):
        """
        Record stats for a made 3. Return True for possession change purposes.
        """
        primary_playmaker.game_stats['3fg_taken'] += 1
        primary_playmaker.game_stats['3fg_made'] += 1
        primary_playmaker.game_stats['points'] += 3
        self.game_stat_block[self.curr_quarter][offense]['3fg_taken'] += 1
        self.game_stat_block[self.curr_quarter][offense]['3fg_made'] += 1
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
        offense_team.points_in_q += 2
        self._update_plus_minus(offense_on_court, defense_on_court, 2)
        print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) made a dunk!")
        return True

    def _record_a_steal(self, primary_defender, primary_playmaker, defense, offense):
        """
        Record stats for a successful steal. Returns True for poss_change purposes.
        """
        primary_defender.game_stats['steals'] += 1
        primary_playmaker.game_stats['turnovers'] += 1
        self.game_stat_block[self.curr_quarter][defense]['steals'] += 1
        self.game_stat_block[self.curr_quarter][offense]['turnovers'] += 1
        print(f"Ball stolen from {primary_playmaker.name} by {primary_defender.name}({primary_defender.position}).")
        return True

    def _determine_play_outcome(self, primary_playmaker, primary_defender, play_type,
                                offense_team, defense_team, offense_on_court, defense_on_court,
                                offense_on_bench, defense_on_bench):
        """
        Determines the outcome(s) of a play and updates stats and trackers accordingly.
        """
        # POSSIBLE OUTCOMES
        # (Make or miss) (self-created or pass-created) (open or contested) shot (layup, dunk, 2, or 3)
        # Defensive foul (ft's or OB --> Bonus @ foul #5)
        # Blocked shot (offensive rebound, defensive rebound, or knocked OB)
        # Knocked out of bounds (repeat offense)
        # Offensive rebound off miss (put back potential or kick out and repeat offense)
        # Stolen ball (possession change)
        # Offensive foul (OB --> possession change)
        # Defensive rebound off miss (possession change)

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

        if play_type in ('create_3', 'create_mid', 'iso_drive', 'post_up'):
            print(play_type)
        # OFFENSIVE RATINGS AT PLAY:
        # PRIMARY --> Playmaking (ability to get open) -> open_3/mid or contest_3/mid,
        # ALL --> Miss -> Offensive Rebound
        # DEFENSIVE RATINGS AT PLAY:
        # PRIMARY --> Stickiness (ability to prevent getting open), Steal (poke the ball out), Block (if shot gets off)
        # ALL --> Miss -> Defensive Rebound
        # POSSIBILITY TREE --> 1) Determine Steal or reach-in foul, 2) Determine Open or Contested (create_3 and create_mid only),
        # 3) Determine Block, Shooting Foul, Make, or Miss (contested only for block/foul),
        # 4) Off miss, determine Offensive Rebound, Defensive Rebound, Off-ball foul, or Swat OB,
        # 5) Update stats, points, possession, stamina, substitutes where necessary
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
                            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed an open 3 point basket.")
                        else:
                            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed an open mid-range basket.")
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
                            poss_change = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)
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
                        primary_defender.game_stats['blocks'] += 1
                        self.game_stat_block[self.curr_quarter][defense]['blocks'] += 1
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
                                print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a contested 3 point basket.")
                            else:
                                print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a contested mid-range basket.")
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
                                poss_change = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)
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
                    primary_playmaker.game_stats['fouls'] += 1
                    offense_team.fouls_in_q += 1
                    stoppage = True
                    poss_change = True
                    stoppage_type = 'OB'
                    print(f"Offensive foul committed by {primary_playmaker.name}({offense_team.nickname}) on {primary_defender.name}({defense_team.nickname}).")
                # Low result = Shooting Foul, High result = Block
                block_or_shooting_foul_threshold = {'lo': generate_random_int(8, 12), 'hi': generate_random_int(86, 90)}
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
                    primary_defender.game_stats['blocks'] += 1
                    self.game_stat_block[self.curr_quarter][defense]['blocks'] += 1
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
                else:
                    if play_type == 'iso_drive':
                        initial_shot_threshold = generate_random_int(42, 51)
                        shot_threshold = self._binary_adjust_threshold(primary_playmaker.finishing.curr_rating, initial_shot_threshold, 12, 'offense')
                    else:
                        initial_shot_threshold = generate_random_int(44, 53)
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
                            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a layup.")
                        else:
                            print(f"{primary_playmaker.name}({primary_playmaker.position}, {offense_team.nickname}) missed a post-up attempt.")
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
                                stoppage_type = self._shoot_fts(fouled_player, 2, fouled_team_stats, fouled_team,
                                                                offense_on_court, defense_on_court)
                            else:
                                stoppage_type = 'OB'
                        # Determine Rebound
                        else:
                            poss_change = self._rebound_ball(offense_on_court, defense_on_court, offense, defense)

        elif play_type == 'pick_n_roll':
            print('pick_n_roll')
        elif play_type == 'drive_n_pass':
            print('drive_n_pass')
        else:
            print('find_cutter')

        # Happens after any result
        self._decrease_stamina_onCourt(primary_playmaker, primary_defender, secondary_playmaker, secondary_defender,
                                       offense_on_court, defense_on_court)
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

        # Default all defensive schemes to man, will be more involved later on
        defensive_scheme = 'MAN'

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
        matchup_dict = self._determine_matchups(offense_on_court, defense_on_court, defensive_scheme)
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
        print({'TEAM': self.home_team.nickname})
        for player in self.home_onCourt:
            print({
                'name': player.name,
                'position': player.position,
                'overall': player.overall,
                'o_ovr': player.o_ovr,
                'd_ovr': player.d_ovr
            })
        print({'TEAM': self.away_team.nickname})
        for player in self.away_onCourt:
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
        print('END Q1')
        # Log stats, reset trackers
        self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Simulate Q2
        self.curr_quarter = 2
        for _ in range(self.q2_plays):
            self._simulate_play()
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
        print('END Q3')
        # Log stats, reset trackers
        self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Simulate Q4
        self.curr_quarter = 4
        for _ in range(self.q4_plays):
            self._simulate_play()
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
            self.OT_plays_total += self.OT_plays_current
            for _ in range (self.OT_plays_current):
                self._simulate_play()
            print(f"END OT{ot_count}")
            self._log_fouls_and_points_by_q(self.home_team, self.away_team, self.game_stat_block, self.curr_quarter)
            print(f"{self.home_team.nickname}: {self.home_team.points_total}")
            print(f"{self.away_team.nickname}: {self.away_team.points_total}")
            self.OT_plays_current = 0
            ot_count += 1
        print('END GAME')
        print('FINAL SCORE')
        print(f"{self.home_team.nickname}: {self.home_team.points_total}")
        print(f"{self.away_team.nickname}: {self.away_team.points_total}")
        # Log player stats and game stats

        # Reset starters, stamina, and trackers for next game
        self._reset_stamina()
        self._set_onCourt()
        self.home_team.points_total = 0
        self.away_team.points_total = 0
        self.home_team.timeouts = 5
        self.away_team.timeouts = 5