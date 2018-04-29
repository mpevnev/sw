"""
Entity module.

Provides Entity class from which Doodad and Character classes inherit.
"""


class Entity():
    """
    A thing that can occupy a position and collide with other entities, on one
    hand, and that can die on the other.
    """

    def __init__(self):
        self.position = None
        self.collision_groups = set()

    #--------- container logic ---------#

    def add_to_area(self, area):
        """
        Add this entity to a given area.

        :param area: an area to add this entity to.
        :type area: sw.area.Area
        """
        raise NotImplementedError

    def remove_from_area(self, area):
        """
        Remove this entity from a given area.
        
        :param area: an area from which the entity will be removed.
        :type area: sw.area.Area
        """
        raise NotImplementedError

    #--------- collision logic ---------#

    def add_collision_group(self, group):
        """
        Add a collision group to the entity.
        
        :param group: a collision group to be added.
        :type group: sw.const.entity.CollisionGroup
        """
        self.collision_groups.add(group)

    def can_collide(self, other):
        """
        Test if the entity can collide with an other entity.

        :param Entity other: the other entity.

        :return: True if the entity can collide with the other, False
        otherwise.
        :rtype: bool
        """
        if self is other:
            return False
        return bool(self.collision_groups.intersection(other.collision_groups))

    def collides(self, other):
        """
        Test if the entity collides with an other entity.

        :param Entity other: the other entity.

        :return: True if the entity collides with the other, False otherwise.
        :rtype: bool
        """
        if not self.can_collide(other):
            return False
        if self.position is None or other.position is None:
            return False
        return self.position == other.position

    def distance(self, other):
        """
        Calculate the Manhattan distance to an other entity.
        
        :param Entity other: an entity to which the distance will be
        calculated.

        :return: Manhattan distance to the other entity.
        :rtype: int
        """
        dx = self.position[0] - other.position[0]
        dy = self.position[1] - other.position[1]
        return max(abs(dx), abs(dy))

    def hide(self):
        """ Put the entity into unplaced state, hidden from other entities. """
        self.position = None

    def hidden(self):
        """
        :return: True True if the entity is hidden, False otherwise.
        :rtype: bool
        """
        return self.position is None

    def would_collide(self, other, at_x, at_y):
        """
        Test whether the entity would collide with another if placed at a given
        position.

        :param Entity other: the other entity.
        :param int at_x: the X coordinate of the position to be tested.
        :param int at_y: the Y coordinate of the position to be tested.

        :return: True if the entity would collide with the other, False
        otherwise.
        :rtype: bool
        """
        old = self.position
        self.position = (at_x, at_y)
        res = self.collides(other)
        self.position = old
        return res

    #--------- death logic ---------#

    def alive(self):
        """
        :return: True if the entity is alive, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError

    def death_action(self, state, area, ui):
        """
        Do something when the entity dies.
        
        :param state: the global game environment of the entity.
        :type state: sw.gamestate.GameState
        :param area: the area containing the entity.
        :type area: sw.area.Area
        :param ui: the UI piece that should react to the death of the entity.
        :type ui: sw.ui.MainDungeonWindow or None
        """
        raise NotImplementedError

    def die(self):
        """ Mark this object as dead. """
        raise NotImplementedError

    #--------- visibility logic ---------#

    def transparent_for_player(self, player):
        """
        Test if the entity is transparent for a player.

        :param player: a player being tested.
        :type player: sw.player.Player

        :return: True if the entity is transparent for the player, False
        otherwise.
        :rtype: bool
        """
        raise NotImplementedError

    def transparent_for_monster(self, monster):
        """
        Test if the entity is transparent for a monster.

        :param monster: a monster being tested.
        :type monster: sw.monster.Monster

        :return: True if the entity is transparent for the monster, False
        otherwise.
        :rtype: bool
        """
        raise NotImplementedError

    #--------- other game logic ---------#

    def tick(self, state, area, ui):
        """
        Process a single game turn.
        
        :param state: global game environment of the entity.
        :type state: sw.gamestate.GameState
        :param area: the area containing the entity.
        :type area: sw.area.Area
        :param ui: the UI that should react to whatever happens in this turn.
        :type ui: sw.ui.MainDungeonWindow
        """
        raise NotImplementedError
