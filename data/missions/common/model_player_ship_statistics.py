
class PlayerShipStatistics:
    
    def __init__(self, number, ship_type_key, name):
        self._number = number
        self._ship_type_key = ship_type_key
        self._name = name
        self._was_destroyed = False
        self._remaining_energy = None
        self._remaining_ordinance = None
    
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
    
    # ----- destroyed -----
    
    def record_destroyed(self, player_ship_object):
        self._was_destroyed = True
        self._remaining_energy = None
        self._remaining_ordinance = None
    
    # ----- end-of-game -----
    
    def record_game_end(self, player_ship_object):
        if player_ship_object is None:
            return
        self._remaining_energy = player_ship_object.data_set.get("energy", 0)
        self._remaining_ordinance = {ordinance_type: player_ship_object.data_set.get(f"{ordinance_type}_NUM", 0) for ordinance_type in _get_all_ordinance_types()}
    
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
        return self._remaining_ordinance
    
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
