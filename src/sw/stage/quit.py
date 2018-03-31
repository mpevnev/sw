"""
Game finalization stage.

Responsible for disposing of the UI.
"""

import mofloc


ENTRY_POINT = "the only"


class Quit(mofloc.Flow):
    """ Game shutdown. """

    def __init__(self, ui_spawner):
        super().__init__()
        self.ui = ui_spawner
        self.register_entry_point(ENTRY_POINT, self.quit)

    def quit(self):
        """ Quit the game. """
        self.ui.finish()
        raise mofloc.EndFlow()
