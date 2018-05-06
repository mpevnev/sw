"""
Item module.

Provides base Item class and several subclasses.
"""


from sw.entity import Entity

from sw.const.entity import CollisionGroup
import sw.const.item as const
from sw.const.skill import Skill


#--------- base class ---------#


class Item(Entity):
    """ A thing that can be worn, picked up, dropped, used, etc... """

    def __init__(self, recipe_id):
        super().__init__()
        self.recipe_id = recipe_id
        self.carrying_slot = None
        self.cursed = False
        self.known_cursed = False
        self.wearing_slot = None
        self.add_collision_group(CollisionGroup.WALL)

    #--------- inherited stuff ---------#

    def tick(self, state):
        pass


#--------- abstract subclasses ---------#


class Weapon(Item):
    """ A weapon, either melee or ranged. """

    def __init__(self, recipe_id):
        super().__init__(recipe_id)
        self.action_points_cost = None
        self.armor_penetration = None
        self.min_damage = None
        self.max_damage = None
        self.skill = None
        self.to_hit_bonus = None


#--------- concrete subclasses ---------#


class MeleeWeapon(Weapon):
    """ A generic melee weapon. """

    def __init__(self, recipe_id):
        super().__init__(recipe_id)
        self.wearing_slot = const.EquipmentSlot.MELEE_WEAPON


class RangedWeapon(Weapon):
    """ A generic ranged weapon. """

    def __init__(self, recipe_id):
        super().__init__(recipe_id)
        self.ammo_types = None
        self.range = None
        self.wearing_slot = const.EquipmentSlot.RANGED_WEAPON


#--------- reading ---------#


def item_from_recipe(recipe, other_game_data):
    """
    Create an item from a recipe.

    :param dict recipe: a recipe to base the item on.
    :param other_game_data: a game data instance used to populate the item with
    stuff.
    :type other_game_data: sw.gamedata.GameData

    :return: a freshly created item.
    :rtype: Item
    """
    item_id = recipe[const.ID]
    item_type = recipe[const.TYPE]
    if item_type == const.ItemType.GENERIC_MELEE.value:
        res = MeleeWeapon(item_id)
        read_generic_weapon_fields(res, recipe)
        return res
    if item_type == const.ItemType.GENERIC_RANGED.value:
        res = RangedWeapon(item_id)
        read_ranged_weapon_fields(res, recipe)
        return res
    raise ValueError(f"Unknown item type '{item_type}'")

#--------- reading helpers ---------#


def read_generic_weapon_fields(weapon, from_dict):
    """
    Read fields common for all weapons.

    :param Weapon weapon: read into this.
    :param dict from_dict: read from here.
    """
    weapon.action_points_cost = from_dict[const.WeaponField.ACTION_POINTS_COST.value]
    weapon.armor_penetration = from_dict.get(const.WeaponField.ARMOR_PENETRATION.value, 0)
    weapon.min_damage = from_dict[const.WeaponField.MIN_DAMAGE.value]
    weapon.max_damage = from_dict[const.WeaponField.MAX_DAMAGE.value]
    weapon.skill = Skill(from_dict[const.WeaponField.SKILL.value])
    weapon.to_hit_bonus = from_dict.get(const.WeaponField.TO_HIT_BONUS.value, 0)


def read_ranged_weapon_fields(weapon, from_dict):
    """
    Read ranged weapon's fields.

    :param RangedWeapon weapon: read into this.
    :param dict from_dict: read from here.
    """
    read_generic_weapon_fields(weapon, from_dict)
    weapon.ammo_types = from_dict[const.RangedWeaponField.AMMO_TYPES.value]
    weapon.range = from_dict[const.RangedWeaponField.RANGE.value]
