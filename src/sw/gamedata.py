"""
Game data module.
"""


import sw.const as const
import sw.const.main_menu as mm
import sw.misc as misc


class GameData():
    """ A container for game data and strings. """

    def __init__(self):
        self.strings = _read_strings()


#--------- helper things ---------#


def _read_strings():
    """ Read strings from the data files. """
    res = {}
    res[const.MAIN_MENU] = misc.read("strings", mm.STRINGS_FILE)
    return res
