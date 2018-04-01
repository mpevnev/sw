"""
Species module.

Provides Species class.
"""

import sw.const.species as const
import sw.modifier as mod


class Species():
    """
    Representation of a playable species with modifiers it applies to the
    player character.
    """

    def __init__(self, data):
        self.name = data[const.NAME]
        self.shortname = data[const.SHORTNAME]
        self.forbidden_backgrounds = data[const.FORBIDDEN_BACKGROUNDS]
        self.modifiers = [mod.modifier_from_data((d) for d in data[const.MODIFIERS]]
