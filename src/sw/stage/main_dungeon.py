"""
Main dungeon stage (well, and non-dungeon area exploration too).
"""


import mofloc


import sw.event.main_dungeon as event


FROM_OVERWORLD = "from overworld"


class MainDungeon(mofloc.Flow):
    """ Main dungeon handler. """

    def __init__(self, state, ui_spawner, area):
        super().__init__()
        self.state = state
        self.ui_spawner = ui_spawner
        self.area = area
        self.ui = ui_spawner.spawn_main_dungeon(state, area)
        self.register_entry_point(FROM_OVERWORLD, self.from_overworld)
        self.register_preevent_action(self.draw)
        self.register_event_source(self.ui)
        self.register_event_handler(self.ascend)
        self.register_event_handler(self.descend)
        self.register_event_handler(self.move)

    def draw(self):
        """ Draw the UI. """
        self.ui.draw()

    #--------- entry points ---------#

    def from_overworld(self):
        """
        Figure out the starting position of the player and then proceed as
        usual.
        """
        self.area.randomly_place_player(self.state.player)
        self.area.update_visibility_matrix(self.state.player)


    #--------- event handlers ---------#

    def ascend(self, ev):
        """ Handle 'ascend' event. """
        if ev[0] != event.ASCEND:
            return False
        return True

    def descend(self, ev):
        """ Handle 'descend' event. """
        if ev[0] != event.DESCEND:
            return False
        return True

    def move(self, ev):
        """ Handle 'move' event. """
        if ev[0] != event.MOVE:
            return False
        delta = ev[1]
        if self.area.shift_entity(self.state.player, *delta):
            self.area.update_visibility_matrix(self.state.player)
            self.tick()
        return True

    #--------- helper things ---------#

    def tick(self):
        """ Process a single game turn. """
        self.state.turn += 1
        self.area.tick(self.state, self.state.player, self.ui)
