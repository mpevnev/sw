"""
Entity constants.
"""


class CollisionGroup(Enum):
    """
    An enum with collision groups. Two entities can collide only if their
    collision groups intersect.
    """

    FLYING = "flying"
    LIQUID = "liquid"
    NORMAL = "normal"
    WALL = "wall"
