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

    def spawn_main_menu(self, data):
        from sw.ui.curses.main_menu import MainMenu
        return MainMenu(self.screen, data)
