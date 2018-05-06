"""
Message constants.
"""


from enum import Enum, auto


class Channel(Enum):
    """ A message channel enumeration. """

    MODIFIER_TICK = "modtick"
    MONSTER_ATTACK = "monattack"
    MONSTER_DEATH = "mondeath"
    NORMAL = "normal"
    PLAYER_ATTACK = "player attack"
