"""
A module for things that don't fit anywhere else.
"""


from pathlib import Path
import yaml


#--------- main things ---------#


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
    return _try_read(Path("/", "usr", "share", "severed-world", f))


#--------- helper things ---------#


def _try_read(path, default={}):
    """ Try reading a YAML file. """
    with open(path) as f:
        res = yaml.safe_load(f)
        if res is None:
            return default 
        return res
