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
        self.q1_plays = generate_random_int(40, 60)
        self.q2_plays = generate_random_int(40, 60)
        self.q3_plays = generate_random_int(40, 60)
        self.q4_plays = generate_random_int(40, 60)
        self.total_plays = self.q1_plays + self.q2_plays + self.q3_plays + self.q4_plays
        # Initialize empty game state block
        self.game_stats = full_game_stat_block
        # Initialize empty possession tracker
        self.curr_poss = ''

    # Private Methods
    def _set_onCourt(self):
        for starter in self.home_team.starters.values():
            self.home_onCourt.append(starter)
        for starter in self.away_team.starters.values():
            self.away_onCourt.append(starter)

    def _simulate_play(self):
        print('a play!')

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

    # Public Methods
    def simulate_game(self):
        # Get game started
        self._determine_tipoff()
        self._set_onCourt()
        # Simulate Q1
        for _ in range(self.q1_plays):
            self._simulate_play()
        # Simulate Q2
        for _ in range(self.q2_plays):
            self._simulate_play()
        # Simulate Q3 (re-insert starters)
        self._set_onCourt()
        for _ in range(self.q3_plays):
            self._simulate_play()
        # Simulate Q4
        for _ in range(self.q4_plays):
            self._simulate_play()
