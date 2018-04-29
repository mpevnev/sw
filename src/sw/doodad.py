"""
Doodad module.

Provides base Doodad class and several subclasses.
"""


import sw.const.doodad as const
from sw.const.entity import CollisionGroup
from sw.entity import Entity


#--------- base class ---------#


class Doodad(Entity):
    """
    Some passive or reactive game object - a wall, a water cell, whatever.
    """

    def __init__(self, recipe_id):
        """
        Initialize a doodad.

        :param recipe_id: ID of the recipe from which this doodad is/was
        created.
        """
        super().__init__()
        self.recipe_id = recipe_id
        self.detectable = True
        self.detected = True
        self.dead = False

    #--------- container logic ---------#

    def add_to_area(self, area):
        area.doodads.append(self)

    def remove_from_area(self, area):
        area.doodads.remove(self)

    #--------- generic usage by other entities ---------#

    def use_by_monster(self, monster, state, area, ui):
        """
        React to a monster doing something with the doodad.

        :param monster: a monster attempting to use the doodad.
        :type monster: sw.monster.Monster
        :param state: global game environment.
        :type state: sw.gamestate.GameState
        :param area: the area containing both the monster and the doodad.
        :type area: sw.area.Area
        :param ui: the UI that should react to the event.
        :type ui: sw.ui.MainDungeonWindow

        :return: True if the monster used the doodad successfully, False if the
        doodad is not usable by the monster.
        :rtype: bool
        """
        raise NotImplementedError

    def use_by_player(self, player, state, area, ui):
        """
        React to a player doing something with the doodad.

        :param player: a player attempting to use the doodad.
        :type player: sw.player.Player
        :param state: global game environment.
        :type state: sw.gamestate.GameState
        :param area: the area containing both the player and the doodad.
        :type area: sw.area.Area
        :param ui: the UI that should react to the event.
        :type ui: sw.ui.MainDungeonWindow

        :return: True if the player used the doodad successfully, False if the
        doodad is not usable by the player.
        :rtype: bool
        """
        raise NotImplementedError

    #--------- death logic ---------#

    def alive(self):
        return not self.dead

    def death_action(self, state, area, ui):
        raise NotImplementedError

    def die(self):
        self.dead = True

    #--------- visibility logic ---------#

    def transparent_for_monster(self, monster):
        raise NotImplementedError

    def transparent_for_player(self, player):
        raise NotImplementedError

    #--------- other logic ---------#

    def tick(self, state, area, player, ui):
        pass


#--------- concrete subclasses ---------#


class Wall(Doodad):
    """ A base class for walls. """

    def __init__(self, recipe_id):
        super().__init__(recipe_id)
        self.add_collision_group(CollisionGroup.WALL)

    def use_by_monster(self, monster, state, area, ui):
        return False

    def use_by_player(self, player, state, area, ui):
        return False

    def death_action(self, state, area, ui):
        pass

    def transparent_for_monster(self, monster):
        return const.DoodadType.WALL in monster.see_through_types

    def transparent_for_player(self, player):
        return False


#--------- doodad generation from recipes ---------#


def doodad_from_recipe(recipe):
    """
    Create a doodad from a recipe.
    
    :param dict recipe: the template to base the new doodad on.
    
    :return: the freshly created doodad.
    :rtype: Doodad
    """
    recipe_id = recipe[const.ID]
    subtype = recipe[const.TYPE]
    if subtype == const.DoodadType.WALL.value:
        return Wall(recipe_id)
    raise ValueError(f"Unknown doodad type '{subtype}'")


#--------- doodad generation from saves ---------#


def doodad_from_save(save):
    """
    Create a doodad from a save.

    :param dict save: the saved information about the doodad.

    :return: the recreated doodad.
    :rtype: Doodad
    """
    raise NotImplementedError
