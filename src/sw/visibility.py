"""
Visibility module.

Provides is_transparent function and VisibilityInfo class.
"""


from multipledispatch import dispatch


import sw.character as char
import sw.const.visibility as const
import sw.doodad as doodad
import sw.entity as entity
import sw.monster as monster
import sw.player as player


#--------- generic interactions ---------#


@dispatch(entity.Entity, entity.Entity)
def is_transparent(what, to_what):
    """
    :return: True if a given entity is transparent for another entity, False
    otherwise.
    :rtype: bool
    """
    return True


@dispatch(doodad.Wall, entity.Entity)
def is_transparent(wall, to_what):
    """
    :return: True if a given wall is transparent to a given entity, False
    otherwise.
    :rtype: bool
    """
    return wall.transparent


#--------- visibility info class ---------#


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
