"""
Entity constants.
"""


from enum import Enum


class EntityClass(Enum):
    """ An enum with entity classes. """

    DOODAD = "doodad"
    ITEM = "item"
    MONSTER = "monster"
    PLAYER = "player"


class CollisionGroup(Enum):
    """
    An enum with collision groups. Two entities can collide only if their
    collision groups intersect.
    """

    FLYING = "flying"
    LIQUID = "liquid"
    NORMAL = "normal"
    WALL = "wall"
