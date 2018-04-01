"""
Curses-based main menu.
"""


import mofloc


import sw.const.ui.curses.main_menu as mm
import sw.ui as ui
import sw.ui.curses as curses
import sw.event.main_menu as event


class MainMenu(ui.MainMenu):
    """ The main menu UI. """

    def __init__(self, screen, uidata, data):
        super().__init__()
        self.screen = screen
        self.data = data
        self.uidata = uidata

    def draw(self):
        self.screen.erase()
        uidata = self.uidata
        offset = uidata[mm.HEADER_OFFSET]
        gap = uidata[mm.HEADER_GAP]
        curses.print_centered(self.screen, offset, uidata[mm.HEADER])
        curses.print_centered(self.screen, offset + gap,
                              f"a - {uidata[mm.NEW_GAME]}")
        curses.print_centered(self.screen, offset + gap + 1,
                              f"b - {uidata[mm.QUIT]}")
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch == 'a':
            return (event.NEW_GAME,)
        if ch == 'b':
            return (event.QUIT,)
        raise mofloc.NoEvent
