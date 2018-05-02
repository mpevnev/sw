"""
Main menu module.
"""


import sw.flow as flow
import sw.event.main_menu as event


ENTRY_POINT = "the-only"


class MainMenu(flow.SWFlow):
    """ Main menu control flow. """

    def __init__(self, data, ui_spawner):
        super().__init__(ui_spawner)
        self.data = data
        self.ui = ui_spawner.spawn_main_menu(data)
        self.register_entry_point(ENTRY_POINT, self.run_menu)
        self.register_event_source(self.ui)
        self.register_event_handler(self.new_game)
        self.register_event_handler(self.quit)

    def run_menu(self):
        """ A stub, main processing is done in event handlers. """
        pass

    #--------- event handlers ---------#

    def new_game(self, ev):
        """ Process a 'new game' event. """
        if ev[0] != event.NEW_GAME:
            return False
        import sw.stage.char_creation as char_stage
        new_flow = char_stage.NameInput(self.data, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, char_stage.NAME_INPUT_ENTRY_POINT)

    def quit(self, ev):
        """ Process a 'quit' event. """
        if ev[0] != event.QUIT:
            return False
        import sw.stage.quit as quit_stage
        new_flow = quit_stage.Quit(self.ui_spawner)
        raise flow.ChangeFlow(new_flow, quit_stage.ENTRY_POINT)
