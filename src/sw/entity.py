"""
Entity module.

Provides Entity class from which Doodad and Character classes inherit.
"""


from enum import Enum


class Entity():
    """ A thing that can occupy a position and collide with other entities. """

    def __init__(self):
        self.position = None
        self.collision_groups = set() 
        self.transparent = True

    def add_collision_group(self, group):
        """ Add a collision group to the entity. """
        self.collision_groups.add(group)

    def can_collide(self, other):
        """
        Return True if the entity can collide with the other, False otherwise.
        """
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
