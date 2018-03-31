"""
Main menu module.
"""


import mofloc


import sw.event.main_menu as event
import sw.stage.quit as quit_stage


ENTRY_POINT = "the-only"


class MainMenu(mofloc.Flow):
    """ Main menu control flow. """

    def __init__(self, data, ui_spawner):
        super().__init__()
        self.data = data
        self.ui_spawner = ui_spawner
        self.ui = ui_spawner.spawn_main_menu(data)
        self.register_entry_point(ENTRY_POINT, self.run_menu)
        self.register_event_source(self.ui)
        self.register_preevent_action(self.draw)
        self.register_event_handler(self.new_game)
        self.register_event_handler(self.quit)

    def run_menu(self):
        """ A stub, main processing is done in event handlers. """
        pass

    def draw(self):
        """ Draw the menu. """
        self.ui.draw()

    #--------- event handlers ---------#

    def new_game(self, ev):
        """ Process a 'new game' event. """
        if ev[0] != event.NEW_GAME:
            return False
        return True

    def quit(self, ev):
        """ Process a 'quit' event. """
        if ev[0] != event.QUIT:
            return False
        new_flow = quit_stage.Quit(self.ui_spawner)
        raise mofloc.ChangeFlow(new_flow, quit_stage.ENTRY_POINT)
