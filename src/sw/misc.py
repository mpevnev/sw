"""
A module for things that don't fit anywhere else.
"""


from itertools import chain
from pathlib import Path
import sys


import yaml


from sw.const.misc import INSTALLDIR
import sw.const.skill as skill
import sw.const.stat as stat


#--------- main things ---------#


def convert_skill_dict(data):
    """
    Convert string keys in the 'data' dict to Skill enumeration members.

    :param dict data: a dictionary to be converted.

    :return: a dictionary after the conversion.
    :rtype: dict(sw.const.skill.Skill, int)
    """
    res = empty_skill_dict()
    res.update({skill.Skill(key): value for key, value in data.items()})
    return res


def convert_stat_dict(data):
    """
    Convert string keys in the 'primary' and 'secondary' subdicts of a 'data'
    dict to PrimaryStat and SecondaryStat enumeration members respectively.

    :param dict data: a dictionary to be converted.
    :rtype: dict
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
    Iterate over all items in a given iterator, yielding a pair of a letter of
    the latin alphabet and an item from the iterator.

    :param iterator: an iterator supplying the items.

    :return: pairs (letter, item).
    """
    lower = (chr(i) for i in range(ord('a'), ord('z') + 1))
    upper = (chr(i) for i in range(ord('A'), ord('Z') + 1))
    return zip(chain(lower, upper), iterator)


def empty_skill_dict():
    """
    :return: a dictionary with zeroed skill levels.
    :rtype: dict(sw.const.skill.Skill, int)
    """
    res = {s: 0 for s in skill.Skill}
    return res


def empty_stat_dict():
    """
    :return: a dictionary with zeroed stat values.
    :rtype: dict
    """
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

    :param default: a value to return if the requested YAML file is empty.
    :param filename: chunks of the path to a YAML file.

    :return: contents of the YAML file.
    :rtype: dict
    """
    scriptdir = Path(sys.path[0])
    f = Path(*filename)
    try:
        return _try_read(scriptdir / f, default=default)
    except FileNotFoundError:
        pass
    try:
        return _try_read(scriptdir / ".." / f, default=default)
    except FileNotFoundError:
        pass
    return _try_read(Path("/", "usr", "share", INSTALLDIR, f), default=default)


#--------- helper things ---------#


def _try_read(path, default=None):
    """
    Try reading a YAML file.

    :param Path path: the path to a file to be read.
    :param default: a value to return if the file is empty.

    :return: contents of the YAML file.
    :rtype: dict
    """
    with open(path) as f:
        res = yaml.safe_load(f)
        if res is None:
            return default
        return res
