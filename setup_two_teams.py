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
    curr_pick = 'team1'
    # Tracker for # of guards and forwards
    team1_forwards = 0 # choose 7 fowards
    team1_guards = 0 # choose 5 guards
    team2_forwards = 0
    team2_guards = 0
    for _ in range(24):
        # Determine whose pick
        if curr_pick == 'team1':
            # Check to see if team needs to choose guards
            if team1_forwards == 7 or team1_forwards - team1_guards >= 4:
                # Check to see if team needs a PG or SG specifically at end of draft
                if team1_guards == 4:
                    if has_position(team1, 'PG') == False:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PG']))
                    elif has_position(team1, 'SG') == False:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SG']))
                    else:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG']))
                    team1_guards += 1
                else:
                    team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG']))
                    team1_guards += 1
            # Check to see if team needs to choose forwards
            elif team1_guards == 5 or team1_guards - team1_forwards >= 2:
                # Check to see if team needs a SF, PF, or C specifically at end of draft
                if team1_forwards >= 5:
                    if has_position(team1, 'SF') == False and has_position(team1, 'PF') == False:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF']))
                    elif has_position(team1, 'SF') == False and has_position(team1, 'C') == False:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'C']))
                    elif has_position(team1, 'PF') == False and has_position(team1, 'C') == False:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PF', 'C']))
                    elif has_position(team1, 'SF'):
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF']))
                    elif has_position(team1, 'PF'):
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PF']))
                    elif has_position(team1, 'C'):
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['C']))
                    else:
                        team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF', 'C']))
                    team1_forwards += 1
                else:
                    team1.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF', 'C']))
                    team1_forwards += 1
            # Otherwise, choose best player available
            else:
                player = find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG', 'SF', 'PF', 'C'])
                team1.roster.append(player)
                if player.position == 'PG' or player.position == 'SG':
                    team1_guards += 1
                else:
                    team1_forwards += 1
            curr_pick = 'team2'
        else:
            # Check to see if team needs to choose guards
            if team2_forwards == 7 or team2_forwards - team2_guards >= 4:
                # Check to see if team needs a PG or SG specifically at end of draft
                if team2_guards == 4:
                    if has_position(team2, 'PG') == False:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PG']))
                    elif has_position(team2, 'SG') == False:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SG']))
                    else:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG']))
                    team2_guards += 1
                else:
                    team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG']))
                    team2_guards += 1
            # Check to see if team needs to choose forwards
            elif team2_guards == 5 or team2_guards - team2_forwards >= 2:
                # Check to see if team needs a SF, PF, or C specifically at end of draft
                if team2_forwards >= 5:
                    if has_position(team2, 'SF') == False and has_position(team2, 'PF') == False:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF']))
                    elif has_position(team2, 'SF') == False and has_position(team2, 'C') == False:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'C']))
                    elif has_position(team2, 'PF') == False and has_position(team2, 'C') == False:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PF', 'C']))
                    elif has_position(team2, 'SF'):
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF']))
                    elif has_position(team2, 'PF'):
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['PF']))
                    elif has_position(team2, 'C'):
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['C']))
                    else:
                        team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF', 'C']))
                    team2_forwards += 1
                else:
                    team2.roster.append(find_and_draft_best_player_by_pos(prospect_pool, ['SF', 'PF', 'C']))
                    team2_forwards += 1
            # Otherwise, choose best player available
            else:
                player = find_and_draft_best_player_by_pos(prospect_pool, ['PG', 'SG', 'SF', 'PF', 'C'])
                team2.roster.append(player)
                if player.position == 'PG' or player.position == 'SG':
                    team2_guards += 1
                else:
                    team2_forwards += 1
            curr_pick = 'team1'




