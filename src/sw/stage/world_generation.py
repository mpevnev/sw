"""
World generation stage.
"""


import mofloc


import sw.gamestate as state
import sw.world as world


ENTRY_POINT = "the only"


class WorldGeneration(mofloc.Flow):
    """ World generation control flow. """

    def __init__(self, data, ui_spawner, player):
        super().__init__()
        self.data = data
        self.ui_spawner = ui_spawner
        self.player = player
        self.register_entry_point(ENTRY_POINT, self.generate_world)

    #--------- main thing ---------#

    def generate_world(self):
        """
        Generate a world and then transfer control to the main game flow.
        """
        import sw.stage.main_overworld as mo
        new_world = world.WorldFromScratch(self.data)
        fullstate = state.GameStateFromScratch(self.data, self.player, new_world)
        new_flow = mo.MainOverworld(fullstate, self.ui_spawner)
        raise mofloc.ChangeFlow(new_flow, mo.FROM_WORLDGEN)
