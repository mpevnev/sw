"""
Monster-related constants.
"""


from enum import Enum


MONSTER_RECIPES_FILE = "monsters.yaml"
UNIQUES_RECIPES_FILE = "uniques.yaml"


class MonsterType(Enum):
    """ Monster types enum. """

    NORMAL_MELEE = "normal melee"


# Recipe and save dicts keys
ID = "id"
TYPE = "type"
XP_AWARD = "xp"
DEATH_MESSAGE = "death message"
SEE_THROUGH = "see through"
