"""
Visibility constants.
"""


from enum import Enum


class VisibilityLevel(Enum):
    """ An enum with different kinds of location visibility. """

    NEVER_SEEN = 0
    SENSE_DOODADS = 1
    SENSE_ITEMS = 2
    SENSE_MONSTERS = 3
    VISIBLE = 4
