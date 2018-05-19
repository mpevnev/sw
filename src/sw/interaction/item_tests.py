"""
Item tests interaction module.

This module provides several functions used to test if a certain interaction is
possible with a certain item by a certain character.
"""


from multipledispatch import dispatch


import sw.const.item as ci

import sw.character as c
import sw.gamestate as gs
import sw.item as i
import sw.monster as m
import sw.player as p


#--------- drink ---------#


@dispatch(c.Character, i.Item, gs.GameState)
def can_drink(character, item, state):
    """
    Test if a character can drink an item, generic version.

    :param character: who is doing the drinking part.
    :type character: sw.character.Character
    :param item: what is being drunk.
    :type item: sw.item.Item
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: True if the character can drink the item, False otherwise.
    :rtype: bool
    """
    return False


#--------- equip ---------#


@dispatch(c.Character, i.Item, gs.GameState)
def can_equip(character, item, state):
    """
    Test if an item can be equipped by a character.

    :param character: who is tested.
    :type character: sw.character.Character
    :param item: what is potentially being equipped.
    :type item: sw.item.Item
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: True if the item can be quipped, False otherwise.
    :rtype: bool
    """
    return False


@dispatch(c.Character, i.Equipable, gs.GameState)
def can_equip(character, item, state):
    """
    Test if an item can be equipped by a character.

    :param character: who is tested.
    :type character: sw.character.Character
    :param item: what is potentially being equipped.
    :type item: sw.item.Item
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: True if the item can be quipped, False otherwise.
    :rtype: bool
    """
    return True


#--------- read ---------#


@dispatch(c.Character, i.Item, gs.GameState)
def can_read(character, item, state):
    """
    Test if a character can read an item.

    :param character: who is reading.
    :type character: sw.character.Character
    :param item: what is being read.
    :type item: sw.item.Item
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: True if the character can read the item, False otherwise.
    :rtype: bool
    """
    return False


#--------- use ---------#


@dispatch(c.Character, i.Item, gs.GameState)
def can_use(character, item, state):
    """
    Test if a character can use an item.

    :param character: who is trying to use an item.
    :type character: sw.character.Character
    :param item: what is being used.
    :type item: sw.item.Item
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: True if the character can use the item, False otherwise.
    :rtype: bool
    """
    return True
