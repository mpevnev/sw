"""
Message constants.
"""


from enum import Enum, auto


class Channel(Enum):
    """ A message channel enumeration. """

    MODIFIER_TICK = "modtick"
    MONSTER_DEATH = "mondeath"
    NORMAL = "normal"
