"""
Curses UI subpackage.

Provides the usual ASCII interface.
"""


import curses


import sw.ui as ui


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
        import sw.ui.curses.main_menu as mm
        return mm.MainMenu(self.screen, data)


#--------- helper things ---------#


def print_centered(screen, y, msg, attr=None):
    """
    Print a message in the middle of the screen horizontally and in the given
    row.
    """
    _, w = screen.getmaxyx()
    attr = attr or curses.A_NORMAL
    screen.addstr(y, w // 2 - len(msg) // 2, msg, attr)
