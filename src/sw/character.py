"""
Character module.

Provides base Character class that Monster and Player classes inherit from.
"""


from sw.entity import Entity
from sw.modifiable import Modifiable


class Character(Entity, Modifiable):
    """ An active game entity. """

    def __init__(self):
        Entity.__init__(self)
        Modifiable.__init__(self)
        self.health = 0

    #--------- container logic ---------#

    def add_to_area(self, area):
        raise NotImplementedError

    def remove_from_area(self, area):
        raise NotImplementedError

    #--------- death logic ---------#

    def alive(self):
        return self.health > 0

    def death_action(self, state, area, ui):
        raise NotImplementedError

    def die(self):
        self.health = 0
