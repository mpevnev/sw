"""
Statistics module.

Provides HasStats class for things that can have statistics and modifiers to
them.
"""


import sw.const.stat as stat


#--------- main class ---------#

class HasStats():
    """
    A class for things that have statistics.
    """

    def __init__(self):
        self.base_stats = empty_stat_dict()
        self.total_stats = empty_stat_dict()

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


#--------- convenience things ---------#

def empty_stat_dict():
    """ Return an empty statistics dict. """
    res = {}
    res[stat.StatGroup.PRIMARY] = {s: 0 for s in stat.PrimaryStat}
    res[stat.StatGroup.SECONDARY] = {s: 0 for s in stat.SecondaryStat}
    res[stat.StatGroup.TERTIARY] = {s: 0 for s in stat.TertiaryStat}
    return res
