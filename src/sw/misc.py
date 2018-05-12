"""
A module for things that don't fit anywhere else.
"""


from collections import deque
from pathlib import Path
import string
import sys


import yaml


import sw.const.item as item
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


def dist(a, b):
    """
    Return Manhattan distance between two points.

    :param a: first point.
    :type a: tuple(int, int)
    :param b: second point.
    :type b: tuple(int, int)

    :return: distance.
    :rtype: int
    """
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def enumerate_with_letters(iterator):
    """
    Iterate over all items in a given iterator, yielding a pair with a letter
    of the latin alphabet and an item from the iterator. If there are more
    items in the iterator than fits in the alphabet, use uppercase letters,
    then pairs of letters, then triples, and so on.

    :param iterator: an iterator supplying the items.

    :return: pairs (letter(s), item).
    """
    def letter_generator():
        """
        Generate an infinite sequence of letters, then pairs of letters, then
        triples of letters and so on.
        """
        digits = ['a']
        while True:
            yield "".join(digits)
            if digits[-1] == 'z':
                digits[-1] = 'A'
                continue
            if digits[-1] == 'Z':
                digits[-1] = 'a'
                carry = True
                i = -2
                last_index = -len(digits)
                while carry and i >= last_index:
                    carry = digits[i] == 'Z'
                    digits[i] = 'a'
                    i -= 1
                if carry:
                    digits = ['a'] + digits
                continue
            digits[-1] = chr(ord(digits[-1]) + 1)
    return zip(letter_generator(), iterator)


def empty_equipment_dict():
    """
    :return: a dictionar with zero-length equipment slots.
    :rtype: dict(sw.const.item.EquipmentSlot, list)
    """
    return {slot: [] for slot in item.EquipmentSlot}


def empty_inventory_dict():
    """
    :return: a dictionary with zero-length inventory slots.
    :rtype: dict(sw.const.item.InventorySlot, list)
    """
    return {slot: [] for slot in item.InventorySlot}


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


def segment_interpolation(x, *points):
    """
    Perform a segment interpolation.
    Find a segment between two points such that
    'left_x <= x <= right_x' and return a value based on linear interpolation
    between those two points.
    If no such segment is found, use Y value of leftmost or rightmost segment.

    :raises IndexError: if 'points' has less than two elements.
    """
    if len(points) < 2:
        raise IndexError
    left_x, left_y = points[0]
    if x < left_x:
        return left_y
    for point in points[1:]:
        right_x, right_y = point
        if left_x <= x <= right_x:
            return (x - left_x) / (right_x - left_x) * (right_y - left_y) + left_y
        left_x, left_y = right_x, right_y
    return right_y


def slot_stat(slot_type):
    """
    Return a stat governing the number of slots of a given type.

    :param slot_type: the type of slot to get statistics for.
    :type slot_type: sw.const.item.InventorySlot

    :return: the relevant *_SLOTS statistic.
    :rtype: sw.const.stat.SecondaryStat

    :raises ValueError: if the slot type is unknown.
    """
    if slot_type is item.InventorySlot.SMALL:
        return stat.SecondaryStat.SMALL_SLOTS
    if slot_type is item.InventorySlot.MEDIUM:
        return stat.SecondaryStat.MEDIUM_SLOTS
    if slot_type is item.InventorySlot.BIG:
        return stat.SecondaryStat.BIG_SLOTS
    if slot_type is item.InventorySlot.HUGE:
        return stat.SecondaryStat.HUGE_SLOTS
    raise ValueError(f"Unknown slot type '{self.carrying_slot}'")

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
