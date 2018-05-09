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
        self.blocks = set()
        self.blocked_by = set()

    #--------- collision logic ---------#

    def add_blocked_by(self, group):
        """
        Add a group that will block this entity.

        :param group: a collision group to be added.
        :type group: sw.const.entity.CollisionGroup
        """
        self.blocked_by.add(group)

    def add_blocks(self, group):
        """
        Add a group that this entity will block.

        :param group: a collision group to be added.
        :type group: sw.const.entity.CollisionGroup
        """
        self.blocks.add(group)

    def can_be_blocked_by(self, other):
        """
        Test if this entity can be blocked by another entity.

        :param Entity other: the other entity.

        :return: True if the entity can be blocked by the other, False
        otherwise.
        :rtype: bool
        """
        if self is other:
            return False
        return bool(self.blocked_by.intersection(other.blocks))

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

    def would_be_blocked_by(self, other, at_x, at_y):
        """
        Test whether the entity would be blocked by another if placed at a
        given position.

        :param Entity other: the other entity.
        :param int at_x: the X coordinate of the position to be tested.
        :param int at_y: the Y coordinate of the position to be tested.

        :return: True if the entity would collide with the other, False
        otherwise.
        :rtype: bool
        """
        if not self.can_be_blocked_by(other):
            return False
        if other.position is None:
            return False
        return (at_x, at_y) == other.position

    #--------- death logic ---------#

    def alive(self):
        """
        :return: True if the entity is alive, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError

    def death_action(self, state):
        """
        Do something when the entity dies.

        :param state: the global game environment of the entity.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def die(self):
        """ Mark this object as dead. """
        raise NotImplementedError

    #--------- other game logic ---------#

    def tick(self, state):
        """
        Process a single game turn.

        :param state: global game environment of the entity.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError
