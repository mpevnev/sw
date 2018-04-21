"""
Constants for modifier module.
"""

from enum import Enum

# Modifier header info
ID = "id"
TYPE = "type"
PRIORITY = "priority"
DURATION = "duration"

# Types
class ModifierType(Enum):
    """ Type of a modifier, determining its behaviour. """

    FLAT_STAT_INCREASE = "flat stat"


# Fields for Flat type
class FlatStatFields(Enum):
    """ Keys into a YAML dict for FlatStatIncrease type. """

    WHICH_STAT = "which"
    HOW_MUCH = "amount"
