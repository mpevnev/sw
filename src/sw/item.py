"""
Item module.

Provides base Item class and several subclasses.
"""


from sw.const.entity import CollisionGroup
import sw.const.item as const
import sw.const.stat as stat
from sw.entity import Entity


#--------- base class ---------#


class Item(Entity):
    """ A thing that can be worn, picked up, dropped, used, etc... """

    def __init__(self, recipe_id):
        super().__init__()
        self.recipe_id = recipe_id
        self.carrying_slot = None
        self.cursed = False
        self.known_cursed = False
        self.owner = None
        self.wearing_slot = None
        self.add_collision_group(CollisionGroup.WALL)

    #--------- inherited stuff ---------#

    def add_to_area(self, area):
        area.items.append(self)

    def remove_from_area(self, area):
        area.items.remove(self)

    def transparent_for_player(self, player):
        return True

    def transparent_for_monster(self, monster):
        return True

    def tick(self, state):
        raise NotImplementedError

    #--------- interactions ---------#

    def drop(self, state, force=False):
        """
        Try to drop the item.

        :param state: a global state that might affect or get affected by the
        drop.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be dropped even if it
        would destroy it, otherwise a WOULD_GET_DESTROYED code will be returned
        in such circumstances.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.DropError
        """
        raise NotImplementedError

    def equip(self, state, force=False):
        """
        Try to equip the item.

        :param state: a global state that might affect or get affected by the
        donning.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be equipped even if
        is (visibly) cursed or has harmful properties.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.EquipError
        """
        raise NotImplementedError

    def pick_up(self, by, state, force=False):
        """
        Try to pick up the item.

        :param by: the character that picks up the item.
        :type by: sw.character.Character
        :param state: a global state that might affect or get affected by the
        pickup.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be picked up even if
        it's dangerous.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.PickUpError
        """
        raise NotImplementedError

    def use_on_doodad(self, target, state, force=False):
        """
        Try to use the item on a doodad.

        :param target: a target doodad.
        :type target: sw.doodad.Doodad
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_item(self, target, state, force=False):
        """
        Try to use the item on another item.

        :param target: a target item.
        :type target: Item
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_monster(self, target, state, force=False):
        """
        Try to use the item on a monster.

        :param target: a target monster.
        :type target: sw.monster.Monster
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_player(self, state, force=False):
        """
        Try to use the item on a player.

        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_position(self, x, y, state, force=False):
        """
        Try to use the item on a position.

        :param int x: X coordinate of the target position.
        :param int y: Y coordinate of the target position.
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    #--------- convenience things ---------#

    def slot_stat(self):
        """
        Return a secondary statistics governing how many slots are suited to
        hold this item.

        :return: the relevant *_SLOTS statistic.
        :rtype: sw.const.stat.SecondaryStat

        :raises ValueError: if the slot type is unknown.
        """
        if self.carrying_slot is const.InventorySlot.SMALL:
            return stat.SecondaryStat.SMALL_SLOTS
        if self.carrying_slot is const.InventorySlot.MEDIUM:
            return stat.SecondaryStat.MEDIUM_SLOTS
        if self.carrying_slot is const.InventorySlot.BIG:
            return stat.SecondaryStat.BIG_SLOTS
        if self.carrying_slot is const.InventorySlot.HUGE:
            return stat.SecondaryStat.HUGE_SLOTS
        raise ValueError(f"Unknown slot type '{self.carrying_slot}'")
