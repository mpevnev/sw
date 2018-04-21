"""
Character statistics constants.
"""

from enum import Enum, auto


class StatGroup(Enum):
    """ Enumeration of statistics' groups. """

    PRIMARY = "primary"
    SECONDARY = "secondary"


class PrimaryStat(Enum):
    """ Enumeration of primary statistics. """

    STR = "str"
    DEX = "dex"
    INT = "int"
    SPI = "spi"


class SecondaryStat(Enum):
    """ Enumeration of secondary statistics. """

    ARMOR = "armor"
    DAMAGE = "damage"
    DODGE = "dodge"
    TO_HIT = "to hit"

    HEALTH = "health"
    HEALTH_REGEN = "health regen"

    MAGIC_KNOWLEDGE = "magic knowledge"
    MAGIC_POWER = "magic power"
    MAGIC_REGEN = "magic regen"

    RESIST = "resist"
    RESIST_AIR = "resist air"
    RESIST_ARCANUM = "resist arcanum"
    RESIST_EARTH = "resist earth"
    RESIST_FIRE = "resist fire"
    RESIST_POISON = "resist poison"
    RESIST_WATER = "resist water"

    SIGHT = "sight"
