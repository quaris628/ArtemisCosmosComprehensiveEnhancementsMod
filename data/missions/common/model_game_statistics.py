from math import floor

from sbs_utils.helpers import FrameContext
from sbs_utils.procedural.roles import role, all_roles, has_role
from sbs_utils.procedural.query import to_space_object

from data.missions.common.model_game_and_players_statistics import GameAndPlayersStatistics
from data.missions.common.model_player_ship_statistics import PlayerShipStatistics

# Many functions have unused parameters.
# This is to make it easier to start recording the data in those
# parameters in the future, even though they aren't tracked right now.

class GameStatistics(GameAndPlayersStatistics):
    
    def __init__(self):
        # Note that python does not impicitly call super().__init__()
        # Its omission here is intentional, since it'd be redundant with the
        # super().record_game_start() call inside self.record_game_start()
        self.record_game_start()
    
    def record_game_start(self):
        super().record_game_start()
        self._start_tick_count = FrameContext.sim.time_tick_counter
        self._duration_in_seconds = None
        self._reason_for_end = None
        self._is_successful_end = None
        self._remaining_enemies = None
        self._player_ships_statistics = {}
    
    def record_player_ship_added(self, ship_number, ship_id, ship_type_key, name):
        player_ship_statistics = PlayerShipStatistics(ship_number, ship_type_key, name)
        self._player_ships_statistics[ship_id] = player_ship_statistics
    
    # ----- end-of-game -----
    
    def record_game_end(self, reason="Game ended.", is_success=None, zero_remaining_enemies=False):
        # I don't know why this pylint warning was firing for setting
        # attributes in this function but not for any others.
        # Regardless, the attributes are actually defined in __init__,
        # so this warning can be safely ignored.
        # pylint: disable=attribute-defined-outside-init
        
        # Assumes the simulation runs at 30 ticks per second
        # See the commend in preferences.json for the scriptTickDelay setting
        # This is the same math as in vanilla (as of 1.2.7), which I tested with a
        # different scriptTickDelay and it still seemed accurate as far as I could tell.
        self._duration_in_seconds = (FrameContext.sim.time_tick_counter - self._start_tick_count) / 30
        self._reason_for_end = reason
        self._is_successful_end = is_success
        if zero_remaining_enemies:
            self._remaining_enemies = 0
        else:
            self._remaining_enemies = len(role("raider") | all_roles("enemy,station"))
        
        player_ship_ids = role("__player__") - role("cockpit")
        for player_ship_id in player_ship_ids:
            player_ship_object = to_space_object(player_ship_id)
            player_ship_statistics = self._player_ships_statistics[player_ship_id]
            player_ship_statistics.record_game_end(player_ship_object)
    
    def get_duration_in_seconds(self):
        return self._duration_in_seconds
    
    def get_duration_in_minutes(self):
        return floor(self._duration_in_seconds / 60)
    
    def get_reason_for_end(self):
        return self._reason_for_end
    
    def is_end_success(self):
        return self._is_successful_end
    
    def get_remaining_enemies(self):
        return self._remaining_enemies
    
    # ----- player ships -----
    
    def get_player_ship_statistics_by_id(self, player_ship_id):
        if player_ship_id not in self._player_ships_statistics:
            return None
        return self._player_ships_statistics[player_ship_id]
    
    def get_player_ship_statistics_by_number(self, ship_number):
        # Maybe use an index instead? But that's more complicated
        # and might not be worth any peformance improvement
        for player_ship_statistics in self._player_ships_statistics.values():
            if player_ship_statistics.number == ship_number:
                return player_ship_statistics
        return None
    
    def get_all_player_ships_statistics(self):
        return sorted(self._player_ships_statistics.values())

    # ----- overrides (and related functions) -----
    
    def record_vessel_destroyed(self, dead_vessel_id):
        super().record_vessel_destroyed(dead_vessel_id)
        if has_role(dead_vessel_id, "__player__") and not has_role(dead_vessel_id, "cockpit"):
            self._player_ships_statistics[dead_vessel_id].record_self_destroyed()
    
    def record_player_killed(self, player_ship_id, dead_vessel_id):
        # If a vessel is destroyed by any source, including a player ship,
        # then GameStatistics.record_vessel_destroyed should get called.
        # If a vessel is killed by a player ship, then record_player_killed
        # should ALSO get called.
        # So, do NOT call super().record_vessel_destroyed() here, to avoid
        # calling it twice for the same vessel.
        self._player_ships_statistics[player_ship_id].record_vessel_destroyed(dead_vessel_id)
    
    def record_vessel_surrendered(self, player_ship_id, surrendered_vessel_object):
        super().record_vessel_surrendered(surrendered_vessel_object)
        self._player_ships_statistics[player_ship_id].record_vessel_surrendered(surrendered_vessel_object)
    
    def record_player_fired_beam(self, player_ship_id):
        super().record_player_fired_beam()
        self._player_ships_statistics[player_ship_id].record_player_fired_beam()
    
    # TODO record this; waiting on sbs_utils feature to be implemented
    # https://github.com/artemis-sbs/LegendaryMissions/issues/385
    
    def record_player_fired_ordinance(self, player_ship_id):
        super().record_player_fired_ordinance()
        self._player_ships_statistics[player_ship_id].record_player_fired_ordinance()
    
    def record_player_successful_dock(self, player_ship_id):
        super().record_player_successful_dock()
        self._player_ships_statistics[player_ship_id].record_player_successful_dock()
    
    def record_player_picked_up_anomaly(self, player_ship_id):
        super().record_player_picked_up_anomaly()
        self._player_ships_statistics[player_ship_id].record_player_picked_up_anomaly()
