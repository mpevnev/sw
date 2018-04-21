"""
Constants for the AI module.
"""


from enum import Enum


REMEMBERED_TASKS_NUM = 10


class Task(Enum):
    """ An AI task type. """

    ATTACK = "attack"
    CAST_SPELL = "cast"
    EXPLORE = "explore"
    FOLLOW = "follow"
    INVESTIGATE = "investigate"
    PURSUE = "pursue"
    REST = "rest"
    RETREAT = "retreat"
    STEP_ASIDE = "step aside"


class AIType(Enum):
    """ AI types. """

    MELEE_ZOMBIE = "melee zombie"
