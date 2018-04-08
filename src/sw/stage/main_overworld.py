"""
Main overworld stage.
"""


import mofloc


import sw.event.main_overworld as event


FROM_WORLDGEN = "from worldgen"


class MainOverworld(mofloc.Flow):
    """ Main overworld handler. """

    def __init__(self, state, ui_spawner):
        super().__init__()
        self.state = state
        self.ui_spawner = ui_spawner
        self.ui = ui_spawner.spawn_main_overworld_window(state)
        self.register_entry_point(FROM_WORLDGEN, self.from_worldgen)
        self.register_preevent_action(self.draw)
        self.register_event_source(self.ui)
        self.register_event_handler(self.descend)
        self.register_event_handler(self.move)

    def draw(self):
        """ Draw the UI. """
        self.ui.draw()

    #--------- entry points ---------#

    def from_worldgen(self):
        """ Print out an introductory message and proceed as normal. """
        pass

    #--------- event handlers ---------#

    def descend(self, ev):
        """ Handle 'descend' command. """
        if ev[0] != event.DESCEND:
            return False
        import sw.stage.main_dungeon as md
        header = self.state.current_overworld_header()
        area = header.load_or_generate_area()
        new_flow = md.MainDungeon(self.state, self.ui_spawner, area)
        raise mofloc.ChangeFlow(new_flow, mo.FROM_OVERWORLD)

    def move(self, ev):
        """ Handle 'move' command. """
        if ev[0] != event.MOVE:
            return False
        dx, dy = ev[1]
        x, y = self.state.player_position
        new_xy = (x + dx, y + dy)
        self.state.player_position = new_xy
        self.state.world.generate_area_buffer(*new_xy)
        return True
