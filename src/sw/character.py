"""
Character module.

Provides base Character class that Monster and Player classes inherit from.
"""


from sw.skill import HasSkills
from sw.stat import HasStats


class Character(HasSkills, HasStats):
    """
    The base class in the hierarchy of active game entities.
    """

    def __init__(self, recipe):
        HasSkills.__init__(self)
        HasStats.__init__(self)
