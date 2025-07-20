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
        "basketball. A gifted strategist and a careful coach, her deep intentionality will serve your team well.",
    "Jacques Monet":
        "A successful painter, who maintains his artistic pursuits on the side, Jaques is a calm pillar amid "
        "turbulent situations. Prone to spacing out and disappearing into other pursuits, he may not be the most "
        "reliable of the bunch. But his eye for defensive integrity is nearly unmatched.",
    "Nikki Dimes":
        "A young firebrand, Nikki is the epitome of youthful energy. Channelling her natural verve, she imbues an "
        "aggressive nature to her strategy, often resulting in torrents of scoring. But if she finds herself in a "
        "situation where she feels she cannot thrive, she will be the first one on the bus out of town.",
    "Emeka Umar":
        "Once a highly successful businessman, Emeka made his money then began to pursue his passion, the game of "
        "basketball. He is a consummate professional, meticulous and precise in all he does. While he possesses no "
        "obvious strength above the rest of the field, he offers a high floor to every aspect of the coaching game.",
    "Jackie Croc":
        "Following a serious injury sustained while wrangling a threatening crocodile, she opted for a more stable "
        "environment for her next expedition. She implements the lessons she learned from her time among Austalia's "
        "many frightening critters into a tenacious defensive mindset in her teams.",
    "Santiago Gonzales":
        "A social media influencer and successful player in his own right, Santiago leveraged his following "
        "and fans to grow the game of basketball and to grow his own brand. Energetic, startlingly handsome, "
        "and gregarious, Santiago connects with players in ways that many coaches could only dream to. His charm "
        "and wit also give him a remarkable confidence that leads him to not necessarily stay in one place for long.",
    "Will Dill":
        "A true pickle enthusiast, Bill was world-renowned for his pickle palette, able to distinguish different "
        "varieties, vintages, and picklers like a true sommelier. While on his eleventh pickle tour, he stumbled into "
        "a basketball game in Europe and was immediately smitten. Turning his very specific attention span to "
        "basketball, he cooked up some incredible strategic blueprints and quickly rose through the ranks to being a "
        "top candidate.",
    "Philip Mycup":
        "The oldest coaching candidate, Philip may not be in this for the long haul of a dynasty, but there's not soul "
        "who has anything bad to say about Philip. Not only does he have a sharp mind, he is a kind and gentle fellow, "
        "capable of endearing players and fans alike.",
    "Elle Belle":
        "Tired of the exploitative dynamics of the modeling industry, the beautiful Elle Belle made an early pivot "
        "in life to the game of basketball. Her youth can show at times in regards to her strategic eye, but she is "
        "gifted interacting with people and demonstrates great coaching potential.",
    "Candace Oren":
        "Once a successful roper in Oklahoma, Candace decided to apply her skills to a different, less physically taxing, "
        "endeavor. Her ability to hang with riled up cattle has translated to a tenacity on offense which other "
        "teams find remarkably difficult to play against. From a personality perspective, Candace is a bit of a lone "
        "wolf and may alienate players from time to time with her unusual social tendencies.",
    "Hirsh Wolfe":
        "Catching basketball games here and there around his hometown of Portland, OR, Hirsh left his job as a "
        "specialty bartender to take his talents to the sidelines. His many hours spent chatting with customers "
        "has given him an undeniable charisma. His youth means there is still much to learn and develop to his coaching "
        "game, but given enough time, it's hard to vote against him.",
    "Li Xiao":
        "A former business mogul, Li quickly proved herself to be a gifted basketball mind. A jack-of-all-trades, "
        "there are no obvious weaknesses to her coaching game. She is a bit of a recluse and very difficult to read, "
        "but, rest assured, she will never miss an appointment, game, or practice.",
    "Mira Ntuli":
        "One of the busier people in the coaching pool, Mira is attempting to straddle two worlds: music and sport. "
        "She leads a successful jazz group with her booming tenor saxophone, but has made the difficult decision to scale "
        "back her music career and lead a team as well. Her offenses play with the improvisational vivacity of her "
        "band. Her defenses... a bit more of a work in progress.",
    "Lumber Jack":
        "His defensive prowess is as imposing as his beard and axe. Not exactly known for an intimidating intellect, "
        "he wins via pure, in-your-face, aggressive defense. That said, time spent wandering in the woods while felling "
        "trees may provide the solitude he needs to develop further.",
    "John Smith":
        "The youngest member of the coaching pool, John is as young as the youngest players to populate a team. "
        "While this will understandably scare some off, John was pinned as a protege by many leading basketball minds "
        "from the ripe age of 17. His sense of strategy soars over his contemporaries. And while other aspects of "
        "his coaching game may be lacking, many agree he is on a path for stardom.",
    "Bob Boston":
        "A Boston-ite through and through, down to his last name, Bob sunk his teeth as voraciously into basketball "
        "as soon as it started to burgeon on the global scene. While he's a little rough around the edges and a bit "
        "old school in regards to strategy, few folks will get the level of play on both ends of the floor from their "
        "guys that Bob will.",
    "Terri Brooks":
        "One of the first female figures to truly make a mark on the game of basketball, Terri is a daunting figure in "
        "all the best possible ways. She is confident, a ferocious competitor, and a careful student of the game. Her "
        "teams will impose their will on offense and defense without an ounce of fear, whether favorite or underdog.",
    "Birdy Constantinople":
        "There's no one in basketball quite like Birdy. Hailing from Chile, she spent most of her twenties as an avid "
        "bird watcher, an understatement really for the meticulous work she was doing on exotic bird species. Now she "
        "has set her eyes to a new frontier. Considering herself an expert in the realm of shooting mechanics, she "
        "has had more luck developing shooters and offensive players in general than just about anyone in the sport. "
        "Tread cautiously though, she makes some rather... unexpected moves and decisions at times.",
    "Al Filer":
        "Al Filer is an all around good guy. A caring father for his two young daughters and a loving husband, "
        "Al is about as inoffensive as they come. Carrying in tow a ferocious work ethic, Al is a trustworthy "
        "strategic mind who can work with anyone. On top of that, he is as loyal as they come.",
    "Buck Snow":
        "To pursue the basketball dream, Buck left his high ranking position at the oil company. He carries much "
        "of his no-nonsense attitude into his coaching. He runs hard practices and asks the utmost of his players. "
        "Because of this approach, Buck's defenses are a known problem. Buck wants to win and win now, if the right "
        "team is not built around him, you can anticipate he'll be ready for that next venture.",
    "Corbyn Keller":
        "For a gentleman in his 30s, Keller has already had a remarkable amount of success on the court. He led his "
        "amateur squad to not one, not two, but three Middle USA Conference championships. He brings an immediate "
        "floor to your basketball team, and you don't have to worry about any nonsense with Corbyn around.",
    "Mabel Willows":
        "Mabel Willows is just a downright kind soul. Over the years in her Canadian community, she has been "
        "renowned as a philanthropist, bent on providing the care she can for the most vulnerable. She has a "
        "crystal clean track record in regards to the players she has coached absolutely adoring her. While her "
        "other pursuits have left her with some gaps in her knowledge regarding the game, hiring her may be the "
        "impetus she needs to become both great human being and great basketball coach.",
    "Dmitri Ivanov":
        "Hailing from icy Moscow, Dmitri spent most of his childhood as a burgeoning chessmaster. But after a "
        "brutalizing defeat at the hand of his arch rival, Dmitri pivoted to applying his chess acumen on the "
        "basketball court. Widely renowned as a gifted strategist who knows how to deploy and develop players "
        "effectively, his potential is not the fear in hiring him. Rather his frigid disposition leaves some players "
        "out in the deep cold, and his anger is known to be quite intimidating.",
    "Thanalah Patel":
        "Thanalah comes from an influential family in India. She spent years playing the games of modern palace intrigue "
        "before deciding that she was tired of the money games. Instead, she dove deeply into basketball, and felt the love "
        "and fire she had been missing much of her life. She still carries herself with immense poise from those days and "
        "has added on a great mind for strategy. Her amateur teams have often won while severe underdogs due to her "
        "ability to squeeze every last bit out of a game plan.",
    "Brick Wright":
        "Most people who meet Brick think, 'Wow, that is a huge man.' And he is a huge man. As daunting as his presence "
        "can be physically, his defenses may be even more daunting, absolutely crushing anything in their path. Fouls "
        "may be his kyptonite...",
    "Ishmael Chibueze":
        "Ishmael is known as a man of impeccable poise. A player himself for years, he was an unshakable shooter, renowned "
        "for his clutch 3-point making ability. He carries that poise with him in his coaching, unflappable under pressure "
        "and capable of imparting wisdom to the gifted shooters on his team, he has a bright future in the league."
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
    Coach(
        "Jacques Monet", "Canada", coach_descriptions["Jacques Monet"], 45,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(40, 90)),
        CoachRating('coach_intangibles', generate_random_int(10, 70)),
        CoachRating('coach_strategy', generate_random_int(5, 60)),
        "Low", "Average", "Average"
    ),
    Coach(
        "Nikki Dimes", "South America", coach_descriptions["Nikki Dimes"], 25,
        CoachRating('coach_offense', generate_random_int(30, 70)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(5, 60)),
        CoachRating('coach_strategy', generate_random_int(15, 75)),
        "High", "Average", "Average"
    ),
    Coach(
        "Emeka Umar", "Africa", coach_descriptions["Emeka Umar"], 44,
        CoachRating('coach_offense', generate_random_int(20, 70)),
        CoachRating('coach_defense', generate_random_int(20, 70)),
        CoachRating('coach_intangibles', generate_random_int(20, 70)),
        CoachRating('coach_strategy', generate_random_int(20, 60)),
        "Somewhat Low", "Average", "Somewhat High"
    ),
    Coach(
        "Jackie Croc", "Australia", coach_descriptions["Jackie Croc"], 49,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(40, 90)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Somewhat Low", "Average", "High"
    ),
    Coach(
        "Santiago Gonzales", "South America", coach_descriptions["Santiago Gonzales"], 33,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(40, 90)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Somewhat High", "Average", "Average"
    ),
    Coach(
        "Will Dill", "South USA", coach_descriptions["Will Dill"], 50,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(40, 90)),
        "Average", "Average", "Somewhat High"
    ),
    Coach(
        "Philip Mycup", "Midwest USA", coach_descriptions["Philip Mycup"], 61,
        CoachRating('coach_offense', generate_random_int(20, 70)),
        CoachRating('coach_defense', generate_random_int(20, 70)),
        CoachRating('coach_intangibles', generate_random_int(40, 90)),
        CoachRating('coach_strategy', generate_random_int(20, 70)),
        "Low", "Average", "High"
    ),
    Coach(
        "Elle Belle", "Europe", coach_descriptions["Elle Belle"], 32,
        CoachRating('coach_offense', generate_random_int(10, 70)),
        CoachRating('coach_defense', generate_random_int(10, 70)),
        CoachRating('coach_intangibles', generate_random_int(40, 90)),
        CoachRating('coach_strategy', generate_random_int(5, 60)),
        "Somewhat High", "Average", "Average"
    ),
    Coach(
        "Candace Oren", "South USA", coach_descriptions["Candace Oren"], 41,
        CoachRating('coach_offense', generate_random_int(40, 90)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(5, 50)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Average", "Average", "Somewhat High"
    ),
    Coach(
        "Hirsh Wolfe", "West Coast USA", coach_descriptions["Hirsh Wolfe"], 30,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(40, 90)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Somewhat High", "Average", "Somewhat Low"
    ),
    Coach(
        "Li Xiao", "Asia", coach_descriptions["Li Xiao"], 44,
        CoachRating('coach_offense', generate_random_int(20, 70)),
        CoachRating('coach_defense', generate_random_int(20, 70)),
        CoachRating('coach_intangibles', generate_random_int(20, 70)),
        CoachRating('coach_strategy', generate_random_int(20, 70)),
        "Average", "Average", "Average"
    ),
    Coach(
        "Mira Ntuli", "Africa", coach_descriptions["Mira Ntuli"], 37,
        CoachRating('coach_offense', generate_random_int(30, 80)),
        CoachRating('coach_defense', generate_random_int(5, 50)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(20, 70)),
        "Average", "Average", "High"
    ),
    Coach(
        "Lumber Jack", "Canada", coach_descriptions["Lumber Jack"], 41,
        CoachRating('coach_offense', generate_random_int(5, 60)),
        CoachRating('coach_defense', generate_random_int(40, 90)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(5, 50)),
        "Low", "Average", "Somewhat High"
    ),
    Coach(
        "John Smith", "Australia", coach_descriptions["John Smith"], 21,
        CoachRating('coach_offense', generate_random_int(5, 50)),
        CoachRating('coach_defense', generate_random_int(5, 50)),
        CoachRating('coach_intangibles', generate_random_int(5, 50)),
        CoachRating('coach_strategy', generate_random_int(40, 95)),
        "Somewhat High", "Average", "Somewhat Low"
    ),
    Coach(
        "Bob Boston", "East Coast USA", coach_descriptions["Bob Boston"], 48,
        CoachRating('coach_offense', generate_random_int(25, 80)),
        CoachRating('coach_defense', generate_random_int(25, 80)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Average", "Average", "Somewhat Low"
    ),
    Coach(
        "Terri Brooks", "West Coast USA", coach_descriptions["Terri Brooks"], 55,
        CoachRating('coach_offense', generate_random_int(25, 80)),
        CoachRating('coach_defense', generate_random_int(25, 80)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Average", "Average", "Somewhat High"
    ),
    Coach(
        "Birdy Constantinople", "South America", coach_descriptions["Birdy Constantinople"], 29,
        CoachRating('coach_offense', generate_random_int(40, 90)),
        CoachRating('coach_defense', generate_random_int(5, 50)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "High", "Average", "Average"
    ),
    Coach(
        "Al Filer", "East Coast USA", coach_descriptions["Al Filer"], 41,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(25, 80)),
        CoachRating('coach_strategy', generate_random_int(25, 80)),
        "Low", "Average", "High"
    ),
    Coach(
        "Buck Snow", "South USA", coach_descriptions["Buck Snow"], 50,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(40, 90)),
        CoachRating('coach_intangibles', generate_random_int(5, 50)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Average", "Average", "Average"
    ),
    Coach(
        "Corbyn Keller", "Midwest USA", coach_descriptions["Corbyn Keller"], 35,
        CoachRating('coach_offense', generate_random_int(20, 80)),
        CoachRating('coach_defense', generate_random_int(20, 80)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(20, 80)),
        "Low", "Average", "High"
    ),
    Coach(
        "Mabel Willows", "Canada", coach_descriptions["Mabel Willows"], 42,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(40, 90)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Somewhat Low", "Average", "High"
    ),
    Coach(
        "Dmitri Ivanov", "Europe", coach_descriptions["Dmitri Ivanov"], 33,
        CoachRating('coach_offense', generate_random_int(20, 70)),
        CoachRating('coach_defense', generate_random_int(20, 70)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(40, 90)),
        "Somewhat Low", "Average", "Somewhat Low"
    ),
    Coach(
        "Thanalah Patel", "Asia", coach_descriptions["Thanalah Patel"], 46,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(25, 80)),
        CoachRating('coach_strategy', generate_random_int(25, 80)),
        "Low", "Average", "High"
    ),
    Coach(
        "Brick Wright", "Australia", coach_descriptions["Brick Wright"], 46,
        CoachRating('coach_offense', generate_random_int(10, 60)),
        CoachRating('coach_defense', generate_random_int(40, 90)),
        CoachRating('coach_intangibles', generate_random_int(10, 60)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Average", "Average", "Average"
    ),
    Coach(
        "Ishmael Chibueze", "Africa", coach_descriptions["Ishmael Chibueze"], 37,
        CoachRating('coach_offense', generate_random_int(20, 70)),
        CoachRating('coach_defense', generate_random_int(10, 60)),
        CoachRating('coach_intangibles', generate_random_int(40, 90)),
        CoachRating('coach_strategy', generate_random_int(10, 60)),
        "Somewhat Low", "Average", "High"
    )
]