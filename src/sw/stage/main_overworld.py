"""
Main overworld stage.
"""


import mofloc


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

    def draw(self):
        """ Draw the UI. """
        self.ui.draw()

    #--------- entry points ---------#

    def from_worldgen(self):
        """ Print out an introductory message and proceed as normal. """
        pass
