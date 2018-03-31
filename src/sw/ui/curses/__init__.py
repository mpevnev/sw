"""
Curses UI subpackage.

Provides the usual ASCII interface.
"""


from curses import *
from curses.textpad import *


def print_centered(screen, y, msg, attr=None):
    """
    Print a message in the middle of the screen horizontally and in the given
    row.
    """
    _, w = screen.getmaxyx()
    attr = attr or A_NORMAL
    screen.addstr(y, w // 2 - len(msg) // 2, msg, attr)
