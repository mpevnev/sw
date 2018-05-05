"""
Modifiable module.

Provides Modifiable class for things that can have modifiers attached to them.
"""


from collections import deque
from itertools import chain


from sw.skill import HasSkills
from sw.stat import HasStats


class Modifiable(HasSkills, HasStats):
    """
    A class for things that can have modifiers attached to them.
    """

    def __init__(self):
        HasSkills.__init__(self)
        HasStats.__init__(self)
        self.innate_modifiers = deque()
        self.temp_modifiers = deque()

    #--------- modifiers manipulation ---------#

    def add_innate_modifiers(self, *modifiers):
        """
        Add innate modifiers to the modifiable.

        :param modifiers: modifiers to be added.
        """
        self.innate_modifiers.extend(modifiers)

    def add_temp_modifiers(self, *modifiers):
        """
        Add temporary modifiers to the modifiable.

        :param modifiers: modifiers to be added.
        """
        self.temp_modifiers.extend(modifiers)

    def clear_all_modifiers(self):
        """ Remove all modifiers. """
        self.innate_modifiers = deque()
        self.temp_modifiers = deque()

    def clear_innate_modifiers(self):
        """ Remove all innate modifiers. """
        self.innate_modifiers = deque()

    def clear_temp_modifiers(self):
        """ Remove all temporary modifiers. """
        self.temp_modifiers = deque()

    def remove_innate_modifiers(self, *modifiers):
        """
        Remove an innate modifier or several from the character.

        :param modifiers: modifiers to be removed.
        """
        for mod in modifiers:
            try:
                self.innate_modifiers.remove(mod)
            except ValueError:
                pass

    def remove_temp_modifiers(self, *modifiers):
        """
        Remove a temporary modifier or several from the character.

        :param modifiers: modifiers to be removed.
        """
        for mod in modifiers:
            try:
                self.temp_modifiers.remove(mod)
            except ValueError:
                pass

    def sort_modifiers(self):
        """ Sort modifier deques. """
        self.innate_modifiers = deque(sorted(self.innate_modifiers, lambda m: m.priority))
        self.temp_modifiers = deque(sorted(self.temp_modifiers, lambda m: m.priority))

    #--------- application of modifiers ---------#

    def update_totals(self, state):
        """
        Update total statistics and skills of the modifiable.

        :param state: the global game environment modifiers might factor in.
        :type state: sw.gamestate.GameState
        """
        self.sort_modifiers()
        self._update_skill_totals(state)
        self._update_primary_totals(state)
        self._update_secondary_totals(state)

    def _update_skill_totals(self, state):
        self.total_skills = self.base_skills.copy()
        for mod in chain(self.innate_modifiers, self.temp_modifiers):
            mod.apply_skills(self, state)

    def _update_primary_totals(self, state):
        self.total_primary = self.base_primary.copy()
        for mod in chain(self.innate_modifiers, self.temp_modifiers):
            mod.apply_primary(self, state)

    def _update_secondary_totals(self, state):
        self.total_secondary = self.base_secondary.copy()
        for mod in chain(self.innate_modifiers, self.temp_modifiers):
            mod.apply_secondary(self, state)
