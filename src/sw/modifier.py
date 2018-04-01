"""
Modifier module.

Provides Modifier class used to manipulate character's statistics and other
properties.

The class is supposed to be subclassed.
"""


import sw.const.modifier as mod


class Modifier():
    """
    A change in character's statistics and other properties.
    """

    def __init__(self, data):
        self.priority = data[PRIORITY]

    def apply_skills(self, apply_to, old_skills):
        """ Apply changes to the skills. """
        raise NotImplementedError

    def apply_primary(self, apply_to, skills, old_primary):
        """ Apply changes to the primary statistics. """
        raise NotImplementedError

    def apply_secondary(self, apply_to, skills, primary):
        """ Apply changes to the secondary statistics. """
        raise NotImplementedError

    def apply_tertiary(self, apply_to, skills, primary, secondary):
        """ Apply changes to the tertiary statistics. """
        raise NotImplementedError
