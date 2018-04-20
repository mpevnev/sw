"""
Constants for curses-based interface.
"""


import curses
import enum


BACKGROUND_SELECTION = "background selection"
CHAR_NAME_PROMPT = "char name prompt"
MAIN_DUNGEON = "main dungeon"
MAIN_MENU = "main menu"
MAIN_OVERWORLD = "main overworld"
SPECIES_SELECTION = "species selection" 


class Color(enum.Enum):
    """ An enumeration with text colors. """

    BLACK = curses.COLOR_BLACK
    BLUE = curses.COLOR_BLUE
    CYAN = curses.COLOR_CYAN
    GREEN = curses.COLOR_GREEN
    MAGENTA = curses.COLOR_MAGENTA
    RED = curses.COLOR_RED
    WHITE = curses.COLOR_WHITE
    YELLOW = curses.COLOR_YELLOW
