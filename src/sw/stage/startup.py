"""
Startup stage, responsible for reading game data and initializing the UI.
"""


import mofloc


from sw.gamedata import GameData
from sw.ui import make_spawner


ENTRY_POINT = "the only"


class Startup(mofloc.Flow):
    """ Game initialization. """

    def __init__(self):
        super().__init__()
        self.register_entry_point(ENTRY_POINT, init_game)


def init_game(ui_type):
    """ Initialize the game. """
    import sw.stage.main_menu as mm
    data = GameData()
    spawner = make_spawner(ui_type)
    raise mofloc.ChangeFlow(mm.MainMenu(data, spawner), mm.ENTRY_POINT)
