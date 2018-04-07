"""
Main game stage.

Consists primarily of Overworld and Area substages.
"""


import enum


import mofloc


import sw.event.overworld as overevent


#--------- entry points ---------#


class OverworldEntry(enum.Enum):
    """ Overworld entry points. """

    WORLDGEN = enum.auto()


#--------- overworld handlers ---------#


class Overworld(mofloc.Flow):
    """ The primary overworld view. """


    def __init__(self, data, ui_spawner, player, world):
        super().__init__()
        self.data = data
        self.ui_spawner = ui_spawner
        self.player = player
        self.world = world
        self.ui = ui_spawner.spawn_main_overworld_window(data, world, player)
        self.register_entry_point(OverworldEntry.WORLDGEN, self.from_worldgen)
        self.register_event_source(self.ui)
        self.register_preevent_action(self.draw)

    def draw(self):
        self.ui.draw()

    #--------- entry points  ---------#

    def from_worldgen(self):
        """ Print the introductory message and then proceed as usual. """
        pass

    #--------- event handlers ---------#

    def quit(self, ev):
        """ Process a 'quit' command. """
        if ev[0] != overevent.QUIT:
            return False
        import sw.stage.quit as q
        new_flow = q.Quit(self.ui_spawner)
        raise mofloc.ChangeFlow(new_flow, q.ENTRY_POINT)


#--------- area handlers ---------#
