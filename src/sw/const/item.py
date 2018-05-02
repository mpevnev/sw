"""
Item constnats.
"""


from enum import Enum


#--------- error codes ---------#


class DropError(Enum):
    """ An error that can happen when an item is dropped. """

    COLLISION = "collision"
    HIDDEN = "hidden"
    WOULD_GET_DESTROYED = "would get destroyed"

    def __bool__(self):
        return False


class EquipError(Enum):
    """ An error that can happen when an item is equipped. """

    DANGEROUS = "dangerous"
    INCOMPATIBLE_BODY = "incompatible body"
    NO_SLOTS = "no slots"
    UNEQUIPABLE = "unequipable"
    VISIBLY_CURSED = "cursed"

    def __bool__(self):
        return False


class PickUpError(Enum):
    """ An error that can happen when an item is picked up. """

    DANGEROUS = "dangerous"
    NO_SLOTS = "no slots"
    TOO_HEAVY = "too heavy"

    def __bool__(self):
        return False


class TakeOffError(Enum):
    """ An error that can happen when an item is removed. """

    CURSED = "cursed"
    DANGEROUS = "dangerous"
    NO_SLOTS = "no slots"

    def __bool__(self):
        return False


class UseError(Enum):
    """ An error that can happen when an item is used. """

    DANGEROUS = "dangerous"
    NO_CHARGES = "no charges"
    USELESS = "useless"
    UNUSABLE = "unusable"
