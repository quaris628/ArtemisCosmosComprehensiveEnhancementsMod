from sbs_utils.procedural.comms import comms_broadcast
from sbs_utils.procedural.execution import get_shared_variable, set_shared_variable
from sbs_utils.procedural.roles import has_role, has_roles, role, all_roles

from data.missions.common.pirate_features_definitions import can_loot, is_looted

#from data.missions.legendarymissions.comms.surrendered_navigation import is_close_enough_to_spawnpoint_for_deletion, is_a_player_too_close_for_deletion
from sbs_utils.mast.mast_globals import MastGlobals
is_close_enough_to_spawnpoint_for_deletion = MastGlobals.globals["is_close_enough_to_spawnpoint_for_deletion"]
is_a_player_too_close_for_deletion = MastGlobals.globals["is_a_player_too_close_for_deletion"]

# ----- Misc -----

def is_enemy(space_object_id):
    return has_role(space_object_id, "raider") or has_roles(space_object_id, "enemy,station")

def get_all_enemy_ids(except_enemy_id=None):
    all_enemy_ids = role("raider") | all_roles("enemy,station")
    all_enemy_ids.discard(except_enemy_id)
    return all_enemy_ids

def wait_for_looting():
    """
    Checks whether the simulation should wait to end in order
    to allow player ships to loot surrendered ships.
    
    More precisely, returns True when all of the following are true:
    1) There is at least one non-destroyed player ship that can loot
    2) There is at least one unlooted surrendered ship that is NOT in
       a state where it would be deleted if it were at its spawnpoint.
    
    Returns:
        boolean: True if we need to wait to end the game;
            False if the game can end immediately.
    """
    is_looter_player_in_play = False
    for player_ship_id in role("__player__"):
        if can_loot(player_ship_id):
            is_looter_player_in_play = True
            break
    if not is_looter_player_in_play:
        return False
    
    unlooted_ship_in_play = False
    for ship_id in role("surrendered"):
        if is_looted(ship_id):
            continue
        if is_close_enough_to_spawnpoint_for_deletion(ship_id) and not is_a_player_too_close_for_deletion(ship_id):
            continue
        unlooted_ship_in_play = True
        break
    if not unlooted_ship_in_play:
        print(f"wait_for_looting not unlooted_ship_in_play")
        return False
    
    for player_ship_id in role("__player__"):
        comms_broadcast(player_ship_id, msg="Mission is won! Waiting 60s to allow looting.", color="lime")
    return True

# ----- Setter/getter wrappers -----

def reset_game_end_conditions():
    set_game_end_conditions(end_if_no_enemies=None, end_if_no_ally_stations=None)

# There's also a timer which can end the game. It's always respected if it's set.
# end_if_no_enemies default is True
# end_if_no_ally_stations default is True
# TODO also provide override for no player ships, e.g. for all-fighter custom mission script
# And/or maybe provide override for whether single-seat craft should count as player ships
# for the purposes of whether the game ends
def set_game_end_conditions(end_if_no_enemies=None, end_if_no_ally_stations=None):
    set_shared_variable(_IS_END_IF_NO_ENEMIES_ENABLED_VAR_NAME, end_if_no_enemies)
    set_shared_variable(_IS_END_IF_NO_ALLY_STATIONS_ENABLED_VAR_NAME, end_if_no_ally_stations)
 
def is_end_if_no_enemies_enabled():
    is_enabled = get_shared_variable(_IS_END_IF_NO_ENEMIES_ENABLED_VAR_NAME)
    if is_enabled is None:
        return True
    return is_enabled

def is_end_if_no_ally_stations_enabled():
    is_enabled = get_shared_variable(_IS_END_IF_NO_ALLY_STATIONS_ENABLED_VAR_NAME)
    if is_enabled is None:
        return True
    return is_enabled

_IS_END_IF_NO_ENEMIES_ENABLED_VAR_NAME = "_is_end_if_no_enemies_enabled"
_IS_END_IF_NO_ALLY_STATIONS_ENABLED_VAR_NAME = "_is_end_if_no_ally_stations_enabled"
