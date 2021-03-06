"""
Item interaction module.

Provides functions to work with items.
"""


from multipledispatch import dispatch


import sw.const.item as ci

import sw.character as c
import sw.doodad as d
import sw.gamestate as gs
import sw.item as i
import sw.monster as m
import sw.player as p


#--------- picking up ---------#


@dispatch(i.Item, c.Character, gs.GameState, bool)
def pick_up_item(item, character, state, force):
    """
    Pick up an item, generic version.

    :param item: an item to pick up.
    :type item: sw.item.Item
    :param character: a character to do the picking up.
    :type character: sw.character.Character
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    :param bool force: if set to True, pick up the item if it's dangerous.

    :return: True on success, an error code on failure.
    :rtype: sw.const.item.PickUpError or bool
    """
    if character.free_inventory_slots(item.carrying_slot) == 0:
        return ci.PickUpError.NO_SLOTS
    character.add_item_to_inventory_slot(item)
    item.hide()
    return True


#--------- equipping ---------#


@dispatch(i.Item, c.Character, gs.GameState, bool)
def equip_item(item, character, state, force):
    """
    Try to equip an unequipable item.

    :param item: an item to equip.
    :type item: sw.item.Equipable
    :param character: a character to do the equipping.
    :type character: sw.character.Character
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    :param bool force: if set to True, equip the item if it's dangerous.

    :return: always EquipError.UNEQUIPABLE
    :rtype: sw.const.item.EquipError
    """
    return ci.EquipError.UNEQUIPABLE


@dispatch(i.Equipable, c.Character, gs.GameState, bool)
def equip_item(item, character, state, force):
    """
    Equip an item, generic version.

    :param item: an item to equip.
    :type item: sw.item.Item
    :param character: a character to do the equipping.
    :type character: sw.character.Character
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    :param bool force: if set to True, equip the item if it's dangerous.

    :return: True on success, an error code on failure
    :rtype: bool or sw.const.item.EquipError
    """
    if character.free_equipment_slots(item.wearing_slot) == 0:
        return ci.EquipError.NO_SLOTS
    if item.cursed and item.known_cursed and not force:
        return ci.EquipError.VISIBLY_CURSED
    character.add_item_to_equipment_slot(item)
    return True


#--------- dropping ---------#


@dispatch(i.Item, c.Character, gs.GameState, bool)
def drop_item(item, character, state, force):
    """
    Drop an item, generic version.

    :param item: an item to drop.
    :type item: sw.item.Item
    :param character: a character to drop the item.
    :type character: sw.character.Character
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    :param bool force: if set to True, drop the item even if it's dangerous.

    :return: True on success, an error code on failure.
    :rtype: sw.const.item.DropError or bool
    """
    if character.hidden():
        return ci.DropError.HIDDEN
    if state.area is None and not force:
        return ci.DropError.WOULD_GET_DESTROYED
    pos = character.position
    for blocker in state.area.entities_at(*pos):
        if item.would_be_blocked_by(blocker, *pos):
            return ci.DropError.COLLISION
    character.remove_item_from_slot(item)
    item.position = pos
    return True


#--------- unequipping ---------#


@dispatch(i.Equipable, c.Character, gs.GameState, bool)
def take_item_off(item, character, state, force):
    """
    Take off an item, generic version.

    :param item: an item to take off.
    :type item: sw.item.Equipable
    :param character: a character to take off the item.
    :type character: sw.character.Character
    :param state: a global environment
    :type state: sw.gamestate.GameState
    :param bool force: take off the item even if it's dangerous.

    :return True on success, an error code on failure.
    :rtype: bool or sw.const.item.TakeOffError
    """
    if item.cursed:
        return ci.TakeOffError.CURSED
    has_free_slots = character.free_inventory_slots(item.carrying_slot) > 0
    if not has_free_slots:
        return ci.TakeOffError.NO_SLOTS
    character.remove_item_from_slot(item)
    character.add_item_to_inventory_slot(item)
    return True

