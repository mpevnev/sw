"""
Area module.

Provides Area class, a container of game entities.
"""


from collections import deque
from itertools import chain
import random as rand


import sw.const.area as const
from sw.doodad import doodad_from_recipe


#--------- parent classes ---------#


class HasDoodads():
    """ A container for doodads. """

    def __init__(self):
        self.doodads = deque()

    def all_doodads(self, living_flag):
        """
        Return a list with all doodads with specified living flag.

        :param bool living_flag: if set to true, only alive doodads will be
        included, otherwise only dead doodads will be.

        :return: a list with all doodads (including hidden) in the area.
        :rtype: list[sw.doodad.Doodad]
        """
        cond = lambda d: ((living_flag and d.alive())
                          or (not living_flag and not d.alive()))
        return [d for d in self.doodads if cond(d)]

    def doodads_at(self, at_x, at_y, living_flag):
        """
        Return a list with all doodads with specified living flag at the given
        position.

        :param int at_x: the X coordinate of the position to look for doodads
        at.
        :param int at_y: the Y coordinate of the position to look for doodads
        at.
        :param bool living_flag: if set to True, only alive doodads will be
        returned, otherwise only dead doodads will be returned.

        :return: a list of doodads at the given position.
        :rtype: list[sw.doodad.Doodad]
        """
        pos = (at_x, at_y)
        cond = lambda d: ((living_flag and d.alive())
                          or (not living_flag and not d.alive()))
        return [d for d in self.doodads if cond(d) and d.position == pos]

    def hidden_doodads(self):
        """
        :return: a list of hidden doodads.
        :rtype: list[sw.doodad.Doodad]
        """
        return [d for d in self.doodads if d.hidden()]


class HasItems():
    """ A container for items. """

    def __init__(self):
        self.items = deque()

    def all_items(self, living_flag):
        """
        Return a list with all items with specified living flag.

        :param bool living_flag: if set to true, only alive items will be
        included, otherwise only dead items will be.

        :return: a list with all items (including hidden) in the area.
        :rtype: list[sw.item.Item]
        """
        cond = lambda it: ((living_flag and it.alive())
                           or (not living_flag and not it.alive()))
        return [it for it in self.items if cond(it)]

    def hidden_items(self):
        """
        :return: a list with all hidden items.
        :rtype: list[sw.item.Item]
        """
        return [it for it in self.items if it.hidden()]

    def items_at(self, at_x, at_y, living_flag):
        """
        Return a list with all items with specified living flag at the given
        position.

        :param int at_x: the X coordinate of the position to look for items at.
        :param int at_y: the Y coordinate of the position to look for items at.
        :param bool living_flag: if set to True, only alive items will be
        returned, otherwise only dead items will be returned.

        :return: a list of items at the given position.
        :rtype: list[sw.item.Item]
        """
        cond = lambda it: ((living_flag and it.alive())
                           or (not living_flag and not it.alive()))
        pos = (at_x, at_y)
        return [it for it in self.items if cond(it) and it.position == pos]


class HasMonsters():
    """ A container for monsters. """

    def __init__(self):
        self.monsters = deque()

    def all_monsters(self, living_flag):
        """
        Return a list with all monsters with specified living flag.

        :param bool living_flag: if set to true, only alive monsters will be
        included, otherwise only dead monsters will be.

        :return: a list with all monsters (including hidden) in the area.
        :rtype: list[sw.monster.Monster]
        """
        cond = lambda m: ((living_flag and m.alive())
                          or (not living_flag and not m.alive()))
        return [m for m in self.monsters if cond(m)]

    def hidden_monsters(self):
        """
        Return a list of all hidden monsters.

        :return: a list of monsters.
        :rtype: list[sw.monster.Monster]
        """
        return [m for m in self.monsters if m.hidden()]

    def monsters_at(self, at_x, at_y, living_flag):
        """
        Return a list with all monsters with specified living flag at the given
        position.

        :param int at_x: the X coordinate of the position to look for monsters
        at.
        :param int at_y: the Y coordinate of the position to look for monsters
        at.
        :param bool living_flag: if set to True, only alive monsters will be
        returned, otherwise only dead monsters will be returned.

        :return: a list of monsters at the given position.
        :rtype: list[sw.monster.Monster]
        """
        pos = (at_x, at_y)
        cond = lambda m: ((living_flag and m.alive())
                          or (not living_flag and not m.alive()))
        return [m for m in self.monsters if cond(m) and m.position == pos]


#--------- main class ---------#


class Area(HasDoodads, HasItems, HasMonsters):
    """ A container of game entities and geometry driver. """

    def __init__(self, data):
        """
        Initialize an Area object.

        :param data: a game data object used to populate the area with things.
        :type data: sw.gamedata.GameData
        """
        HasDoodads.__init__(self)
        HasItems.__init__(self)
        HasMonsters.__init__(self)
        self.data = data
        self.width = None
        self.height = None
        self.player = None
        self.visibility_matrix = {}

    #--------- geometry ---------#

    def all_coordinates(self):
        """
        Iterate over all coordinate pairs in the area.

        :return: coordinate pairs
        :rtype: tuple(int, int)
        """
        return ((x, y) for x in range(self.width) for y in range(self.height))

    def borders(self):
        """
        Iterate over all coordinate pairs on the edges of the area.

        :return: coordinate pairs
        :rtype: tuple(int, int)
        """
        w = self.width
        h = self.height
        for x in range(1, w - 1):
            yield (x, 0)
            yield (x, h - 1)
        for y in range(h):
            yield (0, y)
            yield (w - 1, y)

    def contains_point(self, x, y):
        """
        Return True if the given point is in the area.

        :param int x: the X coordinate of the point being tested.
        :param int y: the Y coordinate of the point being tested.
        :return: True if the point is in the area, False otherwise.
        :rtype: bool
        """
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def line(self, from_x, from_y, to_x, to_y):
        """
        Iterate over coordinate pairs of points between two given points, ends
        included.

        :param int from_x: X coordinate of the starting point.
        :param int from_y: Y coordinate of the starting point.
        :param int to_x: X coordinate of the endpoint.
        :param int to_y: Y coordinate of the endpoint.

        :return: coordinate pairs.
        :rtype: tuple(int, int)
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

        :param entity: the entity to be added.
        :type entity: sw.entity.Entity
        :param int at_x: the X coordinate of the spot to add the entity to.
        :param int at_y: the Y coordinate of the spot to add the entity to.

        :return: True on success, False if the spot is occupied.
        :rtype: bool
        """
        if not self.place_entity(entity, at_x, at_y):
            return False
        entity.add_to_area(self)
        return True

    def entities(self, living_flag, ignore_doodads=False, ignore_items=False,
                 ignore_monsters=False, ignore_player=False):
        """
        Return a list with all entities in the area. Optionally ignore entities
        of certain types.

        :param bool living_flag: if set to true, only alive entities will be
        included in the list, otherwise only dead entities will be included.
        :param bool ignore_doodads: if set to true, doodads will not be
        included.
        :param bool ignore_items: if set to true, items will not be included.
        :param bool ignore_monsters: if set to true, monsters will not be
        included.
        :param bool ignore_player: if set to true, the player will not be
        included.

        :return: a list with entities from the area.
        :rtype: list(sw.entity.Entity)
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
        Return a list with all entities at the given position in the area.
        Optionally ignore entities of certain types.

        :param int x: the X coordinate of the position to look for entities at.
        :param int y: the Y coordinate of the position to look for entities at.
        :param bool living_flag: if set to true, only alive entities will be
        included in the list, otherwise only dead entities will be included.
        :param bool ignore_doodads: if set to true, doodads will not be
        included.
        :param bool ignore_items: if set to true, items will not be included.
        :param bool ignore_monsters: if set to true, monsters will not be
        included.
        :param bool ignore_player: if set to true, the player will not be
        included.

        :return: a list with entities at the given position from the area.
        :rtype: list(sw.entity.Entity)
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
        Place an entity at a given position.

        :param entity: the entity to be placed.
        :type entity: sw.entity.Entity
        :param int at_x: the X coordinate of the desired entity position.
        :param int at_y: the Y coordinate of the desired entity position.

        :return: True if the operation was successful, False if either the
        target point is outside area's bounds or if the entity would collide
        with something.
        :rtype: bool
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
        """
        Remove an entity from the area.

        :param entity: the entity to be removed.
        :type entity: sw.entity.Entity
        """
        entity.remove_from_area(self)

    def shift_entity(self, entity, dx, dy):
        """
        Move the entity relative to its current position.

        :param entity: the entity to be moved.
        :type entity: sw.entity.Entity
        :param int dx: the desired change in X coordinate.
        :param int dy: the desired change in Y coordinate.

        :return: True on success, False if placement has failed due to either
        the target point being out of the area's bounds or the spot being
        already occupied by something.
        """
        return self.place_entity(entity,
                                 entity.position[0] + dx,
                                 entity.position[1] + dy)

    #--------- player manipulation ---------#

    def randomly_place_player(self, player):
        """
        Place the player at a random position.

        :param player: the player character to be placed.
        :type player: sw.player.Player
        """
        x = rand.randrange(self.width)
        y = rand.randrange(self.height)
        while not self.place_entity(player, x, y):
            x = rand.randrange(self.width)
            y = rand.randrange(self.height)

    #--------- visibility logic ---------#

    def can_see(self, character, x, y):
        """
        Test if a character can see a given point.

        :param character: the character to be tested.
        :type character: sw.character.Character
        :param int x: the X coordinate of the point to be tested.
        :param int y: the Y coordinate of the point to be tested.

        :return: True if the character can see the point, False otherwise.
        :rtype: bool
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

    def update_visibility_matrix(self):
        """
        Update the visibility matrix of this area as seen by the given player.
        """
        for (x, y), info in self.visibility_matrix.items():
            if self.can_see(self.player, x, y):
                info.levels = {const.VisibilityLevel.VISIBLE}
                info.remembered_doodads = self.doodads_at(x, y, True)
                info.remembered_items = self.items_at(x, y, True)
                info.remembered_monsters = self.monsters_at(x, y, True)
            else:
                info.levels.discard(const.VisibilityLevel.VISIBLE)

    #--------- other game logic ---------#

    def ai_turn(self, state, ui, actions):
        """
        Make contained AI-controlled entities do something.

        :param state: game state to be modified by the active entities.
        :type state: sw.gamestate.GameState
        :param ui: the UI that should react to actions of the AI entities.
        :type ui: sw.ui.MainDungeonWindow
        :param int actions: the amount of action points to be added to the
        entities' action point pools.
        """
        for monster in self.all_monsters(True):
            if monster.hidden():
                continue
            monster.action_points += actions
            task = monster.ai.evaluate(monster, state, self)
            monster.perform_task(task, state, self, ui)

    def tick(self, state, ui, action_points_for_ai):
        """
        Process a single game turn.

        :param state: the global state of the game.
        :type state: sw.gamestate.GameState
        :param ui: the currently active UI piece.
        :param int action_points_for_ai: the amount of action points to be
        granted to the AI entities.
        """
        player = state.player
        for entity in self.entities(True, ignore_player=True):
            entity.tick(state, self, player, ui)
        for entity in self.entities(False, ignore_player=True):
            entity.death_action(state, self, ui)
        self.remove_dead_entities()
        self.ai_turn(state, ui, action_points_for_ai)


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
        """
        :return: True if the point this info refers to was never seen, False
        otherwise.
        :rtype: bool
        """
        return const.VisibilityLevel.NEVER_SEEN in self.levels

    def sense_doodads(self):
        """
        :return: True if the player can sense doodads in this point, False
        otherwise.
        :rtype: bool
        """
        return const.VisibilityLevel.SENSE_DOODADS in self.levels

    def sense_items(self):
        """
        :return: True if the player can sense items in this point, False
        otherwise.
        :rtype: bool
        """
        return const.VisibilityLevel.SENSE_ITEMS in self.levels

    def sense_monsters(self):
        """
        :return: True if the player can sense monsters in this point, False
        otherwise.
        :rtype: bool
        """
        return const.VisibilityLevel.SENSE_MONSTERS in self.levels

    def visible(self):
        """
        :return: True if the point this info refers to is visible, False
        otherwise.
        """
        return const.VisibilityLevel.VISIBLE in self.levels


#--------- area generation from scratch ---------#


def area_from_scratch(gamedata, biome, width, height):
    """
    Generate an area from scratch.

    :param gamedata: an object with game data used to populate the new area.
    :type gamedata: sw.gamedata.GameData
    :param biome: a biome for this area.
    :param int width: the width of the new area.
    :param int height: the height of the new area.

    :return: the freshly created area.
    :rtype: Area
    """
    res = Area(gamedata)
    res.width = width
    res.height = height
    # TODO: proper area generation algorithm
    for x, y in res.borders():
        wall = doodad_from_recipe(gamedata.doodad_recipe_by_id("stone wall"))
        res.add_entity(wall, x, y)
    res.reset_visibility_matrix()
    return res

#--------- area generation from saved YAML dicts ---------#


def area_from_save(gamedata, save):
    """
    Generate an area from a save.

    :param gamedata: an object with game data used to regenerate area's
    contents.
    :type gamedata: sw.gamedata.GameData
    :param dict save: a dictionary with the info about the area.
    """
    raise NotImplementedError
