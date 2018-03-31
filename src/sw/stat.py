"""
Statistics module.

Provides HasStats class for things that can have statistics and modifiers to
them.
"""


from collections import deque
from itertools import chain


import sw.const.modifier as modconst
import sw.const.stat as stat


#--------- main class ---------#

class HasStats():
    """
    A class for things that have statistics and can have modifiers to them.
    """

    def __init__(self):
        self.base_stats = empty_stat_dict()
        self.total_stats = empty_stat_dict()
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

    #--------- statistics manipulation ---------#

    @property
    def base_primary(self):
        """ Return base primary statistics. """
        return self.base_stats[stat.StatGroup.PRIMARY]

    @property
    def base_secondary(self):
        """ Return base secondary statistics. """
        return self.base_stats[stat.StatGroup.SECONDARY]

    @property
    def base_tertiary(self):
        """ Return base tertiary statistics. """
        return self.base_stats[stat.StatGroup.TERTIARY]

    @property
    def total_primary(self):
        """ Return total primary statistics. """
        return self.total_stats[stat.StatGroup.PRIMARY]

    @property
    def total_secondary(self):
        """ Return total secondary statistics. """
        return self.total_stats[stat.StatGroup.SECONDARY]

    @property
    def total_tertiary(self):
        """ Return total tertiary statistics. """
        return self.total_stats[stat.StatGroup.TERTIARY]

    def update_stat_totals(self):
        """ Update total statistics of the character. """
        # apply changes to primary statistics
        collector = {}
        for mod in self.all_modifiers():
            mod.apply_primary(collector)
        self.total_stats[stat.StatGroup.PRIMARY] = self.base_primary.copy()
        # TODO: actually apply the collected changes
        # apply changes to secondary statistics
        collector = {}
        for mod in self.all_modifiers():
            mod.apply_secondary(collector, self.total_primary)
        self.total_stats[stat.StatGroup.PRIMARY] = self.base_secondary.copy()
        # apply changes to tertiary statistics
        collector = {}
        for mod in self.all_modifiers():
            mod.apply_primary(collector, self.total_primary, self.total_secondary)
        self.total_stats[stat.StatGroup.PRIMARY] = self.base_tertiary.copy()


#--------- convenience things ---------#

def empty_stat_dict():
    """ Return an empty statistics dict. """
    res = {}
    res[stat.StatGroup.PRIMARY] = {s: 0 for s in stat.PrimaryStat}
    res[stat.StatGroup.SECONDARY] = {s: 0 for s in stat.SecondaryStat}
    res[stat.StatGroup.TERTIARY] = {s: 0 for s in stat.TertiaryStat}
    return res
