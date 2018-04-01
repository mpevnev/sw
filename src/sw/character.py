"""
Character module.

Provides base Character class that Monster and Player classes inherit from.
"""


from sw.modifiable import Modifiable


class Character(Modifiable):
    """ An active game entity. """

    def __init__(self, recipe):
        super().__init__()
