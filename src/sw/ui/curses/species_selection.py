"""
Curses-based species selection UI.
"""


import mofloc


import sw.const as const
import sw.const.ui.species_selection as ss
import sw.event.species_selection as event
import sw.misc as misc
import sw.ui as ui
import sw.ui.curses as curses


class SpeciesSelection(ui.SpeciesSelection):
    """ The species selection UI. """

    def __init__(self, screen, data):
        super().__init__()
        self.screen = screen
        _, w = screen.getmaxyx()
        self.tiles = [
            screen.derwin(ss.SPECIES_PER_TILE, w // 3, 0, 0),
            screen.derwin(ss.SPECIES_PER_TILE, w // 3, 0, w // 3),
            screen.derwin(ss.SPECIES_PER_TILE, w // 3, 0, 2 * w // 3)]
        self.data = data

    def draw(self):
        self.screen.erase()
        tile = 0
        sp_index = 0
        for letter, species in self.enum_species():
            if sp_index > (tile + 1) * ss.SPECIES_PER_TILE:
                tile += 1
            y = ss.VERTICAL_OFFSET + (sp_index - tile * ss.SPECIES_PER_TILE)
            x = 0
            self.tiles[tile].addstr(y, x, f"{letter} - {species.name}")
        for t in self.tiles:
            t.refresh()
        strings = self.data.strings[const.SPECIES_SELECTION]
        curses.print_centered(self.screen, 0, strings[ss.HEADER])
        self.screen.addstr(ss.SPECIES_PER_TILE + 2, 0, strings[ss.SUBSCRIPT])
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        for letter, species in self.enum_species():
            if letter == ch:
                return (event.CHOOSE_SPECIES, species)
        if ch == ss.ABORT_KEY:
            return (event.ABORT_SPECIES,)
        raise mofloc.NoEvent

    def enum_species(self):
        """ Enumerate the species. """
        return misc.enumerate_with_letters(self.data.species)
