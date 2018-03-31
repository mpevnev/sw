"""
Provides the CursesSpawner class.
"""


import sw.ui as ui


class CursesSpawner(ui.UISpawner):
    """ A curses-based UI spawner. """

    def __init__(self):
        self.screen = initscr()
        self.screen.keypad(True)
        cbreak()
        curs_set(0)
        noecho()
        start_color()

    def finish(self):
        nocbreak()
        curs_set(1)
        endwin()

    def spawn_main_menu(self, data):
        from sw.ui.curses.main_menu import MainMenu
        return MainMenu(self.screen, data)
