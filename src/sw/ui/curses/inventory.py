"""
Curses-based UI for the inventory view.
"""


import mofloc


import sw.misc as misc

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
        self.draw_header()
        self.draw_hint_panel()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        for letter, item in self.enumerate_items():
            if letter == ch:
                return (event.EXAMINE_ITEM, item)
        if ch in self.uidata[inv.KEY_CHANGE_TAB]:
            self.advance_active_tab()
            raise mofloc.NoEvent
        if ch in self.uidata[inv.KEY_QUIT]:
            return (event.QUIT,)
        raise mofloc.NoEvent

    #--------- drawing ---------#

    def draw_active_tab(self):
        """ Draw the active tab. """
        tab = self.tabs[self.active_tab]
        y = 1
        for letter, item in self.enumerate_items():
            curses.print_centered(tab, y, f"{letter} - ITEM")
            y += 1
        tab.box()

    def draw_header(self):
        """ Draw the header with tab names. """
        headers = [
            self.uidata[inv.SMALL_TAB],
            self.uidata[inv.MEDIUM_TAB],
            self.uidata[inv.BIG_TAB],
            self.uidata[inv.HUGE_TAB]
            ]
        self.header.move(0, 1)
        for header, item_slot in zip(headers, ic.InventorySlot):
            if item_slot is self.active_tab:
                color = curses.color_from_dict(self.colors, self.uidata[inv.SELECTED_COLOR])
            else:
                color = curses.color_from_dict(self.colors, self.uidata[inv.UNSELECTED_COLOR])
            self.header.addstr(header, color)
            self.header.addch(' ')

    def draw_hint_panel(self):
        """ Draw the hint panel. """
        self.hint_panel.addstr(0, 0, self.uidata[inv.HINT])

    #--------- helper things ---------#

    def advance_active_tab(self):
        """ Cycle through tabs. """
        tabs = list(ic.InventorySlot) + [ic.InventorySlot.SMALL]
        self.active_tab = tabs[tabs.index(self.active_tab) + 1]

    def enumerate_items(self):
        """
        Return a generator with letters and items in the current tab.
        """
        item_list = self.state.player.inventory[self.active_tab]
        item_list = filter(None, item_list)
        return misc.enumerate_with_letters(item_list)
