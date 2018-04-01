"""
Constants for modifier module.
"""

from enum import Enum

# Modifier header info
TYPE = "type"
PRIORITY = "priority"

# Types
class ModifierType(Enum):
    """ Type of a modifier, determining its behaviour. """

    FLAT_STAT_INCREASE = "flat"

# Fields for Flat type
class FlatStatFields(Enum):
    """ Keys into a YAML dict for FlatStatIncrease type. """
    WHICH = "which"
    HOW_MUCH = "amount"
