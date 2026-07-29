from sbs_utils.mast.label import label
from sbs_utils.procedural.cosmos import sim_create, sim_resume, sim_pause
from sbs_utils.procedural.execution import AWAIT, END, get_shared_variable, set_shared_variable, task_cancel, task_schedule
from sbs_utils.procedural.timers import delay_app

from sbs_utils.procedural.signal import signal_emit

from data.missions.common.q_logger import qlog, qlog_level_info

def initialize_game_state():
    _set_game_state(game_state_setting_up())
    _set_tasks_to_end_when_game_ends([])
    signal_emit(signal_game_setup_initialized())

def start_game():
    qlog(qlog_level_info(), "Starting game")
    old_game_state = get_game_state()
    if old_game_state != game_state_setting_up():
        return
    sim_create()
    signal_emit(signal_sim_created_for_game_start())
    sim_resume()
    _set_game_state(game_state_running())
    signal_emit(signal_game_started())
    # for backwards compatibility
    signal_emit("game_started")

def pause_game():
    qlog(qlog_level_info(), "Pausing game")
    old_game_state = get_game_state()
    if old_game_state != game_state_running():
        return
    sim_pause()
    _set_game_state(game_state_paused())
    signal_emit(signal_game_paused())

def resume_game():
    qlog(qlog_level_info(), "Resuming game")
    old_game_state = get_game_state()
    if old_game_state != game_state_paused():
        return
    sim_resume()
    _set_game_state(game_state_running())
    signal_emit(signal_game_resumed())

def end_game():
    qlog(qlog_level_info(), "Ending game")
    old_game_state = get_game_state()
    if old_game_state not in [game_state_running(), game_state_paused()]:
        return
    sim_pause()
    
    # Destroy everything in the previously-running sim.
    # This isn't strictly necessary to do now, but it should help memory,
    # processing, network bandwidth, etc to wipe all the sim data as soon as
    # we don't need it.
    task_schedule(_wipe_sim_on_end_game_after_delay)
    
    _set_game_state(game_state_ended())
    signal_emit(signal_game_ended())
    
    _end_tasks_on_game_end()

@label()
def _wipe_sim_on_end_game_after_delay():
    # For some reason I don't understand, calling sim_create() without/before
    # this delay causes an engine-level server crash (the server window closes).
    # A delay length of 0 seemed sufficient for some ways of ending the game
    # like the gamemaster commaned, but for other ways like no more player ships
    # a zero delay was insufficient while 0.1s seems to work.
    yield AWAIT(delay_app(1))
    # Hypothetically, it's possible a new game started during
    # the above delay.
    # If so, it's very important to not wipe the sim!
    if is_game_in_progress():
        yield END()
    sim_create()
    signal_emit(signal_sim_wiped_after_game_ended())
    yield END()

def set_up_new_game():
    qlog(qlog_level_info(), "Setting up new game")
    old_game_state = get_game_state()
    if old_game_state != game_state_ended():
        return
    _set_game_state(game_state_setting_up())
    signal_emit(signal_game_set_up_for_new())

def _on_change_sbs_utils_sim_state(sbs_utils_sim_state):
    if sbs_utils_sim_state == _sbs_utils_sim_state_running():
        if get_game_state() == game_state_paused():
            _set_game_state(game_state_running())
            signal_emit(signal_game_paused())
    elif sbs_utils_sim_state == _sbs_utils_sim_state_paused():
        if get_game_state() == game_state_running():
            _set_game_state(game_state_paused())
            signal_emit(signal_game_paused())

def end_task_when_game_ends(task):
    tasks = _get_tasks_to_end_when_game_ends()
    
    tasks.append(task)
    
    _set_tasks_to_end_when_game_ends(tasks)

def _end_tasks_on_game_end():
    tasks = _get_tasks_to_end_when_game_ends()
    
    for task in tasks:
        if task is not None:
            print(f"cancelling {task}")
            task_cancel(task)
    tasks = []
    
    _set_tasks_to_end_when_game_ends(tasks)

# ---- setter/getter wrappers -----

def get_game_state():
    return get_shared_variable(_GAME_STATE_VAR_NAME)

def _set_game_state(game_state):
    if get_game_state() != game_state:
        set_shared_variable(_GAME_STATE_VAR_NAME, game_state)
        signal_emit(signal_game_state_changed(), data={"GAME_STATE": game_state})

# This variable name is referenced directly in gui_game_setup.mast
# as part of a workaround. Don't edit this variable name without also
# updating its reference in gui_game_setup.mast.
_GAME_STATE_VAR_NAME = "GAME_STATE"

def _get_tasks_to_end_when_game_ends():
    return get_shared_variable(_TASKS_TO_END_WHEN_GAME_ENDS_VAR_NAME)

def _set_tasks_to_end_when_game_ends(tasks):
    set_shared_variable(_TASKS_TO_END_WHEN_GAME_ENDS_VAR_NAME, tasks)

_TASKS_TO_END_WHEN_GAME_ENDS_VAR_NAME = "_tasks_to_end_when_game_ends"

# ---- Enums -----

# Using functions instead of true enums allows literals to be in mast code

# quasi-enum of possible game states
# most code should interface with this

def game_state_setting_up():
    return 1
def game_state_running():
    return 2
def game_state_paused():
    return 3
def game_state_ended():
    return 4

def is_game_in_progress():
    game_state = get_game_state()
    return game_state == game_state_running() or game_state == game_state_paused()

# quasi-enum of signals sent for all events that change the game state
def signal_game_setup_initialized():
    return "game_state_change_setup_initialized"
def signal_game_started():
    return "game_state_change_started"
def signal_game_paused():
    return "game_state_changed_paused"
def signal_game_resumed():
    return "game_state_changed_resumed"
def signal_game_ended():
    return "game_state_changed_ended"
def signal_game_set_up_for_new():
    return "game_state_changed_set_up_for_new_game"

def signal_game_state_changed():
    return "game_state_changed"

def signal_sim_wiped_after_game_ended():
    return "sim_wiped_after_game_ended"
def signal_sim_created_for_game_start():
    return "sim_created_for_game_start"

# quasi-enum of possible simulation states used by sbs_utils
# abstract these away from (most of) the rest of the code
def _sbs_utils_sim_state_uninitialized():
    return "sim_unknown"
def _sbs_utils_sim_state_running():
    return "sim_running"
def _sbs_utils_sim_state_paused():
    return "sim_paused"
# There might be other values that I don't know about
# (I can't find any comprehensive documentation)
