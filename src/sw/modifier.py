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

    def apply_primary(self, collector):
        """ Apply changes to the primary statistics. """
        raise NotImplementedError

    def apply_secondary(self, collector, primary):
        """ Apply changes to the secondary statistics. """
        raise NotImplementedError

    def apply_tertiary(self, collector, primary, secondary):
        """ Apply changes to the tertiary statistics. """
        raise NotImplementedError
