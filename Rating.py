class Rating:
    def __init__(self, stat_name, curr_rating, floor, ceiling):
        self.stat_name = stat_name
        self.curr_rating = curr_rating
        self.floor = floor
        self.ceiling = ceiling

    def set_curr_rating(self, new_rating):
        self.curr_rating = new_rating

    def set_floor(self, new_floor):
        self.floor = new_floor

    def set_ceiling(self, new_ceiling):
        self.ceiling = new_ceiling