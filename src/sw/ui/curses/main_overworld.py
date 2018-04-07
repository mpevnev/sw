"""
Main overworld UI.
"""


from collections import deque


import mofloc


import sw.const.ui.curses.main_overworld as mo
import sw.event.main_overworld as event
import sw.ui as ui
import sw.ui.curses as curses


class MainOverworld(mofloc.EventSource):
    """ Main overworld view. """

    def __init__(self, screen, uidata, state):
        super().__init__()
        self.screen = screen
        self.uidata = uidata
        self.state = state
        self.message_box = self.make_message_box()
        self.player_status_box = self.make_status_box()
        self.overworld_view = self.make_overworld_view()
        self.messages = deque()

    def draw(self):
        """ Draw the UI piece. """
        self.screen.erase()
        self.draw_message_box()
        self.draw_overworld_view()
        self.draw_player_status_box()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        """ Get a key from the keyboard and transform it into an event. """
        ch = self.screen.getkey()
        raise mofloc.NoEvent

    #--------- subwindow drawing ---------#

    def draw_message_box(self):
        """ Draw the messages and the message box. """
        self.message_box.box()

    def draw_overworld_view(self):
        """ Draw the overworld. """
        self.overworld_view.box()

    def draw_player_status_box(self):
        """ Draw the status box with player info. """
        self.player_status_box.box()

    #--------- subwindow creation ---------#

    def make_message_box(self):
        """ Make a box for messages in the bottom of the screen. """
        h = self.uidata[mo.MESSAGE_BOX_HEIGHT]
        w = self.screen.getmaxyx()[1] - self.uidata[mo.PLAYER_STATUS_BOX_WIDTH]
        return self.screen.derwin(h, w, self.screen.getmaxyx()[0] - h, 0)

    def make_overworld_view(self):
        """ Make a box for the view on the overworld. """
        h = self.screen.getmaxyx()[0] - self.uidata[mo.MESSAGE_BOX_HEIGHT]
        w = self.screen.getmaxyx()[1] - self.uidata[mo.PLAYER_STATUS_BOX_WIDTH]
        return self.screen.derwin(h, w, 0, 0)

    def make_status_box(self):
        """ Make a box for player's status. """
        h = self.screen.getmaxyx()[0]
        w = self.uidata[mo.PLAYER_STATUS_BOX_WIDTH]
        return self.screen.derwin(h, w, 0, self.screen.getmaxyx()[1] - w)
