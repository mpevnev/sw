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
        curses.use_default_colors()
        self.colors = _init_colors()

    def finish(self):
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()

    def spawn_background_selection(self, data, species):
        from sw.ui.curses.background_selection import BackgroundSelection
        uidata = self.uidata[const.BACKGROUND_SELECTION]
        return BackgroundSelection(self.screen, self.colors, uidata, data, species)

    def spawn_char_name_prompt(self):
        from sw.ui.curses.char_name_prompt import CharNamePrompt
        uidata = self.uidata[const.CHAR_NAME_PROMPT]
        return CharNamePrompt(self.screen, self.colors, uidata)

    def spawn_main_dungeon(self, state):
        from sw.ui.curses.main_dungeon import MainDungeon
        uidata = self.uidata[const.MAIN_DUNGEON]
        return MainDungeon(self.screen, self.colors, uidata, state)

    def spawn_main_menu(self, data):
        from sw.ui.curses.main_menu import MainMenu
        uidata = self.uidata[const.MAIN_MENU]
        return MainMenu(self.screen, self.colors, uidata, data)

    def spawn_main_overworld_window(self, state):
        from sw.ui.curses.main_overworld import MainOverworld
        uidata = self.uidata[const.MAIN_OVERWORLD]
        return MainOverworld(self.screen, self.colors, uidata, state)

    def spawn_species_selection(self, data):
        from sw.ui.curses.species_selection import SpeciesSelection
        uidata = self.uidata[const.SPECIES_SELECTION]
        return SpeciesSelection(self.screen, self.colors, uidata, data)


#--------- helper things ---------#


def _init_colors():
    """ Return a dict with color pair attributes. """
    res = {}
    i = 1
    colors = [
        curses.COLOR_BLACK,
        curses.COLOR_BLUE,
        curses.COLOR_CYAN,
        curses.COLOR_GREEN,
        curses.COLOR_MAGENTA,
        curses.COLOR_RED,
        curses.COLOR_WHITE,
        curses.COLOR_YELLOW,
        ]
    for fg in colors:
        res[fg] = {}
        for bg in colors:
            curses.init_pair(i, fg, bg)
            res[fg][bg] = curses.color_pair(i)
            i += 1
    return res


def _read_curses_ui_data():
    """ Read configuration and strings for curses-based interface. """
    import sw.const.ui.curses.background_selection as bs
    import sw.const.ui.curses.char_name_prompt as cnp
    import sw.const.ui.curses.main_dungeon as md
    import sw.const.ui.curses.main_menu as mm
    import sw.const.ui.curses.main_overworld as mo
    import sw.const.ui.curses.species_selection as ss
    res = {}
    res[const.BACKGROUND_SELECTION] = misc.read({}, "ui", "curses", bs.DATA_FILE)
    res[const.CHAR_NAME_PROMPT] = misc.read({}, "ui", "curses", cnp.DATA_FILE)
    res[const.MAIN_DUNGEON] = misc.read({}, "ui", "curses", md.DATA_FILE)
    res[const.MAIN_MENU] = misc.read({}, "ui", "curses", mm.DATA_FILE)
    res[const.MAIN_OVERWORLD] = misc.read({}, "ui", "curses", mo.DATA_FILE)
    res[const.SPECIES_SELECTION] = misc.read({}, "ui", "curses", ss.DATA_FILE)
    return res
