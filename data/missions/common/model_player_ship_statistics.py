
from data.missions.common.model_game_and_players_statistics import GameAndPlayersStatistics
from data.missions.common.pirate_features_definitions import can_loot

class PlayerShipStatistics(GameAndPlayersStatistics):
    
    def __init__(self, number, ship_type_key, name):
        # Note that python does not impicitly call super().__init__()
        # Its omission here is intentional, since it'd be redundant with the
        # super().record_game_start() call
        super().record_game_start()
        self._number = number
        self._ship_type_key = ship_type_key
        self._name = name
        self._looted_energy = 0
        self._looted_ordinance_by_type = {}
        for ordinance_type in _get_all_ordinance_types():
            self._looted_ordinance_by_type[ordinance_type] = 0
        self._was_permabanned_from_tsn = False
        self._was_destroyed = False
        self._remaining_energy = None
        self._remaining_ordinance_by_type = None
        self._could_loot = None
    
    # ----- basic getters -----
    
    @property
    def number(self):
        return self._number
    
    @property
    def ship_type_key(self):
        return self._ship_type_key
    
    @property
    def name(self):
        return self._name
    
    # ----- looting -----
    
    def record_looted_energy(self, energy):
        self._looted_energy += energy
    
    def record_looted_ordinance(self, ordinance_type, count):
        self._looted_ordinance_by_type[ordinance_type] += count
    
    # ----- other pirates stuff -----
    
    def record_tsn_permaban(self):
        self._was_permabanned_from_tsn = True
    
    # ----- destroyed -----
    
    def record_self_destroyed(self):
        self._was_destroyed = True
        self._remaining_energy = None
        self._remaining_ordinance_by_type = None
    
    # ----- end-of-game -----
    
    def record_game_end(self, player_ship_object):
        if player_ship_object is None:
            return
        self._remaining_energy = player_ship_object.data_set.get("energy", 0)
        self._remaining_ordinance_by_type = {ordinance_type: player_ship_object.data_set.get(f"{ordinance_type}_NUM", 0) for ordinance_type in _get_all_ordinance_types()}
        self._could_loot = can_loot(player_ship_object.id)
    
    # ----- after-game-ended getters -----
    
    @property
    def was_destroyed(self):
        return self._was_destroyed
    
    @property
    def remaining_energy(self):
        return self._remaining_energy
    
    # Returns dict where keys are ordinance type strings
    # and values are integer counts
    @property
    def remaining_ordinance(self):
        return self._remaining_ordinance_by_type
    
    @property
    def could_loot(self):
        return self._could_loot
    
    @property
    def looted_energy(self):
        return self._looted_energy
    
    # Returns dict where keys are ordinance type strings
    # and values are integer counts
    @property
    def looted_ordinance(self):
        return self._looted_ordinance_by_type
    
    @property
    def was_permabanned_from_tsn(self):
        return self._was_permabanned_from_tsn
    
    # ----- operator overrides -----
    
    def __lt__(self, other):
        return self.number < other.number
    
    def __gt__(self, other):
        return self != other and not self < other
    def __le__(self, other):
        return self == other or self < other
    def __ge__(self, other):
        return self == other or self > other

# TODO: not great to hardcode these ordinance type strings
# Is there a centralized getter (in vanilla)?
def _get_all_ordinance_types():
    return ["Homing", "Nuke", "EMP", "Mine"]
