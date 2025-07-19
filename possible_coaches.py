from Coach import *
from CoachRating import *
from helper_functions import generate_random_int

coach_descriptions = {
    "Steele Billows":
        "Once a sailor, this grizzled mountain of a man made the shift to guiding young folks with a firm " 
        "hand. He runs a tight ship, with little to no patience for shenanagains and is widely viewed as a " 
        "defensive specialist. He will get the most out of his guys, though he may alienate a few with his hard " 
        "driving, no nonsense personality. He's a bit set in his ways and not quick to implement state-of-the-"
        "art strategic innovation.",
    "Gail Flails":
        "An up and coming mind, Gail left a career in biochemistry after watching her local amateur team steadily "
        "run the same pick-and-roll motion 12 times in a row to little avail. She approached the coach the next day "
        "with some new ideas and they immediately hired her on as the assistant. It's been all up from there. "
        "Her strategic brainpower is her superpower, but she can struggle with interpersonal relationships, being "
        "a bit lost in her massive maze of a mind.",
    "Tig Skibs":
        "A man of incredible peace, favorite hobbies including quitely watching the rain, silently beholding the "
        "mountains, and not speaking while not saying anything. Beneath his quiet frame, he purports a remarkable "
        "acumen for helping his players make wise decisions with and without the ball, on and off the court. His quiet "
        "nature may unnerve some players, but they will certainly play with his sense of center.",
    "Paul Fiere":
        "Once a successful protege of a chef, Paul changed his mind and decided to carry the frenzy of the kitchen "
        "to the court. Unpredictability is both his strength and his achilles heel. His offenses operate quickly and "
        "often confound defenses, but he is also prone to following his hard-to-anticipate desires...",
    "Sally Swish":
        "One of the first ladies to hop on the basketball train with authority, she fell in love with basketball as "
        "many in heart of America were at the time. A tenacious student of the game, she sleeps, eats, and breathes "
        "basketball. A gifted strategist and a careful coach, her deep intentionality will serve your team well."
}

all_coaches = [
    Coach(
        "Steele Billows", "East Coast USA", coach_descriptions["Steele Billows"], 52,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(40, 90)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(5, 50)),
        "Low", "Average", "High"
    ),
    Coach(
        "Gail Flails", "West Coast USA", coach_descriptions["Gail Flails"], 36,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(5, 50)),
        CoachRating('coach_strategy', generate_random_int(40, 90)),
        "Somewhat Low", "Average", "Somewhat High"
    ),
    Coach(
        "Tig Skibs", "Asia", coach_descriptions["Tig Skibs"], 44,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(45, 90)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Low", "Average", "Somewhat High"
    ),
    Coach(
        "Paul Fiere", "Europe", coach_descriptions["Paul Fiere"], 29,
        CoachRating('coach_offense', generate_random_int(45, 90)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(5, 50)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "High", "Average", "Somewhat Low"
    ),
    Coach(
        "Sally Swish", "Midwest USA", coach_descriptions["Sally Swish"], 41,
        CoachRating('coach_offense', generate_random_int(5, 60)),
        CoachRating('coach_defense', generate_random_int(5, 60)),
        CoachRating('coach_intangibles', generate_random_int(30, 70)),
        CoachRating('coach_strategy', generate_random_int(30, 70)),
        "Average", "Average", "Somewhat High"
    ),
]