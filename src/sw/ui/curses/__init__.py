"""
Curses UI subpackage.

Provides the usual ASCII interface.
"""


from curses import *


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


#--------- helper things ---------#


def print_centered(screen, y, msg, attr=None):
    """
    Print a message in the middle of the screen horizontally and in the given
    row.
    """
    _, w = screen.getmaxyx()
    attr = attr or A_NORMAL
    screen.addstr(y, w // 2 - len(msg) // 2, msg, attr)
