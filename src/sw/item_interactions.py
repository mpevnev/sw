"""
Item interaction module.

Provides functions to work with items.
"""


from multipledispatch import dispatch


import sw.const.item as citem

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
    :rtype: citem.PickUpError or bool
    """
    if character.free_inventory_slots(item.carrying_slot) == 0:
        return citem.PickUpError.NO_SLOTS
    character.add_item_to_inventory_slot(item)
    item.position = None
    return True


#--------- equipping ---------#


@dispatch(i.Item, c.Character, gs.GameState, bool)
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

    :return: True on success, an error code on failure.
    :rtype: citem.PickUpError or bool
    """
    if character.free_equipment_slots(item.wearing_slot) == 0:
        return citem.EquipError.NO_SLOTS
    if item.cursed and item.known_cursed and not force:
        return citem.EquipError.DANGEROUS
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
    :rtype: citem.DropError or bool
    """
    if character.hidden():
        return citem.DropError.HIDDEN
    if state.area is None and not force:
        return citem.DropError.WOULD_GET_DESTROYED
    pos = character.position
    for blocker in state.area.entities_at(*pos):
        if item.would_collide(blocker, *pos):
            return citem.DropError.COLLISION
    character.remove_item_from_slot(item)
    item.position = pos
    return True
