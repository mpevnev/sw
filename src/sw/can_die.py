"""
Can Die module.

Provides CanDie class, from which Character and Doodad inherit.
"""


class CanDie():
    """ A thing that can die or otherwise disappear. """

    def alive(self):
        """ Return True if the object is alive. """
        raise NotImplementedError

    def death_action(self, state, area):
        """ This method will be called when this object dies. """
        raise NotImplementedError

    def die(self):
        """ Mark this object as dead. """
        raise NotImplementedError
