"""
Curses-based background selection menu.
"""


import mofloc


import sw.const as const
import sw.const.ui.background_selection as bg
import sw.event.background_selection as event
import sw.misc as misc
import sw.ui as ui
import sw.ui.curses as curses


class BackgroundSelection(ui.BackgroundSelection):
    """ The background selection UI. """

    def __init__(self, screen, data, species):
        super().__init__()
        self.screen = screen
        h, w = screen.getmaxyx()
        self.tiles = [
            screen.derwin(h, w // 3, 0, 0),
            screen.derwin(h, w // 3, 0, w // 3),
            screen.derwin(h, w // 3, 0, 2 * w // 3)]
        self.data = data
        self.species = species

    def draw(self):
        self.screen.erase()
        tile = 0
        bg_index = 0
        for letter, background in self.enum_backgrounds():
            if bg_index > (tile + 1) * bg.BACKGROUNDS_PER_TILE:
                tile += 1
            y = bg.VERTICAL_OFFSET + (bg_index - tile * bg.BACKGROUNDS_PER_TILE)
            x = 0
            self.tiles[tile].addstr(y, x, f"{letter} - {background.name}")
        for t in self.tiles:
            t.refresh()
        strings = self.data.strings[const.BACKGROUND_SELECTION]
        curses.print_centered(self.screen, 0, strings[bg.HEADER])
        self.screen.addstr(bg.BACKGROUNDS_PER_TILE + 2, 0, strings[bg.SUBSCRIPT])
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        for letter, background in self.enum_backgrounds():
            if letter == ch:
                return (event.CHOOSE_BACKGROUND, background)
        if ch == bg.ABORT_KEY:
            return (event.ABORT_BACKGROUND,)
        if ch == bg.BACK_KEY:
            return (event.BACK_TO_SPECIES,)
        raise mofloc.NoEvent

    def enum_backgrounds(self):
        """ Enumerate the backgrounds. """
        allowed = filter(lambda bg: bg.id not in self.species.forbidden_backgrounds,
                         self.data.backgrounds)
        return misc.enumerate_with_letters(allowed)
