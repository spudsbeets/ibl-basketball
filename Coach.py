class Coach:
    def __init__(self, name, region, description, age,
                 coach_offense, coach_defense, coach_intangibles, coach_strategy,
                 mercuriality, contentment, character):
        # General Info
        self.name = name
        self.region = region
        self.description = description
        self.age = age
        self.salary = 0
        # Coach Ratings
        self.coach_offense = coach_offense
        self.coach_defense = coach_defense
        self.coach_intangibles = coach_intangibles
        self.coach_strategy = coach_strategy
        self.coach_overall = self._calculate_coach_overall()
        # Personal Ratings
        self.mercuriality = mercuriality
        self.contentment = contentment
        self.character = character
        # Stats/Records/Year Tracker
        self.wins = 0
        self.losses = 0
        self.accolades = {'2030': None}
        self.records_archive = {}
        self.curr_year = 2030

    # Private Methods
    def _calculate_coach_overall(self):
        return round((self.coach_offense.rating * .3) + (self.coach_defense.rating * .3) + \
                     (self.coach_intangibles.rating * .15) + (self.coach_strategy.rating * .25))

    # Public Methods
    def increment_wins(self):
        self.wins += 1

    def increment_losses(self):
        self.losses += 1

    def set_salary(self, new_num):
        self.salary = new_num

    def change_mercuriality(self, new_merc):
        self.mercuriality = new_merc

    def change_contentment(self, new_content):
        self.contentment = new_content

    def change_character(self, new_character):
        self.character = new_character

    def go_to_next_season(self):
        self.records_archive[str(self.curr_year)] = {'wins': self.wins, 'losses': self.losses}
        self.wins = 0
        self.losses = 0
        self.age += 1
        self.curr_year += 1