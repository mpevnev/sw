"""
Curses-based background selection menu.
"""


import mofloc


import sw.const.ui.background_selection as bg
import sw.event.background_selection as event
import sw.misc as misc
import sw.ui as ui
import sw.ui.curses as curses


class BackgroundSelection(ui.BackgroundSelection):
    """ The background selection UI. """

    def __init__(self, screen, data):
        super().__init__()
        self.screen = screen
        h, w = screen.getmaxyx()
        self.tiles = [
            screen.derwin(h, w // 3, 0, 0),
            screen.derwin(h, w // 3, 0, w // 3),
            screen.derwin(h, w // 3, 0, 2 * w // 3)]
        self.data = data

    def draw(self):
        self.screen.erase()
        tile = 0
        bg_index = 0
        for letter, background in misc.enumerate_with_letters(self.data.backgrounds):
            if bg_index > (tile + 1) * bg.BACKGROUNDS_PER_TILE:
                tile += 1
            x = bg_index - tile * bg.BACKGROUNDS_PER_TILE
            self.tiles[tile].addstr(0, x, f"{letter} - {background.name}")
        for t in self.tiles:
            t.refresh()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        for letter, background in misc.enumerate_with_letters(self.data.backgrounds):
            if letter == ch:
                return (event.CHOOSE_BACKGROUND, background)
        raise mofloc.NoEvent
