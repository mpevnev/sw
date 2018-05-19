"""
Constants for modifier module.
"""

from enum import Enum

# Common fields - main
ID = "id"
TYPE = "type"

# Common fields - secondary
ATTACH_MESSAGE = "attach message"
DISSIPATE_MESSAGE = "dissipate message"
DURATION = "duration"
PRIORITY = "priority"
TICK_MESSAGE = "tick message"


# Types
class ModifierType(Enum):
    """ Type of a modifier, determining its behaviour. """

    FLAT_STAT_INCREASE = "flat stat"


# Fields for Flat type
class FlatStatFields(Enum):
    """ Keys into a YAML dict for FlatStatIncrease type. """

    WHICH_STAT = "which"
    HOW_MUCH = "amount"
