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
        self._draw_area_background()
        self._draw_entities(
            self.area.doodads, self.uidata[md.DOODAD_MAP],
            self.uidata[md.SENSED_DOODAD_CHAR],
            lambda visinfo: visinfo.remembered_doodads,
            lambda visinfo: visinfo.sense_doodads())
        self._draw_entities(
            self.area.items, self.uidata[md.ITEM_MAP],
            self.uidata[md.SENSED_ITEM_CHAR],
            lambda visinfo: visinfo.remembered_items,
            lambda visinfo: visinfo.sense_items())
        self._draw_entities(
            self.area.monsters, self.uidata[md.MONSTER_MAP],
            self.uidata[md.SENSED_MONSTER_CHAR],
            lambda visinfo: visinfo.remembered_monsters,
            lambda visinfo: visinfo.sense_monsters())
        self._draw_player()
        self.area_view.box()

    def draw_message_box(self):
        """ Draw the messages and the message box. """
        self.message_box.box()

    def draw_player_status_box(self):
        """ Draw the status box with player info. """
        self.player_status_box.box()

    #--------- helper drawing procedures ---------#

    def _draw_area_background(self):
        """ Draw the empty spaces in the area. """
        offset_x, offset_y = self._drawing_offsets()
        char = self.uidata[md.EMPTY_SPACE_CHAR]
        seen_attr = curses.A_NORMAL
        unseen_attr = self._unseen_attr()
        for x, y in self.area.all_coordinates():
            visible = self.area.visibility_matrix[(x, y)].visible()
            x = x + offset_x
            y = y + offset_y
            self.area_view.addstr(y, x, char, seen_attr if visible else unseen_attr)

    def _draw_entities(self, entities, art_map, sensed_char, remembered_func, sense_func):
        """
        Draw the entities in the area.

        Entities themselves will be taken from 'entities' iterable.

        Entities' art will be taken from 'art_map', which should be a YAML
        dict.

        'sensed_char' will be used in place of unseen, but sensed entities.

        'remembered_func' should be a callable that take a VisibilityInfo
        argument and returns an iterable with remembered entities from it.

        Likewise, 'sense_func' should take a VisibilityInfo argument and return
        True if this info has 'sense_ENTITY_TYPE' set.
        """
        offset_x, offset_y = self._drawing_offsets()
        unseen_attr = self._unseen_attr()
        for entity in entities:
            if entity.hidden():
                continue
            x, y = entity.position
            mapping = art_map[entity.recipe_id]
            char = mapping[md.MAP_CHAR]
            attr = curses.color_from_dict(self.colors, mapping[md.MAP_COLOR])
            visinfo = self.area.visibility_matrix[(x, y)]
            x += offset_x
            y += offset_y
            if visinfo.visible():
                self.area_view.addstr(y, x, char, attr)
            else:
                if entity in remembered_func(visinfo):
                    self.area_view.addstr(y, x, char, unseen_attr)
                elif sense_func(visinfo):
                    self.area_view.addstr(y, x, sensed_char, unseen_attr)

    def _draw_player(self):
        """ Draw the player. """
        h, w = self.area_view.getmaxyx()
        self.area_view.addstr(h // 2, w // 2, self.uidata[md.PLAYER_CHAR])

    def _drawing_offsets(self):
        """ Return a tuple with drawing offsets for entities in the area. """
        h, w = self.area_view.getmaxyx()
        offset_x = w // 2 - self.state.player.position[0]
        offset_y = h // 2 - self.state.player.position[1]
        return (offset_x, offset_y)

    def _unseen_attr(self):
        """ Return the attribute used for unseen entities. """
        return curses.color_from_dict(self.colors, self.uidata[md.UNSEEN_ENTITY_COLOR])

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
