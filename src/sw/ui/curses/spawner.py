"""
Provides the CursesSpawner class.
"""


import sw.const.ui.curses as const
import sw.misc as misc
import sw.ui as ui
import sw.ui.curses as curses


class CursesSpawner(ui.UISpawner):
    """ A curses-based UI spawner. """

    def __init__(self):
        self.uidata = _read_curses_ui_data()
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.cbreak()
        curses.curs_set(0)
        curses.noecho()
        curses.start_color()

    def finish(self):
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def spawn_background_selection(self, data, species):
        from sw.ui.curses.background_selection import BackgroundSelection
        uidata = self.uidata[const.BACKGROUND_SELECTION]
        return BackgroundSelection(self.screen, uidata, data, species)

    def spawn_char_name_prompt(self):
        from sw.ui.curses.char_name_prompt import CharNamePrompt
        uidata = self.uidata[const.CHAR_NAME_PROMPT]
        return CharNamePrompt(self.screen, uidata)

    def spawn_main_menu(self, data):
        from sw.ui.curses.main_menu import MainMenu
        uidata = self.uidata[const.MAIN_MENU]
        return MainMenu(self.screen, uidata, data)

    def spawn_main_overworld_window(self, data, world, player):
        from sw.ui.curses.main_overworld import MainOverworld
        uidata = self.uidata[const.MAIN_OVERWORLD]
        return MainOverworld(self.screen, uidata, data, world, player)

    def spawn_species_selection(self, data):
        from sw.ui.curses.species_selection import SpeciesSelection
        uidata = self.uidata[const.SPECIES_SELECTION]
        return SpeciesSelection(self.screen, uidata, data)


#--------- helper things ---------#


def _read_curses_ui_data():
    """ Read configuration and strings for curses-based interface. """
    import sw.const.ui.curses.background_selection as bs
    import sw.const.ui.curses.char_name_prompt as cnp
    import sw.const.ui.curses.main_menu as mm
    import sw.const.ui.curses.main_overworld as mo
    import sw.const.ui.curses.species_selection as ss
    res = {}
    res[const.BACKGROUND_SELECTION] = misc.read({}, "ui", "curses", bs.DATA_FILE)
    res[const.CHAR_NAME_PROMPT] = misc.read({}, "ui", "curses", cnp.DATA_FILE)
    res[const.MAIN_MENU] = misc.read({}, "ui", "curses", mm.DATA_FILE)
    res[const.MAIN_OVERWORLD] = misc.read({}, "ui", "curses", mo.DATA_FILE)
    res[const.SPECIES_SELECTION] = misc.read({}, "ui", "curses", ss.DATA_FILE)
    return res
