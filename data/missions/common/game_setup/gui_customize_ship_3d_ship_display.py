
from sbs_utils.mast.label import label
from sbs_utils.procedural.execution import END, get_variable, set_variable
from sbs_utils.procedural.signal import signal_register
from sbs_utils.procedural.gui import gui_represent, gui_section, gui_ship

from model_player_ship_setup_data import signal_player_ship_setup_data_ship_type_changed

# ----- creation -----

def create_3d_ship_display(ship, x_left, y_top, x_right, y_bottom):
    
    gui_section(style=f"area:{x_left},{y_top},{x_right},{y_bottom};")
    threeD_ship_display = gui_ship(ship.ship_type_key)
    
    _set_3d_ship_display(threeD_ship_display)
    
    signal_register(signal_player_ship_setup_data_ship_type_changed(ship.number), _sync_3d_ship_display_on_ship_type_changed, is_temporary=True)

# ----- syncing -----

@label()
def _sync_3d_ship_display_on_ship_type_changed():
    ship = get_variable("SHIP")
    threeD_ship_display = _get_3d_ship_display()
    
    # Reading threeD_ship_display.value or .ship causes a crash
    # https://github.com/artemis-sbs/LegendaryMissions/issues/585
    if threeD_ship_display._ship[:8] != ship.ship_type_key: # pylint: disable=protected-access
        threeD_ship_display.value = ship.ship_type_key
        gui_represent(threeD_ship_display)
    
    yield END()

# ----- setter/getter wrappers -----

def _get_3d_ship_display():
    return get_variable(_3D_SHIP_DISPLAY_VAR_NAME)

def _set_3d_ship_display(threeD_ship_display):
    set_variable(_3D_SHIP_DISPLAY_VAR_NAME, threeD_ship_display)

_3D_SHIP_DISPLAY_VAR_NAME = "_3d_ship_display"
