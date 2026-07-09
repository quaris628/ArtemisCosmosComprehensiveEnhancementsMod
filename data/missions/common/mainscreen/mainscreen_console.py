from sbs_utils.procedural.inventory import get_inventory_value, set_inventory_value
from sbs_utils.procedural.settings import settings_get_defaults

# ----- setter/getter wrappers -----

# View could be; 3d_view, lrs, tactical, data
# The facing and mode are not applicable unless the view is 3d_view.
# Facing could be: right, left, front, back
# Mode could be: first_person, chase, tracking

def initialize_mainscreen_view_facing_and_mode(player_ship_id):
    SETTINGS = settings_get_defaults()
    set_mainscreen_view(player_ship_id, SETTINGS.get("DEFAULT_MAINSCREEN_VIEW", "3d_view"))
    set_mainscreen_facing(player_ship_id, SETTINGS.get("DEFAULT_MAINSCREEN_FACING", "front"))
    set_mainscreen_mode(player_ship_id, SETTINGS.get("DEFAULT_MAINSCREEN_MODE", "chase"))

def get_mainscreen_view(player_ship_id):
    return get_inventory_value(player_ship_id, _INVENTORY_KEY_MAINSCREEN_VIEW)
def get_mainscreen_facing(player_ship_id):
    return get_inventory_value(player_ship_id, _INVENTORY_KEY_MAINSCREEN_FACING)
def get_mainscreen_mode(player_ship_id):
    return get_inventory_value(player_ship_id, _INVENTORY_KEY_MAINSCREEN_MODE)

def set_mainscreen_view(player_ship_id, view):
    set_inventory_value(player_ship_id, _INVENTORY_KEY_MAINSCREEN_VIEW, view)
def set_mainscreen_facing(player_ship_id, facing):
    set_inventory_value(player_ship_id, _INVENTORY_KEY_MAINSCREEN_FACING, facing)
def set_mainscreen_mode(player_ship_id, mode):
    set_inventory_value(player_ship_id, _INVENTORY_KEY_MAINSCREEN_MODE, mode)

_INVENTORY_KEY_MAINSCREEN_VIEW = "mainscreen_view"
_INVENTORY_KEY_MAINSCREEN_FACING = "mainscreen_facing"
_INVENTORY_KEY_MAINSCREEN_MODE = "mainscreen_mode"
