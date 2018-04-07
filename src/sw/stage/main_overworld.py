"""
Main overworld stage.
"""


import mofloc


FROM_WORLDGEN = "from worldgen"


class MainOverworld(mofloc.Flow):
    """ Main overworld handler. """

    def __init__(self, data, ui_spawner, player, world):
        super().__init__()
        self.data = data
        self.ui_spawner = ui_spawner
        self.player = player
        self.world = world
        self.ui = ui_spawner.spawn_main_overworld_window(data, world, player)
        self.register_entry_point(FROM_WORLDGEN, self.from_worldgen)
        self.register_preevent_action(self.draw)

    def draw(self):
        """ Draw the UI. """
        self.ui.draw()

    #--------- entry points ---------#

    def from_worldgen(self):
        """ Print out an introductory message and proceed as normal. """
        pass
