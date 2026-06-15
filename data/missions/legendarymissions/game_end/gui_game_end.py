
from sbs_utils.mast.label import label
from sbs_utils.procedural.execution import END, AWAIT, jump, get_variable, set_variable, task_schedule
from sbs_utils.procedural.signal import signal_register
from sbs_utils.procedural.gui import gui_section, gui_sub_section, gui_text, gui_message, gui_ship, gui_row, gui_show, gui_hide
from sbs_utils.procedural.timers import delay_app

from data.missions.common.library_function_patches import gui_represent_patched, gui_dropdown_patched
from data.missions.common.gui_top_tabs import GuiTopTab
from data.missions.common.model_single_seat_craft_type import CraftCategory
from data.missions.common.controller_game_statistics import get_game_statistics
from data.missions.common.controller_vessel_types_data import get_vessel_types_data
from data.missions.common.gui_color_scheme import color_text, color_text_secondary, color_background, color_divider, color_divider_secondary

def create_top_banner(difficulty, map_name):
    client_id = get_variable("client_id")
    GAME_STATISTICS = get_game_statistics()
    
    gui_section(style=f"area:0,36px,100,180px;")
    with gui_sub_section(style=f"padding:10px,10px,10px,10px;background:{color_background()};"):
        gui_row(style="row-height:60px;")
        gui_text("GAME RESULTS", style=f"font:gui-6;justify:left;col-width:400px;color:{color_text()};")
        gui_text(f"LEVEL {difficulty} {map_name}", style=f"font:gui-5;justify:right;color:pink;")
        
        gui_row(style="row-height:80px;")
        gui_text(f"Game ended because {GAME_STATISTICS.get_reason_for_end()}", style=f"font:gui-3;justify:left;color:cyan;")

def create_label_value_pair(label_display_string, value_display_string, text_color=None):
    if text_color is None:
        text_color = color_text()
    gui_row(style="row-height:32px;padding:0,4px;")
    gui_text(label_display_string, style=f"font:gui-3;justify:right;col-width:38-30px;color:{text_color};")
    gui_text(value_display_string, style=f"font:gui-3;justify:right;color:{text_color};")

def get_game_results_top_tabs():
    GAME_STATISTICS = get_game_statistics()
    
    top_tabs = [_GAME_RESULTS_TOP_TAB_MAIN]
    for player_ship_statistics in GAME_STATISTICS.get_all_player_ships_statistics():
        ship_number = player_ship_statistics.number
        ship_name = player_ship_statistics.name
        tab_label = f"gui_game_end_ship_{ship_number}"
        top_tabs.append(GuiTopTab(ship_number, ship_name, tab_label))
    return top_tabs

_GAME_RESULTS_TOP_TAB_MAIN = GuiTopTab("main", "Overall", "gui_game_end_main")
