"""
Character statistics constants.
"""

from enum import Enum, auto


class StatGroup(Enum):
    """ Enumeration of statistics' groups. """

    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


class PrimaryStat(Enum):
    """ Enumeration of primary statistics. """

    STR = "strength"
    DEX = "dexterity"
    INT = "intelligence"
    SPI = "spirit"


class SecondaryStat(Enum):
    """ Enumeration of secondary statistics. """

    ARMOR = "armor"
    DAMAGE = "damage"
    DODGE = "dodge"
    HEALTH = "health"
    MAGIC_POWER = "magic power"
    RESIST = "resist"
    TO_HIT = "to hit"


class TertiaryStat(Enum):
    """ Enumeration of tertiary statistics. """

    HEALTH_REGEN = "health regen"
    MAGIC_REGEN = "magic regen"
    RESIST_AIR = "resist air"
    RESIST_ARCANUM = "resist arcanum"
    RESIST_EARTH = "resist earth"
    RESIST_FIRE = "resist fire"
    RESIST_WATER = "resist water"
