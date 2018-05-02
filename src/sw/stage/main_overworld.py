"""
Main overworld stage.
"""


import sw.event.main_overworld as event
import sw.flow as flow


FROM_WORLDGEN = "from worldgen"


class MainOverworld(flow.SWFlow):
    """ Main overworld handler. """

    def __init__(self, state, ui_spawner):
        super().__init__(ui_spawner)
        self.state = state
        self.ui = ui_spawner.spawn_main_overworld_window(state)
        self.register_entry_point(FROM_WORLDGEN, self.from_worldgen)
        self.register_event_source(self.ui)
        self.register_event_handler(self.descend)
        self.register_event_handler(self.move)

    #--------- entry points ---------#

    def from_worldgen(self):
        """ Print out an introductory message and proceed as normal. """
        self.state.player.update_totals(self.state, None)

    #--------- event handlers ---------#

    def descend(self, ev):
        """ Handle 'descend' command. """
        if ev[0] != event.DESCEND:
            return False
        import sw.stage.main_dungeon as md
        header = self.state.current_overworld_header()
        area = header.load_or_generate_area()
        new_flow = md.MainDungeon(self.state, self.ui_spawner, area)
        raise flow.ChangeFlow(new_flow, md.FROM_OVERWORLD)

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
