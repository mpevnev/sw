"""
Monster-related constants.
"""


from enum import Enum


MONSTER_RECIPES_FILE = "monsters.yaml"
UNIQUES_RECIPES_FILE = "uniques.yaml"


class MonsterType(Enum):
    """ Monster types enum. """

    GENERIC = "generic"


# Recipe and save dicts keys
ID = "id"
TYPE = "type"
#
AI_TYPE = "ai"
DEATH_MESSAGE = "death message"
SEE_THROUGH = "see through"
SKILLS = "skills"
STATS = "stats"
XP_AWARD = "xp"
