"""
Curses UI subpackage.

Provides the usual ASCII interface.
"""


from curses import *
from curses.textpad import *


import sw.const.ui.curses as const


def color_from_dict(colors, from_dict):
    """
    Return an attribute based on a given dict with foreground and background
    colors.
    """
    mapping = {
        const.COLOR_BLACK: curses.COLOR_BLACK,
        const.COLOR_BLUE: curses.COLOR_BLUE,
        const.COLOR_CYAN: curses.COLOR_CYAN,
        const.COLOR_GREEN: curses.COLOR_GREEN,
        const.COLOR_MAGENTA: curses.COLOR_MAGENTA,
        const.COLOR_RED: curses.COLOR_RED,
        const.COLOR_WHITE: curses.COLOR_WHITE,
        const.COLOR_YELLOW: curses.COLOR_YELLOW,
        }
    fg = mapping[from_dict[const.COLOR_FG]]
    bg = mapping[from_dict[const.COLOR_BG]]
    return colors[fg][bg]


def print_centered(screen, y, msg, attr=None):
    """
    Print a message in the middle of the screen horizontally and in the given
    row.
    """
    _, w = screen.getmaxyx()
    attr = attr or A_NORMAL
    screen.addstr(y, w // 2 - len(msg) // 2, msg, attr)
