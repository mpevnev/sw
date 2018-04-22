"""
Species module.

Provides Species class.
"""

import sw.const.species as const
import sw.misc as misc
import sw.modifier as mod


class Species():
    """
    Representation of a playable species with modifiers it applies to the
    player character.
    """

    def __init__(self, data):
        self.id = data[const.ID]
        #
        self.base_stats = misc.convert_stat_dict(data[const.STATS])
        self.forbidden_backgrounds = data[const.FORBIDDEN_BACKGROUNDS]
        self.modifiers = [mod.modifier_from_recipe(d) for d in data[const.MODIFIERS]]
        self.name = data[const.NAME]
        self.shortname = data[const.SHORTNAME]
