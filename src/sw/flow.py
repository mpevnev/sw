"""
Flow module.

Provides base SWFlow class, a thin wrapper over mofloc.Flow.
"""


from mofloc import *


class SWFlow(Flow):
    """
    A UI-spawner-aware flow.
    """

    def __init__(self, state, ui_spawner, ui):
        super().__init__()
        self.ui_spawner = ui_spawner
        self.ui = ui
        self.state = state
        self.register_exception_action((Exception, KeyboardInterrupt), self.clean_ui)
        if ui is not None:
            self.register_preevent_action(self.draw)
            self.register_event_source(ui)

    def clean_ui(self, exception):
        """ Clean up the UI. """
        self.ui_spawner.finish()

    def draw(self):
        """ Draw the UI. """
        self.ui.draw()
