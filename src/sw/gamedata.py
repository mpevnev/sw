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
    import sw.const.ui.background_selection as bg
    import sw.const.ui.main_menu as mm
    import sw.const.ui.char_name_prompt as cnp
    import sw.const.ui.species_selection as ss
    res = {}
    res[const.BACKGROUND_SELECTION] = misc.read({}, "strings", bg.STRINGS_FILE)
    res[const.CHAR_NAME_PROMPT] = misc.read({}, "strings", cnp.STRINGS_FILE)
    res[const.MAIN_MENU] = misc.read({}, "strings", mm.STRINGS_FILE)
    res[const.SPECIES_SELECTION] = misc.read({}, "strings", ss.STRINGS_FILE)
    return res
