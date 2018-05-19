"""
Item view UI.
"""


import mofloc


import sw.interaction.item_tests as test

import sw.const.ui.curses.item_view as iv

import sw.event.item_view as event

import sw.ui.curses as curses


class ItemView(mofloc.EventSource):
    """ An item view. """

    def __init__(self, screen, colors, uidata, state, item):
        mofloc.EventSource.__init__(self)
        self.screen = screen
        self.colors = colors
        self.uidata = uidata
        self.state = state
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
            return (event.TAKE_OFF,)
        if ch in self.uidata[iv.KEY_USE]:
            return (event.USE,)
        raise mofloc.NoEvent

    #--------- drawing ---------#

    def draw_hints(self):
        """ Draw the hints panel. """
        item = self.item
        state = self.state
        player = state.player
        self.hints_panel.move(0, 0)
        if test.can_drink(player, item, state):
            self.hints_panel.addstr(f"{self.uidata[iv.HINT_DRINK]}\n")
        self.hints_panel.addstr(f"{self.uidata[iv.HINT_DROP]}\n")
        if test.can_equip(player, item, state) and not player.has_equipped(item):
            self.hints_panel.addstr(f"{self.uidata[iv.HINT_EQUIP]}\n")
        if test.can_read(player, item, state):
            self.hints_panel.addstr(f"{self.uidata[iv.HINT_READ]}\n")
        if player.has_equipped(item):
            self.hints_panel.addstr(f"{self.uidata[iv.HINT_UNEQUIP]}\n")
        if test.can_use(player, item, state):
            self.hints_panel.addstr(f"{self.uidata[iv.HINT_USE]}\n")
        self.hints_panel.addstr(f"{self.uidata[iv.HINT_BIG_QUIT]}\n")
        self.hints_panel.addstr(f"{self.uidata[iv.HINT_QUIT]}\n")

    def draw_info(self):
        """ Draw the information about the item. """
        self.info_panel.box()
