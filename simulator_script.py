from generate_prospect_pool import *
from generate_league import *
from pools import *
from generate_coaches import *
from setup_two_teams import *
from helper_functions import *
from Game import *

# Generate draft class.
generate_entry_draft_class()

# Optional print statement to see draft class and ratings. Comment out if desired.
# Sort pool
#sorted_player_pool = get_sorted_players()
#for player in sorted_player_pool:
#    print({
#        'name': player.name,
#        'height': player.height,
#        'weight': player.weight,
#        'position': player.position,
#        'region': player.region,
#        'age': player.age,
#        'mercuriality': player.mercuriality,
#        'contentment': player.contentment,
#        'character': player.character,
#        'o_reb': player.o_reb.curr_rating,
#        'finishing': player.finishing.curr_rating,
#        'open_mid': player.open_mid.curr_rating,
#        'open_3': player.open_3.curr_rating,
#        'contest_mid': player.contest_mid.curr_rating,
#        'contest_3': player.contest_3.curr_rating,
#        'playmaking': player.playmaking.curr_rating,
#        'ft_shoot': player.ft_shoot.curr_rating,
#        'd_reb': player.d_reb.curr_rating,
#        'block': player.block.curr_rating,
#        'steal': player.steal.curr_rating,
#        'stickiness': player.stickiness.curr_rating,
#        'awareness': player.awareness.curr_rating,
#        'endurance': player.endurance.curr_rating,
#        'confidence': player.confidence.curr_rating,
#        'speed': player.speed.curr_rating,
#        'strength': player.strength.curr_rating,
#        'o_ovr': player.o_ovr,
#        'd_ovr': player.d_ovr,
#        'intangibles_ovr': player.intangibles_ovr,
#        'overall': player.overall
#    })

# Generate two randomized teams.
generate_league()

# Optional print statement to see information concerning two teams. Comment out if desired.
#for team in teams:
#    print({
#        'name': team.nickname,
#        'city': team.city,
#        'region': team.region,
#        'colors': team.colors
#    })

# Generate coaching pool
generate_initial_coaching_pool()

# Optional print statement to see information concerning available coaches. Comment out if desired.
# Sort pool
#sorted_coach_pool = get_sorted_coaches()
#for coach in sorted_coach_pool:
#    print({
#        'name': coach.name,
#        'region': coach.region,
#        'age': coach.age,
#        'offense': coach.coach_offense.rating,
#        'defense': coach.coach_defense.rating,
#        'intangibles': coach.coach_intangibles.rating,
#        'strategy': coach.coach_strategy.rating,
#        'overall': coach.coach_overall,
#        'mercuriality': coach.mercuriality,
#        'contentment': coach.contentment,
#        'character': coach.character,
#        'description': coach.description
#    })

# Setup both teams with players and coaches
team1 = teams[0]
team2 = teams[1]
two_team_setup(team1, team2)

# Optional print statement to show relevant team info. Comment out if desired.
#for team in teams:
#    roster_info = [{'name': player.name, 'position': player.position, 'overall': player.overall} for player in team.roster]
#    print({
#        'team': team.nickname,
#        'roster': roster_info,
#        'coach': team.coach.name
#    })

# Move undrafted players into available_players and empty prospect_pool
available_players = prospect_pool
prospect_pool = []

# Alter player ratings by coach
for team in teams:
    team.alter_defensive_player_ratings_by_coach()
    team.alter_offensive_player_ratings_by_coach()
    team.alter_intangible_player_ratings_by_coach()

# Set starting lineups
team1.set_starters()
team2.set_starters()

# Simulate a game
sim_game = Game(team1, team2)
sim_game.simulate_game()