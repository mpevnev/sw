"""
Background module.

Provides Background class.
"""


import sw.const.background as const
import sw.modifier as mod


class Background():
    """
    A class representing a playable playground with modifiers it applies to the
    player character.
    """

    def __init__(self, data):
        self.name = data[const.NAME]
        self.shortname = data[const.SHORTNAME]
        self.modifiers = [mod.modifier_from_data(d) for d in data[const.MODIFIERS]]
