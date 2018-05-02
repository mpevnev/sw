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
        self._sorted_modifiers = None

    #--------- modifiers manipulation ---------#

    def add_innate_modifiers(self, *modifiers):
        """
        Add innate modifiers to the modifiable.

        :param modifiers: modifiers to be added.
        """
        self.innate_modifiers.extend(modifiers)
        self._sorted_modifiers = None

    def add_temp_modifiers(self, *modifiers):
        """
        Add temporary modifiers to the modifiable.

        :param modifiers: modifiers to be added.
        """
        self.temp_modifiers.extend(modifiers)
        self._sorted_modifiers = None

    def all_modifiers(self):
        """
        :return: a list with all modifiers sorted by their priority.
        :rtype: list[sw.modifier.Modifier]
        """
        if self._sorted_modifiers is not None:
            return self._sorted_modifiers
        res = chain(sorted(self.innate_modifiers, key=lambda mod: mod.priority),
                    sorted(self.temp_modifiers, key=lambda mod: mod.priority))
        res = list(res)
        self._sorted_modifiers = res
        return res

    def clear_all_modifiers(self):
        """ Remove all modifiers. """
        self.innate_modifiers = deque()
        self.temp_modifiers = deque()
        self._sorted_modifiers = []

    def clear_innate_modifiers(self):
        """ Remove all innate modifiers. """
        self.innate_modifiers = deque()
        self._sorted_modifiers = None

    def clear_temp_modifiers(self):
        """ Remove all temporary modifiers. """
        self.temp_modifiers = deque()
        self._sorted_modifiers = None

    def remove_innate_modifiers(self, *modifiers):
        """
        Remove an innate modifier or several from the character.

        :param modifiers: modifiers to be removed.
        """
        for mod in modifiers:
            try:
                self.innate_modifiers.remove(mod)
                self._sorted_modifiers = None
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
                self._sorted_modifiers = None
            except ValueError:
                pass

    #--------- application of modifiers ---------#

    def update_totals(self, state, area):
        """
        Update total statistics and skills of the modifiable.

        :param state: the global game environment modifiers might factor in.
        :type state: sw.gamestate.GameState
        :param area: the area containing the modifiable.
        :type area: sw.area.Area
        """
        self._update_skill_totals(state, area)
        self._update_primary_totals(state, area)
        self._update_secondary_totals(state, area)

    def _update_skill_totals(self, state, area):
        self.total_skills = self.base_skills.copy()
        for mod in self.all_modifiers():
            mod.apply_skills(self, state, area)

    def _update_primary_totals(self, state, area):
        self.total_primary = self.base_primary.copy()
        for mod in self.all_modifiers():
            mod.apply_primary(self, state, area)

    def _update_secondary_totals(self, state, area):
        self.total_secondary = self.base_secondary.copy()
        for mod in self.all_modifiers():
            mod.apply_secondary(self, state, area)
