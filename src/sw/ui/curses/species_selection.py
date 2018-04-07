"""
Curses-based species selection UI.
"""


import mofloc


import sw.const.ui.curses.species_selection as ss
import sw.event.species_selection as event
import sw.misc as misc
import sw.ui as ui
import sw.ui.curses as curses


class SpeciesSelection(mofloc.EventSource):
    """ The species selection UI. """

    def __init__(self, screen, uidata, data):
        super().__init__()
        self.screen = screen
        self.uidata = uidata
        self.data = data
        h, w = screen.getmaxyx()
        num_tiles = uidata[ss.NUM_TILES]
        self.tiles = [
            screen.derwin(h, w // num_tiles, 0, i * w // num_tiles)
            for i in range(num_tiles)]

    def draw(self):
        """ Draw the menu. """
        self.screen.erase()
        tile = 0
        sp_index = 0
        uidata = self.uidata
        sp_per_tile = uidata[ss.SPECIES_PER_TILE]
        for letter, species in self.enum_species():
            if sp_index > (tile + 1) * sp_per_tile:
                tile += 1
            y = uidata[ss.LIST_VERTICAL_OFFSET] + (sp_index - tile * sp_per_tile)
            x = 0
            self.tiles[tile].addstr(y, x, f"{letter} - {species.name}")
        for t in self.tiles:
            t.refresh()
        curses.print_centered(self.screen, uidata[ss.HEADER_OFFSET], uidata[ss.HEADER])
        self.screen.addstr(sp_per_tile + uidata[ss.SUBSCRIPT_OFFSET], 0,
                           uidata[ss.SUBSCRIPT])
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        for letter, species in self.enum_species():
            if letter == ch:
                return (event.CHOOSE_SPECIES, species)
        if ch == self.uidata[ss.ABORT_KEY]:
            return (event.ABORT_SPECIES,)
        raise mofloc.NoEvent

    def enum_species(self):
        """ Enumerate the species. """
        return misc.enumerate_with_letters(self.data.species)
