"""
Game state module.

Provides GameState class to bundle together information about player, world,
and various other game data.
"""


from collections import deque


class GameState():
    """ A container with all game information. """

    def __init__(self):
        self.area = None
        self.data = None
        self.messages = None
        self.player = None
        self.player_position = None
        self.turn = 0
        self.ui = None
        self.world = None

    def current_overworld_header(self):
        """
        :return: the header of the area where the player is located.
        :rtype: sw.area_header.AreaHeader
        """
        return self.world.area_headers[self.player_position]


#--------- reading game state from a saved YAML dict ---------#


def game_state_from_save(gamedata, save):
    """
    Read game state from a save.

    :param gamedata: an object with game data used to regenerate game objects.
    :type gamedata: sw.gamedata.GameData
    :param dict save: information about game objects, game configuration and so
    on.

    :return: regenerated game state object.
    :rtype: GameState
    """
    raise NotImplementedError


#--------- creating game state from bottom up ---------#


def game_state_from_scratch(gamedata, player, world):
    """
    Create a GameState instance from separate parts.

    :param gamedata: game data used to populate the state with game objects.
    :type gamedata: sw.gamedata.GameData
    :param player: previously created player object.
    :type player: sw.player.Player
    :param world: previously created world object.
    :type world: sw.world.World

    :return: new game state.
    :rtype: GameState
    """
    res = GameState()
    res.data = gamedata
    res.player = player
    res.world = world
    res.player_position = (0, 0)
    res.turn = 0
    res.messages = deque(maxlen=gamedata.message_limit)
    return res
