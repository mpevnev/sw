"""
Area module.

Provides Area class, a container of game entities.
"""


from collections import deque
from itertools import chain
import random as rand


import sw.const.area as const
from sw.doodad import doodad_from_recipe


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
        self.visibility_matrix = {}

    #--------- doodads manipulation ---------#

    def doodads_at(self, at_x, at_y, living_flag):
        """
        Return a list with all doodads with specified living flag at the given
        position.
        """
        return self.entities_at(at_x, at_y, living_flag,
                                ignore_doodads=False,
                                ignore_items=True,
                                ignore_monsters=True,
                                ignore_player=True)

    #--------- geometry ---------#

    def all_coordinates(self):
        """ Return a generator with all coordinate pairs in the area. """
        return ((x, y) for x in range(self.width) for y in range(self.height))

    def borders(self):
        """ Return a generator with all border points. """
        w = self.width
        h = self.height
        for x in range(1, w - 1):
            yield (x, 0)
            yield (x, h - 1)
        for y in range(h):
            yield (0, y)
            yield (w - 1, y)

    def contains_point(self, x, y):
        """ Return True if the given point is in the area. """
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def line(self, from_x, from_y, to_x, to_y):
        """
        Return a generator with all points between two given points, ends
        included.
        """
        # Uses DDA algorithm
        dx = to_x - from_x
        dy = to_y - from_y
        curx, cury = from_x, from_y
        n = max(abs(dx), abs(dy))
        last = (curx, cury)
        for _ in range(n):
            yield last
            curx += dx / n
            cury += dy / n
            last = (int(curx), int(cury))
        if last != (to_x, to_y):
            yield (to_x, to_y)

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

    def entities(self, living_flag, ignore_doodads=False, ignore_items=False,
                 ignore_monsters=False, ignore_player=False):
        """
        Return a list with all alive entities in the area if 'living_flag' is
        truthy, or a list with all dead entities if 'living_flag' is falsey.

        Optionally ignore entities of certain types.
        """
        everything = []
        if not ignore_player:
            everything = [self.player]
        if not ignore_doodads:
            everything = chain(everything, self.doodads)
        if not ignore_items:
            everything = chain(everything, self.items)
        if not ignore_monsters:
            everything = chain(everything, self.monsters)
        if living_flag:
            cond = lambda e: e is not None and e.alive()
        else:
            cond = lambda e: e is not None and not e.alive()
        return [e for e in everything if cond(e)]

    def entities_at(self, x, y, living_flag, ignore_doodads=False, ignore_items=False,
                    ignore_monsters=False, ignore_player=False):
        """
        Return a list with all alive entities at the given position if
        'living_flag' is truthy, or a list with all dead entities at the given
        position if 'living_flag' if falsey.

        Optionally filter away entities of certain types.
        """
        everything = []
        if not ignore_player:
            everything = [self.player]
        if not ignore_doodads:
            everything = chain(everything, self.doodads)
        if not ignore_items:
            everything = chain(everything, self.items)
        if not ignore_monsters:
            everything = chain(everything, self.monsters)
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

    #--------- items manipulation ---------#

    def items_at(self, at_x, at_y, living_flag):
        """
        Return a list with all items with specified living flag at the given
        position.
        """
        return self.entities_at(at_x, at_y, living_flag,
                                ignore_doodads=True,
                                ignore_items=False,
                                ignore_monsters=True,
                                ignore_player=True)

    #--------- monsters manipulation ---------#

    def hidden_monsters(self):
        """ Return a list of all hidden monsters. """
        return [m for m in self.monsters if m.hidden()]

    def monsters_at(self, at_x, at_y, living_flag):
        """
        Return a list with all monsters with specified living flag at the given
        position.
        """
        return self.entities_at(at_x, at_y, living_flag,
                                ignore_doodads=True,
                                ignore_items=True,
                                ignore_monsters=False,
                                ignore_player=True)

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

    #--------- visibility logic ---------#

    def can_see(self, character, x, y):
        """
        Return True if the given character can see the given point, False
        otherwise.
        """
        if not character.within_sight(x, y):
            return False
        origin_x, origin_y = character.position
        for cur in self.line(origin_x, origin_y, x, y):
            if cur == (x, y):
                break
            potential_blockers = self.entities_at(cur[0], cur[1], True)
            for blocker in potential_blockers:
                if not character.can_see_through(blocker):
                    return False
        return True

    def reset_visibility_matrix(self):
        """ Fill the entire visibility matrix with 'NEVER_SEEN' markers. """
        self.visibility_matrix = {(x, y): VisibilityInfo(const.VisibilityLevel.NEVER_SEEN)
                                  for (x, y) in self.all_coordinates()}

    def update_visibility_matrix(self, for_player):
        """
        Update the visibility matrix of this area as seen by the given player.
        """
        for (x, y), info in self.visibility_matrix.items():
            if self.can_see(for_player, x, y):
                info.levels = {const.VisibilityLevel.VISIBLE}
                info.remembered_doodads = self.entities_at(
                    x, y, True,
                    ignore_player=True, ignore_items=True, ignore_monsters=True)
                info.remembered_items = self.entities_at(
                    x, y, True,
                    ignore_player=True, ignore_doodads=True, ignore_monsters=True)
                info.remembered_monsters = self.entities_at(
                    x, y, True,
                    ignore_player=True, ignore_doodads=True, ignore_items=True)
            else:
                try:
                    info.levels.remove(const.VisibilityLevel.VISIBLE)
                except KeyError:
                    pass


#--------- helper classes ---------#


class VisibilityInfo():
    """
    A class containing remembered and sensed information about a position.
    """

    def __init__(self, base_level=None):
        if base_level is None:
            self.levels = {}
        else:
            self.levels = {base_level}
        self.remembered_doodads = []
        self.remembered_items = []
        self.remembered_monsters = []

    def never_seen(self):
        """ Return True if the point this info refers to was never seen. """
        return const.VisibilityLevel.NEVER_SEEN in self.levels

    def sense_doodads(self):
        """ Return True if the player can sense doodads in this point. """
        return const.VisibilityLevel.SENSE_DOODADS in self.levels

    def sense_items(self):
        """ Return True if the player can sense items in this point. """
        return const.VisibilityLevel.SENSE_ITEMS in self.levels

    def sense_monsters(self):
        """ Return True if the player can sense monsters in this point. """
        return const.VisibilityLevel.SENSE_MONSTERS in self.levels

    def visible(self):
        """ Return True if the point this info refers to is visible. """
        return const.VisibilityLevel.VISIBLE in self.levels


#--------- area generation from scratch ---------#


def area_from_scratch(gamedata, biome, width, height):
    """ Generate an area from scratch. """
    res = Area(gamedata)
    res.width = width
    res.height = height
    # TODO: proper area generation algorithm
    for x, y in res.borders():
        wall = doodad_from_recipe(gamedata.doodad_by_id("stone wall"))
        res.add_entity(wall, x, y)
    res.reset_visibility_matrix()
    return res

#--------- area generation from saved YAML dicts ---------#


def area_from_save(gamedata, yaml_dict):
    """ Generate an area from a saved YAML dict. """
    raise NotImplementedError
