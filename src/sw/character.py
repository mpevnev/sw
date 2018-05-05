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

    def drop_item(self, item, state, force=False):
        """
        Drop an item.

        :param item: an item to be dropped.
        :type item: sw.item.Item
        :param state: a global environment which affects dropping the item.
        :type state: sw.gamestate.GameState
        :param bool force: if set to true, the item will be dropped even if
        it's dangerous.

        :return: True on success, an error code if something makes dropping the
        item dangerous or impossible.
        :rtype: bool or sw.const.item.DropError
        """
        res = item.drop(state, force)
        if not res:
            return res
        slot = item.carrying_slot
        relevant_list = self.inventory[slot]
        relevant_list[relevant_list.index(item)] = None
        item.position = item.owner.position
        item.owner = None
        return True

    def equip_item(self, item, state, force=False):
        """
        Equip an item.

        :param item: an item to equip.
        :type item: sw.item.Item
        :param state: a global environment that may affect equipping.
        :type state: sw.gamestate.GameState
        :param bool force: if set to true, the item will be equipped even if
        it's dangerous.

        :return: True on success, an error code if something makes equipping
        the item dangerous or impossible.
        :rtype: bool or sw.const.item.EquipError
        """
        if item.wearing_slot is None:
            return citem.EquipError.UNEQUIPABLE
        if item.cursed and item.visibly_cursed and not force:
            return citem.EquipError.VISIBLY_CURSED
        relevant_list = self.equipment[item.wearing_slot]
        try:
            index = relevant_list.index(None)
        except ValueError:
            return citem.EquipError.NO_SLOTS
        res = item.equip(state, force)
        if not res:
            return res
        relevant_list[index] = item
        remove_from_list = self.inventory[item.carrying_slot]
        remove_index = remove_from_list.index(item)
        remove_from_list[remove_index] = None
        return True

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
        num_items = len(filter(None, inv_list))
        num_slots = self.total_secondary[misc.slot_stat(slot_type)]
        return num_slots - num_items

    def pick_up_item(self, item, state, force=False):
        """
        Pick up an item.

        :param item: an item to pick up.
        :type item: sw.item.Item
        :param state: a global environment that may affect pick up.
        :type state: sw.gamestate.GameState
        :param bool force: if set to true, the item will be picked up even if
        it's dangerous.

        :return: True on success, an error code if something makes pick up
        dangerous or impossible.
        :rtype: bool or sw.const.item.PickUpError
        """
        inv_list = self.inventory[item.carrying_slot]
        if self.free_inventory_slots(item.carrying_slots) == 0:
            return citem.PickUpError.NO_SLOTS
        res = item.pick_up(self, state, force)
        if not res:
            return res
        item.owner = self
        item.position = None
        inv_list[inv_list.index(None)] = item
        return True

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

    #--------- container logic ---------#

    def add_to_area(self, area):
        raise NotImplementedError

    def remove_from_area(self, area):
        raise NotImplementedError

    #--------- death logic ---------#

    def alive(self):
        return self.health > 0

    def death_action(self, state):
        raise NotImplementedError

    def die(self):
        self.health = 0

    #--------- visibility logic ---------#

    def can_see_through(self, entity):
        """
        Test if a given entity is transparent for this character.

        :param entity: the entity to be tested.
        :type entity: sw.entity.Entity

        :return: True if the entity is transparent for this character, False
        otherwise.
        :rtype: bool
        """
        raise NotImplementedError

    def transparent_for_monster(self, monster):
        return True

    def transparent_for_player(self, player):
        return True

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
                inventory_list.extend([None] * (new_len - old_len))
