"""
Player constants.
"""


from enum import Enum


AP_PER_WAIT = 10


class AttackError(Enum):
    """ An error that can happen when attacking. """

    DANGEROUS = "dangerous"
    FRIENDLY_TARGET = "friendly target"
    NO_AMMO = "no ammo"
    OBSCURED_BY_ALLY = "ally in the way"
    OUT_OF_RANGE = "out of range"
    USELESS = "useless"

    def __bool__(self):
        return False


class MoveError(Enum):
    """ An error that can happen when moving. """

    BLOCKED = "blocked"
    DANGEROUS = "dangerous"
    DEADLY = "deadly"

    def __bool__(self):
        return False
