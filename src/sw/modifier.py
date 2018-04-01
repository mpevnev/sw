"""
Modifier module.

Provides Modifier class used to manipulate character's statistics and other
properties.

The class is supposed to be subclassed.
"""


import sw.const.modifier as mod
import sw.const.skill as skill
import sw.const.stat as stat


#--------- main things ---------#


class Modifier():
    """
    A change in character's statistics and other properties.
    """

    def __init__(self, data):
        self.priority = data[mod.PRIORITY]

    def apply_skills(self, apply_to, old_skills):
        """ Apply changes to the skills. """
        pass

    def apply_primary(self, apply_to, skills, old_primary):
        """ Apply changes to the primary statistics. """
        pass

    def apply_secondary(self, apply_to, skills, primary):
        """ Apply changes to the secondary statistics. """
        pass

    def apply_tertiary(self, apply_to, skills, primary, secondary):
        """ Apply changes to the tertiary statistics. """
        pass


def modifier_from_data(data):
    """ Create a modifier with its class determined by the supplied data. """
    cls = data[mod.TYPE]
    if cls == mod.ModifierType.FLAT_STAT_INCREASE.value:
        return FlatStatIncrease(data)
    raise ValueError(f"Unknown modifier type '{cls}'")


#--------- subclasses ---------#


class FlatStatIncrease(Modifier):
    """ Flat increase (or decrease) of statistics. """

    def __init__(self, data):
        super().__init__(data)
        self.amount = data[mod.FlatStatFields.HOW_MUCH.value]
        which = data[mod.FlatStatFields.WHICH.value]
        try:
            which = stat.PrimaryStat(which)
            self.which = which
            self.which_group = stat.StatGroup.PRIMARY
            return
        except ValueError:
            pass
        try:
            which = stat.SecondaryStat(which)
            self.which = which
            self.which_group = stat.StatGroup.SECONDARY
            return
        except ValueError:
            pass
        try:
            which = stat.TertiaryStat(which)
            self.which = which
            self.which_group = stat.StatGroup.TERTIARY
            return
        except ValueError:
            pass
        raise ValueError(f"Unknown statistics '{which}'")

    def apply_primary(self, apply_to, skills, old_primary):
        if self.which_group == stat.StatGroup.PRIMARY:
            apply_to[self.which] += self.amount

    def apply_secondary(self, apply_to, skills, primary):
        if self.which_group == stat.StatGroup.SECONDARY:
            apply_to[self.which] += self.amount

    def apply_tertiary(self, apply_to, skills, primary, secondary):
        if self.which_group == stat.StatGroup.TERTIARY:
            apply_to[self.which] += self.amount
