"""
Flow module.

Provides base SWFlow class, a thin wrapper over mofloc.Flow.
"""


from mofloc import *


class SWFlow(Flow):
    """
    A UI-spawner-aware flow.
    """

    def __init__(self, ui_spawner):
        super().__init__()
        self.ui_spawner = ui_spawner
        self.ui = None
        self.register_exception_action(Exception, self.clean_ui)

    def clean_ui(self, exception):
        """ Clean up the UI. """
        self.ui_spawner.finish()

    def draw(self):
        """ Draw the UI. """
        self.ui.draw()
