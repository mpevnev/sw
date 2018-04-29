"""
Statistics module.

Provides HasStats class for things that can have statistics and modifiers to
them.
"""


import sw.const.stat as stat
from sw.misc import empty_stat_dict


#--------- main class ---------#

class HasStats():
    """
    A class for things that have statistics.
    """

    def __init__(self):
        self.base_stats = empty_stat_dict()
        self.total_stats = empty_stat_dict()

    #--------- statistics manipulation - getters ---------#

    @property
    def base_primary(self):
        """
        :return: base primary statistics.
        :rtype: dict
        """
        return self.base_stats[stat.StatGroup.PRIMARY]

    @property
    def base_secondary(self):
        """
        :return: base secondary statistics.
        :rtype: dict
        """
        return self.base_stats[stat.StatGroup.SECONDARY]

    @property
    def total_primary(self):
        """
        :return: total primary statistics.
        :rtype: dict
        """
        return self.total_stats[stat.StatGroup.PRIMARY]

    @property
    def total_secondary(self):
        """
        :return: total secondary statistics.
        :rtype: dict
        """
        return self.total_stats[stat.StatGroup.SECONDARY]

    #--------- statistics manipulation - setters ---------#

    @base_primary.setter
    def base_primary(self, new):
        """"
        Set base primary statistics.

        :param dict new: new dict with base primary statistics.
        """
        self.base_stats[stat.StatGroup.PRIMARY] = new

    @base_secondary.setter
    def base_secondary(self, new):
        """"
        Set base secondary statistics.

        :param dict new: new dict with base secondary statistics.
        """
        self.base_stats[stat.StatGroup.SECONDARY] = new

    @total_primary.setter
    def total_primary(self, new):
        """"
        Set total primary statistics.

        :param dict new: new dict with total primary statistics.
        """
        self.total_stats[stat.StatGroup.PRIMARY] = new

    @total_secondary.setter
    def total_secondary(self, new):
        """"
        Set total secondary statistics.

        :param dict new: new dict with total secondary statistics.
        """
        self.total_stats[stat.StatGroup.SECONDARY] = new
