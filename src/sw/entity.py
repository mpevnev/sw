"""
Entity module.

Provides Entity class from which Doodad and Character classes inherit.
"""


from enum import Enum


class Entity():
    """
    A thing that can occupy a position and collide with other entities, on one
    hand, and can die on the other.
    """

    def __init__(self):
        self.position = None
        self.collision_groups = set() 
        self.transparent = True

    #--------- collision logic ---------#

    def add_collision_group(self, group):
        """ Add a collision group to the entity. """
        self.collision_groups.add(group)

    def can_collide(self, other):
        """
        Return True if the entity can collide with the other, False otherwise.
        """
        if self is other:
            return False
        return bool(self.collision_groups.intersect(other.collision_groups))

    def collides(self, other):
        """ Return True if the entity collides with the other. """
        if not self.can_collide(other):
            return False
        if self.position is None or other.position is None:
            return False
        return self.position == other.position

    def hide(self):
        """ Put the entity into unplaced state, hidden from other entities. """
        self.position = None

    def hidden(self):
        """ Return True if the entity is hidden, False otherwise. """
        return self.position is None

    def would_collide(self, other, at_x, at_y):
        """
        Return True if the entity, when placed at the position given by 'at_x'
        and 'at_y', would collide with the other.
        """
        old = self.position
        self.position = (at_x, at_y)
        res = self.collides(other)
        self.position = old
        return res

    #--------- death logic ---------#

    def alive(self):
        """ Return True if the object is alive. """
        raise NotImplementedError

    def death_action(self, state, area):
        """ This method will be called when this object dies. """
        raise NotImplementedError

    def die(self):
        """ Mark this object as dead. """
        raise NotImplementedError
