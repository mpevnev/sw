"""
Doodad module.

Provides base Doodad class and several subclasses.
"""


from sw.entity import Entity


#--------- base class ---------#


class Doodad(Entity):
    """
    Some passive or reactive game object - a wall, a water cell, whatever.
    """

    def __init__(self):
        super().__init__()
        self.detectable = True
        self.detected = True
        self.dead = False

    #--------- container logic ---------#

    def add_to_area(self, area):
        area.doodads.append(self)

    def remove_from_area(self, area):
        area.doodads.remove(self)

    #--------- generic usage by other entities ---------#

    def usable_by_monster(self, monster):
        """
        Return True if a given monster can use this object, False otherwise.
        """
        raise NotImplementedError

    def usable_by_player(self, player):
        """
        Return True if the player can use this object, False otherwise.
        """
        raise NotImplementedError

    #--------- death logic ---------#

    def alive(self):
        return not self.dead

    def death_action(self, state, area, ui):
        raise NotImplementedError

    def die(self):
        self.dead = True
