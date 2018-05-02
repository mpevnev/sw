"""
Game finalization stage.

Responsible for disposing of the UI.
"""

import sw.flow as flow


ENTRY_POINT = "the only"


class Quit(flow.SWFlow):
    """ Game shutdown. """

    def __init__(self, ui_spawner):
        super().__init__(ui_spawner)
        self.register_entry_point(ENTRY_POINT, self.quit)

    def quit(self):
        """ Quit the game. """
        self.ui_spawner.finish()
        raise flow.EndFlow()
