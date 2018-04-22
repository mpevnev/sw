"""
Character module.

Provides base Character class that Monster and Player classes inherit from.
"""


from collections import deque


import sw.const.stat as stat
from sw.entity import Entity
from sw.modifiable import Modifiable


class Character(Entity, Modifiable):
    """ An active game entity. """

    def __init__(self):
        Entity.__init__(self)
        Modifiable.__init__(self)
        self._health = 0

    #--------- health logic ---------#

    @property
    def max_health(self):
        """ Return the maximum health of the character. """
        return self.total_secondary[stat.SecondaryStat.HEALTH]

    @property
    def health(self):
        """ Return the health of the character. """
        return self._health

    @health.setter
    def health(self, value):
        """ Set the health. """
        value = max(0, value)
        value = min(value, self.max_health)
        self._health = value

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

    #--------- visibility logic ---------#

    def can_see_through(self, entity):
        """
        Return True if the given entity is transparent for this character.
        """
        raise NotImplementedError

    def transparent_for_monster(self, monster):
        return True

    def transparent_for_player(self, player):
        return True

    def within_sight(self, x, y):
        """
        Return True if the given position is within character's line of sight.
        """
        sight_range = self.total_secondary[stat.SecondaryStat.SIGHT]
        own_x, own_y = self.position
        return (own_x - sight_range <= x <= own_x + sight_range and
                own_y - sight_range <= y <= own_y + sight_range)

    #--------- other logic ---------#

    def tick(self, state, area, ui):
        self.update_totals(state, area, ui)
        for mod in self.innate_modifiers:
            mod.tick(self, state, area, ui)
        remaining_mods = deque()
        for mod in self.temp_modifiers:
            mod.tick(self, state, area, ui)
            if mod.duration == 0:
                mod.expire(self, state, area, ui)
            else:
                remaining_mods.append(mod)
        self.temp_modifiers = remaining_mods
