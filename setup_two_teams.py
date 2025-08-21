from pools import *
from get_sorted_pools import *

# Loops a roster to determine if a team has a certain position, returns a boolean
def has_position(team, position):
    return any(player.position == position for player in team.roster)

# Finds best available player then removes them from prospect pool
def find_and_draft_best_player_by_pos(pool, positions):
    sorted_pool = get_sorted_players()
    for player in sorted_pool:
        if player.position in positions:
            for i, p in enumerate(pool):
                if p.name == player.name:
                    del pool[i]
                    break
            return player

def two_team_setup(team1, team2):
    # Assign coaches to teams
    # Get sorted pool by overall
    sorted_coach_pool = get_sorted_coaches()
    # Add highest rated coach to team2
    team2.coach = sorted_coach_pool[0]
    # Remove from available_coaches pool
    available_coach_index = available_coaches.index(team2.coach)
    del available_coaches[available_coach_index]
    # Repeat for team2
    sorted_coach_pool = get_sorted_coaches()
    team1.coach = sorted_coach_pool[0]
    available_coach_index = available_coaches.index(team1.coach)
    del available_coaches[available_coach_index]

    # Fill rosters
    # Tracker for which team is picking
    curr_pick = team1
    teams = [team1, team2]
    # Tracker for # of guards and forwards
    MAX_GUARDS = 5
    MAX_FORWARDS = 7
    for _ in range(24):
        team = curr_pick
        other = teams[0] if curr_pick is teams[1] else teams[1]

        # Count guards/forwards
        guards = sum(1 for p in team.roster if p.position in ['PG', 'SG'])
        forwards = sum(1 for p in team.roster if p.position in ['SF', 'PF', 'C'])

        # Figure out what positions are missing
        missing_positions = [pos for pos in ['PG', 'SG', 'SF', 'PF', 'C']
                             if not has_position(team, pos)]

        # Draft
        # Prioritize filling missing positions
        if missing_positions:
            player = find_and_draft_best_player_by_pos(prospect_pool, missing_positions)
        # Team needs guards
        elif guards < MAX_GUARDS and (forwards == MAX_FORWARDS or forwards - guards >= 4):
            player = find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG'])
        # Team needs forwards
        elif forwards < MAX_FORWARDS and (guards == MAX_GUARDS or guards - forwards >= 2):
            player = find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF', 'C'])
        # Draft best available player
        else:
            player = find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG', 'SF', 'PF', 'C'])

        # Add player
        team.roster.append(player)

        # Switch pick
        curr_pick = other
