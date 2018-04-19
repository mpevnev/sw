"""
Entity constants.
"""


from enum import Enum


class CollisionGroup(Enum):
    """
    An enum with collision groups. Two entities can collide only if their
    collision groups intersect.
    """

    LIQUID = "liquid"
    CHARACTER = "character"
    WALL = "wall"
