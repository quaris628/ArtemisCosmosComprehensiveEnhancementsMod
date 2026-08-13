from sbs_utils.procedural.gui import gui_blank, gui_row, gui_section, gui_sub_section, gui_text

from data.missions.common.gui_top_tabs import GuiTopTab
from data.missions.common.controller_game_statistics import get_game_statistics
from data.missions.common.gui_color_scheme import color_text, color_background, color_divider_secondary

from data.missions.common.model_game_and_players_statistics import OriginSpecificCountDataType

def color_game_end_losses():
    return "lime"

def color_game_end_offensive():
    return "yellow"

def color_game_end_misc():
    return "white"

def create_top_banner(difficulty, map_name):
    GAME_STATISTICS = get_game_statistics()
    
    gui_section(style="area:0,36px,100,180px;")
    with gui_sub_section(style=f"padding:10px,10px,10px,10px;background:{color_background()};"):
        gui_row(style="row-height:60px;")
        gui_text("GAME RESULTS", style="font:gui-6;justify:left;col-width:400px;color:white;")
        gui_text(f"LEVEL {difficulty} {map_name}", style="font:gui-5;justify:right;color:pink;")
        
        gui_row(style="row-height:80px;")
        gui_text(GAME_STATISTICS.get_reason_for_end(), style="font:gui-3;justify:left;color:cyan;")

def create_offensive_combat_stats_text(object_statistics, surrender_title_text, destroyed_title_text, no_surrendered_or_destroyed_text):
    GAME_STATISTICS = get_game_statistics()
    origins_with_nonzero_count = object_statistics.get_origins_with_nonzero_count()
    
    gui_row(style="row-height:32px;")
    if len(origins_with_nonzero_count) == 0:
        gui_text(no_surrendered_or_destroyed_text, style=f"font:gui-3;justify:left;color:{color_game_end_offensive()};")
        _create_surrendered_killed_text(object_statistics)
        create_total_enemies_remaining_text()
        return
    
    total_surrendered_count = object_statistics.get_origin_specific_total_count(OriginSpecificCountDataType.SURRENDERED)
    total_destroyed_count = object_statistics.get_origin_specific_total_count(OriginSpecificCountDataType.DESTROYED)
    # $text is necessary in order to display a colon
    # https://github.com/artemis-sbs/LegendaryMissions/issues/566#issuecomment-4291760757
    gui_text(f"$text:{total_surrendered_count} {surrender_title_text}, {total_destroyed_count} {destroyed_title_text}:;", style=f"font:gui-3;justify:left;color:{color_game_end_offensive()};")
    
    create_label_value_value_triplet("", surrender_title_text[:4], destroyed_title_text[:4], color_game_end_offensive())
    for origin in origins_with_nonzero_count:
        if origin == "tsn":
            origin_display_string = "TSN"
        else:
            origin_display_string = origin.capitalize()
        surrendered_count = object_statistics.get_origin_specific_count(OriginSpecificCountDataType.SURRENDERED, origin)
        destroyed_count = object_statistics.get_origin_specific_count(OriginSpecificCountDataType.DESTROYED, origin)
        create_label_value_value_triplet(origin_display_string, str(surrendered_count), str(destroyed_count), color_game_end_offensive())
    
    _create_surrendered_killed_text(object_statistics)

def _create_surrendered_killed_text(object_statistics):
    create_label_value_pair("Surrendered Enemies Killed", str(object_statistics.get_surrendered_destroyed_count()), color_game_end_offensive())

def create_total_enemies_remaining_text():
    GAME_STATISTICS = get_game_statistics()
    remaining_enemies_count = GAME_STATISTICS.get_remaining_enemies()
    if 0 < remaining_enemies_count:
        create_label_value_pair("Total Enemies Remaining", str(remaining_enemies_count), color_game_end_offensive())

def create_allied_losses_stats_text(object_statistics, title_text):
    player_ships_count = object_statistics.get_player_ships_destroyed_count()
    friendly_single_seat_count = object_statistics.get_friendly_single_seat_destroyed_count()
    friendly_stations_count = object_statistics.get_friendly_stations_destroyed_count()
    friendly_ships_count = object_statistics.get_friendly_ships_destroyed_count()
    
    total_count = player_ships_count + friendly_single_seat_count + friendly_stations_count + friendly_ships_count
    
    gui_row(style="row-height:32px;padding:8px,4px,8px,0;")
    if total_count == 0:
        gui_text(f"No {title_text}", style=f"font:gui-3;justify:left;color:{color_game_end_losses()};")
        return
    # $text is necessary in order to display a colon
    # https://github.com/artemis-sbs/LegendaryMissions/issues/566#issuecomment-4291760757
    gui_text(f"$text:{total_count} {title_text}:;", style=f"font:gui-3;justify:left;color:{color_game_end_losses()};")
    
    if 0 < player_ships_count:
        create_label_value_pair("Player Ships", str(player_ships_count), color_game_end_losses())
    if 0 < friendly_single_seat_count:
        create_label_value_pair("Player Single-seat Craft", str(friendly_single_seat_count), color_game_end_losses())
    if 0 < friendly_stations_count:
        create_label_value_pair("Friendly Stations", str(friendly_stations_count), color_game_end_losses())
    if 0 < friendly_ships_count:
        create_label_value_pair("Friendly NPC Ships", str(friendly_ships_count), color_game_end_losses())

def create_label_value_pair(label_display_string, value_display_string, text_color=None):
    if text_color is None:
        text_color = color_text()
    gui_row(style="row-height:32px;")
    gui_text(label_display_string, style=f"font:gui-3;justify:right;color:{text_color};")
    gui_text(value_display_string, style=f"font:gui-3;col-width:9;justify:right;color:{text_color};")

def create_label_value_value_triplet(label_display_string, value1_display_string, value2_display_string, text_color=None):
    if text_color is None:
        text_color = color_text()
    gui_row(style="row-height:32px;")
    gui_text(label_display_string, style=f"font:gui-3;justify:right;color:{text_color};")
    gui_text(value1_display_string, style=f"font:gui-3;col-width:9;justify:right;color:{text_color};")
    gui_text(value2_display_string, style=f"font:gui-3;col-width:9;justify:right;color:{text_color};")

def create_divider():
    gui_row(style=f"row-height:3px;")
    gui_blank()
    gui_row(style=f"row-height:2px;background:{color_divider_secondary()};")
    gui_blank()
    gui_row(style=f"row-height:3px;")
    gui_blank()

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
