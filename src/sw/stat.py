"""
Statistics module.

Provides several convenience things to work with character statistics.
"""


import sw.const.stat as stat


def empty_stat_dict():
    """ Return an empty statistics dict. """
    res = {}
    res[stat.StatGroup.PRIMARY] = {s: 0 for s in stat.PrimaryStat}
    res[stat.StatGroup.SECONDARY] = {s: 0 for s in stat.SecondaryStat}
    res[stat.StatGroup.TERTIARY] = {s: 0 for s in stat.TertiaryStat}
    return res
