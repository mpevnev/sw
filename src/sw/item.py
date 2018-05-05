"""
Item module.

Provides base Item class and several subclasses.
"""


from sw.const.entity import CollisionGroup
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
        self.wearing_slot = None
        self.add_collision_group(CollisionGroup.WALL)

    #--------- inherited stuff ---------#

    def tick(self, state):
        raise NotImplementedError
