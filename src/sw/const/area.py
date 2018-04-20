"""
Area constants.
"""


from enum import Enum


class ArcanumLevel(Enum):
    """ An enumeration of levels of area's arcanum corruption. """

    ZERO = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    COMPLETE = 4


class HostilityLevel(Enum):
    """ An enumeration of area's hostility level. """

    SAFE = 0
    WILD = 1
    DANGEROUS = 2
    WAR_ZONE = 3
    DEEP_ARCANUM = 4


class VisibilityLevel(Enum):
    """ An enum with different kinds of location visibility. """

    NEVER_SEEN = 0
    SENSE_DOODADS = 1
    SENSE_ITEMS = 2
    SENSE_MONSTERS = 3
    VISIBLE = 4
