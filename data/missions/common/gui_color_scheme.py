
def color_text():
    return "#eee"

def color_text_secondary():
    return "#bbb"

def color_text_element_enabled():
    return color_text()

def color_text_element_disabled():
    # NOt actually referenced
    return "#777"

def color_background():
    return "#1578"

def color_background_secondary():
    return "#1572"

def color_background_secondary_opaque():
    return "#020a0e"

def color_background_title():
    return "#157"

def color_divider():
    return color_text()

def color_divider_secondary():
    return color_text_secondary()

# The options button in the upper left sometimes gets a fake replacement
# For details as to why see legendarymissions/game_setup/background_skybox_hack.py
# The fake button's background should be roughtly match the real button's background
def color_fake_options_button_background():
    return "#002e40"

# Also see color config fields in preferences.json
