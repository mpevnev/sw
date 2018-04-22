"""
A module for things that don't fit anywhere else.
"""


from itertools import chain
from pathlib import Path


import yaml


from sw.const.misc import INSTALLDIR
import sw.const.skill as skill
import sw.const.stat as stat


#--------- main things ---------#


def convert_skill_dict(data):
    """
    Convert string keys in the 'data' dict to Skill enumeration members and
    return the resulting dictionary.
    """
    res = empty_skill_dict()
    res.update({skill.Skill(key): value for key, value in data.items()})
    return res


def convert_stat_dict(data):
    """
    Convert string keys in the 'data' dict to PrimaryStat and SecondaryStat
    enumeration members and return the resulting dictionary.
    """
    res = empty_stat_dict()
    primary_source = data[stat.StatGroup.PRIMARY.value]
    secondary_source = data[stat.StatGroup.SECONDARY.value]
    primary = {stat.PrimaryStat(key): value for key, value in primary_source.items()}
    secondary = {stat.SecondaryStat(key): value for key, value in secondary_source.items()}
    res[stat.StatGroup.PRIMARY].update(primary)
    res[stat.StatGroup.SECONDARY].update(secondary)
    return res


def enumerate_with_letters(iterator):
    """
    Return an iterator of things from the given iterator zipped with lowercase
    letters a-z followed by uppercase letters A-Z.
    """
    lower = (chr(i) for i in range(ord('a'), ord('z') + 1))
    upper = (chr(i) for i in range(ord('A'), ord('Z') + 1))
    return zip(chain(lower, upper), iterator)


def empty_skill_dict():
    """ Return a dict with all skills set to zero. """
    res = {s: 0 for s in skill.Skill}
    return res


def empty_stat_dict():
    """ Return an empty statistics dict. """
    res = {}
    res[stat.StatGroup.PRIMARY] = {s: 0 for s in stat.PrimaryStat}
    res[stat.StatGroup.SECONDARY] = {s: 0 for s in stat.SecondaryStat}
    return res


def read(default, *filename):
    """
    Read a YAML file.
    Search for it in the following directories:
    1) ./
    2) ../
    3) /usr/share/severed-world/
    """
    f = Path(*filename)
    try:
        return _try_read(f, default=default)
    except FileNotFoundError:
        pass
    try:
        return _try_read(".." / f, default=default)
    except FileNotFoundError:
        pass
    return _try_read(Path("/", "usr", "share", INSTALLDIR, f), default=default)


#--------- helper things ---------#


def _try_read(path, default=None):
    """ Try reading a YAML file. """
    with open(path) as f:
        res = yaml.safe_load(f)
        if res is None:
            return default
        return res
