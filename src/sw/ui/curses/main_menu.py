"""
Curses-based main menu.
"""


import mofloc


import sw.const as const
import sw.const.main_menu as mm
import sw.ui as ui
import sw.ui.curses as curses
import sw.event.main_menu as event


class MainMenu(ui.MainMenuUI):
    """ The main menu UI. """

    def __init__(self, screen, data):
        self.screen = screen
        self.data = data

    def draw(self):
        self.screen.erase()
        strings = self.data.strings
        curses.print_centered(self.screen, 5, strings[const.MAIN_MENU][mm.GREETING])
        curses.print_centered(self.screen, 8,
                              f"a - {strings[const.MAIN_MENU][mm.NEW_GAME]}")
        curses.print_centered(self.screen, 9,
                              f"b - {strings[const.MAIN_MENU][mm.QUIT]}")
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch == 'a':
            return (event.NEW_GAME,)
        if ch == 'b':
            return (event.QUIT,)
        raise mofloc.NoEvent
