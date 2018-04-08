"""
Area module.

Provides Area class, a container of game entities.
"""


from collections import deque
from itertools import chain


#--------- main class ---------#


class Area():
    """ A container of game entities and geometry driver. """

    def __init__(self):
        self.width = None
        self.height = None
        self.monsters = deque()
        self.doodads = deque()

    #--------- geometry ---------#

    def all_coordinates(self):
        """ Return a generator with all coordinate pairs in the area. """
        return ((x, y) for x in range(self.width) for y in range(self.height))

    #--------- generic entity manipulation ---------#

    def entities_at(self, x, y):
        """ Return a list of entities occupying a given position. """
        return [e for e in chain(self.monsters, self.doodads) if e.position == (x, y)]

    #--------- monsters manipulation ---------#

    def add_monster(self, monster, at_x, at_y):
        """
        Place a monster at the given position.
        Return True on success, False if the position is occupied.
        """
        potential_blockers = self.entities_at(at_x, at_y)
        for blocker in potential_blockers:
            if blocker.collides(monster):
                return False
        monster.position = (at_x, at_y)
        return True

    def hidden_monsters(self):
        """ Return a list of all hidden monsters. """
        return [m for m in self.monsters if m.hidden()]

    def remove_dead_monsters(self):
        """ Remove all dead (but not hidden!) monsters from the area. """
        self.monsters = deque((m for m in self.monsters if m.alive() or m.hidden()))

    def remove_monster(self, monster):
        """ Remove a monster from the area. """
        self.monsters = deque((m for m in self.monsters if monster is not m))


#--------- area generation variants ---------#


class AreaFromScratch(Area):
    """ A randomly-generated area. """

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height


class AreaFromData(Area):
    """ An area loaded from a YAML dict. """

    def __init__(self, data):
        raise NotImplementedError
