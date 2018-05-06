"""
Item constnats.
"""


from enum import Enum


#--------- reading from dicts - main things ---------#


class ItemType(Enum):
    """ An item type. """

    DAGGER = "dagger"

ID = "id"
TYPE = "type"


#--------- reading from dicts - generic fields ---------#


class WeaponField(Enum):
    """ A field of both ranged and melee weapons. """

    ACTION_POINT_COST = "ap cost"
    ARMOR_PENETRATION = "armor penetration"
    MIN_DAMAGE = "min damage"
    MAX_DAMAGE = "max damage"
    TO_HIT_BONUS = "to hit"


class MeleeWeaponField(Enum):
    """ A field of a melee weapon. """

    pass


class RangedWeaponField(Enum):
    """ A field of a ranged weapon. """

    AMMO_TYPES = "ammo"
    RANGE = "range"


#--------- reading from dicts - fields of concrete classes ---------#


class DaggerField(Enum):
    """ A field of a dagger-type weapon. """

    STABBING_DAMAGE_BONUS = "stab damage bonus"
    STABBING_TO_HIT_BONUS = "stab to hit bonus"


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


#--------- slots ---------#


class EquipmentSlot(Enum):
    """ A slot where equipped items are placed. """

    AMULET = "amulet"
    ARMOR = "armor"
    BOOTS = "boots"
    HAT = "hat"
    MELEE_WEAPON = "weapon"
    RANGED_WEAPON = "ranged weapon"
    RING = "ring"


class InventorySlot(Enum):
    """ A slot where unequipped items are stored. """

    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"
    HUGE = "huge"
