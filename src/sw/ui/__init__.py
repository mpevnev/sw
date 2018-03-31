"""
UI subpackage.

Provides base UISpawner class used to spawn pieces of UI bound to pieces of the
game flow.
"""


import mofloc


# UI types
CURSES = "curses"
# eventually a UI with tiles support


#--------- main things ---------#


def make_spawner(ui_type):
    """ Create a UI spawner of appropriate type. """
    if ui_type == CURSES:
        import sw.ui.curses as curses
        return curses.CursesSpawner()
    raise NotImplementedError


class UISpawner():
    """ A factory for UI pieces. """

    def finish(self):
        """ Terminate the UI. """
        raise NotImplementedError

    def spawn_main_menu(self):
        """ Spawn the main menu UI piece. """
        raise NotImplementedError


#--------- concrete UI pieces ---------#


class MainMenuUI(mofloc.EventSource):
    """ Main menu. """

    def draw(self):
        """ Draw the menu. """
        raise NotImplementedError

    def get_event(self):
        raise NotImplementedError
