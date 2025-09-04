def make_individual_stat_block_overalls():
    return {
    'games_played': 0,
    'minutes': {
        'total': 0,
        'average': 0,
    },
    'points': {
        'total': 0,
        'average': 0,
    },
    '2fg_taken': 0,
    '2fg_made': 0,
    '2fg%': 0,
    '3fg_taken': 0,
    '3fg_made': 0,
    '3fg%': 0,
    'ft_taken': 0,
    'ft_made': 0,
    'ft%': 0,
    'rebounds': {
        'total': 0,
        'average': 0,
    },
    'offensive_rebounds': {
        'total': 0,
        'average': 0,
    },
    'defensive_rebounds': {
        'total': 0,
        'average': 0,
    },
    'assists': {
        'total': 0,
        'average': 0,
    },
    'steals': {
        'total': 0,
        'average': 0,
    },
    'blocks': {
        'total': 0,
        'average': 0,
    },
    'turnovers': {
        'total': 0,
        'average': 0,
    },
    'fouls': {
        'total': 0,
        'average': 0,
    },
    '+/-': 0
}

def make_individual_stat_block_game():
    return {
    'minutes': 0,
    'points': 0,
    'plays': 0,
    '2fg_taken': 0,
    '2fg_made': 0,
    '3fg_taken': 0,
    '3fg_made': 0,
    'ft_taken': 0,
    'ft_made': 0,
    'rebounds': 0,
    'offensive_rebounds': 0,
    'defensive_rebounds': 0,
    'assists': 0,
    'steals': 0,
    'blocks': 0,
    'turnovers': 0,
    'fouls': 0,
    '+/-': 0
}

def make_game_stat_block():
    return {
    'home_team': {
        'points': 0,
        '2fg_taken': 0,
        '2fg_made': 0,
        '3fg_taken': 0,
        '3fg_made': 0,
        'ft_taken': 0,
        'ft_made': 0,
        'rebounds': 0,
        'offensive_rebounds': 0,
        'defensive_rebounds': 0,
        'assists': 0,
        'steals': 0,
        'blocks': 0,
        'turnovers': 0,
        'fouls': 0
    },
    'away_team': {
        'points': 0,
        '2fg_taken': 0,
        '2fg_made': 0,
        '3fg_taken': 0,
        '3fg_made': 0,
        'ft_taken': 0,
        'ft_made': 0,
        'rebounds': 0,
        'offensive_rebounds': 0,
        'defensive_rebounds': 0,
        'assists': 0,
        'steals': 0,
        'blocks': 0,
        'turnovers': 0,
        'fouls': 0
    }
}

full_game_stat_block = {
    1: make_game_stat_block(),
    2: make_game_stat_block(),
    3: make_game_stat_block(),
    4: make_game_stat_block(),
    'OT': make_game_stat_block(),
    'Full Game': make_game_stat_block()
}

def make_team_totals():
    return {
    'games_played': 0,
    'points': 0,
    '2fg_taken': 0,
    '2fg_made': 0,
    '3fg_taken': 0,
    '3fg_made': 0,
    'ft_taken': 0,
    'ft_made': 0,
    'rebounds': 0,
    'offensive_rebounds': 0,
    'defensive_rebounds': 0,
    'assists': 0,
    'steals': 0,
    'blocks': 0,
    'turnovers': 0,
    'fouls': 0
}