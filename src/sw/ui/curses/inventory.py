"""
Curses-based UI for the inventory view.
"""


from itertools import chain
import string


import mofloc


import sw.misc as misc

import sw.const.item as ic
import sw.const.ui.curses.inventory as inv

import sw.event.inventory as event

import sw.ui.curses as curses


class Inventory(mofloc.EventSource):
    """ Inventory view. """

    def __init__(self, screen, colors, uidata, inventory):
        mofloc.EventSource.__init__(self)
        self.screen = screen
        self.colors = colors
        self.uidata = uidata
        self.inventory = inventory
        h, w = screen.getmaxyx()
        self.panel = {
            slot: screen.derwin(h - 2, w // 4, 0, i * w // 4)
            for i, slot in enumerate(ic.InventorySlot)}
        self.hint_panel = screen.derwin(2, w, h - 2, 0)
        self.filter_text = ""
        self.filtered_items = list(self.enumerate_items())

    def draw(self):
        """ Draw the UI piece. """
        self.screen.erase()
        self.draw_hint_panel()
        self.draw_panels()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch in string.ascii_letters:
            self.filter_text += ch
            self.filter_items()
            filter_length = len(self.filtered_items)
            if filter_length == 1:
                return (event.EXAMINE_ITEM, self.filtered_items[0][1])
            if filter_length == 0:
                self.filter_text = ""
                self.filter_items()
            raise mofloc.NoEvent
        if ch == self.uidata[inv.KEY_CONFIRM_SELECTION]:
            for code, item in self.filtered_items:
                if code == self.filter_text:
                    return (event.EXAMINE_ITEM, item)
            raise mofloc.NoEvent
        if ch in self.uidata[inv.KEY_CHANGE_TAB]:
            self.advance_active_tab()
            raise mofloc.NoEvent
        if ch in self.uidata[inv.KEY_QUIT]:
            return (event.QUIT,)
        raise mofloc.NoEvent

    #--------- drawing ---------#

    def draw_hint_panel(self):
        """ Draw the hint panel. """
        self.hint_panel.addstr(0, 0, self.uidata[inv.HINT])

    def draw_panels(self):
        """ Draw the panels with items. """
        y = 1
        for code, item in self.filtered_items:
            panel = self.panel[item.carrying_slot]
            try:
                curses.print_centered(panel, y, f"{code} - ITEM")
            except curses.error:
                continue
            y += 1
        for panel in self.panel.values():
            panel.box()

    #--------- helper things ---------#

    def enumerate_items(self):
        """
        Return a generator with letters and items.
        """
        inventory = self.inventory
        items = chain.from_iterable((inventory[slot] for slot in ic.InventorySlot))
        items = filter(None, items)
        return misc.enumerate_with_letters(items)

    def filter_items(self):
        """
        Filter away some items based on a new filter string.
        """
        if self.filter_text == "":
            self.filtered_items = self.enumerate_items()
            return
        cond = lambda t: t[0].startswith(self.filter_text)
        self.filtered_items = list(filter(cond, self.filtered_items))
