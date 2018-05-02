"""
Item module.

Provides base Item class and several subclasses.
"""


from sw.const.entity import CollisionGroup
from sw.entity import Entity


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

    def add_to_area(self, area):
        area.items.append(self)

    def remove_from_area(self, area):
        area.items.remove(self)

    def transparent_for_player(self, player):
        return True

    def transparent_for_monster(self, monster):
        return True

    def tick(self, state, area, ui):
        raise NotImplementedError

    #--------- interactions ---------#

    def drop(self, by, state, area, ui, force=False):
        """
        Try to drop the item.

        :param by: the character that drops the item.
        :type by: sw.character.Character
        :param state: a global state that might affect or get affected by the
        drop.
        :type state: sw.gamestate.GameState
        :param area: an area from where the item is dropped to.
        :type area: sw.area.Area
        :param ui: a UI that should react to the drop.
        :param bool force: if set to True, the item will be dropped even if it
        would destroy it, otherwise a WOULD_GET_DESTROYED code will be returned
        in such circumstances.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.DropError
        """
        raise NotImplementedError

    def equip(self, by, state, area, ui, force=False):
        """
        Try to equip the item.

        :param by: the character that equips the item.
        :type by: sw.character.Character
        :param state: a global state that might affect or get affected by the
        donning.
        :type state: sw.gamestate.GameState
        :param area: an area where the character is.
        :type area: sw.area.Area
        :param ui: a UI that should react to the donning.
        :param bool force: if set to True, the item will be equipped even if
        is (visibly) cursed or has harmful properties.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.EquipError
        """
        raise NotImplementedError

    def pick_up(self, by, state, area, ui, force=False):
        """
        Try to pick up the item.

        :param by: the character that picks up the item.
        :type by: sw.character.Character
        :param state: a global state that might affect or get affected by the
        pickup.
        :type state: sw.gamestate.GameState
        :param area: an area from where the item is picked up.
        :type area: sw.area.Area
        :param ui: a UI that should react to the pickup.
        :param bool force: if set to True, the item will be picked up even if
        it's dangerous.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.PickUpError
        """
        raise NotImplementedError

    def use_on_doodad(self, by, target, state, area, ui, force=False):
        """
        Try to use the item on a doodad.

        :param by: the character that uses the item.
        :type by: sw.character.Character
        :param target: a target doodad.
        :type target: Item
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param area: an area where the target and the user are.
        :type area: sw.area.Area
        :param ui: a UI that should react to the use.
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_item(self, by, target, state, area, ui, force=False):
        """
        Try to use the item on another item.

        :param by: the character that uses the item.
        :type by: sw.character.Character
        :param target: a target item.
        :type target: Item
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param area: an area where the target and the user are.
        :type area: sw.area.Area
        :param ui: a UI that should react to the use.
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_monster(self, by, target, state, area, ui, force=False):
        """
        Try to use the item on a monster.

        :param by: the character that uses the item.
        :type by: sw.character.Character
        :param target: a target monster.
        :type target: Item
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param area: an area where the target and the user are.
        :type area: sw.area.Area
        :param ui: a UI that should react to the use.
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_player(self, by, state, area, ui, force=False):
        """
        Try to use the item on a player.

        :param by: the character that uses the item.
        :type by: sw.character.Character
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param area: an area where the target and the user are.
        :type area: sw.area.Area
        :param ui: a UI that should react to the use.
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError

    def use_on_position(self, by, x, y, state, area, ui, force=False):
        """
        Try to use the item on a position.

        :param by: the character that uses the item.
        :type by: sw.character.Character
        :param int x: X coordinate of the target position.
        :param int y: Y coordinate of the target position.
        :param state: a global state that might affect or get affected by the
        use.
        :type state: sw.gamestate.GameState
        :param area: an area where the target and the user are.
        :type area: sw.area.Area
        :param ui: a UI that should react to the use.
        :param bool force: if set to True, the item will be used even if it's
        dangerous or useless.

        :return: True on success, an error code (which all are considered
        False) otherwise.
        :rtype: bool or sw.const.item.UseError
        """
        raise NotImplementedError
