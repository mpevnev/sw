"""
World generation stage.
"""


import sw.flow as flow
import sw.gamestate as state
import sw.world as world


ENTRY_POINT = "the only"


class WorldGeneration(flow.SWFlow):
    """ World generation control flow. """

    def __init__(self, state, ui_spawner):
        super().__init__(state, ui_spawner, None)
        self.register_entry_point(ENTRY_POINT, self.generate_world)

    #--------- main thing ---------#

    def generate_world(self):
        """
        Generate a world and then transfer control to the main game flow.
        """
        import sw.stage.main_overworld as mo
        self.state.ui = None
        self.state.world = world.world_from_scratch(self.state.data)
        new_flow = mo.MainOverworld(self.state, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, mo.FROM_WORLDGEN)
