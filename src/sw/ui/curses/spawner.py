"""
Provides the CursesSpawner class.
"""


import sw.ui as ui
import sw.ui.curses as curses


class CursesSpawner(ui.UISpawner):
    """ A curses-based UI spawner. """

    def __init__(self):
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

    def spawn_background_selection(self, data):
        from sw.ui.curses.background_selection import BackgroundSelection
        return BackgroundSelection(self.screen, data)

    def spawn_char_name_prompt(self, data, default_name=""):
        from sw.ui.curses.char_name_prompt import CharNamePrompt
        return CharNamePrompt(self.screen, data, default_name)

    def spawn_main_menu(self, data):
        from sw.ui.curses.main_menu import MainMenu
        return MainMenu(self.screen, data)
