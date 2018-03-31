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
        from sw.ui.curses.spawner import CursesSpawner
        return CursesSpawner()
    raise NotImplementedError


class UISpawner():
    """ A factory for UI pieces. """

    def finish(self):
        """ Terminate the UI. """
        raise NotImplementedError

    def spawn_background_selection(self, data):
        """ Spawn a menu with background selection. """
        raise NotImplementedError

    def spawn_char_name_prompt(self, data):
        """ Spawn a propmt for character's name. """
        raise NotImplementedError

    def spawn_main_menu(self, data):
        """ Spawn the main menu UI piece. """
        raise NotImplementedError


#--------- concrete UI pieces ---------#


class BackgroundSelection(mofloc.EventSource):
    """ Background selection UI. """

    def draw(self):
        """ Draw the menu. """
        raise NotImplementedError

    def get_event(self):
        raise NotImplementedError


class CharNamePrompt(mofloc.EventSource):
    """ Character name prompt. """

    def draw(self):
        """ Draw the prompt. """
        raise NotImplementedError

    def get_event(self):
        raise NotImplementedError


class MainMenu(mofloc.EventSource):
    """ Main menu. """

    def draw(self):
        """ Draw the menu. """
        raise NotImplementedError

    def get_event(self):
        raise NotImplementedError
