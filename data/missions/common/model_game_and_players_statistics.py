from enum import Enum

from sbs_utils.procedural.roles import has_role, has_roles, has_any_role
from sbs_utils.procedural.query import to_space_object

from data.missions.common.controller_vessel_types_data import get_vessel_types_data

# Parent class for stats shared between the overall GameStatistics
# and the ship-specific PlayerShipStatistics

class OriginSpecificCountDataType(Enum):
    DESTROYED = 0
    SURRENDERED = 1

# Use functions to expose enum values to mast code
def origin_specific_destroyed_counts():
    return OriginSpecificCountDataType.DESTROYED
def origin_specific_surrendered_counts():
    return OriginSpecificCountDataType.SURRENDERED

class GameAndPlayersStatistics:
    
    def __init__(self):
        self.record_game_start()
    
    def record_game_start(self):
        self._destroyed_counts_by_origin = {}
        self._surrendered_counts_by_origin = {}
        for origin in get_vessel_types_data().get_all_origins():
            self._destroyed_counts_by_origin[origin.lower()] = 0
            self._surrendered_counts_by_origin[origin.lower()] = 0
        self._friendly_single_seat_destroyed_count = 0
        self._player_ships_destroyed_count = 0
        self._friendly_stations_destroyed_count = 0
        self._friendly_ships_destroyed_count = 0
        self._surrendered_destroyed_count = 0
        self._surrendered_count = 0
        self._player_beams_fired_count = 0
        self._player_ordinance_fired_count = 0
        self._player_successful_docks_count = 0
        self._picked_up_anomaly_count = 0
    
    # ----- vessel destroyed -----
    
    def record_vessel_destroyed(self, dead_vessel_id):
        if has_roles(dead_vessel_id, "surrendered"):
            self._surrendered_destroyed_count += 1
        
        if has_roles(dead_vessel_id, "cockpit,__player__"):
            self._friendly_single_seat_destroyed_count += 1
        elif has_role(dead_vessel_id, "__player__"):
            self._player_ships_destroyed_count += 1
        # TODO probably shouldn't hardcode "tsn,civ" to be equivalent to friendly
        elif has_any_role(dead_vessel_id, "tsn,civ") and has_role(dead_vessel_id, "station"):
            self._friendly_stations_destroyed_count += 1
        elif has_any_role(dead_vessel_id, "tsn,civ") and not has_role(dead_vessel_id, "raider"):
            self._friendly_ships_destroyed_count += 1
        else:
            dead_vessel_object = to_space_object(dead_vessel_id)
            if dead_vessel_object is not None:
                self._record_origin_specific_count(OriginSpecificCountDataType.DESTROYED, dead_vessel_object)
    
    def get_player_ships_destroyed_count(self):
        return self._player_ships_destroyed_count
    
    def get_friendly_stations_destroyed_count(self):
        return self._friendly_stations_destroyed_count
    
    def get_friendly_single_seat_destroyed_count(self):
        return self._friendly_single_seat_destroyed_count
    
    def get_friendly_ships_destroyed_count(self):
        return self._friendly_ships_destroyed_count
    
    def get_surrendered_destroyed_count(self):
        return self._surrendered_destroyed_count
    
    # ----- vessel surrendered -----
    
    def record_vessel_surrendered(self, surrendered_vessel_object):
        self._record_origin_specific_count(OriginSpecificCountDataType.SURRENDERED, surrendered_vessel_object)
    
    # TODO: Tonnage surrendered? Or shield points surrendered?
    
    # ----- shared b/t destroyed and surrendered counts -----
    
    def _record_origin_specific_count(self, data_type, vessel_object):
        # Anomalies (and probably other things too?) have their origin set to "no origin"
        # These (and probably similar things) shouldn't be counted
        if vessel_object.origin is None or vessel_object.origin == "no origin":
            return
        
        lowercase_origin = vessel_object.origin.lower()
        _dictionary = self._get_origin_specific_dict(data_type)
        if lowercase_origin in _dictionary:
            _dictionary[lowercase_origin] += 1
        else:
            _dictionary[lowercase_origin] = 1
    
    # If data_type is omitted, then returns union of all, i.e. all origins with
    # at least one non-zero value for at least one origin-specific data type
    def get_origins_with_nonzero_count(self, data_type=None):
        if data_type is not None:
            _dictionary = self._get_origin_specific_dict(data_type)
            return {origin for origin, count in _dictionary.items() if 0 < count}
        else: # data_type is None
            origins = set()
            for data_type1 in OriginSpecificCountDataType:
                origins.update(self.get_origins_with_nonzero_count(data_type1))
            return origins
    
    def get_origin_specific_count(self, data_type, origin):
        _dictionary = self._get_origin_specific_dict(data_type)
        if origin not in _dictionary:
            return 0
        return _dictionary[origin]
    
    def get_origin_specific_counts_iterable(self, data_type):
        _dictionary = self._get_origin_specific_dict(data_type)
        return _dictionary.items()
    
    def get_origin_specific_total_count(self, data_type):
        _dictionary = self._get_origin_specific_dict(data_type)
        return sum(_dictionary.values())
    
    def _get_origin_specific_dict(self, defeat_type):
        match defeat_type:
            case OriginSpecificCountDataType.DESTROYED:
                return self._destroyed_counts_by_origin
            case OriginSpecificCountDataType.SURRENDERED:
                return self._surrendered_counts_by_origin
            case _:
                return None
    
    # ----- player fired beam -----
    
    def record_player_fired_beam(self):
        self._player_beams_fired_count += 1
    
    def get_player_beams_fired_count(self):
        return self._player_beams_fired_count
    
    # ----- player fired ordinance -----
    
    # TODO record this; waiting on sbs_utils feature to be implemented
    # https://github.com/artemis-sbs/LegendaryMissions/issues/385
    
    def record_player_fired_ordinance(self):
        self._player_ordinance_fired_count += 1
    
    def get_player_ordinance_fired_count(self):
        #return self._player_ordinance_fired_count
        return "?"
    
    # ----- player successfully docked -----
    
    def record_player_successful_dock(self):
        self._player_successful_docks_count += 1
    
    def get_player_successful_docks_count(self):
        return self._player_successful_docks_count
    
    # ----- picked up anomaly -----
    
    def record_player_picked_up_anomaly(self):
        self._picked_up_anomaly_count += 1
    
    def get_player_picked_up_anomaly_count(self):
        return self._picked_up_anomaly_count
