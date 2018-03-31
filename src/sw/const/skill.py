"""
Skill contants module.
"""


from enum import Enum


class Skill(Enum):
    """ An enumeration for skill types. """

    DAGGER = "dagger"
    SWORD = "sword"
    AXE = "axe"
    MACE = "mace"
    STAFF = "staff"
    SPEAR = "spear"

    THROWING = "throwing"
    SLING = "sling"
    BOW = "bow"
    CROSSBOW = "crossbow"
    FIREARM = "firearm"

    STEALTH = "stealth"
    COOKING = "cooking"

    SPELLCASTING = "spellcasting"
    FIRE_MAGIC = "fire"
    WATER_MAGIC = "water"
    EARTH_MAGIC = "earth"
    AIR_MAGIC = "air"
    ARCANUM_MAGIC = "arcanum"
