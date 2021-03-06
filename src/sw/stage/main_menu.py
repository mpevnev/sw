"""
Main menu module.
"""


import sw.flow as flow
import sw.event.main_menu as event


class MainMenu(flow.SWFlow):
    """ Main menu control flow. """

    def __init__(self, state, ui_spawner):
        super().__init__(state, ui_spawner, ui_spawner.spawn_main_menu(state.data))
        self.register_event_handler(self.new_game)
        self.register_event_handler(self.quit)

    #--------- event handlers ---------#

    def new_game(self, ev):
        """ Process a 'new game' event. """
        if ev[0] != event.NEW_GAME:
            return False
        import sw.stage.char_creation as char_stage
        new_flow = char_stage.NameInput(self.state, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, None)

    def quit(self, ev):
        """ Process a 'quit' event. """
        if ev[0] != event.QUIT:
            return False
        import sw.stage.quit as quit_stage
        new_flow = quit_stage.Quit(self.ui_spawner)
        raise flow.ChangeFlow(new_flow, quit_stage.ENTRY_POINT)
