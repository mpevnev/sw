"""
Character module.

Provides base Character class that Monster and Player classes inherit from.
"""


from collections import deque


import sw.const.item as citem
import sw.const.stat as stat
from sw.entity import Entity
import sw.misc as misc
from sw.modifiable import Modifiable


class Character(Entity, Modifiable):
    """ An active game entity. """

    def __init__(self):
        Entity.__init__(self)
        Modifiable.__init__(self)
        self._health = 0
        self.equipment = misc.empty_equipment_dict()
        self.inventory = misc.empty_inventory_dict()

    #--------- item logic ---------#

    def add_item_to_equipment_slot(self, item):
        """
        Add an item to its equipment slot.

        :param item: an item to add.
        :type item: sw.item.Item

        :raises ValueError: if there is no free slot.
        """
        equip_list = self.equipment[item.wearing_slot]
        index = equip_list.index(None)
        equip_list[index] = item

    def add_item_to_inventory_slot(self, item):
        """
        Add an item to an inventory slot of relevant type.

        :param item: an item to add.
        :type item: sw.item.Item

        :raises ValueError: if there is no free slot.
        """
        inv_list = self.inventory[item.carrying_slot]
        index = inv_list.index(None)
        inv_list[index] = item

    def armor(self):
        """
        :return: a list of worn armor.
        :rtype: list[sw.item.Armor]
        """
        return self.equipment[citem.EquipmentSlot.ARMOR]

    def free_equipment_slots(self, slot_type):
        """
        :param slot_type: slot type to get the number of slots of.
        :type slot_type: sw.const.item.EquipmentSlot

        :return: the number of free slots of a given type for equipment.
        :rtype: int
        """
        equip_list = self.equipment[slot_type]
        return equip_list.count(None)

    def free_inventory_slots(self, slot_type):
        """
        :param slot_type: slot type to get the number of slots of.
        :type slot_type: sw.const.item.InventorySlot

        :return: the number of free slots of a given type in the inventory.
        :rtype: int
        """
        inv_list = self.inventory[slot_type]
        num_items = len(list(filter(None, inv_list)))
        num_slots = self.total_secondary[misc.slot_stat(slot_type)]
        return num_slots - num_items

    def has_melee_weapon_equipped(self):
        """
        :return: True if the character wields a melee weapon, False otherwise.
        :rtype: bool
        """
        return any(map(lambda i: i is not None, self.melee_weapons()))

    def has_ranged_weapon_equipped(self):
        """
        :return: True if the character wields a ranged weapon, False otherwise.
        :rtype: bool
        """
        return any(map(lambda i: i is not None, self.ranged_weapons()))

    def melee_weapons(self):
        """
        :return: a list of wielded melee weapons.
        :rtype: list[sw.item.MeleeWeapon]
        """
        return self.equipment[citem.EquipmentSlot.MELEE_WEAPON]

    def ranged_weapons(self):
        """
        :return: a list of wielded ranged weapons.
        :rtype: list[sw.item.RangedWeapon]
        """
        return self.equipment[citem.EquipmentSlot.RANGED_WEAPON]

    def remove_item_from_slot(self, item):
        """
        Remove an item from its slot either in inventory or equipment.

        :param item: an item to remove.
        :type item: sw.item.Item
        """
        try:
            self.inventory[self.inventory.index(item)] = None
            return
        except ValueError:
            pass
        try:
            self.equipment[self.equipment.index(item)] = None
            return
        except ValueError:
            pass

    #--------- health logic ---------#

    @property
    def max_health(self):
        """
        :return: the maximum health of the character.
        :rtype: float
        """
        return self.total_secondary[stat.SecondaryStat.HEALTH]

    @property
    def health(self):
        """
        :return: the health of the character.
        :rtype: float
        """
        return self._health

    @health.setter
    def health(self, value):
        """
        Set the health of the character.

        :param float value: new value for the health.
        """
        value = max(0, value)
        value = min(value, self.max_health)
        self._health = value

    #--------- death logic ---------#

    def alive(self):
        return self.health > 0

    def death_action(self, state):
        raise NotImplementedError

    def die(self):
        self.health = 0

    #--------- other logic ---------#

    def tick(self, state):
        self.update_totals(state)
        for mod in self.innate_modifiers:
            mod.tick(self, state)
        remaining_mods = deque()
        for mod in self.temp_modifiers:
            mod.tick(self, state)
            if mod.duration == 0:
                mod.expire(self, state)
            else:
                remaining_mods.append(mod)
        self.temp_modifiers = remaining_mods

    def update_totals(self, state):
        super().update_totals(state)
        for slot_type in citem.InventorySlot:
            inventory_list = self.inventory[slot_type]
            old_len = len(inventory_list)
            new_len = self.total_secondary[misc.slot_stat(slot_type)]
            if new_len > old_len:
                inventory_list.extend((None for _ in range(new_len - old_len)))

    def within_sight(self, x, y):
        """
        Test if a given position is withing character's line of sight.

        :param int x: the X coordinate of the position being tested.
        :param int y: the Y coordinate of the position being tested.

        :return: True if the given position is within character's line of
        sight, False otherwise.
        :rtype: bool
        """
        sight_range = self.total_secondary[stat.SecondaryStat.SIGHT]
        own_x, own_y = self.position
        return (own_x - sight_range <= x <= own_x + sight_range and
                own_y - sight_range <= y <= own_y + sight_range)
