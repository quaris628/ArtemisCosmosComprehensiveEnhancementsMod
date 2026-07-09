from sbs_utils.procedural.execution import get_shared_variable, set_shared_variable

from data.missions.common.model_game_statistics import GameStatistics

# ----- Initializing -----

def initialize_game_statistics():
    _set_game_statistics(GameStatistics())

# ----- Setter/getter wrappers -----

def get_game_statistics():
    return get_shared_variable(_GAME_STATISTICS_VAR_NAME)

def _set_game_statistics(setup_data):
    set_shared_variable(_GAME_STATISTICS_VAR_NAME, setup_data)

_GAME_STATISTICS_VAR_NAME = "_game_statistics"
