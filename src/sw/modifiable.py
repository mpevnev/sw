"""
Modifiable module.

Provides Modifiable class for things that can have modifiers attached to them.
"""


from collections import deque
from itertools import chain


import sw.const.stat as stat
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
        """ Add innate modifiers to the character. """
        self.innate_modifiers.extend(modifiers)
        self._sorted_modifiers = None

    def add_temp_modifiers(self, *modifiers):
        """ Add temporary modifiers to the character. """
        self.temp_modifiers.extend(modifiers)
        self._sorted_modifiers = None

    def all_modifiers(self):
        """
        Return a list with all modifiers sorted by their priority.
        """
        if self._sorted_modifiers is not None:
            return self._sorted_modifiers
        res = sorted(chain(self.innate_modifiers, self.temp_modifiers),
                     key=lambda mod: mod.priority)
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
        """ Remove an innate modifier or several from the character. """
        for mod in modifiers:
            try:
                self.innate_modifiers.remove(mod)
                self._sorted_modifiers = None
            except ValueError:
                pass

    def remove_temp_modifiers(self, *modifiers):
        """ Remove a temporary modifier or several from the character. """
        for mod in modifiers:
            try:
                self.temp_modifiers.remove(mod)
                self._sorted_modifiers = None
            except ValueError:
                pass

    #--------- application of modifiers ---------#

    def update_totals(self):
        """ Update total statistics and skills of the character. """
        self._update_skill_totals()
        self._update_primary_totals()
        self._update_secondary_totals()
        self._update_tertiary_totals()

    def _update_skill_totals(self):
        new_skills = self.base_skills.copy()
        for mod in self.all_modifiers():
            mod.apply_skills(new_skills, self.base_skills)
        self.total_skills = new_skills

    def _update_primary_totals(self):
        new_primary = self.base_primary.copy()
        for mod in self.all_modifiers():
            mod.apply_primary(new_primary, self.base_skills, self.base_primary)
        self.total_stats[stat.StatGroup.PRIMARY] = new_primary

    def _update_secondary_totals(self):
        new_secondary = self.base_secondary.copy()
        for mod in self.all_modifiers():
            mod.apply_secondary(new_secondary, self.base_skills, self.total_primary)
        self.total_stats[stat.StatGroup.SECONDARY] = new_secondary

    def _update_tertiary_totals(self):
        new_tertiary = self.base_tertiary.copy()
        for mod in self.all_modifiers():
            mod.apply_tertiary(new_tertiary, self.base_skills, self.total_primary,
                               self.total_secondary)
        self.total_stats[stat.StatGroup.TERTIARY] = new_tertiary
