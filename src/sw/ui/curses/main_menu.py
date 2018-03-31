"""
Curses-based main menu.
"""


import curses


import mofloc


import sw.ui as ui
import sw.event.main_menu as event


class MainMenu(ui.MainMenuUI):
    """ The main menu UI. """

    def __init__(self, screen):
        self.screen = screen
        self.text = "hello"

    def draw(self):
        self.screen.erase()
        self.screen.addstr(20, 20, self.text)
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch == 'a':
            return (event.NEW_GAME,)
        if ch == 'b':
            return (event.QUIT,)
        self.text = ch
        raise mofloc.NoEvent
