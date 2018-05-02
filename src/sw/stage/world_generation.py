"""
World generation stage.
"""


import sw.flow as flow
import sw.gamestate as state
import sw.world as world


ENTRY_POINT = "the only"


class WorldGeneration(flow.SWFlow):
    """ World generation control flow. """

    def __init__(self, data, ui_spawner, player):
        super().__init__(ui_spawner)
        self.data = data
        self.player = player
        self.register_entry_point(ENTRY_POINT, self.generate_world)

    #--------- main thing ---------#

    def generate_world(self):
        """
        Generate a world and then transfer control to the main game flow.
        """
        import sw.stage.main_overworld as mo
        new_world = world.world_from_scratch(self.data)
        fullstate = state.game_state_from_scratch(self.data, self.player, new_world)
        new_flow = mo.MainOverworld(fullstate, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, mo.FROM_WORLDGEN)
