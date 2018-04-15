"""
Area module.

Provides Area class, a container of game entities.
"""


from collections import deque
from itertools import chain
import random as rand


#--------- main class ---------#


class Area():
    """ A container of game entities and geometry driver. """

    def __init__(self, data):
        self.data = data
        self.width = None
        self.height = None
        self.player = None
        self.doodads = deque()
        self.items = deque()
        self.monsters = deque()

    #--------- geometry ---------#

    def all_coordinates(self):
        """ Return a generator with all coordinate pairs in the area. """
        return ((x, y) for x in range(self.width) for y in range(self.height))

    def borders(self):
        """ Return a generator with all border points. """
        w = self.width
        h = self.heigth
        for x in range(1, w - 1):
            yield (x, 0)
            yield (x, h - 1)
        for y in range(h):
            yield (0, y)
            yield (w - 1, y)

    def contains_point(self, x, y):
        """ Return True if the given point is in the area. """
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    #--------- generic entity manipulation ---------#

    def add_entity(self, entity, at_x, at_y):
        """
        Place a given entity at the given position and add it to appropriate
        subcontainer in the area.

        Return True on success, False if the spot is occupied.
        """
        if not self.place_entity(entity, at_x, at_y):
            return False
        entity.add_to_area(self)
        return True

    def entities(self, living_flag):
        """
        Return a list with all alive entities in the area if 'living_flag' is
        truthy, or a list with all dead entities if 'living_flag' is falsey.
        """
        everything = chain([self.player], self.monsters, self.doodads)
        if living_flag:
            cond = lambda e: e is not None and e.alive()
        else:
            cond = lambda e: e is not None and not e.alive()
        return [e for e in everything if cond(e)]

    def entities_at(self, x, y, living_flag):
        """
        Return a list with all alive entities at the given position if
        'living_flag' is truthy, or a list with all dead entities at the given
        position if 'living_flag' if falsey.
        """
        everything = chain([self.player], self.monsters, self.doodads)
        if living_flag:
            cond = lambda e: e is not None and e.alive() and e.position == (x, y)
        else:
            cond = lambda e: e is not None and not e.alive() and e.position == (x, y)
        return [e for e in everything if cond(e)]

    def place_entity(self, entity, at_x, at_y):
        """
        Return True and change entity's position to (at_x, at_y) if the entity
        can occupy this spot without colliding with anything and the new
        position is within area bounds.

        Return False otherwise.
        """
        if at_x < 0 or at_y < 0 or at_x >= self.width or at_y >= self.height:
            return False
        potential_blockers = self.entities_at(at_x, at_y, True)
        for blocker in potential_blockers:
            if entity.would_collide(blocker, at_x, at_y):
                return False
        entity.position = (at_x, at_y)
        return True

    def remove_dead_entities(self):
        """ Remove all dead entities from the area. """
        self.doodads = deque((d for d in self.doodads if d.alive()))
        self.items = deque((i for i in self.items if i.alive()))
        self.monsters = deque((m for m in self.monsters if m.alive()))

    def remove_entity(self, entity):
        """ Remove the entity from the area. """
        entity.remove_from_area(self)

    def shift_entity(self, entity, dx, dy):
        """
        Shift the entity by (dx, dy). Return True on success, False if the spot
        is either occupied or beyond area bounds.
        """
        return self.place_entity(entity,
                                 entity.position[0] + dx,
                                 entity.position[1] + dy)

    #--------- monsters manipulation ---------#

    def hidden_monsters(self):
        """ Return a list of all hidden monsters. """
        return [m for m in self.monsters if m.hidden()]

    #--------- player manipulation ---------#

    def randomly_place_player(self, player):
        """
        Place the player at a random position.
        """
        while True:
            x = rand.randrange(self.width)
            y = rand.randrange(self.height)
            if self.place_entity(player, x, y):
                break


#--------- area generation from scratch ---------#


def area_from_scratch(gamedata, width, height):
    """ Generate an area from scratch. """
    res = Area(gamedata)
    res.width = width
    res.height = height
    return res

#--------- area generation from YAML dicts ---------#


def area_from_data(gamedata, yaml_dict):
    """ Generate an area from a YAML dict. """
    raise NotImplementedError
