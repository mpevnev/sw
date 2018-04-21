"""
Modifier module.

Provides Modifier class used to manipulate character's statistics and other
properties.

The class is supposed to be subclassed.
"""


import sw.const.modifier as mod
import sw.const.skill as skill
import sw.const.stat as stat


#--------- base class ---------#


class Modifier():
    """
    A change in character's statistics and other properties.
    """

    def __init__(self, recipe_id):
        self.recipe_id = recipe_id
        self.priority = 0
        self.duration = 0

    def apply_skills(self, attached_to, state, area, ui):
        """ Apply changes to the skills. """
        pass

    def apply_primary(self, attached_to, state, area, ui):
        """ Apply changes to the primary statistics. """
        pass

    def apply_secondary(self, attached_to, state, area, ui):
        """ Apply changes to the secondary statistics. """
        pass

    def tick(self, attached_to, state, area, ui):
        """ Apply periodic changes to the 'attached_to' modifiable. """
        pass


#--------- creating modifiers from recipes  ---------#


def modifier_from_recipe(recipe, other_data):
    """ Create a modifier from scratch. """
    cls = recipe[mod.TYPE]
    recipe_id = recipe[mod.ID]
    if cls == mod.ModifierType.FLAT_STAT_INCREASE.value:
        res = FlatStatIncrease(recipe_id)
        _read_common_fields(res, recipe)
        return res
    raise ValueError(f"Unknown modifier type '{cls}'")


#--------- creating modifiers from saves ---------#


def modifier_from_save(save, data):
    """ Create a modifier from a save. """
    raise NotImplementedError


#--------- subclasses ---------#


class FlatStatIncrease(Modifier):
    """ Flat increase (or decrease) of statistics. """

    def __init__(self, recipe_id):
        super().__init__(recipe_id)
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
        raise ValueError(f"Unknown statistics '{which}'")

    def apply_primary(self, apply_to, overworld, area):
        if self.which_group == stat.StatGroup.PRIMARY:
            apply_to.total_primary[self.which] += self.amount

    def apply_secondary(self, apply_to, overworld, area):
        if self.which_group == stat.StatGroup.SECONDARY:
            apply_to.total_secondary[self.which] += self.amount


#--------- helper things ---------#


def _read_common_fields(modifier, recipe):
    """ Read common fields from a recipe into the modifier. """
    modifier.duration = recipe.get(mod.DURATION, -1)
    modifier.priority = recipe.get(mod.PRIORITY, 0)
