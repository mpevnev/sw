"""
Curses-based background selection menu.
"""


import mofloc


import sw.const.ui.curses.background_selection as bs
import sw.event.background_selection as event
import sw.misc as misc
import sw.ui as ui
import sw.ui.curses as curses


class BackgroundSelection(mofloc.EventSource):
    """ The background selection UI. """

    def __init__(self, screen, uidata, data, species):
        super().__init__()
        self.screen = screen
        self.data = data
        self.species = species
        self.uidata = uidata
        h, w = screen.getmaxyx()
        num_tiles = uidata[bs.NUM_TILES]
        self.tiles = [
            screen.derwin(h, w // num_tiles, 0, i * w // num_tiles)
            for i in range(num_tiles)]

    def draw(self):
        """ Draw the menu. """
        self.screen.erase()
        tile = 0
        bg_index = 0
        uidata = self.uidata
        bg_per_tile = uidata[bs.BACKGROUNDS_PER_TILE]
        for letter, background in self.enum_backgrounds():
            if bg_index > (tile + 1) * bg_per_tile:
                tile += 1
            y = uidata[bs.LIST_VERTICAL_OFFSET] + (bg_index - tile * bg_per_tile)
            x = 0
            self.tiles[tile].addstr(y, x, f"{letter} - {background.name}")
        for t in self.tiles:
            t.refresh()
        curses.print_centered(self.screen, uidata[bs.HEADER_OFFSET], uidata[bs.HEADER])
        self.screen.addstr(bg_per_tile + uidata[bs.SUBSCRIPT_OFFSET], 0,
                           uidata[bs.SUBSCRIPT])
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        for letter, background in self.enum_backgrounds():
            if letter == ch:
                return (event.CHOOSE_BACKGROUND, background)
        if ch == self.uidata[bs.ABORT_KEY]:
            return (event.ABORT_BACKGROUND,)
        if ch == self.uidata[bs.BACK_KEY]:
            return (event.BACK_TO_SPECIES,)
        raise mofloc.NoEvent

    def enum_backgrounds(self):
        """ Enumerate the backgrounds. """
        allowed = filter(lambda bg: bg.id not in self.species.forbidden_backgrounds,
                         self.data.backgrounds)
        return misc.enumerate_with_letters(allowed)
