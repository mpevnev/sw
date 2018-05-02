"""
Modifier module.

Provides Modifier class used to manipulate character's statistics and other
properties.

The class is supposed to be subclassed.
"""


import sw.const.message as msg
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
        self.attach_message = None
        self.dissipate_message = None
        self.duration = 0
        self.priority = 0
        self.tick_message = None

    def apply_skills(self, attached_to, state):
        """
        Apply changes to skills. 
        
        :param attached_to: a thing to apply the changes of this modifier to.
        :type attached_to: sw.modifiable.Modifiable
        :param state: a global environment.
        :type state: sw.gamestate.GameState
        """
        pass

    def apply_primary(self, attached_to, state):
        """
        Apply changes to the primary statistics.
        
        :param attached_to: a thing to apply the changes of this modifier to.
        :type attached_to: sw.modifiable.Modifiable
        :param state: a global environment.
        :type state: sw.gamestate.GameState
        """
        pass

    def apply_secondary(self, attached_to, state):
        """
        Apply changes to the secondary statistics.
        
        :param attached_to: a thing to apply the changes of this modifier to.
        :type attached_to: sw.modifiable.Modifiable
        :param state: a global environment.
        :type state: sw.gamestate.GameState
        """
        pass

    def expire(self, attached_to, state):
        """ Perform some actions on modifier's expiration. """
        pass

    def tick(self, attached_to, state):
        """ Apply periodic changes to the 'attached_to' modifiable. """
        pass


#--------- creating modifiers from recipes  ---------#


def modifier_from_recipe(recipe, other_data):
    """ Create a modifier from scratch. """
    cls = recipe[mod.TYPE]
    recipe_id = recipe[mod.ID]
    if cls == mod.ModifierType.FLAT_STAT_INCREASE.value:
        res = FlatStatIncrease(recipe_id)
        _read_common_fields_from_recipe(res, recipe)
        _read_flat_increase_fields_from_recipe(res, recipe)
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
        self.amount = 0
        self.which = None
        self.which_group = None

    def apply_primary(self, attached_to, state):
        if self.which_group == stat.StatGroup.PRIMARY:
            attached_to.total_primary[self.which] += self.amount

    def apply_secondary(self, attached_to, state):
        if self.which_group == stat.StatGroup.SECONDARY:
            attached_to.total_secondary[self.which] += self.amount

    def tick(self, attached_to, state):
        if self.duration > 0:
            self.duration -= 1
        if self.tick_message is not None:
            state.ui.message(self.tick_message, msg.Channel.MODIFIER_TICK)


#--------- helper things ---------#


def _read_common_fields_from_recipe(modifier, recipe):
    """ Read common fields from the recipe into the modifier. """
    modifier.attach_message = recipe.get(mod.ATTACH_MESSAGE, None)
    modifier.dissipate_message = recipe.get(mod.DISSIPATE_MESSAGE, None)
    modifier.duration = recipe.get(mod.DURATION, -1)
    modifier.priority = recipe.get(mod.PRIORITY, 0)
    modifier.tick_message = recipe.get(mod.TICK_MESSAGE, None)


def _read_flat_increase_fields_from_recipe(modifier, recipe):
    """ Read FlatStatIncrease fields from the recipe into the modifier. """
    modifier.amount = recipe[mod.FlatStatFields.HOW_MUCH.value]
    which = recipe[mod.FlatStatFields.WHICH.value]
    try:
        which = stat.PrimaryStat(which)
        modifier.which = which
        modifier.which_group = stat.StatGroup.PRIMARY
        return
    except ValueError:
        pass
    try:
        which = stat.SecondaryStat(which)
        modifier.which = which
        modifier.which_group = stat.StatGroup.SECONDARY
        return
    except ValueError:
        pass
    raise ValueError(f"Unknown statistics '{which}'")
