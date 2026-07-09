from sbs_utils.procedural.gui import gui_row, gui_section, gui_sub_section, gui_text

from data.missions.common.gui_top_tabs import GuiTopTab
from data.missions.common.controller_game_statistics import get_game_statistics
from data.missions.common.gui_color_scheme import color_text, color_background

def create_top_banner(difficulty, map_name):
    GAME_STATISTICS = get_game_statistics()
    
    gui_section(style="area:0,36px,100,180px;")
    with gui_sub_section(style=f"padding:10px,10px,10px,10px;background:{color_background()};"):
        gui_row(style="row-height:60px;")
        gui_text("GAME RESULTS", style="font:gui-6;justify:left;col-width:400px;color:white;")
        gui_text(f"LEVEL {difficulty} {map_name}", style="font:gui-5;justify:right;color:pink;")
        
        gui_row(style="row-height:80px;")
        gui_text(GAME_STATISTICS.get_reason_for_end(), style="font:gui-3;justify:left;color:cyan;")

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
        tab_label = get_game_end_gui_label_for_ship(ship_number)
        top_tabs.append(GuiTopTab(ship_number, ship_name, tab_label))
    return top_tabs

def get_game_end_gui_label_for_ship(ship_number):
    return f"gui_game_end_ship_{ship_number}"

_GAME_RESULTS_TOP_TAB_MAIN = GuiTopTab("main", "Overall", "gui_game_end_main")
