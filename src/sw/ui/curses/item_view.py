"""
Item view UI.
"""


import mofloc


import sw.const.item as ic
import sw.const.ui.curses.item_view as iv

import sw.event.item_view as event

import sw.ui.curses as curses


class ItemView(mofloc.EventSource):
    """ An item view. """

    def __init__(self, screen, colors, uidata, item):
        mofloc.EventSource.__init__(self)
        self.screen = screen
        self.colors = colors
        self.uidata = uidata
        self.item = item
        h, w = screen.getmaxyx()
        self.info_panel = screen.derwin(h - iv.NUM_HINTS, w, 0, 0)
        self.hints_panel = screen.derwin(iv.NUM_HINTS, w, h - iv.NUM_HINTS, 0)

    def draw(self):
        """ Draw the UI piece. """
        self.screen.erase()
        self.draw_hints()
        self.draw_info()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch in self.uidata[iv.KEY_BIG_QUIT]:
            return (event.QUIT_ALTOGETHER,)
        if ch in self.uidata[iv.KEY_QUIT]:
            return (event.QUIT_TO_INVENTORY,)
        if ch in self.uidata[iv.KEY_DRINK]:
            return (event.DRINK,)
        if ch in self.uidata[iv.KEY_DROP]:
            return (event.DROP,)
        if ch in self.uidata[iv.KEY_EQUIP]:
            return (event.EQUIP,)
        if ch in self.uidata[iv.KEY_READ]:
            return (event.READ,)
        if ch in self.uidata[iv.KEY_UNEQUIP]:
            return (event.UNEQUIP,)
        if ch in self.uidata[iv.KEY_USE]:
            return (event.USE,)
        raise mofloc.NoEvent

    #--------- drawing ---------#

    def draw_hints(self):
        """ Draw the hints panel. """
        # TODO: filter out irrelevant hints
        self.hints_panel.addstr(0, 0, self.uidata[iv.HINT_DRINK])
        self.hints_panel.addstr(1, 0, self.uidata[iv.HINT_DROP])
        self.hints_panel.addstr(2, 0, self.uidata[iv.HINT_EQUIP])
        self.hints_panel.addstr(3, 0, self.uidata[iv.HINT_READ])
        self.hints_panel.addstr(4, 0, self.uidata[iv.HINT_UNEQUIP])
        self.hints_panel.addstr(5, 0, self.uidata[iv.HINT_USE])

        self.hints_panel.addstr(6, 0, self.uidata[iv.HINT_BIG_QUIT])
        self.hints_panel.addstr(7, 0, self.uidata[iv.HINT_QUIT])

    def draw_info(self):
        """ Draw the information about the item. """
        self.info_panel.box()
