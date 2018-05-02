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
    """
    Create a UI spawner of appropriate type.

    :param str ui_type: an identifier of a UI type.

    :return: a UI spawner.
    :rtype: UISpawner
    
    """
    if ui_type == CURSES:
        from sw.ui.curses.spawner import CursesSpawner
        return CursesSpawner()
    raise NotImplementedError


class UISpawner():
    """ A factory for UI pieces. """

    def finish(self):
        """ Terminate the UI. """
        raise NotImplementedError

    def spawn_background_selection(self, data, species):
        """
        Spawn a menu with background selection.

        :param data: game data.
        :type date: sw.gamedata.GameData
        :param species: chosen player species.
        :type species: sw.species.Species

        :return: a menu with background selection.
        """
        raise NotImplementedError

    def spawn_char_name_prompt(self):
        """
        Spawn a propmt for character's name.

        :return: a prompt
        """
        raise NotImplementedError

    def spawn_main_dungeon_window(self, state, area):
        """
        Spawn a dungeon view.

        :param state: global game state.
        :type state: sw.gamestate.GameState
        :param area: an area to view.
        :type area: sw.area.Area

        :return: a UI piece displaying the given area.
        """
        raise NotImplementedError

    def spawn_main_menu(self, data):
        """
        Spawn a main menu UI piece.

        :param data: game data.
        :type data: sw.gamedata.GameData

        :return: spawned menu.
        """
        raise NotImplementedError

    def spawn_main_overworld_window(self, state):
        """
        Spawn an overworld view.

        :param state: global game state.
        :type state: sw.gamestate.GameState

        :return: a UI piece displaying the overworld.
        """
        raise NotImplementedError

    def spawn_species_selection(self, data):
        """
        Spawn a menu with species selection.

        :param data: game data.
        :type data: sw.gamedata.GameData

        :return: spawned menu.
        """
        raise NotImplementedError


#--------- interfaces for some UI pieces ---------#


class MainDungeonWindow():
    """ An interface for the main dungeon view. """

    def death_animation(self, monster):
        """
        Play a death animation for a given monster.
        
        :param monster: a monster to play an animation for.
        :type monster: sw.monster.Monster
        """
        raise NotImplementedError

    def message(self, msg, channel):
        """
        Display a message. 
        
        :param str msg: a message to display.
        :param channel: a channel to display the message in.
        :type channel: sw.const.message.Channel
        """
        raise NotImplementedError
