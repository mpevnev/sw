"""
Monster module.

Provides base Monster class.
"""


from sw.character import Character


class Monster(Character):
    """ A monster or other NPC. """

    def __init__(self):
        super().__init__()

    def death_action(self, state, area, ui):
        raise NotImplementedError
