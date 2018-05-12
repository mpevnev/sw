"""
Constants for the AI module.
"""


from enum import Enum


REMEMBERED_TASKS_NUM = 10


class Task(Enum):
    """ An AI task type. """

    ATTACK = "attack"
    CARRY_ON = "carry on"
    CAST_SPELL = "cast"
    EXPLORE = "explore"
    FOLLOW = "follow"
    INVESTIGATE = "investigate"
    PURSUE = "pursue"
    REST = "rest"
    RETREAT = "retreat"
    STEP_ASIDE = "step aside"
    WAIT = "wait"


class AIType(Enum):
    """ AI types. """

    MELEE_ZOMBIE = "melee zombie"
