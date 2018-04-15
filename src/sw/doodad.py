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
        Return True and do something when a monster uses the doodad.

        Return False without doing anything if the entity is not usable by the
        given monster.
        """
        raise NotImplementedError

    def use_by_player(self, player, state, area, ui):
        """
        Return True and do something when the player uses the doodad.

        Return False without doing anything if the entity is not usable by the
        player.
        """
        raise NotImplementedError

    #--------- death logic ---------#

    def alive(self):
        return not self.dead

    def death_action(self, state, area, ui):
        raise NotImplementedError

    def die(self):
        self.dead = True


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


#--------- doodad generation from recipes ---------#


def doodad_from_recipe(recipe):
    """ Create a doodad from a recipe (a YAML dict with no instance info). """
    recipe_id = recipe[const.ID]
    subtype = recipe[const.TYPE]
    if subtype == const.DoodadType.WALL.value:
        return Wall(recipe_id)
    raise ValueError(f"Unknown doodad type '{subtype}'")


#--------- doodad generation from saves ---------#


def doodad_from_save(save_dict):
    """ Create a doodad from a saved dict (a YAML dict with instance info). """
    raise NotImplementedError
