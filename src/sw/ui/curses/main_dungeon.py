"""
Curses-based UI for main dungeon view.
"""


import mofloc


import sw.const.ui.curses.main_dungeon as md
import sw.event.main_dungeon as event
import sw.ui.curses as curses


class MainDungeon(mofloc.EventSource):
    """ Main overworld view. """

    def __init__(self, screen, colors, uidata, state, area):
        super().__init__()
        self.screen = screen
        self.colors = colors
        self.uidata = uidata
        self.state = state
        self.area = area
        self.area_view = self.make_area_view()
        self.message_box = self.make_message_box()
        self.player_status_box = self.make_status_box()

    def draw(self):
        """ Draw the UI piece. """
        self.screen.erase()
        self.draw_area_view()
        self.draw_message_box()
        self.draw_player_status_box()
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        ch = self.screen.getkey()
        if ch in self.uidata[md.KEY_RIGHT]:
            return (event.MOVE, (1, 0))
        if ch in self.uidata[md.KEY_RIGHT_UP]:
            return (event.MOVE, (1, -1))
        if ch in self.uidata[md.KEY_UP]:
            return (event.MOVE, (0, -1))
        if ch in self.uidata[md.KEY_LEFT_UP]:
            return (event.MOVE, (-1, -1))
        if ch in self.uidata[md.KEY_LEFT]:
            return (event.MOVE, (-1, 0))
        if ch in self.uidata[md.KEY_LEFT_DOWN]:
            return (event.MOVE, (-1, 1))
        if ch in self.uidata[md.KEY_DOWN]:
            return (event.MOVE, (0, 1))
        if ch in self.uidata[md.KEY_RIGHT_DOWN]:
            return (event.MOVE, (1, 1))
        if ch in self.uidata[md.KEY_ASCEND]:
            return (event.ASCEND,)
        if ch in self.uidata[md.KEY_DESCEND]:
            return (event.DESCEND,)
        raise mofloc.NoEvent

    #--------- drawing ---------#

    def draw_area_view(self):
        """ Draw the area. """
        h, w = self.area_view.getmaxyx()
        player_x, player_y = self.state.player.position
        offset_x = w // 2 - player_x
        offset_y = h // 2 - player_y
        for x, y in self.area.all_coordinates():
            x = x + offset_x
            y = y + offset_y
            if x >= 0 and x < w and y >= 0 and y < h:
                self.area_view.addch(y, x, self.uidata[md.EMPTY_SPACE_CHAR])
        for doodad in self.area.doodads:
            char = self.uidata[md.DOODAD_MAP][doodad.recipe_id][md.MAP_CHAR]
            # TODO: use color
            x = doodad.position[0] + offset_x
            y = doodad.position[1] + offset_y
            self.area_view.addch(y, x, char)
        for (x, y), info in self.area.visibility_matrix.items():
            x = x + offset_x
            y = y + offset_y
            if info.visible():
                self.area_view.addch(y, x, '!')
            else:
                self.area_view.addch(y, x, '?')
        self.area_view.addch(h // 2, w // 2, self.uidata[md.PLAYER_CHAR])
        self.area_view.box()

    def draw_message_box(self):
        """ Draw the messages and the message box. """
        self.message_box.box()

    def draw_player_status_box(self):
        """ Draw the status box with player info. """
        self.player_status_box.box()

    #--------- subwindow creation ---------#

    def make_area_view(self):
        """ Make a box for the view on the area. """
        h = self.screen.getmaxyx()[0] - self.uidata[md.MESSAGE_BOX_HEIGHT]
        w = self.screen.getmaxyx()[1] - self.uidata[md.PLAYER_STATUS_BOX_WIDTH]
        return self.screen.derwin(h, w, 0, 0)

    def make_message_box(self):
        """ Make a box for messages in the bottom of the screen. """
        h = self.uidata[md.MESSAGE_BOX_HEIGHT]
        w = self.screen.getmaxyx()[1] - self.uidata[md.PLAYER_STATUS_BOX_WIDTH]
        return self.screen.derwin(h, w, self.screen.getmaxyx()[0] - h, 0)

    def make_status_box(self):
        """ Make a box for player's status. """
        h = self.screen.getmaxyx()[0]
        w = self.uidata[md.PLAYER_STATUS_BOX_WIDTH]
        return self.screen.derwin(h, w, 0, self.screen.getmaxyx()[1] - w)
