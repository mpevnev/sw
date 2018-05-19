"""
Startup stage, responsible for reading game data and initializing the UI.
"""


import mofloc


from sw.gamedata import GameData
from sw.gamestate import game_state_from_scratch
import sw.stage.main_menu as mm
from sw.ui import make_spawner


ENTRY_POINT = "the only"


class Startup(mofloc.Flow):
    """ Game initialization. """

    def __init__(self):
        super().__init__()
        self.register_entry_point(ENTRY_POINT, init_game)


def init_game(ui_type):
    """ Initialize the game. """
    data = GameData()
    state = game_state_from_scratch(data)
    spawner = make_spawner(ui_type)
    raise mofloc.ChangeFlow(mm.MainMenu(state, spawner), None)
