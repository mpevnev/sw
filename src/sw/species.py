"""
Species module.

Provides Species class.
"""

import sw.misc as misc
import sw.modifier as mod

import sw.const.item as ci
import sw.const.species as const

class Species():
    """
    Representation of a playable species with modifiers it applies to the
    player character.
    """

    def __init__(self, data):
        """
        Initialize a species.

        :param dict data: a dict with species info.
        """
        self.id = data[const.ID]
        #
        self.base_stats = misc.convert_stat_dict(data[const.STATS])
        self.forbidden_backgrounds = data[const.FORBIDDEN_BACKGROUNDS]
        self.modifiers = [mod.modifier_from_recipe(d) for d in data[const.MODIFIERS]]
        self.name = data[const.NAME]
        self.shortname = data[const.SHORTNAME]
        self.slots = _read_slots(data[const.SLOTS])


#--------- helper things ---------#


def _read_slots(data):
    """
    Read distribution of equipment slots from a dictionary.

    :param dict data: a dictionary to read from.
    
    :return: a dictionary with empty slot lists of length read from the dict.
    :rtype: dict(sw.const.item.EquipmentSlot, list)
    """
    new_list = lambda length: list((0 for _ in range(length)))
    return {slot: new_list(data[slot.value]) for slot in ci.EquipmentSlot}
