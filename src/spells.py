
class Rage(object):
    def __init__(self, damage_factor=2, movement_factor=2):
        self.damage_factor = damage_factor
        self.movement_factor = movement_factor
        self.can = 0
        self.mod = 1
    
    def get_damage_factor(self):
        return self.damage_factor

    def get_movement_factor(self):
        return self.movement_factor

    def get_can(self):
        return self.can

    def set_can(self, can):
        self.can = can
    
    def get_mod(self):
        return self.mod

    def set_mod(self, mod):
        self.mod = mod

class Heal(object):
    def __init__(self, heal_factor=1.5):
        self.heal_factor = heal_factor

    def get_heal_factor(self):
        return self.heal_factor

    def set_heal_factor(self, heal_factor):
        self.heal_factor = heal_factor
    
