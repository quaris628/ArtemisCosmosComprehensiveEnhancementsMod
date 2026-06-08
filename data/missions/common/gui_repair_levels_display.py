from enum import Enum

from sbs_utils.mast.label import label
from sbs_utils.procedural.execution import END, get_variable, set_variable
from sbs_utils.procedural.grid import grid_objects
from sbs_utils.procedural.gui import gui_blank, gui_row, gui_text
from sbs_utils.procedural.roles import has_role, has_roles, all_roles, role
from sbs_utils.procedural.signal import signal_register

from data.missions.common.library_function_patches import gui_represent_patched
from data.missions.common.common_signals import signal_system_nodes_repair_changed, signal_heat_pool_system_nodes_repair_changed, signal_all_system_nodes_repair_changed
from data.missions.common.gui_color_scheme import color_text, color_background, color_text_secondary

def create_repair_levels_display(ship_id):
    
    gui_row(f"row-height:23px;background:{_REPAIR_DISPLAY_BACKGROUND_COLOR};")
    gui_text("System", style=f"font:gui-1;justify:left;padding:5px,0;color:{color_text_secondary()};")
    gui_text("Condition", style=f"font:gui-1;col-width:75px;justify:right;padding:0,0,5px,0;color:{color_text_secondary()};")
    gui_row(f"row-height:2px;background:{color_background()};")
    gui_blank()
    
    repair_display_gui_elements = {}
    all_systems_on_ship = _get_all_systems_on_ship(ship_id)
    all_system_grid_object_ids = _get_all_system_grid_object_ids_on_ship(ship_id)
    for system in all_systems_on_ship:
        repair_percentage_str, repair_level = _get_repair_percentage_str_and_repair_level(all_system_grid_object_ids, system)
        gui_row(f"row-height:22px;background:{_REPAIR_DISPLAY_BACKGROUND_COLOR};")
        gui_text(system.get_display_string(), style=f"font:gui-1;justify:left;padding:5px,0;color:{color_text()};")
        repair_percentage_text = gui_text(repair_percentage_str, style=f"font:gui-1;col-width:49px;justify:center;color:{color_text()};background:{repair_level.get_background_color()};")
        gui_row(f"row-height:2px;background:{color_background()};")
        gui_blank()
        
        repair_display_gui_elements[system] = repair_percentage_text
    
    _set_repair_display_gui_elements(repair_display_gui_elements)
    
    # Initialize values to the ship's current repair state
    #_update_repair_levels_display_for_systems(ship_id, all_systems_on_ship)
    
    signal_register(signal_system_nodes_repair_changed(ship_id), _repair_levels_display_on_system_nodes_repair_changed, is_temporary=True)
    signal_register(signal_heat_pool_system_nodes_repair_changed(ship_id), _repair_levels_display_on_heat_pool_system_nodes_repair_changed, is_temporary=True)
    signal_register(signal_all_system_nodes_repair_changed(ship_id), _repair_levels_display_on_all_system_nodes_repair_changed, is_temporary=True)

@label()
def _repair_levels_display_on_system_nodes_repair_changed():
    ship_id = get_variable("SHIP_ID")
    grid_object_ids = get_variable("GRID_OBJECT_IDS")
    
    affected_systems = set()
    for grid_object_id in grid_object_ids:
        system = _get_system(grid_object_id)
        if system is None:
            continue
        affected_systems.add(system)
    _update_repair_levels_display_for_systems(ship_id, affected_systems)
    
    yield END()

@label()
def _repair_levels_display_on_heat_pool_system_nodes_repair_changed():
    ship_id = get_variable("SHIP_ID")
    heat_pool_id = get_variable("HEAT_POOL_ID")
    
    affected_systems = HeatPool(heat_pool_id).get_systems()
    _update_repair_levels_display_for_systems(ship_id, affected_systems)
    
    yield END()

@label()
def _repair_levels_display_on_all_system_nodes_repair_changed():
    ship_id = get_variable("SHIP_ID")
    is_reset_to_all_nominal = get_variable("IS_RESET_TO_ALL_NOMINAL")
    
    all_systems_on_ship = _get_all_systems_on_ship(ship_id)
    if not is_reset_to_all_nominal:
        _update_repair_levels_display_for_systems(ship_id, all_systems_on_ship)
    else: # if is_reset_to_all_nominal:
        repair_display_gui_elements = _get_repair_display_gui_elements()
        for system in all_systems_on_ship:
            repair_percentage_text = repair_display_gui_elements[system]
            repair_percentage_text.background = RepairLevel.NOMINAL.get_background_color()
            repair_percentage_text.value = "100%"
            gui_represent_patched(repair_percentage_text)
    
    yield END()

def _update_repair_levels_display_for_systems(ship_id, affected_systems):
    repair_display_gui_elements = _get_repair_display_gui_elements()
    all_system_grid_object_ids = _get_all_system_grid_object_ids_on_ship(ship_id)
    for system in affected_systems:
        repair_percentage_str, repair_level = _get_repair_percentage_str_and_repair_level(all_system_grid_object_ids, system)
        repair_percentage_text = repair_display_gui_elements[system]
        repair_percentage_text.background_color = repair_level.get_background_color()
        repair_percentage_text.value = repair_percentage_str
        gui_represent_patched(repair_percentage_text)

def _get_repair_percentage_str_and_repair_level(all_system_grid_object_ids, system):
    system_grid_object_ids = all_system_grid_object_ids & all_roles(system.value)
    total_count = len(system_grid_object_ids)
    undamaged_count = len(system_grid_object_ids & role("__undamaged__"))
    if total_count == 0:
        # Should never happen, but just in case, avoid divide by zero crash
        repair_percentage_str = "-"
        repair_level = RepairLevel.UNKNOWN
    else:
        repair_percentage_str = f"{undamaged_count / total_count:.0%}"
        if undamaged_count == 0:
            repair_level = RepairLevel.GONE
        elif undamaged_count * 2 < total_count:
            repair_level = RepairLevel.MAJOR_DAMAGE
        elif undamaged_count < total_count:
            repair_level = RepairLevel.MINOR_DAMAGE
        else: # total_count == undamaged_count
            repair_level = RepairLevel.NOMINAL
    
    return repair_percentage_str, repair_level

def _is_system_grid_object_damaged(system_grid_object_id):
    return has_role(system_grid_object_id, "__damaged__")
    # An __undamaged__ role also exists
    # has_role(system_grid_object_id, "__undamaged__")

def _get_all_systems_on_ship(ship_id):
    return System
    # I considered doing something like this, where only the systems on the ship
    # will be listed. However, this was complicated by the fact that the grid
    # objects might not exist at the time the gui is initialized.
    # Besides, having a consistent position for each system helps slightly with
    # identifying which row is for which system, especially at a glance.
    # all_system_grid_object_ids = _get_all_system_grid_object_ids_on_ship(ship_id)
    # if len(all_system_grid_object_ids) == 0:
        # # the ship's grid objects haven't been built yet
        # # (this happens if the engineering client was ready when the game started)
        # # ???
    # return [system for system in System if 0 < len(all_system_grid_object_ids & all_roles(system.value))]

def _get_all_system_grid_object_ids_on_ship(ship_id):
    return grid_objects(ship_id) & role("system")

def _get_system(system_grid_object_id):
    # This isn't very efficient, but unfortunately I can't think of a
    # reasonably better alternative.
    # The data structure is pretty tightly coupled to the rest of the code,
    # i.e. it can't be easily changed.
    # node.get_roles() won't work because it will include irrelevant roles.
    # Could cache the roles as an inventory value to each system, but that would
    # unnecessarily add a memory burden of storing the strings inefficiently,
    # so it might not actually be more efficient overall.
    for system in System:
        if has_roles(system_grid_object_id, system.value):
            return system
    return None

# ---- enums -----

class System(Enum):
    BEAMS = "weapon,beam"
    TORPEDO = "weapon,torpedo"
    IMPULSE = "engine,impulse"
    WARP_DRIVE = "engine,warp"
    JUMP_DRIVE = "engine,jump"
    MANEUVER = "engine,maneuver"
    SENSORS = "sensor"
    FRONT_SHIELD = "shield,fwd"
    REAR_SHIELD = "shield,aft"
    
    def get_display_string(self):
        return self.name.title().replace("_", " ")

class HeatPool(Enum):
    WEAPONS = 0
    ENGINES = 1
    SENSORS = 2
    SHIELDS = 3
    
    def get_systems(self):
        return _HEAT_POOL_SYSTEMS[self]

_HEAT_POOL_SYSTEMS = {
    HeatPool.WEAPONS: [System.BEAMS, System.TORPEDO],
    HeatPool.ENGINES: [System.MANEUVER, System.IMPULSE, System.WARP_DRIVE, System.JUMP_DRIVE],
    HeatPool.SENSORS: [System.SENSORS],
    HeatPool.SHIELDS: [System.FRONT_SHIELD, System.REAR_SHIELD],
}

class RepairLevel(Enum):
    NOMINAL = 0
    MINOR_DAMAGE = 1
    MAJOR_DAMAGE = 2
    GONE = 3
    UNKNOWN = 4
    
    def get_background_color(self):
        match self:
            case RepairLevel.NOMINAL:
                return "#007f00a0"
            case RepairLevel.MINOR_DAMAGE:
                return "#cc6600cc"
            case RepairLevel.MAJOR_DAMAGE:
                return "#cc0000ff"
            case RepairLevel.GONE:
                return "#000000ff"
            case RepairLevel.UNKNOWN:
                return _REPAIR_DISPLAY_BACKGROUND_COLOR
            case _:
                return _REPAIR_DISPLAY_BACKGROUND_COLOR

_REPAIR_DISPLAY_BACKGROUND_COLOR = "#000000ff"

# ---- setter/getter wrappers -----

def _set_repair_display_gui_elements(repair_display_gui_elements):
    set_variable(_REPAIR_DISPLAY_GUI_ELEMENTS_VAR_NAME, repair_display_gui_elements)

def _get_repair_display_gui_elements():
    return get_variable(_REPAIR_DISPLAY_GUI_ELEMENTS_VAR_NAME)

_REPAIR_DISPLAY_GUI_ELEMENTS_VAR_NAME = "_repair_display_gui_elements"
