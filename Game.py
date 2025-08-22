from get_sorted_pools import *
from initial_templates import *
from helper_functions import *

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
        # Initialize empty possession tracker
        self.curr_poss = ''

    # Private Methods
    def _set_onCourt(self):
        # Reset the onCourt and onBench lists completely
        self.home_onCourt = list(self.home_team.starters.values())
        self.away_onCourt = list(self.away_team.starters.values())

        # Everyone else goes to the bench
        self.home_onBench = self.home_team.bench
        self.away_onBench = self.away_team.bench

    def _determine_tipoff(self):
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

    def _increase_stamina_all(self, stoppage_type):
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

    def _increase_stamina_bench(self):
        print('increasing resters stamina!')

    def _decrease_stamina_onCourt(self, primary_playmaker, primary_defender, secondary_playmaker, secondary_defender):
        print('dropping players stamina!')

    def _reset_stamina(self):
        for player in self.home_team.roster:
            player.stamina = 99
        for player in self.away_team.roster:
            player.stamina = 99

    def _update_play_counts(self):
        for player in self.home_onCourt:
            player.game_stats['plays'] += 1
        for player in self.away_onCourt:
            player.game_stats['plays'] += 1

    def _check_for_subs(self):
        for court_player in self.home_onCourt[:]:
            if court_player.stamina < 30 or court_player not in self.home_team.starters:
                cp_position = 'guard' if court_player.position in ('PG', 'SG') else 'forward'
                sorted_home_bench = get_sorted_players(self.home_onBench)
                for bench_player in sorted_home_bench:
                    if bench_player.stamina <= 75:
                        continue  # skip tired bench players

                    if (bench_player.position in ('PG', 'SG') and cp_position == 'guard') or \
                            (bench_player.position in ('SF', 'PF', 'C') and cp_position == 'forward'):
                        # perform the swap
                        self.home_onCourt.append(bench_player)
                        self.home_onBench.remove(bench_player)
                        self.home_onBench.append(court_player)
                        self.home_onCourt.remove(court_player)

                        print(f"{court_player.name} ({court_player.position}) subs out for {bench_player.name} ({bench_player.position})")
                        break  # done once a valid sub is made

        for court_player in self.away_onCourt[:]:
            if court_player.stamina < 30 or court_player not in self.away_team.starters:
                cp_position = 'guard' if court_player.position in ('PG', 'SG') else 'forward'
                sorted_home_bench = get_sorted_players(self.away_onBench)
                for bench_player in sorted_home_bench:
                    if bench_player.stamina <= 75:
                        continue  # skip tired bench players

                    if (bench_player.position in ('PG', 'SG') and cp_position == 'guard') or \
                            (bench_player.position in ('SF', 'PF', 'C') and cp_position == 'forward'):
                        # perform the swap
                        self.away_onCourt.append(bench_player)
                        self.away_onBench.remove(bench_player)
                        self.away_onBench.append(court_player)
                        self.away_onCourt.remove(court_player)

                        print(f"{court_player.name} ({court_player.position}) subs out for {bench_player.name} ({bench_player.position})")
                        break  # done once a valid sub is made

    def _check_for_timeout(self, offense_on_court, offense_team, defense_team):
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
                    (defense_team.points - offense_team.points) >= rules['min_deficit']:
                print(f"Timeout taken by {offense_team.nickname}")
                self._update_play_counts()
                offense_team.timeouts -= 1
                self._check_for_subs()
                self._increase_stamina_all('timeout')
                return True

        return False

    def _determine_primary_playmaker(self, offense_on_court):
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

    def _determine_matchups(self, offense_on_court, defense_on_court, defensive_scheme):

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

    def _determine_play_type(self, primary_playmaker, primary_defender):
        # Returns a string from these OPTIONS:
        # 'create_3'
        # 'create_mid'
        # 'iso_drive'
        # 'pick_n_roll' --> secondary POTENTIALLY needed
        # 'drive_n_pass' --> secondary needed
        # 'find_cutter' --> secondary needed

        # Determine decision tree based off offensive archetype
        if primary_playmaker.offensive_archetype == 'offensive_beast' or primary_playmaker.offensive_archetype == 'offensive_dud':
            probabilities = {
                'create_3': 15, # 15% chance
                'create_mid': 30, # 15% chance
                'iso_drive': 50, # 20% chance
                'pick_n_roll': 70, # 20% chance
                'drive_n_pass': 85, # 15% chance
                'find_cutter': 100 # 15% chance
            }
        elif primary_playmaker.offensive_archetype == 'creates_jumpers':
            probabilities = {
                'create_3': 25, # 25% chance
                'create_mid': 50, # 25% chance
                'iso_drive': 65, # 15% chance
                'pick_n_roll': 80, # 15% chance
                'drive_n_pass': 90, # 10% chance
                'find_cutter': 100 # 10% chance
            }
        elif primary_playmaker.offensive_archetype == 'create_drives':
            probabilities = {
                'create_3': 10, # 10% chance
                'create_mid': 20, # 10% chance
                'iso_drive': 50, # 30% chance
                'pick_n_roll': 65, # 15% chance
                'drive_n_pass': 85, # 20% chance
                'find_cutter': 100 # 15% chance
            }
        # 'creates_for_teammates'
        else:
            probabilities = {
                'create_3': 10, # 10% chance
                'create_mid': 20, # 10% chance
                'iso_drive': 30, # 10% chance
                'pick_n_roll': 55, # 25% chance
                'drive_n_pass': 75, # 20% chance
                'find_cutter': 100 # 25% chance
            }

        # Prioritize getting ball out of hands if defender is awesome
        if primary_defender.d_ovr > 75:
            probabilities['create_3'] -= 5
            probabilities['create_mid'] -= 10
            probabilities['iso_drive'] -= 15
            probabilities['pick_n_roll'] -= 10
            probabilities['drive_n_pass'] -= 5

        randomNum = generate_random_int(0, 100)

        if randomNum <= probabilities['create_3']:
            return 'create_3'
        elif randomNum <= probabilities['create_mid']:
            return 'create_mid'
        elif randomNum <= probabilities['iso_drive']:
            return 'iso_drive'
        elif randomNum <= probabilities['pick_n_roll']:
            return 'pick_n_roll'
        elif randomNum <= probabilities['drive_n_pass']:
            return 'drive_n_pass'
        else:
            return 'find_cutter'

    def _simulate_play(self):
        # POSSIBLE OUTCOMES
        # (Make or miss) (self-created or pass-created) (open or contested) shot (layup, dunk, 2, or 3)
        # Defensive foul (ft's or OB --> Bonus @ foul #5)
        # Blocked shot (offensive rebound, defensive rebound, or knocked OB)
        # Knocked out of bounds (repeat offense)
        # Offensive rebound off miss (put back potential or kick out and repeat offense)
        # Stolen ball (possession change)
        # Offensive foul (OB --> possession change)
        # Defensive rebound off miss (possession change)
        # Potential for fast break bucket (off turnover, low chance off d-reb)

        # Add injury possibility later...

        # FLOW
        # SETUP

        # Default all defensive schemes to man, will be more involved later on
        defensive_scheme = 'MAN'

        if self.curr_poss == 'home_team':
            offense_team = self.home_team
            defense_team = self.away_team
            offense_on_court = self.home_onCourt
            defense_on_court = self.away_onCourt
        else:
            offense_team = self.away_team
            defense_team = self.home_team
            offense_on_court = self.away_onCourt
            defense_on_court = self.home_onCourt

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
        print(play_type, primary_playmaker.name, primary_playmaker.position, primary_defender.name, primary_defender.position)
        # Determine outcome

        # Update game and individual stats (if necessary)

        # Update stamina for bench and onCourt
        # (big boost for all on timeout, slightly bigger drop for primary defender(s)/playmaker(s))

        # Update possession tracker (if necessary)

        # If play caused a stoppage (OB, foul, timeout), allow opportunity for substitutions

    # Public Methods
    def simulate_game(self):
        # Get game started
        self._determine_tipoff()
        self._set_onCourt()
        # Simulate Q1
        for _ in range(self.q1_plays):
            self._simulate_play()
        print('END Q1')
        # Simulate Q2
        self.home_team.fouls_in_q = 0
        self.away_team.fouls_in_q = 0
        self.curr_quarter = 2
        for _ in range(self.q2_plays):
            self._simulate_play()
        print('END Q2')
        # Simulate Q3 (re-insert starters, reset stamina)
        self._reset_stamina()
        self._set_onCourt()
        self.home_team.fouls_in_q = 0
        self.away_team.fouls_in_q = 0
        self.curr_quarter = 3
        for _ in range(self.q3_plays):
            self._simulate_play()
        print('END Q3')
        # Simulate Q4
        self.home_team.fouls_in_q = 0
        self.away_team.fouls_in_q = 0
        self.curr_quarter = 4
        for _ in range(self.q4_plays):
            self._simulate_play()
        print('END Q4')
        # If OT is needed COMMENT OUT ONCE POINT TRACKING IS ADDED IN
        # self.home_team.fouls_in_q = 0
        # self.away_team.fouls_in_q = 0
        # Two timeouts awarded to each team for OT periods
        # self.home_team.timeouts = 2
        # self.away_team.timeouts = 2
        # self.curr_quarter = 'OT'
        # while self.home_team.points == self.away_team.points:
        #    self.OT_plays_current += generate_random_int(13, 20)
        #    self.OT_plays_total += self.OT_plays_current
        #    for _ in range (self.OT_plays_current):
        #        self._simulate_play()
        #    self.home_team.fouls_in_q = 0
        #    self.away_team.fouls_in_q = 0
        #    self.OT_plays_current = 0
        # Log player stats and game stats

        # Reset starters and stamina for next game
        self._reset_stamina()
        self._set_onCourt()
        self.home_team.points = 0
        self.away_team.points = 0
        self.home_team.timeouts = 5
        self.away_team.timeouts = 5
        self.home_team.fouls_in_q = 0
        self.away_team.fouls_in_q = 0