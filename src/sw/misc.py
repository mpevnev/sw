"""
A module for things that don't fit anywhere else.
"""


from itertools import chain
from pathlib import Path


import yaml


from sw.const.misc import INSTALLDIR


#--------- main things ---------#


def enumerate_with_letters(iterator):
    """
    Return an iterator of things from the given iterator zipped with lowercase
    letters a-z followed by uppercase letters A-Z.
    """
    lower = (chr(i) for i in range(ord('a'), ord('z') + 1))
    upper = (chr(i) for i in range(ord('A'), ord('Z') + 1))
    return zip(chain(lower, upper), iterator)


def read(*filename):
    """
    Read a YAML file.
    Search for it in the following directories:
    1) ./
    2) ../
    3) /usr/share/severed-world/
    """
    f = Path(*filename)
    try:
        return _try_read(f)
    except FileNotFoundError:
        pass
    try:
        return _try_read(".." / f)
    except FileNotFoundError:
        pass
    return _try_read(Path("/", "usr", "share", INSTALLDIR, f))


#--------- helper things ---------#


def _try_read(path, default={}):
    """ Try reading a YAML file. """
    with open(path) as f:
        res = yaml.safe_load(f)
        if res is None:
            return default 
        return res
