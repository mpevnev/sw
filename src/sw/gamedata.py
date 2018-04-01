"""
Game data module.
"""


import sw.background as bg
import sw.const as const
import sw.misc as misc
import sw.species as sp


class GameData():
    """ A container for game data and strings. """

    def __init__(self):
        self.backgrounds = _read_backgrounds()
        self.species = _read_species()
        self.strings = _read_strings()


#--------- helper things ---------#


def _read_backgrounds():
    """ Read backgrounds from the data files. """
    import sw.const.background as constbg
    res = [bg.Background(data) for data in misc.read([], "data", constbg.BACKGROUNDS_FILE)]
    return res


def _read_species():
    """ Read species from the data files. """
    import sw.const.species as constsp
    res = [sp.Species(data) for data in misc.read([], "data", constsp.SPECIES_FILE)]
    return res


def _read_strings():
    """ Read strings from the data files. """
    res = {}
    return res
