"""
Curses-based UI for the inventory view.
"""


import mofloc


import sw.const.item as ic
import sw.const.ui.curses.inventory as inv

import sw.event.inventory as event

import sw.ui.curses as curses


class Inventory(mofloc.EventSource):
    """ Inventory view. """

    def __init__(self, screen, colors, uidata, state):
        mofloc.EventSource.__init__(self)
        self.screen = screen
        self.colors = colors
        self.uidata = uidata
        self.state = state
        self.active_tab = ic.InventorySlot.SMALL
        h, w = screen.getmaxyx()
        self.header = screen.derwin(1, w, 0, 0)
        self.tabs = {tab: screen.derwin(h - 3, w, 1, 0) for tab in ic.InventorySlot}
        self.hint_panel = screen.derwin(2, w, h - 2, 0)

    def draw(self):
        """ Draw the UI piece. """
        self.screen.erase()
        self.draw_active_tab()
        self.draw_hint_panel()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch in self.uidata[inv.KEY_QUIT]:
            return (event.QUIT,)
        raise mofloc.NoEvent

    #--------- drawing ---------#

    def draw_active_tab(self):
        """ Draw the active tab. """
        tab = self.tabs[self.active_tab]
        tab.box()

    def draw_header(self):
        """ Draw the header with tab names. """
        pass

    def draw_hint_panel(self):
        """ Draw the hint panel. """
        self.hint_panel.addstr(self.uidata[inv.HINT])
