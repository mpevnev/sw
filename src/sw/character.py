"""
Character module.

Provides base Character class that Monster and Player classes inherit from.
"""


from sw.entity import Entity
from sw.modifiable import Modifiable


class Character(Modifiable, Entity):
    """ An active game entity. """

    def __init__(self):
        Modifiable.__init__(self)
        Entity.__init__(self)
        self.health = 0
        
    def alive(self):
        """ Return True if the character is alive. """
        return self.health > 0
