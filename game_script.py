from generate_prospect_pool import *
from generate_league import *
from pools import *
from generate_scouts import *
from generate_coaches import *

generate_entry_draft_class()

generate_league()

generate_initial_scouts()

generate_initial_coaching_pool()

sorted_pool = sorted(prospect_pool, key=lambda x: x.overall)

for player in sorted_pool:
    print({
        'name': player.name,
        'age': player.age,
        'position': player.position,
        'o_reb': player.o_reb.curr_rating,
        'finishing': player.finishing.curr_rating,
        'open_mid': player.open_mid.curr_rating,
        'open_3': player.open_3.curr_rating,
        'contest_mid': player.contest_mid.curr_rating,
        'contest_3': player.contest_3.curr_rating,
        'playmaking': player.playmaking.curr_rating,
        'ft_shoot': player.ft_shoot.curr_rating,
        'd_reb': player.d_reb.curr_rating,
        'block': player.block.curr_rating,
        'steal': player.steal.curr_rating,
        'stickiness': player.stickiness.curr_rating,
        'awareness': player.awareness.curr_rating,
        'endurance': player.endurance.curr_rating,
        'confidence': player.confidence.curr_rating,
        'speed': player.speed.curr_rating,
        'strength': player.strength.curr_rating,
        'overall': player.overall,
        'o_ovr': player.o_ovr,
        'd_ovr': player.d_ovr
    })

for team in teams:
    print({
        'name': team.nickname,
        'city': team.city,
        'region': team.region,
        'logo': team.logo,
        'colors': team.colors
    })

for scout in available_scouts:
    print({
        'name': scout.name,
        'region': scout.region,
        'specialty': scout.specialty,
        'level': scout.level
    })

for coach in available_coaches:
    print({
        'name': coach.name,
        'region': coach.region,
        'offense': coach.coach_offense.rating,
        'defense': coach.coach_defense.rating,
        'intangibles': coach.coach_intangibles.rating,
        'strategy': coach.coach_strategy.rating,
        'overall': coach.coach_overall
    })