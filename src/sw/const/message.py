"""
Message constants.
"""


from enum import Enum, auto


class Channel(Enum):
    """ A message channel enumeration. """

    NORMAL = auto()
    MONSTER_DEATH = auto()
