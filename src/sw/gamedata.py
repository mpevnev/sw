"""
Game data module.
"""


import sw.background as bg
import sw.const as const
import sw.misc as misc


class GameData():
    """ A container for game data and strings. """

    def __init__(self):
        self.strings = _read_strings()
        self.backgrounds = _read_backgrounds()


#--------- helper things ---------#


def _read_backgrounds():
    """ Read backgrounds from the data files. """
    import sw.const.background as constbg
    res = [bg.Background(data) for data in misc.read("data", constbg.BACKGROUNDS_FILE)]
    return res


def _read_strings():
    """ Read strings from the data files. """
    import sw.const.ui.background_selection as bg
    import sw.const.ui.main_menu as mm
    import sw.const.ui.char_name_prompt as cnp
    res = {}
    res[const.BACKGROUND_SELECTION] = misc.read("strings", bg.STRINGS_FILE)
    res[const.CHAR_NAME_PROMPT] = misc.read("strings", cnp.STRINGS_FILE)
    res[const.MAIN_MENU] = misc.read("strings", mm.STRINGS_FILE)
    return res
